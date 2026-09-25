#!/usr/bin/env python3
"""Add synonym and antonym relations to the thesaurus, symmetrically.

Reads JSON of the shape ``{"synonyms": [["a","b"], ...], "antonyms": [...]}``
and writes each relation into both ends, because antonymy and synonymy run
both ways and the validator enforces that for antonyms.

**Nothing is written unless every pair passes.** A word must be admissible
at the level, and where it carries several senses the sense must be given
as ``word/concept``, since `right` opposes `left` as a direction and
`wrong` as a judgement.

    PYTHONPATH=src python3 tools/relate.py pairs.json [--level N]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import cast

from epagoge.vocabulary import load_vocabulary

ROOT = Path(__file__).resolve().parent.parent


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument("--level", type=int, default=1)
    args = parser.parse_args(argv[1:])

    payload = cast(dict[str, list[list[str]]], json.loads(args.file.read_text()))
    vocabulary = load_vocabulary(ROOT / "curriculum/vocabulary.json")
    path = ROOT / "curriculum/thesaurus.json"
    book = cast(dict[str, object], json.loads(path.read_text(encoding="utf-8")))
    entries = cast(list[dict[str, object]], book["senses"])

    by_word: dict[str, list[dict[str, object]]] = {}
    for entry in entries:
        by_word.setdefault(str(entry["word"]), []).append(entry)

    admissible = set(vocabulary.core) | set(vocabulary.exempt)
    for term in vocabulary.terms:
        if term.level <= args.level:
            admissible.update(term.surface_forms())

    problems: list[str] = []
    resolved: list[tuple[str, dict[str, object], str]] = []

    def find(spec: str) -> dict[str, object] | None:
        if "/" in spec:
            word, concept = spec.split("/", 1)
            return next(
                (e for e in by_word.get(word, []) if str(e["concept"]) == concept), None
            )
        candidates = by_word.get(spec, [])
        if len(candidates) == 1:
            return candidates[0]
        if len(candidates) > 1:
            problems.append(f"{spec}: has {len(candidates)} senses, say word/concept")
        return None

    for field in ("synonyms", "antonyms"):
        for pair in payload.get(field, []):
            left, right = pair
            for spec, other in ((left, right), (right, left)):
                entry = find(spec)
                plain = other.split("/", 1)[0]
                if entry is None:
                    if not any(p.startswith(f"{spec}:") for p in problems):
                        problems.append(f"{spec}: no entry at level {args.level}")
                    continue
                if plain not in admissible:
                    problems.append(f"{plain}: not admissible at level {args.level}")
                    continue
                if plain == str(entry["word"]):
                    problems.append(f"{spec}: paired with itself")
                    continue
                resolved.append((field, entry, plain))

    if problems:
        print(f"{len(problems)} problem(s), nothing written:", file=sys.stderr)
        for line in sorted(set(problems)):
            print(f"  {line}", file=sys.stderr)
        return 1

    added = 0
    for field, entry, other in resolved:
        current = cast(list[str], entry.setdefault(field, []))
        if other not in current:
            current.append(other)
            current.sort()
            added += 1
    path.write_text(
        json.dumps(book, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    carry = sum(1 for e in entries if e.get("synonyms"))
    print(f"added {added} relation(s); {carry} entries now carry a synonym")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
