#!/usr/bin/env python3
"""Check that every defined word reduces to words needing no definition.

**Closure is a property that can be lost by adding a definition**, which
is exactly what coverage work does. A new entry leaning on an undefined
word puts that word on the frontier and takes the dictionary back out of
self-hosting, silently, while every other check stays green.

Exits non-zero when anything fails to ground. Coverage is reported and is
deliberately NOT enforced, since a level whose dictionary is incomplete is
unfinished rather than broken.

    PYTHONPATH=src python3 tools/validate_closure.py \
        <vocabulary.json> <book-dir> [level]
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import cast

from epagoge.book import dictionary_closure, load_book_dir
from epagoge.vocabulary import load_vocabulary, tokenise


def main(argv: list[str]) -> int:
    if len(argv) not in (3, 4):
        print(f"usage: {argv[0]} <vocabulary.json> <book-dir> [level]", file=sys.stderr)
        return 2
    level = int(argv[3]) if len(argv) == 4 else 1
    vocabulary = load_vocabulary(Path(argv[1]))
    seed = set(vocabulary.seed_words())
    _books, records = load_book_dir(Path(argv[2]))

    definitions: dict[str, str] = {}
    for record in records:
        entry = cast(dict[str, object], record)
        defines = cast(dict[str, object], entry.get("defines") or {})
        if defines.get("kind") == "word":
            definitions[str(defines["target"])] = str(entry["content"])

    def resolve(token: str) -> str | None:
        found = vocabulary.lookup(token)
        return found.word if found is not None else None

    closure = dictionary_closure(definitions, seed, tokenise, resolve)
    # **Seed words need no definition, so they do not belong in the
    # denominator.** Counting them made full coverage unreachable by
    # construction, since the dictionary is never going to define `red`.
    wanted = {
        term.word
        for term in vocabulary.terms
        if term.level <= level and term.word not in seed
    }
    ungrounded = len(definitions) - len(closure.grounded)

    print(f"{argv[2]}: dictionary at level {level}")
    # Some definitions target a seed word, which is allowed and is not
    # coverage. The figure is the share of words that NEED one and have one.
    covered = wanted & set(definitions)
    extra = len(definitions) - len(covered)
    print(
        f"  defined      {len(covered)} of {len(wanted)} words needing one"
        f"  {len(covered) / len(wanted) * 100:.1f}% coverage"
    )
    if extra:
        print(f"  also         {extra} definition(s) of seed words, not counted")
    print(f"  grounded     {len(closure.grounded)}  closure {closure.fraction:.1%}")
    print(f"  seed         {len(seed)} words need no definition and are excluded")
    outstanding = sorted(wanted - set(definitions))
    if outstanding:
        print(f"  undefined    {len(outstanding)}: {' '.join(outstanding[:15])}")

    if not (closure.undefined or closure.blocked or closure.cycles):
        print("  self-hosting  yes")
        return 0

    print(
        f"\nNOT self-hosting: {ungrounded} definition(s) do not reduce", file=sys.stderr
    )
    if closure.undefined:
        print(
            f"  frontier ({len(closure.undefined)}), used and never defined:",
            file=sys.stderr,
        )
        print("    " + " ".join(closure.undefined[:30]), file=sys.stderr)
    if closure.blocked:
        print(
            f"  blocked ({len(closure.blocked)}), resting on the frontier:",
            file=sys.stderr,
        )
        print("    " + " ".join(sorted(closure.blocked)[:30]), file=sys.stderr)
    for cycle in closure.cycles:
        print(f"  cycle: {' / '.join(cycle)}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
