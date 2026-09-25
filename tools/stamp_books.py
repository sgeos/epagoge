"""Stamp each book with its author, licence, and publication dates.

Four of a book's six metadata fields are not prose and must not be
written by a teacher. Two are decisions and two are derivations.

**The dates are derived from version history, never assigned.** A date a
person types is a claim; a date read from the commit that introduced the
file is a fact, and this project's post-facto analysis requirement is that
an artifact can say when it came to exist and be checked. `first_published`
is the date of the earliest commit touching the file and `published` the
date of the latest.

**The author and the licence are decisions**, recorded in
`docs/decisions/BOOK_ATTRIBUTION.md` along with what was rejected. They are
constants here rather than arguments so that the tree carries one answer
rather than whatever the last invocation passed.

**A book modified in the working tree is stamped but its `published` date
is not trusted**, because the edit is not in history yet and the date it
would produce is the date of the previous commit. `--check` says so rather
than reporting a false agreement.

    PYTHONPATH=src python3 tools/stamp_books.py --level 1
    PYTHONPATH=src python3 tools/stamp_books.py --level 1 --check
"""

from __future__ import annotations

import argparse
import subprocess  # noqa: S404
import sys
from collections import defaultdict
from dataclasses import replace
from pathlib import Path
from typing import cast

from epagoge.book import book_head, parse_book, render_book

ROOT = Path(__file__).resolve().parent.parent

AUTHOR = "Epagoge"
"""Who the book is by.

**Not a person.** The prose is written by a local teacher model against
prompts from this project and accepted by its checks, with some
definitions authored by hand. Which records came by which route is not
recoverable from the history, so a per-book split would be invented.

Naming a person would also assert an authorship the project has said may
not exist: `docs/decisions/LICENSING.md` records that work without human
authorship may not be copyrightable at all, which is why the corpus is
CC0 rather than permissively licensed.

The project is therefore the author of record. Rationale and the rejected
alternatives are in `docs/decisions/BOOK_ATTRIBUTION.md`.
"""

LICENCE = "CC0-1.0"
"""The corpus licence, per `LICENSING.md`.

The SPDX identifier rather than a prose name, because the field is read by
tools as often as by people.
"""


def history_dates(directory: Path) -> dict[str, tuple[str, str]]:
    """First and last commit date for every file under a directory.

    One pass over the log rather than one call per file. At 246 books the
    per-file form costs a subprocess each and answers the same question.
    """
    result = subprocess.run(  # noqa: S603
        [  # noqa: S607
            "git",
            "log",
            "--format=%ad",
            "--date=short",
            "--name-only",
            "--",
            str(directory.relative_to(ROOT)),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    seen: dict[str, list[str]] = defaultdict(list)
    date = ""
    for line in result.stdout.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if len(stripped) == 10 and stripped[4] == "-" and stripped[7] == "-":
            date = stripped
            continue
        if date:
            seen[stripped].append(date)
    # git log is newest first, so the last date recorded is the earliest.
    return {path: (dates[-1], dates[0]) for path, dates in seen.items()}


def modified_in_tree(directory: Path) -> set[str]:
    result = subprocess.run(  # noqa: S603
        ["git", "status", "--porcelain", "--", str(directory.relative_to(ROOT))],  # noqa: S607
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    )
    return {line[3:].strip() for line in result.stdout.splitlines() if line.strip()}


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--level", type=int, default=1)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv[1:])

    directory = ROOT / f"curriculum/books/level_{args.level}"
    dates = history_dates(directory)
    dirty = modified_in_tree(directory)

    stamped = 0
    unchanged = 0
    missing: list[str] = []
    untracked: list[str] = []
    stale: list[str] = []

    for path in sorted(directory.glob("bk.*.md")):
        relative = str(path.relative_to(ROOT))
        book, records = parse_book(path.read_text(encoding="utf-8"), path.name)
        entries = [cast(dict[str, object], r) for r in records]

        known = dates.get(relative)
        if known is None:
            untracked.append(book.id)
            first = last = ""
        else:
            first, last = known

        if args.check:
            absent = [
                name
                for name in ("about", "teaches", "author", "licence")
                if not getattr(book, name)
            ]
            if not book.first_published or not book.published:
                absent.append("dates")
            if absent:
                missing.append(f"{book.id}: {', '.join(absent)}")
            elif known and relative not in dirty and book.published != last:
                stale.append(f"{book.id}: says {book.published}, history says {last}")
            continue

        # `replace` rather than a field list. Two constructions in this
        # project each dropped five fields by enumerating them.
        wanted = replace(
            book,
            author=AUTHOR,
            licence=LICENCE,
            first_published=first or book.first_published,
            published=last or book.published,
        )
        if wanted == book:
            unchanged += 1
            continue
        path.write_text(render_book(book_head(wanted), entries), encoding="utf-8")
        stamped += 1

    if args.check:
        print(f"  books            {len(list(directory.glob('bk.*.md')))}")
        print(f"  missing a field  {len(missing)}")
        for line in missing[:20]:
            print(f"    {line}")
        if untracked:
            print(f"  not yet in history {len(untracked)}, dates cannot be derived")
        if stale:
            print(f"  published date disagrees with history {len(stale)}")
            for line in stale[:20]:
                print(f"    {line}")
        return 1 if missing or stale else 0

    print(f"stamped {stamped}, already correct {unchanged}")
    if untracked:
        print(f"  {len(untracked)} not in history yet, dates left alone")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
