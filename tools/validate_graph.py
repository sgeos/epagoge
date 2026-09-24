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
    declared = sorted(graph.domains)
    inferred = sorted({n.domain for n in graph.nodes.values() if n.domain is not None})
    formal = [n for n in graph.nodes.values() if n.domain is None]

    print(f"{path}: valid")
    print(f"  nodes              {len(graph.nodes)}")
    print(f"  formal structures  {len(formal)}")
    print(f"  domains declared   {len(declared)}")
    for d in declared or inferred:
        members = sorted(graph.concepts_in(d))
        # An empty domain is declared and awaiting content, not a defect. It
        # is printed anyway, because a gap that is not shown is a gap nobody
        # is accountable for.
        if members:
            # Two depths, because they answer different questions once the
            # domains are connected. Global depth measures where a domain
            # sits in the graph. Internal depth measures its own structure,
            # and is the quantity the ordering ablation contrasts.
            deepest = max(depth[n] for n in members)
            inside = graph.within_domain_depth(d)
            summary = (
                f"{len(members):>3} concepts, depth {inside} internal, {deepest} global"
            )
        else:
            summary = "  AWAITING CONTENT"
        print(f"  domain {d:<32} {summary}")

    empty = graph.empty_domains()
    print(f"  awaiting content   {len(empty)} declared domains hold no concept")

    # Four connectivity measures, each of which reports a defect as a number
    # rather than as silence. The earlier "foundation feeds" count was
    # retired on 2026-09-24: it assumed three named domains were foundations,
    # which the domain restructure removed, and it was reporting immaturity
    # in those domains as though it were disconnection.
    isolated = graph.isolated_concepts()
    print(f"  isolated concepts  {len(isolated)} carry no edge of any kind")
    by_domain: dict[str, int] = {}
    for node_id in isolated:
        key = graph.nodes[node_id].domain or "<formal>"
        by_domain[key] = by_domain.get(key, 0) + 1
    for name, count in sorted(by_domain.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"    {name:<32} {count:>2}")

    crossing = graph.cross_domain_prerequisites()
    print(
        f"  cross-domain prereq {len(crossing)} prerequisites cross a domain boundary"
    )
    for target, source in crossing:
        t = graph.nodes[target].domain
        src = graph.nodes[source].domain
        print(f"    {target} [{t}] <- {source} [{src}]")

    specialisations = sum(len(graph.generalisations_of(n)) for n in graph.nodes)
    print(f"  specialisations    {specialisations} edges in the specialisation layer")

    inert = graph.inert_structures()
    print(f"  inert structures   {len(inert)} instantiated fewer than twice")
    for structure_id in inert:
        print(f"    {structure_id}")

    edges = sorted(graph.transfer_edges())
    print(f"  transfer edges     {len(edges)}")
    for a, b in edges:
        shared = ", ".join(sorted(graph.structures_of(a) & graph.structures_of(b)))
        print(f"    {a} <-> {b}  via {shared}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
