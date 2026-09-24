#!/usr/bin/env python3
"""Validate curriculum schedules in level order and report their shape.

Levels are validated in sequence because a prerequisite may be scheduled at
any earlier level, so a level cannot be checked on its own.

    PYTHONPATH=src python3 tools/validate_schedule.py \
        curriculum/graph/concepts.json curriculum/primitives.json \
        curriculum/schedule/level_01.json ...
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import cast

from epagoge import schedule as sched
from epagoge.concept_graph import ConceptGraph


def _primitive_ids(path: Path) -> list[str]:
    """Accept either a bare list or an object wrapping one, and validate.

    The register is external input to this tool, so its shape is checked
    rather than assumed.
    """
    parsed: object = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(parsed, dict):
        parsed = cast(dict[str, object], parsed).get("primitives", [])
    if not isinstance(parsed, list):
        raise ValueError("primitive register must be a list, or hold one")
    out: list[str] = []
    for entry in cast(list[object], parsed):
        if isinstance(entry, dict):
            value = cast(dict[str, object], entry).get("id")
        else:
            value = entry
        if not isinstance(value, str):
            raise ValueError(f"primitive id must be a string, got {value!r}")
        out.append(value)
    return out


def main(argv: list[str]) -> int:
    if len(argv) < 4:
        print(f"usage: {argv[0]} <graph> <primitives> <level.json>...", file=sys.stderr)
        return 2

    graph = ConceptGraph.load(Path(argv[1]))
    primitives = _primitive_ids(Path(argv[2]))
    paths = [Path(a) for a in argv[3:]]

    assigned: dict[str, int] = {}
    failed = False
    for path in sorted(paths, key=lambda p: sched.load(p).level):
        plan = sched.load(path)
        violations = sched.validate(plan, graph, primitives, assigned)
        if violations:
            failed = True
            print(f"{path}: {len(violations)} violation(s)", file=sys.stderr)
            for v in violations:
                print(f"  [{v.code}] {v.detail}", file=sys.stderr)
            continue

        assigned.update(sched.assignment(plan))
        shares = plan.shares()
        units = sum(len(d.units) for d in plan.domains)
        existing = len(plan.all_teaches())
        planned = len(plan.all_introduces())
        print(f"{path}: valid")
        print(f"  level            {plan.level}")
        print(
            f"  budget           10^{len(str(plan.budget.low)) - 1}"
            f" to 10^{len(str(plan.budget.high)) - 1} tokens"
        )
        print(f"  domains          {len(plan.domains)}")
        print(f"  units            {units}")
        print(f"  concepts         {existing} existing, {planned} planned")
        for d in plan.domains:
            count = len(d.teaches()) + len(d.introduces())
            new = len(d.introduces())
            tag = f"{count:>2} concepts" + (f", {new} planned" if new else "")
            print(f"    {d.domain:<34} {shares[d.domain] * 100:>5.1f}%  {tag}")

    if failed:
        return 1

    # A concept nothing schedules is a concept no record will be written for.
    unscheduled = sorted(
        n
        for n, node in graph.nodes.items()
        if node.domain is not None and n not in assigned
    )
    print()
    print(
        f"unscheduled concepts {len(unscheduled)} of "
        f"{sum(1 for n in graph.nodes.values() if n.domain is not None)} in the graph"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
