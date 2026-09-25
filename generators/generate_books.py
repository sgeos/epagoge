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
from typing import cast

from generate import ask, well_formed
from epagoge import prompt as prompts
from epagoge import schedule as sched
from epagoge.book import render_book
from epagoge.vocabulary import Vocabulary, load_vocabulary, unlicensed

ROOT = Path(__file__).resolve().parent.parent
MAX_DEFINED = 8
"""Words defined per book. More than this and the definitions crowd out the
story, which is the part the book shape exists to produce."""

SUBJECT_RE = re.compile(r"^SUBJECT:\s*(.+)$")
WORD_RE = re.compile(r"^WORD\s+([a-z']+)\s*:\s*(.+)$")
STORY_RE = re.compile(r"^STORY:\s*(.+)$")


@dataclass
class Reject:
    """A line the teacher wrote that could not be used as written.

    Kept rather than dropped. Either the words belong in the lexicon or the
    sentence needs different words, and neither question can be answered by
    a counter.
    """

    book: str
    slot: str
    text: str
    offending: tuple[str, ...]
    reason: str
    concepts: tuple[str, ...] = ()


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


def judge(text: str, vocabulary: Vocabulary, level: int) -> tuple[str, tuple[str, ...]]:
    """Empty reason means usable. Otherwise the reason and the words at fault."""
    if not well_formed(text):
        return "not a sentence", ()
    offending = unlicensed(vocabulary, text, level)
    if offending:
        return "outside the ceiling", tuple(sorted(set(offending)))
    return "", ()


