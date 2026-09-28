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
from typing import Final, cast

from epagoge import schedule as sched
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
    WarmStart,
    chunk,
    format_seconds,
    is_finite,
    load_checkpoint,
    parameter_count,
    select_device,
    train_once,
)
from epagoge.tokeniser import PAD, build
from epagoge.variance import (
    MIN_OBSERVATIONS,
    PairedObservation,
    detectable_effect,
    estimate,
    required_seeds,
)
from epagoge.vocabulary import load_vocabulary

ROOT = Path(__file__).resolve().parent.parent

LENGTH_WEIGHT: Final[float] = 0.265
"""How strongly the `length` arm sorts by book length.

Chosen so that arm's position-to-length correlation matches the topological
arm's, which is what makes it a control rather than another variable.
**Both are measured per seed and then averaged**, at +0.211 for topological
and +0.213 for this arm over six seeds, and the weight was tuned against
the arm as implemented rather than against a reconstruction of it.

**Tuned to 0.40 first, against the wrong statistic.** Correlating a book's
*mean* position across seeds against its length gives +0.311 for the
topological arm, because averaging the positions removes the per-run noise.
That is a fact about the arm across seeds, and the quantity a single
training run sees is the per-run one. Matching the wrong target would have
given this arm half again the length ordering it is supposed to hold fixed.
"""

PAIRED_ARMS: Final[frozenset[str]] = frozenset({"curriculum", "topological"})
"""The two arms the pre-registered contrast is between.

`evals/PRE_REGISTRATION.md` item 3 names this pair. Variance statistics are
computed over it and over nothing else, so selecting a set of arms that
omits either one yields no paired estimate.
"""

ARMS: Final[tuple[str, ...]] = ("curriculum", "topological", "shuffled")
"""The orderings compared, and why there are three.

**`shuffled` was added 2026-09-26 and its absence was a real gap.** The
other two both respect the prerequisite graph, so the ablation compared two
curricula against each other. A result from that pair says which valid
ordering is better and says nothing about whether ordering helps, which is
the project's actual hypothesis.

It also answers the control Wu, Dyer and Neyshabur ask for. They found any
curriculum benefit attributable to the training set growing rather than to
the order, and their control grows the set with random membership. See
`docs/decisions/CURRICULUM_LITERATURE.md` for what that does and does not
isolate in a trainer that cycles a fixed ordered list.
"""


