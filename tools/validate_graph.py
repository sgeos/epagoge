#!/usr/bin/env python3
"""Validate a concept graph and report its derived structure.

Exits non-zero on any invariant violation, so it is usable as a gate.

    PYTHONPATH=src python3 tools/validate_graph.py curriculum/graph/seed.json
"""

from __future__ import annotations

import sys
from pathlib import Path

from epagoge.concept_graph import ConceptGraph


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(f"usage: {argv[0]} <graph.json>", file=sys.stderr)
        return 2

    path = Path(argv[1])
    if not path.is_file():
        print(f"no such file: {path}", file=sys.stderr)
        return 2

    graph = ConceptGraph.load(path)
    violations = graph.validate()
    if violations:
        print(f"{len(violations)} violation(s) in {path}:", file=sys.stderr)
        for v in violations:
            print(f"  [{v.code}] {v.detail}", file=sys.stderr)
        return 1

    depth = graph.prerequisite_depth()
    domains = sorted({n.domain for n in graph.nodes.values() if n.domain is not None})
    formal = [n for n in graph.nodes.values() if n.domain is None]

    print(f"{path}: valid")
    print(f"  nodes              {len(graph.nodes)}")
    print(f"  formal structures  {len(formal)}")
    for d in domains:
        members = [n for n, node in graph.nodes.items() if node.domain == d]
        deepest = max(depth[n] for n in members)
        label = f"  domain {d:<18}"
        summary = f"{len(members):>3} concepts, max depth {deepest}"
        print(f"{label} {summary}")

    # A foundation nothing rests on is not functioning as a foundation.
    foundations = {"physical_world", "space_and_time", "agency", "society"}
    feeds = sum(
        1
        for node_id, node in graph.nodes.items()
        for p in graph.prerequisites_of(node_id)
        if (q := graph.nodes.get(p)) is not None
        and q.domain in foundations
        and node.domain not in foundations
    )
    print(f"  foundation feeds   {feeds} prerequisites run from a foundation outward")

    edges = sorted(graph.transfer_edges())
    print(f"  transfer edges     {len(edges)}")
    for a, b in edges:
        shared = ", ".join(sorted(graph.structures_of(a) & graph.structures_of(b)))
        print(f"    {a} <-> {b}  via {shared}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
