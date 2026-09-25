#!/usr/bin/env python3
"""Generate whole books from the schedule, through the local teacher.

One completion per book. Sentence-at-a-time prompting produced true,
admissible, lifeless records, because nothing connected one sentence to the
next and the teacher had no reason to vary them.

    PYTHONPATH=src python3 generators/generate_books.py --limit 2 --out tmp/
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

from generate import ask, well_formed
from epagoge import prompt as prompts
from epagoge import schedule as sched
from epagoge.vocabulary import Vocabulary, load_vocabulary, unlicensed

ROOT = Path(__file__).resolve().parent.parent
MAX_DEFINED = 8
"""Words defined per book. More than this and the definitions crowd out the
story, which is the part the book shape exists to produce."""

SUBJECT_RE = re.compile(r"^SUBJECT:\s*(.+)$")
WORD_RE = re.compile(r"^WORD\s+([a-z']+)\s*:\s*(.+)$")
STORY_RE = re.compile(r"^STORY:\s*(.+)$")


@dataclass
class Tally:
    subjects: int = 0
    words: int = 0
    story: int = 0
    rejected: int = 0
    reasons: dict[str, int] = field(default_factory=dict[str, int])

    def reject(self, why: str) -> None:
        self.rejected += 1
        self.reasons[why] = self.reasons.get(why, 0) + 1


def admissible_words(vocabulary: Vocabulary, level: int) -> list[str]:
    return sorted(
        {*vocabulary.core, *vocabulary.exempt}
        | {t.word for t in vocabulary.terms if t.level <= level}
    )


def words_for(
    vocabulary: Vocabulary, concepts: tuple[str, ...], level: int
) -> dict[str, str]:
    """Pick words to define, spread across the unit's concepts.

    Round-robin rather than all of one concept's words, so a book defines a
    little of each thing it teaches instead of everything about one.
    """
    pools = {
        concept: sorted(
            t.word
            for t in vocabulary.terms
            if t.concept == concept and t.level <= level
        )
        for concept in concepts
    }
    out: dict[str, str] = {}
    index = 0
    while len(out) < MAX_DEFINED and any(len(p) > index for p in pools.values()):
        for concept, pool in pools.items():
            if index < len(pool) and len(out) < MAX_DEFINED:
                out[pool[index]] = concept
        index += 1
    return out


def parse(raw: str) -> tuple[str | None, dict[str, str], list[str]]:
    subject: str | None = None
    words: dict[str, str] = {}
    story: list[str] = []
    for line in raw.splitlines():
        line = line.strip()
        if (m := SUBJECT_RE.match(line)) and subject is None:
            subject = m.group(1).strip()
        elif m := WORD_RE.match(line):
            words[m.group(1)] = m.group(2).strip()
        elif m := STORY_RE.match(line):
            story.append(m.group(1).strip())
    return subject, words, story


def keep(text: str, vocabulary: Vocabulary, level: int, tally: Tally) -> bool:
    if not well_formed(text):
        tally.reject("not a sentence")
        return False
    if offending := unlicensed(vocabulary, text, level):
        tally.reject(f"outside the ceiling: {' '.join(sorted(set(offending))[:4])}")
        return False
    return True


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--level", type=int, default=1)
    parser.add_argument("--limit", type=int, default=2, help="books to write")
    parser.add_argument("--sentences", type=int, default=10)
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--attempts", type=int, default=2)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv[1:])

    plan = sched.load(ROOT / f"curriculum/schedule/level_{args.level:02d}.json")
    vocabulary = load_vocabulary(ROOT / "curriculum/vocabulary.json")
    admissible = admissible_words(vocabulary, args.level)
    tally = Tally()

    args.out.mkdir(parents=True, exist_ok=True)
    books: list[dict[str, object]] = []
    records: list[dict[str, object]] = []

    written = 0
    for domain in plan.domains:
        for unit in domain.units:
            if written >= args.limit:
                break
            if not unit.teaches:
                continue
            defined = words_for(vocabulary, unit.teaches, args.level)
            if not defined:
                continue
            text = prompts.book(
                unit.id, unit.form, defined, args.level, admissible, args.sentences
            )
            print(f"  {unit.id}", file=sys.stderr)
            # Accumulate across attempts rather than replacing. The first
            # version of this took the later answer wholesale, so a worse
            # second attempt discarded a good first one and a book that had
            # seven usable records came back with two.
            subject: str | None = None
            got_words: dict[str, str] = {}
            story: list[str] = []
            prompt_text = text
            for attempt in range(args.attempts):
                got_subject, words_now, story_now = parse(
                    ask(prompt_text, timeout=args.timeout)
                )
                if (
                    subject is None
                    and got_subject
                    and keep(got_subject, vocabulary, args.level, tally)
                ):
                    subject = got_subject
                for word, said in words_now.items():
                    if (
                        word in defined
                        and word not in got_words
                        and keep(said, vocabulary, args.level, tally)
                    ):
                        got_words[word] = said
                # Definitions accumulate across attempts because each one
                # stands alone. **A story does not.** Merging two attempts
                # stitched two different stories together, so the boy found
                # a book and then, without transition, looked forward to a
                # game. The longest single attempt is kept instead.
                usable = [
                    said
                    for said in story_now
                    if keep(said, vocabulary, args.level, tally)
                ]
                if len(usable) > len(story):
                    story = usable
                missing = sorted(set(defined) - set(got_words))
                if not missing and subject and len(story) >= args.sentences:
                    break
                if attempt + 1 >= args.attempts:
                    break
                notes = ["Your last answer was only partly used."]
                if missing:
                    notes.append(f"WORD lines still needed: {' '.join(missing)}")
                if len(story) < args.sentences:
                    notes.append(
                        f"STORY lines still needed: {args.sentences - len(story)}"
                    )
                notes.append("Every line must end with a full stop.")
                notes.append("Use only the allowed words.")
                prompt_text = "\n".join(notes) + "\n\n" + text

            ids: list[str] = []
            if subject and keep(subject, vocabulary, args.level, tally):
                rid = f"{unit.id}.d00"
                records.append(
                    {
                        "id": rid,
                        "level": args.level,
                        "concepts": list(unit.teaches),
                        "claim_class": "formal",
                        "content": subject,
                        "provenance": {"source_claim": f"topic:{unit.id}"},
                        "defines": {"kind": "topic", "target": unit.id},
                    }
                )
                ids.append(rid)
                tally.subjects += 1
            for n, (word, text_) in enumerate(sorted(got_words.items()), start=1):
                if word not in defined or not keep(
                    text_, vocabulary, args.level, tally
                ):
                    continue
                rid = f"{unit.id}.d{n:02d}"
                records.append(
                    {
                        "id": rid,
                        "level": args.level,
                        "concepts": [defined[word]],
                        "claim_class": "formal",
                        "content": text_,
                        "provenance": {"source_claim": f"lexicon:{word}"},
                        "defines": {"kind": "word", "target": word},
                    }
                )
                ids.append(rid)
                tally.words += 1
            ground = unit.primitives[0] if unit.primitives else None
            for n, text_ in enumerate(story, start=1):
                if not keep(text_, vocabulary, args.level, tally):
                    continue
                rid = f"{unit.id}.s{n:02d}"
                records.append(
                    {
                        "id": rid,
                        "level": args.level,
                        "concepts": list(unit.teaches),
                        "claim_class": "empirical",
                        "content": text_,
                        "provenance": {
                            "source_claim": f"primitive:{ground}"
                            if ground
                            else f"topic:{unit.id}"
                        },
                    }
                )
                ids.append(rid)
                tally.story += 1
            if ids:
                books.append(
                    {
                        "id": f"bk.{unit.id}",
                        "level": args.level,
                        "title": unit.form.split(".")[0],
                        "subject": {"kind": "topic", "target": unit.id},
                        "records": ids,
                    }
                )
                written += 1
        if written >= args.limit:
            break

    (args.out / "books.json").write_text(
        json.dumps(books, indent=2) + "\n", encoding="utf-8"
    )
    with (args.out / "books.jsonl").open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record) + "\n")
    print(
        f"{written} books, {tally.subjects} subjects, {tally.words} words,"
        f" {tally.story} story lines, {tally.rejected} rejected",
        file=sys.stderr,
    )
    for why, count in sorted(tally.reasons.items(), key=lambda kv: -kv[1])[:6]:
        print(f"    {count:>3}  {why}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
