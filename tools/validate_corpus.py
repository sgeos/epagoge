#!/usr/bin/env python3
"""Validate a corpus against a concept graph.

Exits non-zero on any violation, so it is usable as a gate.

    PYTHONPATH=src python3 tools/validate_corpus.py <graph.json> <corpus.jsonl>
"""

from __future__ import annotations

import sys
from pathlib import Path

from epagoge.concept_graph import ConceptGraph
from epagoge.record import load_corpus, validate_corpus


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print(f"usage: {argv[0]} <graph.json> <corpus.jsonl>", file=sys.stderr)
        return 2

    graph = ConceptGraph.load(Path(argv[1]))
    graph_violations = graph.validate()
    if graph_violations:
        print(f"graph {argv[1]} is invalid; fix it first", file=sys.stderr)
        for v in graph_violations:
            print(f"  [{v.code}] {v.detail}", file=sys.stderr)
        return 1

    records = load_corpus(Path(argv[2]))
    violations = validate_corpus(records, graph)
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
