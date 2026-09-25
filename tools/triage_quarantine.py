#!/usr/bin/env python3
"""Report what the teacher could not say, and why it matters.

Every line in the quarantine is a sentence the teacher wanted to write and
could not. **Each offending word is either a gap in the lexicon or a word
genuinely above the level**, and only a reader can tell those apart. This
prints the evidence for that decision, ranked, and decides nothing.

    PYTHONPATH=src python3 tools/triage_quarantine.py <vocab> <quarantine>...
"""

from __future__ import annotations

import collections
import json
import sys
from pathlib import Path

from epagoge.vocabulary import load_vocabulary


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        print(f"usage: {argv[0]} <vocabulary> <quarantine.jsonl>...", file=sys.stderr)
        return 2

    vocabulary = load_vocabulary(Path(argv[1]))
    known = {t.word: t for t in vocabulary.terms}
    counts: collections.Counter[str] = collections.Counter()
    lines = 0
    reasons: collections.Counter[str] = collections.Counter()
    for path in argv[2:]:
        for raw in Path(path).read_text(encoding="utf-8").splitlines():
            if not raw.strip():
                continue
            entry = json.loads(raw)
            lines += 1
            reasons[entry.get("reason", "?")] += 1
            counts.update(entry.get("offending", []))

    print(f"quarantined lines   {lines}")
    for reason, count in reasons.most_common():
        print(f"    {count:>4}  {reason}")
    print(f"distinct words      {len(counts)}")
    print()
    print("  count  word            already licensed at")
    for word, count in counts.most_common(40):
        term = known.get(word)
        where = (
            f"level {term.level} as {term.concept}" if term else "not in the lexicon"
        )
        print(f"  {count:>5}  {word:<15} {where}")
    print()
    print("A word high on this list and absent from the lexicon is a candidate")
    print("for addition. A word already licensed at a higher level is working")
    print("as intended and the sentence using it needs rewording.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
