#!/usr/bin/env python3
"""Report substitution keys that their own level nonetheless admits.

A substitution bans a word and an admission commits to teaching it, so a key
admissible at a level is a contradiction. Prompts already drop such keys
through ``substitutions_at``. Above level one a contradiction is expected,
because the table is a level-one triage and later levels admit some of its
words. At level one it is a defect, so ``--strict`` exits non-zero.

**Strict at level one since 2026-10-07**, when the operator reconciled the
seven level-one contradictions in favor of the admissions, all of them in
heavy use in level-one books.

    PYTHONPATH=src python3 tools/check_substitutions.py --level 2
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from epagoge.vocabulary import contradicted_substitutions, load_vocabulary

ROOT = Path(__file__).resolve().parent.parent


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--level", type=int, required=True)
    parser.add_argument(
        "--vocabulary", type=Path, default=ROOT / "curriculum/vocabulary.json"
    )
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args(argv[1:])
    if args.level < 1:
        parser.error("--level must be at least 1")
    vocabulary = load_vocabulary(args.vocabulary)
    found = contradicted_substitutions(vocabulary, args.level)
    print(
        f"level {args.level}: {len(found)} of {len(vocabulary.substitutions)} "
        f"substitution keys are admissible and are not shown as banned"
    )
    for word in found:
        print(f"  {word}  (substitution {vocabulary.substitutions[word]!r})")
    return 1 if args.strict and found else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