def book_order(
    level: int, graph: ConceptGraph, seed: int, arm: str, plan: sched.Schedule
) -> tuple[list[str], dict[str, str], dict[str, str]]:
    """Book ids in the arm's order, each book's text, and each book's title.

    **The title is returned because it is trained on**, as an announcement
    line at the head of the work. See `Tokeniser.encode_work` and
    `docs/decisions/STRUCTURAL_TOKENS.md`. It was presentation only until
    2026-09-27.

    **A book teaches what its unit teaches.** Taking the union of every
    record's concepts instead counts a word the book merely defines as a
    concept the book teaches, which manufactures dependencies between books
    that have nothing to do with each other. Measured 2026-09-25 over 144
    books, that reading made the dependency graph cyclic in twenty-four
    places, `bk.a1.person` and `bk.b1.keeping_going` each depending on the
    other, and `linear_extension` returns a short list on a cycle. Thirteen
    books reached the trainer and a hundred and thirty-three did not.
    """
    all_books, records = load_book_dir(ROOT / f"curriculum/books/level_{level}")
    by_id = {
        str(cast(dict[str, object], r)["id"]): cast(dict[str, object], r)
        for r in records
    }
    # A dictionary book spans nearly every concept, so it makes the
    # dependency graph cyclic. It is reference material and is emitted last.
    books = [b for b in all_books if not b.id.startswith("bk.dictionary.")]
    reference = [b for b in all_books if b.id.startswith("bk.dictionary.")]
    by_unit = {u.id: set(u.teaches) for d in plan.domains for u in d.units}
    teaches = {b.id: by_unit.get(b.subject, set()) for b in books}
    prerequisites = {n: set(graph.prerequisites_of(n)) for n in graph.nodes}
    deps = book_prerequisites(books, teaches, prerequisites)
    if arm == "length":
        # **The control for the confound found on 2026-09-27.** Orders that
        # respect the prerequisite graph also sort books by length, at
        # +0.311 against +0.062 for a free shuffle, because a book with more
        # prerequisites is placed later and 90 percent of books carry one.
        # Length ordering and graph structure were collinear at -0.76 across
        # the arms, so neither could be credited with the effect.
        #
        # This arm has the length ordering and not the graph. The mixing
        # weight is 0.40 because that reproduces the topological arm's
        # correlation to three decimals, measured over six seeds, so the two
        # differ in the graph and match on length.
        generator = random.Random(seed)
        length = {
            b.id: sum(
                len(str(by_id[i]["content"]).split()) for i in b.records if i in by_id
            )
            for b in books
        }
        by_length = sorted(length, key=lambda n: length[n])
        place = {n: i / max(1, len(by_length) - 1) for i, n in enumerate(by_length)}
        names = sorted(
            place,
            key=lambda n: (
                LENGTH_WEIGHT * place[n] + (1.0 - LENGTH_WEIGHT) * generator.random()
            ),
        )
    elif arm == "shuffled":
        # **The flat control, and it did not exist until 2026-09-26.** The two
        # arms above it both respect the prerequisite graph, so the ablation
        # compared two curricula rather than a curriculum against no
        # curriculum. A result from those two says which valid ordering is
        # better, not whether ordering helps.
        #
        # It is also this design's answer to Wu, Dyer and Neyshabur, who
        # found any curriculum benefit attributable to the training set
        # growing rather than to the order, and whose control is a set that
        # grows with random membership. In a trainer that cycles a fixed
        # ordered list, the order IS the growth schedule for the first epoch,
        # so a random order is that control.
        #
        # **The growth confound is smaller here than in their setting and the
        # record should say so.** At 1,458 chunks and batch 8 an epoch is 182
        # batches, so a 1,600-step run is about 8.8 epochs and every arm has
        # seen everything after the first eleven percent. After that, set size
        # cannot explain a difference and only the order within each cycle
        # can.
        shuffled = [b.id for b in books]
        random.Random(seed).shuffle(shuffled)
        names = shuffled
    elif arm == "topological":
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
    titles = {b.id: b.title or "" for b in all_books}
    return ordered, text, titles


