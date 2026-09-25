#!/usr/bin/env python3
"""Bring thesaurus coverage back in line with the lexicon.

Adds a bare entry for every level-one sense that has none, and drops
entries whose sense no longer exists, which happens when an inflection is
merged into its base. **Relations are never invented** and never removed
from a surviving entry, because a pair is a judgement and this is
bookkeeping.

    PYTHONPATH=src python3 tools/sync_thesaurus.py [--level N]
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
    parser.add_argument("--level", type=int, default=1)
    args = parser.parse_args(argv[1:])

    vocabulary = load_vocabulary(ROOT / "curriculum/vocabulary.json")
    path = ROOT / "curriculum/thesaurus.json"
    payload = cast(dict[str, object], json.loads(path.read_text(encoding="utf-8")))
    entries = cast(list[dict[str, object]], payload["senses"])

    # **Add for this level, remove only what the lexicon no longer holds
    # at any level.** Keyed on the level for both, syncing at level one
    # deleted every level-two entry, because a level-two sense is not a
    # level-one sense and looked stale.
    wanted = {
        (term.word, term.concept)
        for term in vocabulary.terms
        if term.level <= args.level
    }
    senses = {(term.word, term.concept) for term in vocabulary.terms}
    core = set(vocabulary.core)

    kept: list[dict[str, object]] = []
    removed: list[str] = []
    for entry in entries:
        word, concept = str(entry["word"]), str(entry["concept"])
        if concept == "":
            if word in core:
                kept.append(entry)
            else:
                removed.append(f"{word} (core word no longer core)")
            continue
        if (word, concept) in senses:
            kept.append(entry)
        else:
            removed.append(f"{word} under {concept}")

    covered = {(str(e["word"]), str(e["concept"])) for e in kept}
    added = [s for s in sorted(wanted) if s not in covered]
    for word, concept in added:
        kept.append({"word": word, "concept": concept})

    # A relation may name a word that is no longer admissible at this level.
    admissible = set(core) | set(vocabulary.exempt)
    for term in vocabulary.terms:
        admissible.update(term.surface_forms())
    stale = 0
    for entry in kept:
        for field in ("antonyms", "synonyms"):
            related = cast(list[str], entry.get(field) or [])
            surviving = [w for w in related if w in admissible]
            if len(surviving) != len(related):
                stale += len(related) - len(surviving)
            if surviving:
                entry[field] = surviving
            elif field in entry:
                del entry[field]

    kept.sort(key=lambda e: (str(e["word"]), str(e["concept"])))
    payload["senses"] = kept
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"entries {len(kept)}: added {len(added)}, removed {len(removed)}")
    for line in removed[:10]:
        print(f"  removed {line}")
    if stale:
        print(f"  dropped {stale} relation(s) naming a word no longer admissible")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
