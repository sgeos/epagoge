#!/usr/bin/env python3
"""Read and judge corpus records.

This is the sampled expert audit, not only a reading aid. Its output is the
measured residual error rate the project's quality claim rests on.

    PYTHONPATH=src python3 tools/review.py curriculum/graph/concepts.json \
        curriculum/graph/sample_corpus.jsonl --primitives curriculum/primitives.json

Modes.
    (default)   review interactively, resuming where you left off
    --print     format records for reading, no prompts, pipe to a pager
    --report    per-domain rates from verdicts already recorded
"""

from __future__ import annotations

import argparse
import sys
import textwrap
from pathlib import Path

from epagoge.concept_graph import ConceptGraph
from epagoge.record import Record, load_corpus, load_primitives
from epagoge.review import (
    Judgment,
    Verdict,
    append_verdict,
    domain_of,
    error_rates,
    load_verdicts,
    take_sample,
)

RULE = "─" * 74
KEYS = {"a": Judgment.ACCEPT, "r": Judgment.REJECT, "f": Judgment.FLAG}


def render(record: Record, graph: ConceptGraph, primitives: dict[str, str]) -> str:
    """One record, formatted so that judging it needs nothing else on screen."""
    lines: list[str] = []
    domain = domain_of(record, graph)
    lines.append(f"  {record.id:<44} level {record.level} · {domain}")
    lines.append(f"  concepts    {', '.join(record.concepts)}")
    lines.append(f"  class       {record.claim_class.value}")

    provenance = record.provenance
    if provenance.source_claim:
        lines.append(f"  source      {provenance.source_claim}")
        name = provenance.source_claim.removeprefix("primitive:")
        grounding = primitives.get(name)
        if grounding:
            # The reviewer can check the claim against its grounding without
            # looking it up. That is the whole point of showing it here.
            lines.append(f'              "{grounding}"')
    if provenance.position_holder:
        lines.append(f"  position of {provenance.position_holder}")
        if provenance.contested_by:
            lines.append(f"  contested   {', '.join(provenance.contested_by)}")
    if provenance.assumptions:
        lines.append(f"  assumes     {'; '.join(provenance.assumptions)}")
        lines.append(f"  method      {provenance.method}")
        lines.append(f"  validation  {provenance.validation_status}")

    simplification = record.simplification
    if simplification.superseded_by:
        scope = simplification.validity_scope
        span = f"levels {scope[0]}–{scope[1]}" if scope else "unscoped"
        lines.append(
            f"  simplified  {simplification.kind.value}, holds {span}, "
            f"corrected by {simplification.superseded_by}"
        )

    lines.append("")
    for paragraph in record.content.split("\n"):
        lines.extend(
            textwrap.wrap(
                paragraph, width=70, initial_indent="  ", subsequent_indent="  "
            )
            or ["  "]
        )
    return "\n".join(lines)


def report(verdicts: list[Verdict], records: list[Record], graph: ConceptGraph) -> None:
    rates = error_rates(verdicts, records, graph)
    if not rates:
        print("no verdicts recorded yet")
        return
    print(
        f"{'domain':<20} {'reviewed':>8} {'rejected':>8} {'flagged':>8}  rate (95% CI)"
    )
    for rate in rates:
        low, high = rate.interval()
        print(
            f"{rate.domain:<20} {rate.reviewed:>8} {rate.rejected:>8} "
            f"{rate.flagged:>8}  {rate.rate:.3f} [{low:.3f}, {high:.3f}]"
        )
    print()
    print("Rates are per domain and are never aggregated. Verifiability varies")
    print("enormously across domains, so one number would conceal both ends.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("graph", type=Path)
    parser.add_argument("corpus", type=Path)
    parser.add_argument("--primitives", type=Path, default=None)
    parser.add_argument(
        "--verdicts", type=Path, default=Path("evals/review/verdicts.jsonl")
    )
    parser.add_argument("--sample", type=int, default=None)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--reviewer", type=str, default="operator")
    parser.add_argument("--print", dest="dump", action="store_true")
    parser.add_argument("--report", action="store_true")
    args = parser.parse_args()

    graph = ConceptGraph.load(args.graph)
    records = load_corpus(args.corpus)
    primitives = load_primitives(args.primitives) if args.primitives else {}
    verdicts = load_verdicts(args.verdicts)

    if args.report:
        report(verdicts, records, graph)
        return 0

    seen = {v.record_id for v in verdicts}
    pending = (
        take_sample(records, args.sample, args.seed, exclude=seen)
        if args.sample
        else [r for r in records if r.id not in seen]
    )

    if args.dump:
        for record in pending:
            print(RULE)
            print(render(record, graph, primitives))
            print()
        return 0

    if not pending:
        print("nothing left to review")
        report(verdicts, records, graph)
        return 0

    print(f"{len(pending)} record(s) to review. Verdicts append to {args.verdicts}.")
    for index, record in enumerate(pending, 1):
        print()
        print(f"{RULE}  [{index}/{len(pending)}]")
        print(render(record, graph, primitives))
        print()
        while True:
            try:
                choice = (
                    input("  [a]ccept  [r]eject  [f]lag  [s]kip  [q]uit > ")
                    .strip()
                    .lower()
                )
            except (EOFError, KeyboardInterrupt):
                print("\nstopped")
                report(load_verdicts(args.verdicts), records, graph)
                return 0
            if choice == "q":
                report(load_verdicts(args.verdicts), records, graph)
                return 0
            if choice == "s":
                break
            if choice in KEYS:
                reason = ""
                if choice != "a":
                    reason = input("  reason > ").strip()
                append_verdict(
                    args.verdicts,
                    Verdict.now(record.id, KEYS[choice], reason, args.reviewer),
                )
                break
            print("  unrecognised. a, r, f, s, or q.")

    print()
    report(load_verdicts(args.verdicts), records, graph)
    return 0


if __name__ == "__main__":
    sys.exit(main())
