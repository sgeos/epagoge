#!/usr/bin/env python3
"""Build a training stream from the books, in a chosen ordering.

**Three artifacts, three readers.** The books under `curriculum/books/` are
what a person reads and what the validators check. This produces what the
trainer reads, which needs none of the annotation and must not contain the
block markers, since a model trained on them would learn to emit them.

It is derived. Nothing here is authored, and the same books yield a
different stream under a different ordering, which is what the ordering
ablation requires.

    PYTHONPATH=src python3 tools/build_corpus.py <book-dir> <out.jsonl> \
        [--order authored|shuffled] [--seed N]
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path
from typing import cast

from epagoge.book import (
    book_prerequisites,
    linear_extension,
    load_book_dir,
    random_linear_extension,
)
from epagoge.concept_graph import ConceptGraph


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("books", type=Path)
    parser.add_argument("out", type=Path)
    parser.add_argument(
        "--order", choices=("curriculum", "topological"), default="curriculum"
    )
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument(
        "--graph", type=Path, default=Path("curriculum/graph/concepts.json")
    )
    parser.add_argument(
        "--vocabulary", type=Path, default=Path("curriculum/vocabulary.json")
    )
    parser.add_argument("--no-dictionary", action="store_true")
    args = parser.parse_args(argv[1:])

    all_books, records = load_book_dir(args.books)
    # **A dictionary book is a reference, not a step in the curriculum.** It
    # spans every concept it defines, so it depends on almost every other
    # book while almost every other book supplies a word it defines, which
    # made the dependency graph cyclic the moment one existed. It is
    # excluded from the ordering and emitted last, which is where a
    # consolidation belongs anyway.
    books = [b for b in all_books if not b.id.startswith("bk.dictionary.")]
    reference = [b for b in all_books if b.id.startswith("bk.dictionary.")]
    by_id = {
        str(cast(dict[str, object], r)["id"]): cast(dict[str, object], r)
        for r in records
    }

    # A book is one document. Its internal order is not shuffled, because the
    # narrative is the reason a book exists, and shuffling inside one would
    # destroy the thing the ordering hypothesis is about.
    graph = ConceptGraph.load(args.graph)
    teaches = {
        b.id: {
            c
            for i in b.records
            if i in by_id
            for c in cast(list[str], by_id[i].get("concepts", []))
        }
        for b in books
    }
    prerequisites = {n: set(graph.prerequisites_of(n)) for n in graph.nodes}
    deps = book_prerequisites(books, teaches, prerequisites)

    by_book = {b.id: b for b in books}
    if args.order == "topological":
        # A random linear extension, not a random permutation. A permutation
        # can put a book teaching counting before the one teaching same and
        # different, which is not a curriculum in any ordering.
        names = random_linear_extension(deps, random.Random(args.seed))
    else:
        # **The curriculum arm is derived, not authored.** Taking the order
        # off the filenames gave an alphabetical sequence that broke two
        # book dependencies, which is not a curriculum and would have been
        # the treatment arm of an experiment about ordering.
        #
        # Shallowest first among the books that are ready, which is the
        # difficulty-graded ordering the hypothesis is about.
        depth = graph.prerequisite_depth()

        def shallowest(ready: set[str]) -> str:
            return min(
                ready,
                key=lambda name: (
                    max((depth[c] for c in teaches[name] if c in depth), default=0),
                    name,
                ),
            )

        names = linear_extension(deps, shallowest)
    if len(names) != len(deps):
        print("book dependencies are cyclic", file=sys.stderr)
        return 1
    order = [by_book[n] for n in names if n in by_book] + reference

    args.out.parent.mkdir(parents=True, exist_ok=True)
    words = 0
    with args.out.open("w", encoding="utf-8") as handle:
        for book in order:
            text = "\n".join(
                str(by_id[i]["content"]) for i in book.records if i in by_id
            )
            words += len(text.split())
            handle.write(
                json.dumps({"id": book.id, "level": book.level, "text": text}) + "\n"
            )

        # **The dictionary is last, and it is a consolidation.** Every word
        # in it was already defined in context by the book that introduced
        # it. Seven hundred definitions at the front, with no story around
        # them, is the lifeless-assertion failure the books exist to fix.
        defined: dict[str, str] = {}
        for record in records:
            entry = cast(dict[str, object], record)
            definition = cast(dict[str, object], entry.get("defines") or {})
            if definition.get("kind") == "word":
                defined[str(definition["target"])] = str(entry["content"])
        level = order[0].level if order else 1
        if not args.no_dictionary and defined:
            text = "\n".join(f"{w}: {defined[w]}" for w in sorted(defined))
            words += len(text.split())
            handle.write(
                json.dumps(
                    {"id": f"dictionary.level_{level}", "level": level, "text": text}
                )
                + "\n"
            )

    constrained = sum(1 for v in deps.values() if v)
    wanted = {
        t["word"]
        for t in cast(
            list[dict[str, object]],
            json.loads(args.vocabulary.read_text(encoding="utf-8"))["terms"],
        )
        if cast(int, t["level"]) <= level
    }
    total = len(order) + (0 if args.no_dictionary or not defined else 1)
    print(f"{args.out}: {total} documents, {words} words, order {args.order}")
    print(
        f"  dictionary: {len(defined)} of {len(wanted)} level-{level} words defined"
        f"  {len(defined) / len(wanted) * 100:.1f}%"
    )
    print(f"  {constrained} of {len(deps)} books are constrained by another")
    if args.order == "topological":
        print(f"  seed {args.seed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
