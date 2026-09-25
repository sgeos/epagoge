#!/usr/bin/env python3
"""Check that no antonym has been admitted without its opposite.

Exits non-zero on any violation, so it is usable as a gate.

    PYTHONPATH=src python3 tools/validate_thesaurus.py \
        <thesaurus.json> <vocabulary.json> [level]
"""

from __future__ import annotations

import sys
from pathlib import Path

from epagoge.thesaurus import admissible_at, load, validate
from epagoge.vocabulary import load_vocabulary


def main(argv: list[str]) -> int:
    if len(argv) not in (3, 4):
        print(
            f"usage: {argv[0]} <thesaurus.json> <vocabulary.json> [level]",
            file=sys.stderr,
        )
        return 2
    level = int(argv[3]) if len(argv) == 4 else 1
    thesaurus = load(Path(argv[1]))
    vocabulary = load_vocabulary(Path(argv[2]))
    violations = validate(thesaurus, vocabulary, level)
    if violations:
        print(f"{len(violations)} violation(s) in {argv[1]}:", file=sys.stderr)
        for v in violations:
            print(f"  [{v.code}] {v.detail}", file=sys.stderr)
        return 1

    reachable = sum(
        1 for pair in thesaurus.antonyms if admissible_at(vocabulary, pair[0], level)
    )
    print(f"{argv[1]}: valid")
    print(f"  pairs        {len(thesaurus.antonyms)}")
    print(f"  words        {len(thesaurus.words())}")
    print(f"  at level {level}    {reachable} pairs with both ends reachable")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
