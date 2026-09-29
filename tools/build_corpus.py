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
        [--order curriculum|topological] [--seed N]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import cast

from epagoge import schedule as sched
from epagoge.book import load_book_dir, word_definitions
from epagoge.concept_graph import ConceptGraph
from epagoge.ordering import book_order
from epagoge.thesaurus import load as load_thesaurus


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("books", type=Path)
    parser.add_argument("out", type=Path)
    parser.add_argument(
        "--order", choices=("curriculum", "topological"), default="curriculum"
    )
    parser.add_argument("--schedule", type=Path, default=None)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument(
        "--graph", type=Path, default=Path("curriculum/graph/concepts.json")
    )
    parser.add_argument(
        "--vocabulary", type=Path, default=Path("curriculum/vocabulary.json")
    )
    parser.add_argument("--no-dictionary", action="store_true")
    parser.add_argument(
        "--thesaurus", type=Path, default=Path("curriculum/thesaurus.json")
    )
    parser.add_argument("--no-thesaurus", action="store_true")
    args = parser.parse_args(argv[1:])

    all_books, records = load_book_dir(args.books)
    if not all_books:
        parser.error("book directory is empty")
    levels = {book.level for book in all_books}
    if len(levels) != 1:
        parser.error("export one level at a time")
    level = next(iter(levels))
    plan_path = args.schedule or Path(f"curriculum/schedule/level_{level:02d}.json")
    plan = sched.load(plan_path)
    graph = ConceptGraph.load(args.graph)
    try:
        names, text_by_id, _ = book_order(
            args.books, graph, args.seed, args.order, plan
        )
    except ValueError as exc:
        parser.error(str(exc))
    by_book = {book.id: book for book in all_books}
    order = [by_book[name] for name in names]

    args.out.parent.mkdir(parents=True, exist_ok=True)
    words = 0
    with args.out.open("w", encoding="utf-8") as handle:
        for book in order:
            text = text_by_id[book.id]
            words += len(text.split())
            handle.write(
                json.dumps({"id": book.id, "level": book.level, "text": text}) + "\n"
            )

        # **The dictionary is last, and it is a consolidation.** Every word
        # in it was already defined in context by the book that introduced
        # it. Seven hundred definitions at the front, with no story around
        # them, is the lifeless-assertion failure the books exist to fix.
        # Canonical, not whichever record was read last. Which definition
        # reached the stream used to depend on file order.
        defined = word_definitions(
            all_books, [cast(dict[str, object], r) for r in records]
        )
        level = order[0].level if order else 1

        # **The thesaurus is reference material too.** It is an analysis
        # tool while the lexicon is being authored and a level-one
        # reference afterwards, which is the same dual role the dictionary
        # has. Only entries carrying a relation are emitted, since an entry
        # recording that a noun opposes nothing teaches a reader nothing.
        thesaurus_lines: list[str] = []
        if not args.no_thesaurus and args.thesaurus.exists():
            seen_pairs: set[tuple[str, str]] = set()
            for entry in load_thesaurus(args.thesaurus).entries:
                for other in entry.antonyms:
                    key = tuple(sorted((entry.word, other)))
                    if key in seen_pairs:
                        continue
                    seen_pairs.add((key[0], key[1]))
                    thesaurus_lines.append(f"{key[0]} and {key[1]} are opposites.")
                for other in entry.synonyms:
                    key = tuple(sorted((entry.word, other)))
                    if key in seen_pairs:
                        continue
                    seen_pairs.add((key[0], key[1]))
                    thesaurus_lines.append(f"{key[0]} and {key[1]} mean the same.")
        if thesaurus_lines:
            text = "\n".join(sorted(thesaurus_lines))
            words += len(text.split())
            handle.write(
                json.dumps(
                    {"id": f"thesaurus.level_{level}", "level": level, "text": text}
                )
                + "\n"
            )

        if not args.no_dictionary and defined:
            text = "\n".join(f"{w}: {defined[w]}" for w in sorted(defined))
            words += len(text.split())
            handle.write(
                json.dumps(
                    {"id": f"dictionary.level_{level}", "level": level, "text": text}
                )
                + "\n"
            )

    wanted = {
        t["word"]
        for t in cast(
            list[dict[str, object]],
            json.loads(args.vocabulary.read_text(encoding="utf-8"))["terms"],
        )
        if cast(int, t["level"]) <= level
    }
    total = (
        len(order)
        + (0 if args.no_dictionary or not defined else 1)
        + (1 if thesaurus_lines else 0)
    )
    print(f"{args.out}: {total} documents, {words} words, order {args.order}")
    print(
        f"  dictionary: {len(defined)} of {len(wanted)} level-{level} words defined"
        f"  {len(defined) / len(wanted) * 100:.1f}%"
    )
    print(f"  thesaurus:  {len(thesaurus_lines)} relations")
    if args.order == "topological":
        print(f"  seed {args.seed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
