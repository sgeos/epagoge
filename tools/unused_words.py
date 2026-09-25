#!/usr/bin/env python3
"""Every surface form admitted at a level must appear in that level's corpus.

**Operator invariant 2026-09-25.** A word in the lexicon that the corpus
never uses is one of three things and the lexicon cannot tell which:

1. **A module is missing it** and should use it.
2. **A module is missing entirely** and should be drafted around it.
3. **Admitting it was a mistake** and it should be culled.

Each is a judgement and none is automatic, so this reports and never
gates.

**The test is on surface forms, not headwords.** Admitting a verb admits
every inflection and a noun its plural, and a corpus that uses `run` and
never `ran` has not used what the lexicon claims. The existing
`utilisation` in `epagoge.vocabulary` counts headwords reached through
suffix stripping, which answers a softer question.

**Archaism is not a reason to cull.** A historical account needs the words
of its period to tell it accurately, so an archaic word may be exactly
right somewhere. What archaism implies is that the word is not needed
*now*, which is a question about which level it belongs at, and that
placement may be arbitrary. The judgement is where it goes, not whether it
goes.

    PYTHONPATH=src python3 tools/unused_words.py --level 1
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import cast

from epagoge.book import load_book_dir
from epagoge.vocabulary import load_vocabulary, tokenise

ROOT = Path(__file__).resolve().parent.parent


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--level", type=int, default=1)
    parser.add_argument("--top", type=int, default=40)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args(argv[1:])

    vocabulary = load_vocabulary(ROOT / "curriculum/vocabulary.json")
    book_dir = ROOT / f"curriculum/books/level_{args.level}"
    if not book_dir.is_dir():
        print(f"no books at {book_dir}", file=sys.stderr)
        return 2
    _books, records = load_book_dir(book_dir)
    seen: Counter[str] = Counter()
    for record in records:
        entry = cast("dict[str, object]", record)
        seen.update(tokenise(str(entry["content"])))

    # Every form of every term admissible here, with the headword it
    # belongs to, so an unused inflection is reported against its base.
    owed: dict[str, str] = {}
    for term in vocabulary.terms:
        if term.level > args.level:
            continue
        for form in term.surface_forms():
            owed.setdefault(form, term.word)

    unused = sorted(form for form in owed if form not in seen)
    bases = {owed[form] for form in unused}
    whole = sorted(
        base
        for base in bases
        if all(form in unused for form, head in owed.items() if head == base)
    )

    print(f"level {args.level}")
    print(f"  surface forms admitted   {len(owed)}")
    print(f"  used in the corpus       {len(owed) - len(unused)}")
    print(f"  never used               {len(unused)}")
    print(f"  headwords never used at all {len(whole)}")
    print()
    print("NEVER USED, with the word they belong to")
    for form in unused[: args.top]:
        base = owed[form]
        mark = "  whole word unused" if base in whole else ""
        print(f"  {form:<20} {base:<20}{mark}")
    if len(unused) > args.top:
        print(f"  ... and {len(unused) - args.top} more")

    if args.out is not None:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(
            json.dumps(
                {
                    "level": args.level,
                    "forms_admitted": len(owed),
                    "forms_unused": len(unused),
                    "headwords_wholly_unused": whole,
                    "unused": {form: owed[form] for form in unused},
                    "note": (
                        "Each unused word means a module should use it, a "
                        "module should be drafted for it, or admitting it was "
                        "a mistake. A judgement each, and archaism is not by "
                        "itself a reason to cull."
                    ),
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        print(f"\nwrote {args.out}")
    print("\nreported, never gated; every one of these is a judgement")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
