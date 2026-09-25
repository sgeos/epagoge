#!/usr/bin/env python3
"""Put a dictionary book's entries in alphabetical order.

**A dictionary nobody can look a word up in is a list.** The entries were
written in the order they were authored, which is the order the closure
frontier retired words in, and that is meaningful to nothing and nobody.

Operator direction, 2026-09-25.

Confined to dictionary books. A content book's order is its narrative,
and the subject statement and definitions come first by rule, so sorting
one would be rewriting it.

    PYTHONPATH=src python3 tools/sort_dictionary.py curriculum/books/level_1
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import cast

from epagoge.book import parse_book, render_book


def sort_book(path: Path, *, write: bool = True) -> int:
    """Rewrite one dictionary in order. Returns the entries out of place.

    With ``write`` false nothing is written and the count is reported, so
    the same code answers the gate and does the repair. A checker that
    shares no code with the fixer drifts from it.
    """
    book, records = parse_book(path.read_text(encoding="utf-8"), path.name)
    entries = [cast(dict[str, object], r) for r in records]

    def key(entry: dict[str, object]) -> tuple[str, str]:
        defines = cast(dict[str, object], entry.get("defines") or {})
        target = str(defines.get("target", ""))
        # Fall back to the id so an entry defining nothing still has a
        # stable place rather than floating to wherever sort puts equals.
        return (target, str(entry.get("id", "")))

    ordered = sorted(entries, key=key)
    moved = sum(1 for a, b in zip(entries, ordered, strict=True) if a is not b)
    if not moved or not write:
        return moved
    head = {
        "id": book.id,
        "level": book.level,
        "title": book.title,
        "subject": {"kind": book.subject_kind.value, "target": book.subject},
    }
    path.write_text(render_book(head, ordered), encoding="utf-8")
    return moved


def main(argv: list[str]) -> int:
    argv = list(argv)
    check = "--check" in argv
    if check:
        argv.remove("--check")
    if len(argv) < 2:
        print(f"usage: {argv[0]} [--check] <book-dir>...", file=sys.stderr)
        return 2
    total = 0
    for name in argv[1:]:
        directory = Path(name)
        if not directory.is_dir():
            print(f"no such directory: {directory}", file=sys.stderr)
            return 2
        for path in sorted(directory.glob("bk.dictionary.*.md")):
            moved = sort_book(path, write=not check)
            total += moved
            if moved or not check:
                print(f"{path.name}: {moved} entry(s) out of order")
    if check:
        if total:
            print(f"{total} entry(s) out of alphabetical order", file=sys.stderr)
            return 1
        print("every dictionary is in alphabetical order")
        return 0
    print(f"{total} entry(s) moved in total")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
