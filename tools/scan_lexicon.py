#!/usr/bin/env python3
"""Read text, and report the words it uses that the lexicon does not carry.

**A scanned lexicon is a proposal, not a decision.** This project's thesis
is that uncurated input produces undesirable properties, and a frequency
list from any corpus is uncurated by construction. So this ranks and
reports; admitting is still a judgement made one word at a time, through
`admit.py`, which requires a definition that reduces to the seed.

Reports three things about each candidate:

- **how often it occurs**, because a word used once is a word the source
  happened to contain rather than one the level needs;
- **whether the lexicon already carries it at a higher level**, which
  makes it a question about level rather than about admission;
- **whether it is a form of a word already admitted**, which is usually a
  missing inflection rather than a new word, and this project has found
  eleven of those the hard way.

Nothing from the source is copied into the repository. What comes out is a
list of English words, which is a fact about the source rather than a part
of it. That said, the licence of anything scanned is the operator's to
settle, and `../docs/decisions/READING_LEVEL_RESEARCH.md` lists sources
that need no settling.

    PYTHONPATH=src python3 tools/scan_lexicon.py --level 2 reader.txt
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from pathlib import Path

from epagoge.inflection import plural, verb_forms
from epagoge.vocabulary import load_vocabulary, tokenise

ROOT = Path(__file__).resolve().parent.parent


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("--level", type=int, default=2)
    parser.add_argument(
        "--min-count", type=int, default=2, help="ignore words rarer than this"
    )
    parser.add_argument("--top", type=int, default=60)
    args = parser.parse_args(argv[1:])

    vocabulary = load_vocabulary(ROOT / "curriculum/vocabulary.json")
    # **Core and exempt count as admissible.** The first version omitted
    # exempt and reported proper nouns as candidates, which is the same
    # mistake as asking whether a name should be defined.
    here = (
        {
            form
            for term in vocabulary.terms
            if term.level <= args.level
            for form in term.surface_forms()
        }
        | set(vocabulary.core)
        | set(vocabulary.exempt)
    )
    anywhere: dict[str, int] = {}
    for term in vocabulary.terms:
        for form in term.surface_forms():
            anywhere[form] = min(anywhere.get(form, term.level), term.level)

    # A form of an admitted word is a missing inflection, not a new word.
    derived: dict[str, str] = {}
    for term in vocabulary.terms:
        for form in (plural(term.word), *verb_forms(term.word)):
            derived.setdefault(form, term.word)

    counts: Counter[str] = Counter()
    read = 0
    for path in args.files:
        if not path.is_file():
            print(f"no such file: {path}", file=sys.stderr)
            return 2
        text = path.read_text(encoding="utf-8", errors="replace")
        read += len(text)
        counts.update(tokenise(text))

    candidates = [
        (word, n)
        for word, n in counts.most_common()
        if word not in here and n >= args.min_count and word.isalpha()
    ]
    print(f"read {read} characters, {sum(counts.values())} tokens")
    print(f"distinct words {len(counts)}, already admissible {len(here)}")
    print(f"candidates at level {args.level}: {len(candidates)}")
    print()
    print(f"{'count':>6}  {'word':<18} note")
    for word, n in candidates[: args.top]:
        if word in anywhere:
            note = f"already admitted at level {anywhere[word]}"
        elif word in derived:
            note = f"a form of {derived[word]!r}, which is admitted"
        else:
            note = ""
        print(f"{n:>6}  {word:<18} {note}")
    if len(candidates) > args.top:
        print(f"... and {len(candidates) - args.top} more")
    print("\nproposals only; admit.py decides, one word and one definition at a time")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
