#!/usr/bin/env python3
"""Check the thesaurus covers every sense and names reachable words.

**Two roles.** During authoring this finds words admitted without their
opposite. Afterwards it is level-one reference material beside the
dictionary, which is why coverage is required and why every word it names
must itself be admissible at the level.

Exits non-zero on any violation, so it is usable as a gate.

    PYTHONPATH=src python3 tools/validate_thesaurus.py \
        <thesaurus.json> <vocabulary.json> [level]
"""

from __future__ import annotations

import sys
from pathlib import Path

from epagoge.thesaurus import load, validate
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
        for v in violations[:20]:
            print(f"  [{v.code}] {v.detail}", file=sys.stderr)
        if len(violations) > 20:
            print(f"  ... and {len(violations) - 20} more", file=sys.stderr)
        return 1

    opposed = sum(1 for e in thesaurus.entries if e.antonyms)
    paired = sum(1 for e in thesaurus.entries if e.synonyms)
    senses = sum(1 for t in vocabulary.terms if t.level <= level)
    print(f"{argv[1]}: valid")
    print(
        f"  entries      {len(thesaurus.entries)} over {len(thesaurus.words())} words"
    )
    print(f"  covering     {senses} senses admitted at level {level}")
    print(f"  antonyms     {opposed} entries carry one")
    print(f"  synonyms     {paired} entries carry one")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
