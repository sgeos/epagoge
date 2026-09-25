#!/usr/bin/env python3
"""Train one level-one model, sample from it, and say what it produced.

**Held-out loss cannot tell a model that learned the language from one
that learned which words are common.** Every run before this one reported
a loss and discarded sixteen models without a token ever being sampled,
so "the corpus-to-model loop is closed" meant corpus to number and
nothing more.

This trains one model, writes its weights, samples from it, and reports
two things about what came out.

**It does not report admissibility, and the first version of it did.** The
tokeniser is built from the level's lexicon, so every token the model can
emit is admissible by construction. The figure was one hundred per cent on
the first run and would have been one hundred per cent for an untrained
model, which is what a vacuous metric looks like when it agrees with you.

**The report is descriptive.** At this corpus size the samples are
expected to be poor, and a number that looks bad is the measurement
working.

    .venv/bin/python tools/sample_level.py --level 1 --steps 800
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from epagoge import schedule as sched
from epagoge.concept_graph import ConceptGraph
from epagoge.pilot import (
    ModelConfig,
    TrainConfig,
    chunk,
    format_seconds,
    parameter_count,
    sample,
    save_checkpoint,
    select_device,
    train_model,
)
from epagoge.tokeniser import BOOK, PAD, SPECIALS, build
from epagoge.vocabulary import load_vocabulary

sys.path.insert(0, str(Path(__file__).resolve().parent))
from train_level import book_order  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

MIN_SENTENCE_WORDS = 3
"""Shortest run between full stops that counts as a sentence.

The same figure the generator uses to refuse a teacher's fragment, applied
here to the model's output so the two are judged by one rule."""


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--level", type=int, default=1)
    parser.add_argument("--steps", type=int, default=400)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--seq-len", type=int, default=128)
    parser.add_argument("--d-model", type=int, default=256)
    parser.add_argument("--layers", type=int, default=4)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--tokens", type=int, default=240, help="tokens to sample")
    parser.add_argument("--samples", type=int, default=3)
    parser.add_argument("--temperature", type=float, default=1.0)
    parser.add_argument("--device", type=str, default=None)
    # **Defaults are the best configuration the sweep found**, width 256 at
    # four hundred steps, held-out loss 4.789. Every longer run measured on
    # this corpus is worse, because the model memorises it. See
    # LEVEL_ONE_DIAGNOSIS.md.
    parser.add_argument("--weights", type=Path, default=ROOT / "evals/pilot/level_1.pt")
    parser.add_argument(
        "--out", type=Path, default=ROOT / "evals/pilot/level_1_samples.json"
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

    chunks: list[list[int]] = []
    for book_id in ordered:
        chunks.extend(
            chunk(tokeniser.encode(text.get(book_id, "")), args.seq_len, pad_id)
        )
    if len(chunks) < args.batch_size * 2:
        print(f"only {len(chunks)} chunks; too small to train", file=sys.stderr)
        return 1

    held = max(1, len(chunks) // 8)
    model_config = ModelConfig(
        vocab_size=tokeniser.size,
        d_model=args.d_model,
        n_layers=args.layers,
        seq_len=args.seq_len,
    )
    device = select_device(args.device)
    import time

    started = time.time()
    model, loss = train_model(
        chunks,
        list(range(len(chunks) - held)),
        chunks[-held:],
        model_config,
        TrainConfig(steps=args.steps, batch_size=args.batch_size),
        args.seed,
        device,
        pad_id,
    )
    save_checkpoint(model, model_config, tokeniser.words, args.weights)

    # **The prompt is the corpus's own opening move.** A book starts with a
    # marker, so sampling from it asks the model to begin a book rather
    # than to continue an arbitrary fragment.
    prompt = [tokeniser.ids[BOOK]]
    specials = {tokeniser.ids[s] for s in SPECIALS}

    texts: list[str] = []
    words: list[str] = []
    for n in range(args.samples):
        produced = sample(
            model,
            prompt,
            args.tokens,
            device,
            seed=args.seed * 1000 + n,
            temperature=args.temperature,
            seq_len=args.seq_len,
        )
        words.extend(
            tokeniser.words[t]
            for t in produced
            if t not in specials
            and t < len(tokeniser.words)
            and tokeniser.words[t].isalpha()
        )
        texts.append(tokeniser.decode(produced))

    # **Admissibility is not measurable this way and the first version of
    # this tool measured it anyway.** The tokeniser is built from the
    # level's lexicon, so every token the model can emit is admissible by
    # construction and the share is one hundred per cent whatever the model
    # learned. It said 100.0% on the first run and meant nothing.
    #
    # These two say something. Distinct share falls when the model loops,
    # which these samples do on "the cup". Sentence share is the corpus's
    # own shape rule applied to the model's output, and a model that has
    # not learned where a sentence ends scores badly on it.
    distinct = len(set(words)) / len(words) if words else 0.0
    sentences = [
        piece.strip()
        for piece in " ".join(
            tokeniser.words[t] for text in texts for t in tokeniser.encode(text)
        ).split(".")
    ]
    shaped = [p for p in sentences if len(p.split()) >= MIN_SENTENCE_WORDS]
    sentence_share = len(shaped) / len(sentences) if sentences else 0.0
    print(
        f"device {device}, {len(chunks)} chunks, "
        f"{parameter_count(model_config)} parameters"
    )
    print(f"held-out loss {loss:.4f}  elapsed {format_seconds(time.time() - started)}")
    print(
        f"sampled {len(words)} word tokens, "
        f"{distinct * 100:.1f}% distinct, "
        f"{sentence_share * 100:.1f}% of sentences at least "
        f"{MIN_SENTENCE_WORDS} words"
    )
    print(f"wrote {args.weights}")
    for n, body in enumerate(texts):
        print(f"\n--- sample {n} ---\n{body[:600]}")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(
            {
                "level": args.level,
                "steps": args.steps,
                "seed": args.seed,
                "chunks": len(chunks),
                "parameters": parameter_count(model_config),
                "held_out_loss": loss,
                "temperature": args.temperature,
                "sampled_word_tokens": len(words),
                "distinct_share": distinct,
                "sentence_share": sentence_share,
                "samples": texts,
                "note": (
                    "Descriptive, and at this corpus size the samples are "
                    "expected to be poor. Admissibility is deliberately not "
                    "reported: the tokeniser is built from the level's "
                    "lexicon, so every token the model can emit is admissible "
                    "by construction and the figure would be one hundred per "
                    "cent whatever the model learned."
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
