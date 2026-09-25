#!/usr/bin/env python3
"""Train a model on a level's corpus, once per ordering, and report.

**The ordering must be the only difference between the arms.** Building
two streams and tokenising each separately would also change where chunk
boundaries fall, so the arms would differ in their content as well as
their order. Instead each book is tokenised and chunked on its own, and an
ordering is a permutation of the same chunk set. That is what makes a
paired comparison meaningful, and it is the design the variance pilot
established.

A run reports held-out loss per arm per seed, and the same variance
statistics the pilot reports. **It does not decide anything.** The
pre-registered threshold does that, and at this corpus size the honest
expectation is that the arms are indistinguishable.

**Why the statistics are here and not only in the pilot.** The pilot
measured an unpaired sigma of 0.0750, a paired standard deviation of
0.0233 and a correlation of 0.9539, on a synthetic second-order Markov
stream at 818,000 parameters. `evals/pilot/README.md` says plainly that
the correlation is the number most likely to move on real text, and item
6 of the pre-registration stays provisional until it is re-measured on
the corpus. Computing the same quantities here is what makes the two runs
comparable. It does not make them equivalent: the optimiser and schedule
are still AdamW with cosine decay, and `TRAINING_TECHNIQUES.md` adopts
maximal update parametrization, Muon and warmup-stable-decay, none of
which is implemented.

    .venv/bin/python tools/train_level.py --level 1 --seeds 4 --steps 600
"""

from __future__ import annotations

import argparse
import json
import random
import sys
import time
from pathlib import Path
from typing import cast

from epagoge.book import (
    book_prerequisites,
    linear_extension,
    load_book_dir,
    random_linear_extension,
)
from epagoge.concept_graph import ConceptGraph
from epagoge.pilot import (
    ModelConfig,
    TrainConfig,
    chunk,
    format_seconds,
    is_finite,
    parameter_count,
    select_device,
    train_once,
)
from epagoge.tokeniser import build
from epagoge.variance import (
    MIN_OBSERVATIONS,
    PairedObservation,
    detectable_effect,
    estimate,
    required_seeds,
)
from epagoge.vocabulary import load_vocabulary

ROOT = Path(__file__).resolve().parent.parent


