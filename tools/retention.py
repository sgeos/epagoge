"""Which concepts the model has failed to retain, measured rather than audited.

**`coverage.py` asks whether the SCHEDULE mentions a concept more than
once. This asks whether the MODEL still knows it.** The two are different
questions and the literature says the second is the one that matters.

`docs/decisions/CURRICULUM_LITERATURE.md` records the evidence. LFR tracks
a model's performance across data blocks and revisits the regions it is
doing badly on, reporting lower perplexity on 5 to 19 percent of a
full-dataset baseline's tokens. The spaced-repetition work on continual
pretraining argues that scheduling should target what the model is failing
to retain, not what it has already learned.

**So a concept the model predicts well needs no revisiting even if the
schedule teaches it once, and a concept it predicts badly needs revisiting
even if the schedule teaches it five times.** This tool measures the second
axis so the two can be compared.

**HOW IT MEASURES.** Per-token cross-entropy on each book under a trained
checkpoint, then averaged over the books that teach or revisit a concept.
Loss is the model's own surprise at text it was trained on, so a high
figure means the concept's material did not stick.

**WHAT IT DOES NOT DO.** It does not gate, and it cannot: the checkpoint is
not in version control, so in a clone this skips loudly rather than
passing silently. It also reports a RANKING and not a pass or fail, because
there is no principled threshold and inventing one would be the arbitrary
bound this project has met before.

**THE HELD-OUT CAVEAT.** These books are training data. The figure is
retention, not generalisation, which is the quantity LFR selects on too.

    PYTHONPATH=src python3 tools/retention.py --level 1
"""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path
from typing import cast

from epagoge import schedule as sched
from epagoge.book import load_book_dir
from epagoge.tokeniser import build
from epagoge.vocabulary import load_vocabulary

ROOT = Path(__file__).resolve().parent.parent


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--level", type=int, default=1)
    parser.add_argument("--weights", type=Path, default=None)
    parser.add_argument("--show", type=int, default=20)
    parser.add_argument("--device", type=str, default=None)
    args = parser.parse_args(argv[1:])

    weights = args.weights or ROOT / f"evals/pilot/level_{args.level}.pt"
    if not weights.exists():
        print(f"SKIPPED: {weights.relative_to(ROOT)} absent, so nothing is trained.")
        print("  Write one with tools/sample_level.py, then run this again.")
        return 0
    try:
        import torch

        from epagoge.pilot import load_checkpoint, select_device
    except ImportError:
        print("SKIPPED: the optional 'train' dependencies are absent.")
        return 0

    vocabulary = load_vocabulary(ROOT / "curriculum/vocabulary.json")
    tokeniser = build(vocabulary, args.level)
    plan = sched.load(ROOT / f"curriculum/schedule/level_{args.level:02d}.json")
    books, records = load_book_dir(ROOT / f"curriculum/books/level_{args.level}")
    by_id = {
        str(cast("dict[str, object]", r)["id"]): cast("dict[str, object]", r)
        for r in records
    }

    device = select_device(args.device)
    checkpoint = load_checkpoint(weights, device)
    if len(checkpoint.words) != tokeniser.size:
        print(
            f"SKIPPED: the checkpoint carries {len(checkpoint.words)} words and "
            f"the lexicon now admits {tokeniser.size}. Retrain before measuring "
            "retention, or the numbers describe a vocabulary that no longer "
            "exists."
        )
        return 0
    model = checkpoint.model
    seq_len = checkpoint.config.seq_len
    objective = torch.nn.CrossEntropyLoss(reduction="sum")

    # A book's loss is its total surprise over its own tokens, divided by how
    # many there were, so a long book does not dominate by being long.
    per_book: dict[str, float] = {}
    with torch.no_grad():
        for book in books:
            text = "\n".join(
                str(by_id[i]["content"]) for i in book.records if i in by_id
            )
            ids = tokeniser.encode(text)
            if len(ids) < 2:
                continue
            total = 0.0
            counted = 0
            for start in range(0, len(ids) - 1, seq_len):
                piece = ids[start : start + seq_len + 1]
                if len(piece) < 2:
                    continue
                block = torch.tensor([piece], dtype=torch.long, device=device)
                logits = model(block[:, :-1])
                total += float(
                    objective(
                        logits.reshape(-1, checkpoint.config.vocab_size),
                        block[:, 1:].reshape(-1),
                    )
                )
                counted += len(piece) - 1
            if counted:
                per_book[book.id] = total / counted

    # Concepts a unit teaches or revisits, and the books whose subject is
    # that unit. A book teaches what its unit teaches, which is the same
    # reading train_level.py uses and for the same reason.
    concepts_of_unit: dict[str, set[str]] = {}
    revisit_count: dict[str, int] = defaultdict(int)
    for domain in plan.domains:
        for unit in domain.units:
            concepts_of_unit[unit.id] = set(unit.teaches) | set(unit.revisits)
            for concept in unit.revisits:
                revisit_count[concept] += 1
    losses: dict[str, list[float]] = defaultdict(list)
    for book in books:
        if book.id not in per_book:
            continue
        for concept in concepts_of_unit.get(book.subject, ()):
            losses[concept].append(per_book[book.id])

    if not losses:
        print("  no concept could be matched to a book; nothing to report")
        return 0

    ranked = sorted(
        ((sum(v) / len(v), len(v), c) for c, v in losses.items()), reverse=True
    )
    mean = sum(per_book.values()) / len(per_book)
    print(f"  books measured        {len(per_book)}")
    print(f"  concepts matched      {len(ranked)}")
    print(f"  mean loss over books  {mean:.3f}")
    print("\n  worst retained, which is what LFR would revisit first:")
    for loss, count, concept in ranked[: args.show]:
        times = revisit_count.get(concept, 0)
        print(
            f"    {loss:6.3f}  over {count:3d} book(s)  revisited {times} "
            f"time(s) by the schedule  {concept}"
        )
    print("\n  best retained, which the schedule need not revisit:")
    for loss, count, concept in ranked[-5:]:
        print(f"    {loss:6.3f}  over {count:3d} book(s)  {concept}")

    # **The comparison that matters.** If the schedule's audit and the model's
    # measurement disagree, the audit is auditing the wrong thing.
    schedule_gap = {c for c in losses if not revisit_count.get(c)}
    worst = {c for _, _, c in ranked[: len(ranked) // 4 or 1]}
    print(
        f"\n  the schedule flags {len(schedule_gap)} concept(s) as taught once "
        f"and never revisited"
    )
    print(f"  the model is worst on {len(worst)} concept(s), its top quartile")
    agreed = len(schedule_gap & worst)
    verdict = "largely the same" if agreed > len(worst) / 2 else "different"
    print(f"  they agree on {agreed}, so the two identify {verdict} work")
    print("\n  reported, never gated. These books are training data, so this is")
    print("  retention rather than generalisation, and there is no principled")
    print("  threshold to gate on.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
