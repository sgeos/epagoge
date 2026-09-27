#!/usr/bin/env python3
"""Rewrite a book title that the level's vocabulary does not carry.

**A title used to be prose for a person and is now text the model trains
on.** `docs/decisions/STRUCTURAL_TOKENS.md` announces each work with its
title in the stream, on the measured finding that deleting a structural
announcement makes the prose after it harder to predict. The moment that
landed, a title outside the lexicon stopped being a presentation choice and
became an unknown token in training data.

**Two files disagreed about this and the disagreement is now settled.**
`describe_books.py` says the vocabulary ceiling does not apply to `about`
and `teaches` because they are written for a person and are not trained on,
which stays true. `cross_books.py` extended that to the title, reasoning
that it is also prose for a person. **That was right when it was written and
is wrong now**, and it cost 47 titles of 400, every one of them naming a
concept identifier rather than a word: `emptiness`, `discourse marker`,
`conservation`, `correspondence`, `causal chain`.

**The book's own text is the input, not the old title.** Asking for a
rewrite of a title that names concepts produces the concepts again.

**Nothing is written unless the new title is inside the ceiling**, checked
by exact tokenisation rather than by asking the teacher nicely, since a soft
instruction to stay inside a word list is one the teacher does not reliably
follow. A book whose title cannot be replaced keeps the one it has and is
reported, because a bad title that is visible is better than a bad title
that a tool has silently blessed.

    PYTHONPATH=src:generators python3 generators/retitle_books.py --limit 10
"""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Mapping
from dataclasses import replace
from pathlib import Path
from typing import cast

from epagoge.book import book_head, parse_book, render_book
from epagoge.vocabulary import load_vocabulary, unlicensed
from generate import ask

ROOT = Path(__file__).resolve().parent.parent

TITLE_RE = re.compile(r"^TITLE:\s*(.+)$", re.MULTILINE)

MIN_WORDS = 3
"""Shortest title accepted.

One or two words names a topic rather than titling a book, and the corpus's
own titles are short sentences: "She can lift the cup".
"""

MAX_WORDS = 12
"""Longest title kept.

**Set from the corpus rather than guessed, after guessing wrongly.** At 10
this rejected eleven books of forty-seven, and every rejection was this
bound rather than the vocabulary. `bk.b1.mending.x_discourse_marker` was
refused five times for "A cut heals but a broken cup does not fix itself",
which is eleven words and entirely inside the lexicon.

The 400 shipped titles run from 1 to 11 words, with 80 at four, 80 at six
and one at eleven. Twelve admits the observed range with a word to spare.

**Retrying did not help and could not have.** The teacher answered
identically on all five attempts, so attempts are only worth spending where
the answer varies, and a shape bound is not something a second ask can
satisfy.
"""


def prompt_for(body: str, substitutions: Mapping[str, str] | None = None) -> str:
    """Ask for one title, drawn from the book's own words.

    **The admissible word list is deliberately not sent.** At 849 words it
    put the prompt at about 3,548 tokens against a budget of 3,328 and
    `generate.ask` refused it rather than let the server truncate silently.

    Restricting the teacher to the book's own words is the better
    instruction anyway. Every word in the book is admissible by
    construction, so the constraint is stricter than the ceiling and
    shorter to state, and a title built from the book's own words is what a
    title should be. The ceiling is still checked afterwards.

    **The substitutions are supplied because naming a banned word is not
    supplying the replacement**, which `epagoge.prompt` learned first. A
    title was refused four times running for `it's`, a contraction the
    lexicon carries a replacement for, and the teacher returned the same
    line every time because nothing told it what to write instead.

    **The length bound is stated here as well as enforced below, and it was
    not at first.** Every one of the sixteen refusals in the first two runs
    was the length bound rather than the vocabulary, on titles that were
    entirely inside the lexicon, and the teacher answered identically on
    every retry. **A constraint enforced only by rejection is one the
    teacher cannot satisfy**, and spending attempts on it is spending them
    on an answer that will not change.
    """
    return "\n".join(
        [
            "Here is a picture book for a young child.",
            "",
            body,
            "",
            "Write one title for it. The title should say what happens in",
            "the book, as a short sentence a child could read.",
            "",
            f"The title must be between {MIN_WORDS} and {MAX_WORDS} words.",
            "",
            "Use ONLY words that appear in the book above. Do not use any",
            "other word. Do not name a topic or a subject.",
            *(
                [
                    "",
                    "These are NOT allowed. Write the replacement instead:",
                    *(
                        f'  {banned}  ->  write "{instead}"'
                        for banned, instead in sorted((substitutions or {}).items())
                    ),
                ]
                if substitutions
                else []
            ),
            "",
            "Answer with exactly one line, in this form:",
            "TITLE: <the title>",
        ]
    )


def usable(title: str) -> bool:
    """Shape only. Vocabulary is checked separately and is not negotiable."""
    words = title.split()
    return MIN_WORDS <= len(words) <= MAX_WORDS


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--level", type=int, default=1)
    parser.add_argument("--limit", type=int, default=0, help="0 means every one")
    parser.add_argument("--attempts", type=int, default=3)
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--books", type=Path, default=ROOT / "curriculum/books/level_1")
    parser.add_argument(
        "--check",
        action="store_true",
        help="report titles outside the ceiling and write nothing",
    )
    args = parser.parse_args(argv[1:])

    vocabulary = load_vocabulary(ROOT / "curriculum/vocabulary.json")

    paths = sorted(p for p in args.books.glob("*.md"))
    outside: list[tuple[Path, str, list[str]]] = []
    for path in paths:
        book, _ = parse_book(path.read_text(encoding="utf-8"), path.name)
        offending = sorted(set(unlicensed(vocabulary, book.title or "", args.level)))
        if offending:
            outside.append((path, book.title or "", offending))

    print(
        f"{len(outside)} of {len(paths)} title(s) outside the "
        f"level-{args.level} ceiling"
    )
    if args.check:
        for path, title, offending in outside:
            print(f"  {path.stem:38s} {title!r} -> {' '.join(offending)}")
        return 0

    wanted = outside if args.limit <= 0 else outside[: args.limit]
    rewritten = 0
    refused: list[str] = []
    for path, old, _ in wanted:
        book, records = parse_book(path.read_text(encoding="utf-8"), path.name)
        by_id = {
            str(cast("dict[str, object]", r)["id"]): cast("dict[str, object]", r)
            for r in records
        }
        body = "\n".join(
            str(by_id[i].get("content", "")) for i in book.records if i in by_id
        )
        new = ""
        for _ in range(args.attempts):
            raw = ask(prompt_for(body, vocabulary.substitutions), timeout=args.timeout)
            found = TITLE_RE.search(raw or "")
            if not found:
                continue
            candidate = found.group(1).strip().rstrip(".")
            if not usable(candidate):
                continue
            if unlicensed(vocabulary, candidate, args.level):
                continue
            new = candidate
            break
        if not new:
            refused.append(path.stem)
            print(f"  {path.stem:38s} REFUSED, keeping {old!r}", file=sys.stderr)
            continue
        entries = [by_id[i] for i in book.records]
        path.write_text(
            render_book(book_head(replace(book, title=new)), entries),
            encoding="utf-8",
        )
        rewritten += 1
        print(f"  {path.stem:38s} {old!r} -> {new!r}")

    print(f"rewrote {rewritten}, refused {len(refused)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
