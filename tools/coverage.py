#!/usr/bin/env python3
"""What the curriculum covers, and by name what it does not.

**Levels two to six are a scheduling problem** and its failure mode is
silent partial coverage. This project has produced that shape three times:
a book ordering that covered thirteen books of a hundred and forty-six, a
chunker that kept a quarter of the corpus, and a generator that skipped
seven domains. Each reported a number and none named what it left out.

So this names them. A percentage is not a report.

Three questions, and the second is the one the curriculum's own claim
rests on.

1. **Is every concept taught somewhere?** A concept in the graph that no
   schedule teaches is material nobody will write.
2. **Is it revisited?** The curriculum's claim is iteration on the same
   ideas at increasing complexity, so a concept taught once is a claim the
   corpus does not honour.
3. **Does every domain appear at every level?** A level that drops a
   domain narrows the curriculum without saying so.

    PYTHONPATH=src python3 tools/coverage.py curriculum/graph/concepts.json \
        curriculum/schedule
"""

from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

from epagoge import schedule as sched
from epagoge.concept_graph import ConceptGraph


def main(argv: list[str]) -> int:
    strict = "--strict" in argv
    argv = [a for a in argv if a != "--strict"]
    if len(argv) != 3:
        print(
            f"usage: {argv[0]} [--strict] <graph.json> <schedule-dir>", file=sys.stderr
        )
        return 2

    graph = ConceptGraph.load(Path(argv[1]))
    plans = [sched.load(p) for p in sorted(Path(argv[2]).glob("level_*.json"))]
    if not plans:
        print(f"no schedules in {argv[2]}", file=sys.stderr)
        return 2

    domains = {
        node_id: node.domain
        for node_id, node in graph.nodes.items()
        if node.domain is not None
    }
    taught: dict[str, list[int]] = defaultdict(list)
    revisited: dict[str, list[int]] = defaultdict(list)
    covered: dict[int, set[str]] = {}
    for plan in plans:
        covered[plan.level] = {d.domain for d in plan.domains}
        for domain in plan.domains:
            for unit in domain.units:
                for concept in unit.teaches:
                    taught[concept].append(plan.level)
                for concept in unit.revisits:
                    revisited[concept].append(plan.level)

    never = sorted(c for c in domains if c not in taught)
    once = sorted(c for c in taught if not revisited.get(c))
    declared = sorted(graph.domains)
    levels = sorted(covered)

    print(f"concepts in the graph      {len(domains)}")
    print(f"taught at some level       {len(taught)}")
    print(f"schedules present          {levels}")
    print()
    print(f"never taught               {len(never)}")
    for concept in never:
        print(f"  {domains[concept]:36s} {concept}")
    print()
    print(f"taught once, never revisited {len(once)}")
    for concept in once[:20]:
        print(f"  {domains[concept]:36s} {concept}  at {taught[concept]}")
    if len(once) > 20:
        print(f"  ... and {len(once) - 20} more")
    print()
    print("domains by level")
    for level in levels:
        missing = sorted(set(declared) - covered[level])
        state = "all" if not missing else f"missing {' '.join(missing)}"
        print(f"  level {level}: {len(covered[level])} of {len(declared)}, {state}")

    # **Reported, not enforced, and that is deliberate.** Levels three to
    # seven have no schedule, so every concept reserved for them reads as
    # never taught. Gating on this today would refuse the tree for work
    # nobody has started. `--strict` is here so the gate can be turned on
    # in one move once the schedules exist.
    if strict and (never or once):
        print(
            f"\n{len(never)} concept(s) never taught, "
            f"{len(once)} taught once and never revisited",
            file=sys.stderr,
        )
        return 1
    print("\nreported and not enforced; pass --strict to gate on it")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
