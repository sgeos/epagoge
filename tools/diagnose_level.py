#!/usr/bin/env python3
"""Say whether a level's model is undertrained or out of corpus.

**Held-out loss alone cannot tell those apart, and they call for opposite
work.** A model that has not converged wants more steps or more capacity.
A model that has memorised its corpus wants more corpus. The gap between
training and held-out loss separates them, so this sweeps a grid and
reports both.

Reading it: a small gap with both losses high means undertrained or under
capacity, and more steps or a bigger model should move it. A large gap
means the corpus is the limit and no amount of training will help.

    .venv/bin/python tools/diagnose_level.py --level 1
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

from epagoge import schedule as sched
from epagoge.concept_graph import ConceptGraph
from epagoge.pilot import (
    ModelConfig,
    TrainConfig,
    chunk,
    format_seconds,
    parameter_count,
    select_device,
    train_diagnostic,
)
from epagoge.tokeniser import PAD, build
from epagoge.vocabulary import load_vocabulary

sys.path.insert(0, str(Path(__file__).resolve().parent))
from train_level import book_order  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--level", type=int, default=1)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--seq-len", type=int, default=128)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--steps", type=int, nargs="+", default=[400, 800, 1600, 3200])
    parser.add_argument(
        "--width",
        type=int,
        nargs="+",
        default=[128, 256],
        help="d_model values to sweep",
    )
    parser.add_argument("--layers", type=int, nargs="+", default=[4])
    parser.add_argument(
        "--fractions",
        type=float,
        nargs="+",
        default=[1.0],
        help=(
            "fractions of the training chunks to train on, against one "
            "fixed held-out set. This is how the corpus scaling rate is "
            "measured, and IT WAS MISSING: the recorded scaling result was "
            "produced by something never committed, so the number that sets "
            "the project's corpus target could not be reproduced from the "
            "tree. Added 2026-09-25."
        ),
    )
    parser.add_argument(
        "--stream-per-book",
        action="store_true",
        help=(
            "one sequence per book, sized to the longest book, so no window "
            "straddles two books and none holds a fraction of one. Overrides "
            "--seq-len."
        ),
    )
    parser.add_argument(
        "--positions",
        choices=("learned", "rotary"),
        default="learned",
        help=(
            "how position reaches attention. A learned table has one row per "
            "index and starves at long sequences; rotary is a function of "
            "relative distance and has nothing per index to learn."
        ),
    )
    parser.add_argument("--device", type=str, default=None)
    parser.add_argument(
        "--out", type=Path, default=ROOT / "evals/pilot/level_1_diagnosis.json"
    )
    args = parser.parse_args(argv[1:])

    vocabulary = load_vocabulary(ROOT / "curriculum/vocabulary.json")
    tokeniser = build(vocabulary, args.level)
    graph = ConceptGraph.load(ROOT / "curriculum/graph/concepts.json")
    plan = sched.load(ROOT / f"curriculum/schedule/level_{args.level:02d}.json")

    pad_id = tokeniser.ids[PAD]
    ordered, text = book_order(args.level, graph, 0, "curriculum", plan)
    if len(ordered) != len(text):
        print("the book ordering is short; see train_level.py", file=sys.stderr)
        return 1

    encoded = {book_id: tokeniser.encode(text.get(book_id, "")) for book_id in ordered}
    longest = max((len(s) for s in encoded.values()), default=0)

    # **A BOOK IS THE UNIT, and a sequence long enough to hold one makes
    # each book its own stream.** Operator direction 2026-09-26: a picture
    # book is a self-contained coherent work, so a window that straddles two
    # of them teaches the model that unrelated text follows, and a window
    # that holds a fraction of one never shows it a whole work. At 128 a
    # nine-hundred-token book is seven windows and the model has never seen
    # one entire.
    seq_len = longest if args.stream_per_book else args.seq_len

    # **THE SPLIT IS BY BOOK, and it was by chunk until 2026-09-26.**
    # Chunks were concatenated across books and the last eighth taken, so
    # the boundary fell inside a book and one book had its opening in
    # training and its ending held out. It also means held-out is the tail
    # of the curriculum order rather than a sample, which biases the figure
    # and is why held-out loss here is not an estimate of loss on typical
    # corpus text. Splitting by book is also what makes two sequence lengths
    # comparable: both score the same books, so the only difference is how
    # much context each prediction had.
    boundary = max(1, len(ordered) - max(1, len(ordered) // 8))
    train_books, held_books = ordered[:boundary], ordered[boundary:]

    chunks: list[list[int]] = []
    for book_id in train_books:
        chunks.extend(chunk(encoded[book_id], seq_len, pad_id))
    train_ids = list(range(len(chunks)))
    held_out: list[list[int]] = []
    for book_id in held_books:
        held_out.extend(chunk(encoded[book_id], seq_len, pad_id))

    device = select_device(args.device)
    tokens = sum(len(s) for s in encoded.values())
    held_tokens = sum(len(encoded[b]) for b in held_books)
    truncated = sum(1 for b in ordered if len(encoded[b]) > seq_len)

    print(
        f"device {device}, vocab {tokeniser.size}, seq_len {seq_len}"
        f"{' (longest book)' if args.stream_per_book else ''}, "
        f"{args.positions} positions"
    )
    print(
        f"  {len(train_books)} books training over {len(chunks)} sequence(s), "
        f"{len(held_books)} held out over {len(held_out)}"
    )
    print(
        f"  {tokens} corpus tokens, {held_tokens} held out, longest book "
        f"{longest} tokens, {truncated} book(s) longer than seq_len"
    )
    # **A book longer than the sequence is split, not dropped**, so the
    # stream-per-book claim fails quietly for it. Say so.
    if truncated and args.stream_per_book:
        print("  WARNING: stream-per-book was asked for and some book is split")
    print(
        f"{'frac':>6} {'chunks':>7} {'tokens':>8} {'width':>6} {'steps':>6} "
        f"{'params':>10} {'train':>7} {'held':>7} {'gap':>7}"
    )

    rows: list[dict[str, object]] = []
    started = time.time()
    for fraction in args.fractions:
        # **The held-out set never shrinks with the fraction.** Every
        # fraction is scored against the same chunks, or the comparison
        # would be between models measured on different data and would
        # say nothing about corpus size.
        kept = max(1, int(len(train_ids) * fraction))
        subset = train_ids[:kept]
        subset_tokens = sum(len([i for i in chunks[c] if i != pad_id]) for c in subset)
        for width in args.width:
            for layers in args.layers:
                for steps in args.steps:
                    config = ModelConfig(
                        vocab_size=tokeniser.size,
                        d_model=width,
                        n_layers=layers,
                        seq_len=seq_len,
                        positions=args.positions,
                    )
                    result = train_diagnostic(
                        chunks,
                        subset,
                        held_out,
                        config,
                        TrainConfig(steps=steps, batch_size=args.batch_size),
                        args.seed,
                        device,
                        pad_id,
                    )
                    params = parameter_count(config)
                    print(
                        f"{fraction:>6.3f} {len(subset):>7} {subset_tokens:>8} "
                        f"{width:>6} {steps:>6} {params:>10} "
                        f"{result.train_loss:>7.3f} {result.held_out_loss:>7.3f} "
                        f"{result.gap:>7.3f}"
                    )
                    rows.append(
                        {
                            "fraction": fraction,
                            "train_chunks": len(subset),
                            "train_tokens": subset_tokens,
                            "d_model": width,
                            "layers": layers,
                            "steps": steps,
                            "parameters": params,
                            "train_loss": result.train_loss,
                            "held_out_loss": result.held_out_loss,
                            "gap": result.gap,
                            "curve": [list(p) for p in result.curve],
                        }
                    )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(
            {
                "level": args.level,
                "corpus_tokens": tokens,
                "chunks": len(chunks),
                "held_out_chunks": len(held_out),
                "vocab_size": tokeniser.size,
                "seed": args.seed,
                "device": str(device),
                "elapsed": format_seconds(time.time() - started),
                "runs": rows,
                "note": (
                    "A small gap with both losses high means undertrained or "
                    "under capacity. A large gap means the corpus is the limit."
                ),
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"\nwrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
