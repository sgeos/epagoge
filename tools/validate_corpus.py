#!/usr/bin/env python3
"""Validate a corpus against a concept graph and the primitive register.

Exits non-zero on any violation, so it is usable as a gate.

    PYTHONPATH=src python3 tools/validate_corpus.py \
        <graph.json> <corpus.jsonl> [primitives.json]
"""

from __future__ import annotations

import sys
from pathlib import Path

from epagoge.concept_graph import ConceptGraph
from epagoge.record import load_corpus, load_primitives, validate_corpus


def main(argv: list[str]) -> int:
    if len(argv) not in (3, 4):
        print(
            f"usage: {argv[0]} <graph.json> <corpus.jsonl> [primitives.json]",
            file=sys.stderr,
        )
        return 2

    graph = ConceptGraph.load(Path(argv[1]))
    graph_violations = graph.validate()
    if graph_violations:
        print(f"graph {argv[1]} is invalid; fix it first", file=sys.stderr)
        for v in graph_violations:
            print(f"  [{v.code}] {v.detail}", file=sys.stderr)
        return 1

    primitives = load_primitives(Path(argv[3])) if len(argv) == 4 else None
    records = load_corpus(Path(argv[2]))
    violations = validate_corpus(records, graph, primitives)
    if violations:
        print(f"{len(violations)} violation(s) in {argv[2]}:", file=sys.stderr)
        for v in violations:
            print(f"  [{v.code}] {v.detail}", file=sys.stderr)
        return 1

    levels = sorted({r.level for r in records})
    classes = sorted({r.claim_class.value for r in records})
    simplified = sum(1 for r in records if r.simplification.superseded_by is not None)
    print(f"{argv[2]}: valid")
    print(f"  records      {len(records)}")
    print(f"  levels       {levels}")
    print(f"  claim classes {', '.join(classes)}")
    print(f"  simplified   {simplified}")
    if primitives is not None:
        cited = {
            r.provenance.source_claim
            for r in records
            if r.provenance.source_claim is not None
            and r.provenance.source_claim.startswith("primitive:")
        }
        print(f"  primitives   {len(cited)} cited of {len(primitives)} registered")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
