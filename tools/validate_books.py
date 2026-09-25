#!/usr/bin/env python3
"""Validate books and report how much of a level has been defined.

    PYTHONPATH=src python3 tools/validate_books.py <graph> <vocabulary> \
        <schedule-dir> <books.json> <corpus.jsonl>...
"""

from __future__ import annotations

import sys
from pathlib import Path

from epagoge import schedule as sched
from epagoge.book import (
    Definition,
    DefinitionKind,
    definition_coverage,
    load_book_dir,
    typical_words,
    validate_books,
)
from epagoge.concept_graph import ConceptGraph
from epagoge.record import load_corpus, record_from_json
from epagoge.vocabulary import load_vocabulary


def main(argv: list[str]) -> int:
    spreads: int | None = None
    argv = list(argv)
    if "--spreads" in argv:
        at = argv.index("--spreads")
        spreads = int(argv[at + 1])
        del argv[at : at + 2]

    if len(argv) < 5:
        print(
            f"usage: {argv[0]} <graph> <vocab> <sched-dir> <book-dir> [corpus]...",
            file=sys.stderr,
        )
        return 2

    graph = ConceptGraph.load(Path(argv[1]))
    vocabulary = load_vocabulary(Path(argv[2]))
    plans = [sched.load(p) for p in sorted(Path(argv[3]).glob("level_*.json"))]
    books, book_records = load_book_dir(Path(argv[4]))

    levels: dict[str, int] = {}
    words_in: dict[str, int] = {}
    definitions: dict[str, Definition] = {}
    everything = [record_from_json(r) for r in book_records]
    for path in argv[5:]:
        everything.extend(load_corpus(Path(path)))
    for record in everything:
        levels[record.id] = record.level
        words_in[record.id] = len(record.content.split())
        if record.defines is not None:
            definitions[record.id] = record.defines

    topics = {u.id for p in plans for d in p.domains for u in d.units}
    violations = validate_books(
        books,
        levels,
        definitions,
        {t.word for t in vocabulary.terms},
        set(graph.domains),
        topics,
        spreads=spreads,
    )
    if violations:
        print(f"{argv[4]}: {len(violations)} violation(s)", file=sys.stderr)
        for v in violations:
            print(f"  [{v.code}] {v.detail}", file=sys.stderr)
        return 1

    print(f"{argv[4]}: valid")
    print(f"  books              {len(books)}")
    print(f"  records in books   {sum(len(b.records) for b in books)}")
    print(f"  definitions        {len(definitions)}")
    for b in books:
        total = sum(words_in.get(r, 0) for r in b.records)
        band = typical_words(b.level)
        tag = ""
        if band is not None and not band[0] <= total <= band[1]:
            tag = "  outside the typical range"
        print(f"    {b.id:<16} {total:>5} words{tag}")

    # Coverage is reported and never gated. A word with no definition is not
    # a defect in an unfinished corpus and is one in a finished level.
    for level in sorted({b.level for b in books}):
        words = {t.word for t in vocabulary.terms if t.level <= level}
        plan = next((p for p in plans if p.level == level), None)
        units: set[str] = (
            {u.id for d in plan.domains for u in d.units} if plan is not None else set()
        )
        domains: set[str] = set(graph.domains) if plan is None else set(plan.covers)
        for kind, expected, label in (
            (DefinitionKind.WORD, words, "words"),
            (DefinitionKind.DOMAIN, domains, "domains"),
            (DefinitionKind.TOPIC, units, "topics"),
        ):
            got = definition_coverage(definitions, kind, expected)
            done = len(got.defined)
            total = done + len(got.undefined)
            pct = got.fraction * 100
            print(f"  level {level} {label:<8} {done:>4} of {total:<4} {pct:5.1f}%")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
