#!/usr/bin/env python3
"""Propose lexicon candidates from sources, counting each source separately.

**Frequency is per source, not pooled.** A word common in one book and
absent from the rest is a word that book needed, and pooling would bury it
under the long tail of everything else. Operator direction 2026-09-25: a
word frequent in any one source is a candidate, and the per-source long
tail is inspected rather than discarded.

So every candidate is reported with the sources it was frequent in and the
sources where it trailed, and the two groups are separated because they
get different treatment. The frequent group is bulk work. The long tail is
where judgement is, and it is where a source's idiosyncrasies live.

**This proposes and does not decide.** The thesis is that uncurated input
produces undesirable properties, and a frequency list is uncurated by
construction. `admit.py` decides, one word and one definition at a time.

**Archaism is not visible here and will not be.** A public-domain source
is public domain because it is old, so a word can be frequent, plainly
useful in 1880 and wrong for a child now. That is caught at drafting, not
by a counter.

    PYTHONPATH=src python3 tools/scan_lexicon.py --level 2 \
        --seed lists/dale_chall.txt --frequent 5 sources/*.txt
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

from epagoge.inflection import plural, verb_forms
from epagoge.vocabulary import load_vocabulary, tokenise

ROOT = Path(__file__).resolve().parent.parent


def read_seed(paths: list[Path]) -> set[str]:
    """Word lists that are candidates regardless of any source's frequency.

    Dale-Chall, the New General Service List and Ogden's Basic English are
    the operator's starting point. **None is committed to this
    repository**, because two of the three have a licence that a CC0
    repository cannot carry, so they are supplied as files at scan time.
    What the repository keeps is this project's own definitions of whatever
    words survive judgement.
    """
    out: set[str] = set()
    for path in paths:
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            word = line.strip().lower()
            if word and word.isalpha():
                out.add(word)
    return out


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="*", type=Path, help="sources to scan")
    parser.add_argument("--level", type=int, default=2)
    parser.add_argument(
        "--seed",
        action="append",
        type=Path,
        default=[],
        help="a word list whose words are candidates without a frequency test",
    )
    parser.add_argument(
        "--frequent",
        type=int,
        default=5,
        help="occurrences within one source that make a word frequent there",
    )
    parser.add_argument("--top", type=int, default=40)
    parser.add_argument("--out", type=Path, default=None, help="write JSON here")
    args = parser.parse_args(argv[1:])

    vocabulary = load_vocabulary(ROOT / "curriculum/vocabulary.json")
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
    anywhere = {
        form: min(
            (t.level for t in vocabulary.terms if form in t.surface_forms()),
            default=0,
        )
        for t in vocabulary.terms
        for form in t.surface_forms()
    }
    derived: dict[str, str] = {}
    for term in vocabulary.terms:
        for form in (plural(term.word), *verb_forms(term.word)):
            derived.setdefault(form, term.word)

    per_source: dict[str, Counter[str]] = {}
    for path in args.files:
        if not path.is_file():
            print(f"no such file: {path}", file=sys.stderr)
            return 2
        text = path.read_text(encoding="utf-8", errors="replace")
        per_source[path.name] = Counter(
            w for w in tokenise(text) if w.isalpha() and w not in here
        )

    seeded = {w for w in read_seed(args.seed) if w not in here}

    frequent_in: dict[str, list[str]] = {}
    trailing_in: dict[str, list[str]] = {}
    for name, counts in per_source.items():
        for word, n in counts.items():
            target = frequent_in if n >= args.frequent else trailing_in
            target.setdefault(word, []).append(name)

    frequent = sorted(frequent_in)
    tail = sorted(w for w in trailing_in if w not in frequent_in)
    seed_only = sorted(
        w for w in seeded if w not in frequent_in and w not in trailing_in
    )

    def note(word: str) -> str:
        if word in anywhere:
            return f"admitted at level {anywhere[word]}"
        if word in derived:
            return f"a form of {derived[word]!r}"
        return ""

    print(f"sources {len(per_source)}, seed lists {len(args.seed)}")
    print(f"frequent in at least one source  {len(frequent)}")
    print(f"long tail in every source        {len(tail)}")
    print(f"from a seed list only            {len(seed_only)}")
    print()
    print("FREQUENT SOMEWHERE, take in bulk")
    for word in frequent[: args.top]:
        where = " ".join(sorted(frequent_in[word]))
        print(f"  {word:<18} {note(word):<26} {where}")
    if len(frequent) > args.top:
        print(f"  ... and {len(frequent) - args.top} more")
    print()
    print("LONG TAIL EVERYWHERE, inspect per source")
    for word in tail[: args.top]:
        where = " ".join(sorted(trailing_in[word]))
        print(f"  {word:<18} {note(word):<26} {where}")
    if len(tail) > args.top:
        print(f"  ... and {len(tail) - args.top} more")

    if args.out is not None:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(
            json.dumps(
                {
                    "level": args.level,
                    "frequent_at": args.frequent,
                    "sources": sorted(per_source),
                    "frequent": {w: sorted(frequent_in[w]) for w in frequent},
                    "long_tail": {w: sorted(trailing_in[w]) for w in tail},
                    "seed_only": seed_only,
                    "note": (
                        "Proposals. Every word still needs a definition that "
                        "reduces to the seed, and archaism is not visible to a "
                        "counter."
                    ),
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        print(f"\nwrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