def book_order(
    level: int, graph: ConceptGraph, seed: int, arm: str
) -> tuple[list[str], dict[str, str]]:
    """Book ids in the arm's order, and each book's text."""
    all_books, records = load_book_dir(ROOT / f"curriculum/books/level_{level}")
    by_id = {
        str(cast(dict[str, object], r)["id"]): cast(dict[str, object], r)
        for r in records
    }
    # A dictionary book spans nearly every concept, so it makes the
    # dependency graph cyclic. It is reference material and is emitted last.
    books = [b for b in all_books if not b.id.startswith("bk.dictionary.")]
    reference = [b for b in all_books if b.id.startswith("bk.dictionary.")]
    teaches = {
        b.id: {
            c
            for i in b.records
            if i in by_id
            for c in cast(list[str], by_id[i].get("concepts", []))
        }
        for b in books
    }
    prerequisites = {n: set(graph.prerequisites_of(n)) for n in graph.nodes}
    deps = book_prerequisites(books, teaches, prerequisites)
    if arm == "topological":
        names = random_linear_extension(deps, random.Random(seed))
    else:
        depth = graph.prerequisite_depth()

        def shallowest(ready: set[str]) -> str:
            return min(
                ready,
                key=lambda name: (
                    max((depth[c] for c in teaches[name] if c in depth), default=0),
                    name,
                ),
            )

        names = linear_extension(deps, shallowest)
    ordered = names + [b.id for b in reference]
    text = {
        b.id: "\n".join(str(by_id[i]["content"]) for i in b.records if i in by_id)
        for b in all_books
    }
    return ordered, text


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--level", type=int, default=1)
    parser.add_argument("--seeds", type=int, default=4)
    parser.add_argument("--steps", type=int, default=600)
    parser.add_argument("--seq-len", type=int, default=128)
    parser.add_argument("--d-model", type=int, default=128)
    parser.add_argument("--layers", type=int, default=4)
    parser.add_argument("--batch-size", type=int, default=8)
    parser.add_argument("--held-out", type=float, default=0.15)
    parser.add_argument("--device", type=str, default=None)
    parser.add_argument("--out", type=Path, default=ROOT / "evals/pilot/level_1.json")
    args = parser.parse_args(argv[1:])

    vocabulary = load_vocabulary(ROOT / "curriculum/vocabulary.json")
    tokeniser = build(vocabulary, args.level)
    graph = ConceptGraph.load(ROOT / "curriculum/graph/concepts.json")

    curriculum, text = book_order(args.level, graph, 0, "curriculum")
    # Chunks are built per book, so both arms share one chunk set and
    # differ only in the order the chunks are visited.
    chunks: list[list[int]] = []
    owner: list[str] = []
    unknown: list[str] = []
    for book_id in curriculum:
        body = text.get(book_id, "")
        unknown += tokeniser.unknown(body)
        for piece in chunk(tokeniser.encode(body), args.seq_len):
            chunks.append(piece)
            owner.append(book_id)
    if unknown:
        print(
            f"{len(set(unknown))} word(s) outside the level: "
            f"{' '.join(sorted(set(unknown))[:10])}",
            file=sys.stderr,
        )
        return 1
    if len(chunks) < args.batch_size * 2:
        print(
            f"only {len(chunks)} chunks of {args.seq_len} tokens; the corpus is "
            "too small to train on and the run would measure nothing",
            file=sys.stderr,
        )
        return 1

    rng = random.Random(0)
    indices = list(range(len(chunks)))
    rng.shuffle(indices)
    cut = max(1, int(len(indices) * args.held_out))
    held_ids = set(indices[:cut])
    held_out = [chunks[i] for i in sorted(held_ids)]
    train_ids = [i for i in range(len(chunks)) if i not in held_ids]

    def order_for(arm: str, seed: int) -> list[int]:
        names, _ = book_order(args.level, graph, seed, arm)
        rank = {name: n for n, name in enumerate(names)}
        return sorted(train_ids, key=lambda i: (rank.get(owner[i], len(rank)), i))

    model_config = ModelConfig(
        vocab_size=tokeniser.size,
        d_model=args.d_model,
        n_layers=args.layers,
        seq_len=args.seq_len,
    )
    train_config = TrainConfig(steps=args.steps, batch_size=args.batch_size)
    device = select_device(args.device)
    tokens = sum(len(c) for c in chunks)
    print(
        f"device {device}, vocab {tokeniser.size}, {len(chunks)} chunks, "
        f"{tokens} tokens, {parameter_count(model_config)} parameters"
    )

    results: list[dict[str, object]] = []
    started = time.time()
    for seed in range(args.seeds):
        row: dict[str, object] = {"seed": seed}
        for arm in ("curriculum", "topological"):
            loss = train_once(
                chunks,
                order_for(arm, seed),
                held_out,
                model_config,
                train_config,
                seed,
                device,
            )
            row[arm] = loss
            print(f"  seed {seed} {arm:12} held-out loss {loss:.4f}")
        if is_finite(cast(float, row["curriculum"])) and is_finite(
            cast(float, row["topological"])
        ):
            row["difference"] = cast(float, row["curriculum"]) - cast(
                float, row["topological"]
            )
        results.append(row)

    # **Paired, and only over seeds where both arms finished.** A run that
    # diverged carries no information about variance and averaging it in
    # would understate the spread rather than report a failure.
    observations = [
        PairedObservation(
            seed=cast(int, row["seed"]),
            treatment=cast(float, row["curriculum"]),
            control=cast(float, row["topological"]),
        )
        for row in results
        if "difference" in row
    ]
    variance: dict[str, object] | None = None
    if len(observations) >= MIN_OBSERVATIONS:
        est = estimate(observations)
        mean_loss = sum((o.treatment + o.control) / 2 for o in observations) / len(
            observations
        )
        rows: list[dict[str, float | int]] = []
        for relative in (0.02, 0.01, 0.005, 0.002):
            effect = relative * mean_loss
            rows.append(
                {
                    "relative": relative,
                    "effect": effect,
                    "paired": required_seeds(est.paired_sd, effect, paired=True),
                    "unpaired": required_seeds(est.seed_sd, effect, paired=False),
                }
            )
        variance = {
            "pairs": est.n,
            "mean_loss": mean_loss,
            "seed_sd": est.seed_sd,
            "paired_sd": est.paired_sd,
            "correlation": est.correlation,
            "mean_difference": est.mean_difference,
            "pairing_gain": est.pairing_gain,
            "requirements": rows,
            "detectable_at_20_paired_seeds": detectable_effect(est.paired_sd, 20),
            "synthetic_pilot": {
                "seed_sd": 0.0750,
                "paired_sd": 0.0233,
                "correlation": 0.9539,
                "source": "evals/pilot/result_single_epoch.json",
            },
        }
        print(
            f"  seed sd {est.seed_sd:.6f}  paired sd {est.paired_sd:.6f}  "
            f"rho {est.correlation:.4f}  gain {est.pairing_gain:.1f}x"
        )
    else:
        print(
            f"  {len(observations)} usable pair(s); variance needs {MIN_OBSERVATIONS}",
            file=sys.stderr,
        )

    payload = {
        "level": args.level,
        "chunks": len(chunks),
        "tokens": tokens,
        "vocab_size": tokeniser.size,
        "parameters": parameter_count(model_config),
        "steps": args.steps,
        "seeds": args.seeds,
        "device": str(device),
        "elapsed": format_seconds(time.time() - started),
        "results": results,
        "variance": variance,
        "note": (
            "Held-out loss per arm per seed. This decides nothing. The "
            "pre-registered threshold does, and at this corpus size the arms "
            "are expected to be indistinguishable."
        ),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
