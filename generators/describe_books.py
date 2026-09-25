#!/usr/bin/env python3
"""Write the back cover of a book: what it is about and what it teaches.

**These two fields are the only place a level's vocabulary ceiling does
not apply**, because they are written for a person rather than for the
corpus and are not text a model trains on. The title goes on the front,
these go on the back, and between them they are what a parent picking the
book off a shelf has to go on.

That also makes this the one generation task the teacher cannot fail on
vocabulary, which is why it is worth doing in bulk while the corpus work
is blocked on other things.

**The book's own text is the input.** Asking what a book teaches from its
title alone produces the title again in more words.

    PYTHONPATH=src:generators python3 generators/describe_books.py --limit 10
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import cast

from generate import ask
from epagoge.book import book_head, parse_book, render_book

ROOT = Path(__file__).resolve().parent.parent

ABOUT_RE = re.compile(r"^ABOUT:\s*(.+)$", re.MULTILINE)
TEACHES_RE = re.compile(r"^TEACHES:\s*(.+)$", re.MULTILINE)

MIN_WORDS = 12
"""Shortest description accepted.

A sentence of six words restates the title. The field exists because
sixteen spreads in eight hundred words often cannot say what a book is
for, and a description that short has the same problem.
"""

MAX_WORDS = 120
"""Longest description kept, before the rest is dropped at a sentence end.

Back-cover copy. Anything past this is an essay and a curator scanning a
shelf will not read it.
"""


def prompt_for(title: str, subject: str, body: str) -> str:
    return "\n".join(
        [
            "Write the back cover of a children's book.",
            "",
            f"Its title is: {title}",
            f"It is about the topic: {subject}",
            "",
            "Here is the whole book:",
            "",
            body[:4000],
            "",
            "Write exactly two lines, in this format:",
            "",
            "ABOUT: <what the book is about>",
            "TEACHES: <what a reader should come away knowing>",
            "",
            "Rules:",
            "  - Ordinary English. You are NOT limited to the book's words.",
            "  - Write for a parent choosing books, who knows nothing about",
            "    this project. Say what the book actually does.",
            "  - Name the ideas plainly, including any the book shows",
            "    rather than states.",
            "  - Two or three sentences each. No headings, no lists.",
            "  - Do not praise the book and do not address the reader.",
        ]
    )


def trim(text: str) -> str:
    """Keep whole sentences up to the cap."""
    words = text.split()
    if len(words) <= MAX_WORDS:
        return text.strip()
    kept: list[str] = []
    for piece in re.split(r"(?<=[.!?])\s+", text.strip()):
        if kept and len(" ".join([*kept, piece]).split()) > MAX_WORDS:
            break
        kept.append(piece)
    return " ".join(kept) if kept else " ".join(words[:MAX_WORDS])


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--level", type=int, default=1)
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--attempts", type=int, default=2)
    parser.add_argument("--timeout", type=int, default=240)
    parser.add_argument("--rewrite", action="store_true")
    args = parser.parse_args(argv[1:])

    book_dir = ROOT / f"curriculum/books/level_{args.level}"
    written = 0
    refused = 0
    for path in sorted(book_dir.glob("bk.*.md")):
        if written >= args.limit:
            break
        book, records = parse_book(path.read_text(encoding="utf-8"), path.name)
        if book.about and book.teaches and not args.rewrite:
            continue
        entries = [cast(dict[str, object], r) for r in records]
        body = "\n".join(str(e["content"]) for e in entries)

        about = ""
        teaches = ""
        for _attempt in range(args.attempts):
            raw = ask(prompt_for(book.title, book.subject, body), timeout=args.timeout)
            got_about = ABOUT_RE.search(raw)
            got_teaches = TEACHES_RE.search(raw)
            if got_about and len(got_about.group(1).split()) >= MIN_WORDS:
                about = trim(got_about.group(1))
            if got_teaches and len(got_teaches.group(1).split()) >= MIN_WORDS:
                teaches = trim(got_teaches.group(1))
            if about and teaches:
                break
        if not (about and teaches):
            refused += 1
            print(f"  {book.id}: nothing usable", file=sys.stderr)
            continue

        described = type(book)(
            id=book.id,
            level=book.level,
            title=book.title,
            subject_kind=book.subject_kind,
            subject=book.subject,
            records=book.records,
            about=about,
            teaches=teaches,
        )
        path.write_text(render_book(book_head(described), entries), encoding="utf-8")
        written += 1
        print(f"  {book.id}: described", file=sys.stderr)

    print(f"described {written} book(s), {refused} refused")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
