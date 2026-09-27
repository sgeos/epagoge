"""Plan which concept pairs to write next, and say why each was chosen.

**Measured 2026-09-26: the corpus realised 109 concept pairs of 7,626
possible, and every concept's partners were its own unit-mates.** A variant
book repeated its unit, so repetition multiplied words without multiplying
combinations. `docs/decisions/COMBINATORIAL_RICHNESS.md` records the rule
this implements: a concept met again should be met beside something
different.

**Eleven books was a demonstration, not a corpus.** This emits a plan of any
size so the intervention can be run at a scale that moves the numbers.

**HOW A PARTNER IS CHOSEN**, in this order:

1. **It must be new.** A pair already realised is not worth writing again.
2. **Prefer a partner the model retains well**, where a checkpoint is
   available to say so, because grounding an abstract concept in a concrete
   one the model already has is both a new combination and defensible
   teaching.
3. **Spread the load.** A partner already used many times in this plan is
   deprioritised, or the plan would pair everything with `emptiness`.
4. **Prefer a different domain.** Cross-domain pairs are where the unrealised
   combinations are, since same-domain concepts already share units.

**TARGETS ARE ORDERED BY RETENTION** where a checkpoint exists, so the
concepts the model knows least get written for first, which is what the
spaced-repetition literature in `CURRICULUM_LITERATURE.md` argues for.
Without a checkpoint it falls back to book count, fewest first, and says so.

    PYTHONPATH=src python3 tools/plan_pairs.py --count 120 --out tmp/pairs.json
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import cast

from epagoge import schedule as sched
from epagoge.book import load_book_dir

ROOT = Path(__file__).resolve().parent.parent


def retention(level: int) -> dict[str, float]:
    """Mean per-token loss by concept, or empty if nothing is trained.

    Absent a checkpoint the plan still works and says which ordering it
    used, because a plan that silently changes its basis is worse than one
    that admits it has less to go on.
    """
    weights = ROOT / f"evals/pilot/level_{level}.pt"
    if not weights.exists():
        return {}
    try:
        import torch

        from epagoge.pilot import load_checkpoint, select_device
        from epagoge.tokeniser import build
        from epagoge.vocabulary import load_vocabulary
    except ImportError:
        return {}
    vocabulary = load_vocabulary(ROOT / "curriculum/vocabulary.json")
    tokeniser = build(vocabulary, level)
    device = select_device(None)
    checkpoint = load_checkpoint(weights, device)
    if len(checkpoint.words) != tokeniser.size:
        return {}
    books, records = load_book_dir(ROOT / f"curriculum/books/level_{level}")
    by_id = {
        str(cast("dict[str, object]", r)["id"]): cast("dict[str, object]", r)
        for r in records
    }
    objective = torch.nn.CrossEntropyLoss(reduction="sum")
    per_book: dict[str, float] = {}
    with torch.no_grad():
        for book in books:
            text = "\n".join(
                str(by_id[i]["content"]) for i in book.records if i in by_id
            )
            ids = tokeniser.encode_work(text, book.title or "")
            total = counted = 0.0
            for start in range(0, len(ids) - 1, checkpoint.config.seq_len):
                piece = ids[start : start + checkpoint.config.seq_len + 1]
                if len(piece) < 2:
                    continue
                block = torch.tensor([piece], dtype=torch.long, device=device)
                logits = checkpoint.model(block[:, :-1])
                total += float(
                    objective(
                        logits.reshape(-1, checkpoint.config.vocab_size),
                        block[:, 1:].reshape(-1),
                    )
                )
                counted += len(piece) - 1
            if counted:
                per_book[book.id] = total / counted
    plan = sched.load(ROOT / f"curriculum/schedule/level_{level:02d}.json")
    of_unit = {
        u.id: set(u.teaches) | set(u.revisits) for d in plan.domains for u in d.units
    }
    gathered: dict[str, list[float]] = defaultdict(list)
    for book in books:
        if book.id in per_book:
            for concept in of_unit.get(book.subject, ()):
                gathered[concept].append(per_book[book.id])
    return {c: sum(v) / len(v) for c, v in gathered.items()}


def pair(a: str, b: str) -> tuple[str, str]:
    """A pair in a fixed order, so membership is well defined."""
    return (a, b) if a <= b else (b, a)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--level", type=int, default=1)
    parser.add_argument("--count", type=int, default=120)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv[1:])

    plan = sched.load(ROOT / f"curriculum/schedule/level_{args.level:02d}.json")
    books, records = load_book_dir(ROOT / f"curriculum/books/level_{args.level}")
    by_id = {
        str(cast("dict[str, object]", r)["id"]): cast("dict[str, object]", r)
        for r in records
    }
    unit_of: dict[str, str] = {}
    domain_of: dict[str, str] = {}
    for domain in plan.domains:
        for unit in domain.units:
            for concept in set(unit.teaches) | set(unit.revisits):
                unit_of.setdefault(concept, unit.id)
                domain_of.setdefault(concept, domain.domain)

    realised: set[tuple[str, str]] = set()
    count_of: Counter[str] = Counter()
    for book in books:
        if len(book.records) != 16:
            continue
        seen: set[str] = set()
        for rid in book.records:
            record = by_id.get(rid)
            if record:
                seen |= set(cast("list[str]", record.get("concepts", [])))
        for concept in seen:
            count_of[concept] += 1
        for a, b in itertools.combinations(sorted(seen), 2):
            realised.add((a, b))

    used: Counter[str] = Counter()
    losses = retention(args.level)
    basis = "retention" if losses else "book count"
    concepts = sorted(c for c in unit_of if c in count_of)
    if losses:
        concepts.sort(key=lambda c: -losses.get(c, 0.0))
    else:
        concepts.sort(key=lambda c: (count_of[c], c))

    # **SPREAD FIRST, GROUND SECOND, and the first version had this
    # backwards.** Ranking by retention first and using `-count_of` as the
    # tiebreak meant a partner became MORE preferred each time it was used,
    # because a more negative number sorts earlier. A 150-pair plan came out
    # with ten distinct partners and `emptiness` in ninety of them, which is
    # the opposite of combinatorial richness.
    #
    # The primary key is now how often this plan has already used the
    # partner, so every concept is reached before any is reached twice.
    # Retention is the tiebreak, so among equally fresh partners a well
    # retained one wins and the abstract concept still gets grounded.
    def partner_rank(c: str) -> tuple[int, float, str]:
        return (used[c], losses.get(c, 0.0), c)

    ranked = sorted(concepts, key=partner_rank)
    taken = {b.id for b in books}
    spec: list[dict[str, object]] = []
    for target in itertools.cycle(concepts):
        if len(spec) >= args.count:
            break
        unit = unit_of[target]
        chosen = None
        for candidate in ranked:
            if candidate == target:
                continue
            if pair(target, candidate) in realised:
                continue
            if f"bk.{unit}.x_{candidate}" in taken:
                continue
            chosen = candidate
            break
        if chosen is None:
            if all(
                any(tuple(sorted((t, c))) in realised or c == t for c in ranked)
                for t in concepts
            ):
                break
            continue
        realised.add(pair(target, chosen))
        taken.add(f"bk.{unit}.x_{chosen}")
        used[chosen] += 1
        # Re-rank so the partner just used sinks to the back of the queue.
        ranked = sorted(concepts, key=partner_rank)
        spec.append(
            {
                "target": target,
                "unit": unit,
                "partner": chosen,
                "books_now": count_of[target] + 1,
                "cross_domain": domain_of.get(target) != domain_of.get(chosen),
                "target_loss": round(losses.get(target, 0.0), 3) or None,
            }
        )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(spec, indent=1) + "\n", encoding="utf-8")
    cross = sum(1 for s in spec if s["cross_domain"])
    print(f"  planned            {len(spec)} pair(s), all new")
    print(f"  target order from  {basis}")
    print(f"  cross-domain       {cross} of {len(spec)}")
    print(f"  distinct targets   {len({s['target'] for s in spec})}")
    print(f"  distinct partners  {len({s['partner'] for s in spec})}")
    print(f"  busiest partner    {used.most_common(1)[0] if used else 'none'}")
    print(f"  written to         {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
