#!/usr/bin/env python3
"""Lengthen the spreads a book already has, rather than adding books.

**Measured 2026-09-25**: 227 level-one content books, median 164 words,
which is 10.2 words a spread against the operator standard of fifty give
or take thirty. Every one of the 227 is below the band.

Filling what exists multiplies the corpus by about five **without a
single new book**. It is also the better kind of growth: more books about
the same ninety-five units from the same teacher raises the token count
without raising the diversity, and looping on frequent collocations is
the trained model's most visible failure.

The spreads either side are shown to the teacher, so an addition belongs
where it lands rather than restating the page.

    PYTHONPATH=src:generators python3 generators/fill_spreads.py --limit 5
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import cast

from epagoge import prompt as prompts
from epagoge.book import WORDS_PER_SPREAD, book_head, parse_book, render_book
from epagoge.vocabulary import Vocabulary, load_vocabulary, unlicensed
from generate import ask, split_lines, well_formed
from generate_books import Tally, admissible_words

ROOT = Path(__file__).resolve().parent.parent


def admissible_sentences(
    raw: str, vocabulary: Vocabulary, level: int, tally: Tally
) -> list[str]:
    """Every sentence of an answer that is shaped and inside the ceiling.

    **Sentence by sentence, never whole.** Judging a whole passage throws
    all of it away on one bad word, and at the measured acceptance of
    about a half per sentence a passage of any length never survives.
    """
    out: list[str] = []
    for line in split_lines(raw):
        for piece in re.split(r"(?<=[.!?])\s+", line):
            text = piece.strip()
            if not text:
                continue
            if not well_formed(text):
                tally.reject("not a sentence")
                continue
            offending = sorted(set(unlicensed(vocabulary, text, level)))
            if offending:
                tally.reject(f"outside the ceiling: {' '.join(offending[:4])}")
                continue
            out.append(text)
    return out


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--level", type=int, default=1)
    parser.add_argument("--limit", type=int, default=5, help="books to fill")
    parser.add_argument("--attempts", type=int, default=2)
    parser.add_argument("--timeout", type=int, default=240)
    parser.add_argument(
        "--target",
        type=int,
        default=None,
        help="words a spread; defaults to the level's standard",
    )
    args = parser.parse_args(argv[1:])

    vocabulary = load_vocabulary(ROOT / "curriculum/vocabulary.json")
    admissible = admissible_words(vocabulary, args.level)
    nominal, _tolerance = WORDS_PER_SPREAD.get(args.level, (50, 30))
    target = args.target or nominal
    book_dir = ROOT / f"curriculum/books/level_{args.level}"

    tally = Tally()
    filled = 0
    added_words = 0
    for path in sorted(book_dir.glob("bk.*.md")):
        if filled >= args.limit:
            break
        if path.stem.startswith("bk.dictionary."):
            continue
        book, records = parse_book(path.read_text(encoding="utf-8"), path.name)
        entries = [cast(dict[str, object], r) for r in records]
        short = [
            n
            for n, entry in enumerate(entries)
            if len(str(entry["content"]).split()) < target
            and entry.get("defines") is None
        ]
        if not short:
            continue
        print(
            f"  {book.id}: {len(short)} spread(s) under {target} words", file=sys.stderr
        )

        grew = 0
        for index in short:
            entry = entries[index]
            body = str(entry["content"])
            for _attempt in range(args.attempts):
                have = len(body.split())
                if have >= target:
                    break
                question = prompts.fill_spread(
                    book.title,
                    str(entries[index - 1]["content"]) if index else "",
                    body,
                    str(entries[index + 1]["content"])
                    if index + 1 < len(entries)
                    else "",
                    args.level,
                    admissible,
                    target - have,
                )
                for sentence in admissible_sentences(
                    ask(question, timeout=args.timeout),
                    vocabulary,
                    args.level,
                    tally,
                ):
                    # **Stop at the target.** Taking every admissible
                    # sentence the teacher returns overshot a spread to two
                    # hundred words and a book to 1,658 against a cap of
                    # 1,600, so the first run wrote a book the gate refuses.
                    if len(body.split()) >= target:
                        break
                    if sentence not in body:
                        body = f"{body} {sentence}"
            if len(body.split()) > len(str(entry["content"]).split()):
                added_words += len(body.split()) - len(str(entry["content"]).split())
                entry["content"] = body
                grew += 1

        if not grew:
            print("    nothing usable", file=sys.stderr)
            continue
        head = book_head(book)
        path.write_text(render_book(head, entries), encoding="utf-8")
        total = sum(len(str(e["content"]).split()) for e in entries)
        print(f"    grew {grew} spread(s), book now {total} words", file=sys.stderr)
        filled += 1

    print(f"filled {filled} book(s), {added_words} word(s) added")
    for reason, count in sorted(tally.reasons.items(), key=lambda kv: -kv[1])[:6]:
        print(f"  {count:4}  {reason}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