def block_shuffle(names: list[str], size: int, seed: int) -> list[str]:
    """Shuffle within consecutive blocks, keeping the coarse order intact.

    **This separates the two things an arm currently changes at once.**
    `_batches` takes consecutive positions from an ordering, so an arm
    decides both the sequence in which books are visited and what each batch
    is made of. Measured 2026-09-27 over 223 batches: a curriculum ordering
    averages **1.20 distinct subjects per batch** against **1.88** for a
    shuffled one, so curriculum batches are far more homogeneous, and
    homogeneity changes gradient noise for reasons that have nothing to do
    with curricula.

    Shuffling inside blocks of 32 books moves the homogeneity to 1.79,
    which is 87 percent of the way to the shuffled arm, while leaving
    **every book within 10 percent of its curriculum position**. So a run at
    block 32 keeps the curriculum and discards the homogeneity, and the
    difference between it and block 1 is the part of the arm effect that was
    never about ordering.

    A size of 1 or less is the identity, which is the pre-existing
    behaviour and the default.
    """
    if size <= 1:
        return list(names)
    generator = random.Random(seed)
    out: list[str] = []
    for start in range(0, len(names), size):
        part = names[start : start + size]
        generator.shuffle(part)
        out += part
    return out


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
    # **Level N starts from the level N minus one model.** Each level is a
    # continuation rather than a fresh run, so a level-two model inherits
    # what level one learned about the words they share. The vocabulary
    # grows between levels, so the rows are matched by word.
    parser.add_argument(
        "--from-level",
        type=int,
        default=None,
        help="warm start from this level's weights",
    )
    # **An arm changes batch composition as well as visit order**, because
    # `pilot._batches` takes consecutive positions from the ordering.
    # Shuffling inside blocks keeps the sequence and discards the
    # homogeneity, and `evals/pilot/LEVEL_ONE_VARIANCE.md` measures how much
    # of the arm effect each accounts for. One is the identity.
    # **Arms are selectable rather than fixed**, because the `length` control
    # added on 2026-09-27 answers one question and would cost a third more
    # compute on every run that does not ask it. Changing what the ablation
    # compares by default is a design decision and is the operator's.
    parser.add_argument("--arms", type=str, nargs="+", default=list(ARMS))
    parser.add_argument(
        "--block-shuffle",
        type=int,
        default=1,
        help="shuffle books within blocks of this size; 1 is the identity",
    )
    # **The evaluation was truncated and said so.** At 28 held-out batches
    # the default of 24 scores 86 percent of the set, which is a consistent
    # estimator of a slightly different quantity and is the wrong instrument
    # for a variance study whose effects are 0.2 percent of the loss. Zero
    # means every batch.
    parser.add_argument("--eval-batches", type=int, default=0)
    parser.add_argument(
        # **THE DEFAULT WAS A TRACKED ARTIFACT, SO THE DEFAULT WAS A
        # DESTRUCTIVE ACT.** Three tools wrote a recorded result unless told
        # otherwise, and on 2026-09-28 a 200-step probe overwrote
        # `level_1_diagnosis.json` one command after a brief was written
        # warning against exactly that. It is the SECOND occurrence and the
        # THIRD warning: `evals/pilot/LEVEL_ONE_REGULARISATION.md` records the
        # first and says it was reverted, and two briefs carried the caution
        # forward. A warning that has failed three times is not the mechanism,
        # so the lesson is made structural instead: the tool cannot know
        # whether a run is a probe or a record, so it refuses to guess and the
        # caller says which.
        "--out",
        type=Path,
        required=True,
        help="where to write the result; a recorded run and a probe "
        "must not share a path",
    )
    args = parser.parse_args(argv[1:])

    vocabulary = load_vocabulary(ROOT / "curriculum/vocabulary.json")
    tokeniser = build(vocabulary, args.level)
    graph = ConceptGraph.load(ROOT / "curriculum/graph/concepts.json")
    plan = sched.load(ROOT / f"curriculum/schedule/level_{args.level:02d}.json")

    pad_id = tokeniser.ids[PAD]
    curriculum, text, titles = book_order(args.level, graph, 0, "curriculum", plan)
    # **A short ordering is a cycle, and a cycle must stop the run.**
    # `linear_extension` returns what it could order and says nothing, so a
    # truncated corpus trained silently and reported itself as the level.
    if len(curriculum) != len(text):
        dropped = sorted(set(text) - set(curriculum))
        print(
            f"ordering covers {len(curriculum)} of {len(text)} books; "
            f"the dependency graph is cyclic. First dropped: "
            f"{' '.join(dropped[:5])}",
            file=sys.stderr,
        )
        return 1
    # Chunks are built per book, so both arms share one chunk set and
    # differ only in the order the chunks are visited.
    chunks: list[list[int]] = []
    owner: list[str] = []
    unknown: list[str] = []
    for book_id in curriculum:
        body = text.get(book_id, "")
        title = titles.get(book_id, "")
        # **The title is checked too, because it is now trained on.** It was
        # presentation until 2026-09-27 and this loop only ever saw the body.
        unknown += tokeniser.unknown(body) + tokeniser.unknown(title)
        for piece in chunk(
            tokeniser.encode_work(body, title),
            args.seq_len,
            pad=pad_id,
        ):
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
        names, _, _ = book_order(args.level, graph, seed, arm, plan)
        names = block_shuffle(names, args.block_shuffle, seed)
        rank = {name: n for n, name in enumerate(names)}
        return sorted(train_ids, key=lambda i: (rank.get(owner[i], len(rank)), i))

    model_config = ModelConfig(
        vocab_size=tokeniser.size,
        d_model=args.d_model,
        n_layers=args.layers,
        seq_len=args.seq_len,
    )
    train_config = TrainConfig(
        steps=args.steps,
        batch_size=args.batch_size,
        eval_batches=args.eval_batches if args.eval_batches > 0 else 1_000_000,
    )
    device = select_device(args.device)
    # **Two different numbers, and the difference is not small.** A chunk
    # holds seq_len + 1 ids so that inputs and targets can be offset, and a
    # tail chunk is padded, so summing chunk lengths counts every boundary
    # token twice and every pad once. Reported as 44,505 on 2026-09-25 for
    # a corpus of 35,438, which overstated it by a quarter and fed a
    # published shortfall figure.
    chunk_ids = sum(len(c) for c in chunks)
    tokens = sum(
        len(tokeniser.encode_work(text.get(b, ""), titles.get(b, "")))
        for b in curriculum
    )
    print(
        f"device {device}, vocab {tokeniser.size}, {len(chunks)} chunks, "
        f"{tokens} corpus tokens, {chunk_ids} chunk ids including padding, "
        f"{parameter_count(model_config)} parameters"
    )

    # Loaded once, because every arm and every seed starts from the same
    # earlier model. Reloading per run would be the same weights at more
    # cost, and a difference between arms that came from the checkpoint
    # rather than the ordering would invalidate the pair.
    warm: WarmStart | None = None
    if args.from_level is not None:
        weights = ROOT / f"evals/pilot/level_{args.from_level}.pt"
        if not weights.is_file():
            print(
                f"no weights at {weights}; train level {args.from_level} first",
                file=sys.stderr,
            )
            return 1
        # **Loaded through `load_checkpoint`, and it was not until
        # 2026-09-27.** Two defects sat here, both silent. The whole payload
        # was passed as the state, so no parameter name matched and nothing
        # was copied. And the older word list was rebuilt from today's
        # lexicon rather than read from the checkpoint, so had a word been
        # admitted since, every row after it would have carried the wrong
        # word's vector. Carrying the word list is the entire reason
        # `save_checkpoint` writes one.
        try:
            earlier = load_checkpoint(weights, device)
        except ValueError as exc:
            print(exc, file=sys.stderr)
            return 1
        warm = WarmStart(
            state=earlier.model.state_dict(),
            older=list(earlier.words),
            newer=list(tokeniser.words),
        )
        print(
            f"warm start from level {args.from_level}, "
            f"{len(earlier.words)} words into {tokeniser.size}"
        )

    # **Three arms, and the third is the one that makes the comparison mean
    # something.** `curriculum` and `topological` both respect the
    # prerequisite graph, so a difference between them says which valid
    # ordering is better rather than whether ordering helps at all.
    # `shuffled` ignores the graph. The paired test below still contrasts
    # curriculum against topological, because that is the pre-registered
    # comparison; shuffled is reported alongside so a reader can see whether
    # either curriculum beats no curriculum.
    results: list[dict[str, object]] = []
    started = time.time()
    for seed in range(args.seeds):
        row: dict[str, object] = {"seed": seed}
        for arm in args.arms:
            loss = train_once(
                chunks,
                order_for(arm, seed),
                held_out,
                model_config,
                train_config,
                seed,
                device,
                pad_id=pad_id,
                warm_from=warm,
            )
            row[arm] = loss
            print(f"  seed {seed} {arm:12} held-out loss {loss:.4f}")
        # **The paired contrast needs both of its arms present.** `--arms`
        # can select any subset, and asking for a subset that omits one of
        # them used to raise `KeyError` here after the first seed had
        # trained. Skipped loudly rather than silently, because a run that
        # reports no variance statistics should say why.
        if row.keys() >= PAIRED_ARMS and all(
            is_finite(cast(float, row[a])) for a in PAIRED_ARMS
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
    if not set(args.arms) >= PAIRED_ARMS:
        print(
            f"  no variance statistics: the paired contrast needs "
            f"{' and '.join(sorted(PAIRED_ARMS))} and this run has "
            f"{' '.join(args.arms)}",
            file=sys.stderr,
        )
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
        "chunk_ids": chunk_ids,
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
