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

from epagoge.book import load_book_dir


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("books", type=Path)
    parser.add_argument("out", type=Path)
    parser.add_argument("--order", choices=("authored", "shuffled"), default="authored")
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args(argv[1:])

    books, records = load_book_dir(args.books)
    by_id = {
        str(cast(dict[str, object], r)["id"]): cast(dict[str, object], r)
        for r in records
    }

    # A book is one document. Its internal order is not shuffled, because the
    # narrative is the reason a book exists, and shuffling inside one would
    # destroy the thing the ordering hypothesis is about.
    order = list(books)
    if args.order == "shuffled":
        random.Random(args.seed).shuffle(order)

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

    print(f"{args.out}: {len(order)} documents, {words} words, order {args.order}")
    if args.order == "shuffled":
        print(f"  seed {args.seed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
