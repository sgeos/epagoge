#!/usr/bin/env python3
"""Generate level-two textbook modules, one spread at a time.

**A module is seventy picture books of text.** A level-one book runs to
about two hundred and twenty words and a level-two module to about sixteen
thousand, over sixty-four spreads of roughly two hundred and fifty words
each. Asking for one in a single completion is not available: the teacher
timed out at twenty-eight level-one sentences.

So a module is built a spread at a time, and each prompt carries the
previous spread, because the failure that sentence-at-a-time prompting
produced at level one was disconnection. A passage that does not follow
from the one before it is the same failure at a larger size.

**A module may revisit rather than teach.** Seven of the eleven domains
have no concept left for level two, because level one teaches every one
they hold, so their modules revisit what the picture books introduced.
Working only from `teaches` would have skipped them all.

    PYTHONPATH=src:generators python3 generators/generate_modules.py --limit 1
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from epagoge import prompt as prompts
from epagoge import schedule as sched
from epagoge.book import SPREADS_BY_LEVEL, WORDS_PER_SPREAD, render_book
from epagoge.vocabulary import Vocabulary, load_vocabulary, unlicensed
from generate import ask, split_lines, well_formed
from generate_books import Reject, Tally, admissible_words, words_for

ROOT = Path(__file__).resolve().parent.parent

MIN_SPREAD_WORDS = 60
"""Shortest passage accepted as a spread.

A spread is asked for at about two hundred and fifty words. Far below that
is the teacher answering with a sentence, which is a level-one reflex and
not a spread, and keeping it would leave the module short of its word
count while appearing to have the right number of spreads.
"""

DEFAULT_ROUNDS = 4
"""Times a spread is asked for before it is given up on, as ``--attempts``.

**A spread is accepted a sentence at a time, not whole.** The first
version of this judged the whole passage and threw all of it away on one
bad word. At the level-one acceptance of about half per sentence, a
fifteen-sentence passage survives that test three times in a hundred
thousand, which is why nothing was written in twenty-five minutes.

Sentence-level acceptance makes progress monotone: every round adds what
passed and asks again for the rest.
"""


def headings(unit: sched.Unit, count: int) -> list[str]:
    """One heading per spread, cycling the concepts the module covers.

    The heading is what the spread is about. Cycling rather than splitting
    the module into blocks keeps a concept coming back, which is the thing
    a module does that a picture book cannot.
    """
    covered = [*unit.teaches, *unit.revisits] or [unit.id]
    return [covered[n % len(covered)].replace("_", " ") for n in range(count)]


def keep_sentences(
    raw: str,
    vocabulary: Vocabulary,
    level: int,
    tally: Tally,
    *,
    unit: str,
    quarantine: list[Reject],
) -> list[str]:
    """Every sentence of a passage that is shaped and admissible."""
    out: list[str] = []
    for line in split_lines(raw):
        for piece in re.split(r"(?<=[.!?])\s+", line):
            text = piece.strip()
            if not text or not well_formed(text):
                if text:
                    tally.reject("not a sentence")
                continue
            offending = tuple(sorted(set(unlicensed(vocabulary, text, level))))
            if offending:
                tally.reject(f"outside the ceiling: {' '.join(offending[:4])}")
                quarantine.append(
                    Reject(unit, "spread", text, offending, "outside the ceiling")
                )
                continue
            out.append(text)
    return out


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--level", type=int, default=2)
    parser.add_argument("--limit", type=int, default=1, help="modules to write")
    parser.add_argument("--spreads", type=int, default=None)
    parser.add_argument("--timeout", type=int, default=420)
    parser.add_argument("--attempts", type=int, default=DEFAULT_ROUNDS)
    parser.add_argument("--out", type=Path, default=None)
    args = parser.parse_args(argv[1:])

    out = args.out or ROOT / f"curriculum/books/level_{args.level}"
    out.mkdir(parents=True, exist_ok=True)
    plan = sched.load(ROOT / f"curriculum/schedule/level_{args.level:02d}.json")
    vocabulary = load_vocabulary(ROOT / "curriculum/vocabulary.json")
    admissible = admissible_words(vocabulary, args.level)
    want = args.spreads or SPREADS_BY_LEVEL.get(args.level, 64)
    per_spread = WORDS_PER_SPREAD.get(args.level, (250, 50))[0]

    already = {path.stem for path in out.glob("bk.*.md")}
    tally = Tally()
    quarantine: list[Reject] = []
    written = 0
    for domain in plan.domains:
        for unit in domain.units:
            if written >= args.limit:
                break
            if f"bk.{unit.id}" in already:
                continue
            covered = [*unit.teaches, *unit.revisits]
            if not covered:
                continue
            defined = words_for(vocabulary, tuple(covered), args.level)
            print(f"  {unit.id}: {want} spreads", file=sys.stderr)

            records: list[dict[str, object]] = []
            preceding = ""
            for index, heading in enumerate(headings(unit, want)):
                kept: list[str] = []
                for _round in range(args.attempts):
                    if sum(len(s.split()) for s in kept) >= per_spread:
                        break
                    question = prompts.module_spread(
                        unit.id,
                        unit.form,
                        heading,
                        " ".join(kept) or preceding,
                        args.level,
                        admissible,
                        per_spread - sum(len(s.split()) for s in kept),
                    )
                    for sentence in keep_sentences(
                        ask(question, timeout=args.timeout),
                        vocabulary,
                        args.level,
                        tally,
                        unit=unit.id,
                        quarantine=quarantine,
                    ):
                        if sentence not in kept:
                            kept.append(sentence)
                accepted = " ".join(kept)
                if len(accepted.split()) < MIN_SPREAD_WORDS:
                    tally.reject(f"spread too short: {len(accepted.split())} words")
                    continue
                records.append(
                    {
                        "id": f"{unit.id}.s{index:02d}",
                        "level": args.level,
                        "concepts": list(covered),
                        "claim_class": "empirical",
                        "content": accepted,
                        "provenance": {"source_claim": f"topic:{unit.id}"},
                    }
                )
                preceding = accepted
                print(
                    f"    spread {index + 1}/{want}, {len(accepted.split())} words",
                    file=sys.stderr,
                )

            if not records:
                print(f"    nothing usable for {unit.id}", file=sys.stderr)
                continue
            # The subject statement is the first spread, marked as the
            # definition of the topic, so a module says what it is about
            # before saying anything else, exactly as a book does.
            records[0]["claim_class"] = "formal"
            records[0]["defines"] = {"kind": "topic", "target": unit.id}
            head = {
                "id": f"bk.{unit.id}",
                "level": args.level,
                "title": unit.form.split(".")[0],
                "subject": {"kind": "topic", "target": unit.id},
            }
            (out / f"bk.{unit.id}.md").write_text(
                render_book(head, records), encoding="utf-8"
            )
            total = sum(len(str(r["content"]).split()) for r in records)
            print(
                f"    wrote {len(records)} spreads, {total} words, "
                f"{len(defined)} words available to define",
                file=sys.stderr,
            )
            written += 1
        if written >= args.limit:
            break

    print(f"{written} module(s), {tally.rejected} spread(s) rejected")
    for reason, count in sorted(tally.reasons.items(), key=lambda kv: -kv[1])[:8]:
        print(f"  {count:4}  {reason}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