def keep(
    text: str,
    vocabulary: Vocabulary,
    level: int,
    tally: Tally,
    *,
    book: str = "",
    slot: str = "",
    quarantine: list[Reject] | None = None,
    concepts: tuple[str, ...] = (),
) -> bool:
    reason, offending = judge(text, vocabulary, level)
    if not reason:
        return True
    tally.reject(reason if not offending else f"{reason}: {' '.join(offending[:4])}")
    if quarantine is not None:
        quarantine.append(Reject(book, slot, text, offending, reason, concepts))
    return False


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--level", type=int, default=1)
    parser.add_argument("--limit", type=int, default=2, help="books to write")
    parser.add_argument("--sentences", type=int, default=10)
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument("--attempts", type=int, default=2)
    parser.add_argument("--out", type=Path, default=ROOT / "curriculum/books/level_1")
    parser.add_argument(
        "--quarantine", type=Path, default=ROOT / "tmp/quarantine.jsonl"
    )
    args = parser.parse_args(argv[1:])

    plan = sched.load(ROOT / f"curriculum/schedule/level_{args.level:02d}.json")
    vocabulary = load_vocabulary(ROOT / "curriculum/vocabulary.json")
    admissible = admissible_words(vocabulary, args.level)
    tally = Tally()

    args.out.mkdir(parents=True, exist_ok=True)
    books: list[dict[str, object]] = []
    records: list[dict[str, object]] = []

    quarantine: list[Reject] = []
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
                    and keep(
                        got_subject,
                        vocabulary,
                        args.level,
                        tally,
                        book=unit.id,
                        slot="subject",
                        quarantine=quarantine,
                        concepts=unit.teaches,
                    )
                ):
                    subject = got_subject
                for word, said in words_now.items():
                    if (
                        word in defined
                        and word not in got_words
                        and keep(
                            said,
                            vocabulary,
                            args.level,
                            tally,
                            book=unit.id,
                            slot=f"word:{word}",
                            quarantine=quarantine,
                            concepts=(defined[word],),
                        )
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
                    if keep(
                        said,
                        vocabulary,
                        args.level,
                        tally,
                        book=unit.id,
                        slot="story",
                        quarantine=quarantine,
                        concepts=unit.teaches,
                    )
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

    # A rejected line is reworked rather than dropped. What survives the
    # rework enters the book. What does not is written out for triage,
    # because the words in it are either lexicon gaps or genuinely above the
    # level, and a counter cannot tell those apart.
    reworked = 0
    still_bad: list[Reject] = []
    by_id = {r["id"]: r for r in records}
    for reject in quarantine:
        # The subject was excluded from rework, which was exactly backwards.
        # It is the one line a book cannot be valid without.
        if not reject.offending:
            still_bad.append(reject)
            continue
        candidate = ask(
            prompts.reword(reject.text, reject.offending, admissible),
            timeout=args.timeout,
        ).splitlines()
        fixed = next((line.strip() for line in candidate if line.strip()), "")
        if fixed and not judge(fixed, vocabulary, args.level)[0] and reject.concepts:
            slot = reject.slot
            suffix = "s" if slot == "story" else "d"
            rid = f"{reject.book}.{suffix}{len(by_id) + 1:02d}"
            record: dict[str, object] = {
                "id": rid,
                "level": args.level,
                "concepts": list(reject.concepts),
                "claim_class": "empirical" if slot == "story" else "formal",
                "content": fixed,
                "provenance": {"source_claim": f"topic:{reject.book}"},
            }
            if slot == "subject":
                record["defines"] = {"kind": "topic", "target": reject.book}
            elif slot.startswith("word:"):
                word = slot.split(":", 1)[1]
                record["defines"] = {"kind": "word", "target": word}
                record["provenance"] = {"source_claim": f"lexicon:{word}"}
            by_id[rid] = record
            # It was created and then dropped, because nothing added it to
            # the book it came from. A record outside every book is not in
            # the corpus.
            for entry in books:
                if entry["id"] == f"bk.{reject.book}":
                    ids_now = cast(list[str], entry["records"])
                    # A definition must precede the material that uses it,
                    # and a subject must come first of all.
                    if slot == "subject":
                        ids_now.insert(0, rid)
                    elif slot.startswith("word:"):
                        first_story = next(
                            (
                                i
                                for i, x in enumerate(ids_now)
                                if "defines" not in by_id.get(x, {})
                            ),
                            len(ids_now),
                        )
                        ids_now.insert(first_story, rid)
                    else:
                        ids_now.append(rid)
                    break
            reworked += 1
        else:
            still_bad.append(reject)

    args.out.mkdir(parents=True, exist_ok=True)
    withheld = 0
    for entry in books:
        ids = cast(list[str], entry["records"])
        subject_target = cast(dict[str, object], entry["subject"])["target"]
        has_subject = any(
            cast(dict[str, object], by_id[i].get("defines", {})).get("target")
            == subject_target
            for i in ids
            if i in by_id
        )
        if not has_subject:
            withheld += 1
            still_bad.append(
                Reject(
                    book=str(entry["id"]),
                    slot="book",
                    text=f"{len(ids)} records, no subject definition survived",
                    offending=(),
                    reason="book withheld",
                )
            )
            continue
        head = {
            "id": entry["id"],
            "level": entry["level"],
            "title": entry["title"],
            "subject": entry["subject"],
        }
        path = args.out / f"{entry['id']}.md"
        path.write_text(
            render_book(head, [by_id[i] for i in ids if i in by_id]), encoding="utf-8"
        )

    args.quarantine.parent.mkdir(parents=True, exist_ok=True)
    with args.quarantine.open("w", encoding="utf-8") as handle:
        for reject in still_bad:
            handle.write(
                json.dumps(
                    {
                        "book": reject.book,
                        "slot": reject.slot,
                        "reason": reject.reason,
                        "offending": list(reject.offending),
                        "text": reject.text,
                    }
                )
                + "\n"
            )

    print(
        f"{written} books, {tally.subjects} subjects, {tally.words} words,"
        f" {tally.story} story lines, {reworked} reworked,"
        f" {withheld} withheld, {len(still_bad)} quarantined",
        file=sys.stderr,
    )
    for why, count in sorted(tally.reasons.items(), key=lambda kv: -kv[1])[:6]:
        print(f"    {count:>3}  {why}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
