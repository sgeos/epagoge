#!/usr/bin/env python3
"""Write question-and-answer picture books, one exchange a spread.

**A corpus that only ever states produces a model that only ever
continues.** Measured 2026-09-25: one question mark in 4,419 level-one
records, no question with an answer after it, and a model that met
"what is the cup ?" by carrying on rather than answering. A model
reproduces the forms it was shown.

Operator direction: the question-and-answer picture book is a real form
and a rich one for reinforcing a concept, because the question names the
thing and the answer says it again in other words.

These are separate books rather than a change to existing ones, so the
narrative books stay narrative and a curator can choose. They take a
`.qN` suffix, the same mechanism the variant books use.

    PYTHONPATH=src:generators python3 generators/generate_question_books.py --limit 3
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import cast

from epagoge import prompt as prompts
from epagoge import schedule as sched
from epagoge.book import SPREADS, Book, book_head, parse_book, render_book
from epagoge.vocabulary import Vocabulary, load_vocabulary, unlicensed
from generate import ask, well_formed
from generate_books import Tally, admissible_words, words_for

ROOT = Path(__file__).resolve().parent.parent

SUBJECT_RE = re.compile(r"^SUBJECT:\s*(.+)$")
WORD_RE = re.compile(r"^WORD\s+([a-z']+)\s*:\s*(.+)$")
ASK_RE = re.compile(r"^ASK:\s*(.+?)\s*\|\s*(.+)$")


def usable_pair(
    question: str, answer: str, vocabulary: Vocabulary, level: int, tally: Tally
) -> bool:
    """Both halves admissible, and the question actually a question.

    **The question mark is the point of the form.** A pair whose question
    does not ask is a pair of statements, which the corpus already has
    four thousand of.
    """
    if not question.rstrip().endswith("?"):
        tally.reject("question does not ask")
        return False
    if not well_formed(answer):
        tally.reject("answer is not a sentence")
        return False
    if len(question.split()) < 3:
        tally.reject("question too short")
        return False
    for half in (question, answer):
        offending = sorted(set(unlicensed(vocabulary, half, level)))
        if offending:
            tally.reject(f"outside the ceiling: {' '.join(offending[:4])}")
            return False
    return True


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--level", type=int, default=1)
    parser.add_argument("--limit", type=int, default=3)
    parser.add_argument("--attempts", type=int, default=3)
    parser.add_argument("--timeout", type=int, default=300)
    # **Finishing beats starting.** Without this a run spends its limit on
    # new books and leaves the short ones short, so the corpus grows in
    # books that no gate will accept.
    parser.add_argument(
        "--fill-only",
        action="store_true",
        help="only top up question books that exist and are short",
    )
    args = parser.parse_args(argv[1:])

    plan = sched.load(ROOT / f"curriculum/schedule/level_{args.level:02d}.json")
    vocabulary = load_vocabulary(ROOT / "curriculum/vocabulary.json")
    admissible = admissible_words(vocabulary, args.level)
    out = ROOT / f"curriculum/books/level_{args.level}"
    already = {p.stem for p in out.glob("bk.*.md")}

    tally = Tally()
    written = 0
    for domain in plan.domains:
        for unit in domain.units:
            if written >= args.limit:
                break
            book_id = f"bk.{unit.id}.q1"
            path = out / f"{book_id}.md"
            existing: list[dict[str, object]] = []
            held: Book | None = None
            if path.is_file():
                # **Top up rather than rewrite.** The exchanges already
                # there are admissible and were judged usable, and
                # regenerating would throw them away to produce more of
                # the same at the same cost.
                held, records_held = parse_book(
                    path.read_text(encoding="utf-8"), path.name
                )
                if len(held.records) >= SPREADS:
                    continue
                existing = [cast("dict[str, object]", r) for r in records_held]
            elif book_id in already or args.fill_only:
                continue
            if not unit.teaches:
                continue
            defined = words_for(vocabulary, unit.teaches, args.level)
            if not defined:
                continue
            wanted = (
                SPREADS - len(existing)
                if existing
                else max(1, SPREADS - 1 - len(defined))
            )
            print(f"  {unit.id}: {wanted} exchange(s)", file=sys.stderr)

            subject = ""
            got_words: dict[str, str] = {}
            pairs: list[tuple[str, str]] = []
            for _attempt in range(args.attempts):
                raw = ask(
                    prompts.question_book(
                        unit.id,
                        unit.form,
                        defined,
                        args.level,
                        admissible,
                        wanted,
                    ),
                    timeout=args.timeout,
                )
                for line in raw.splitlines():
                    line = line.strip()
                    if (m := SUBJECT_RE.match(line)) and not subject:
                        candidate = m.group(1).strip()
                        if well_formed(candidate) and not unlicensed(
                            vocabulary, candidate, args.level
                        ):
                            subject = candidate
                    elif m := WORD_RE.match(line):
                        word, said = m.group(1), m.group(2).strip()
                        if (
                            word in defined
                            and word not in got_words
                            and well_formed(said)
                            and not unlicensed(vocabulary, said, args.level)
                        ):
                            got_words[word] = said
                    elif m := ASK_RE.match(line):
                        question, answer = m.group(1).strip(), m.group(2).strip()
                        if (question, answer) in pairs:
                            continue
                        if usable_pair(question, answer, vocabulary, args.level, tally):
                            pairs.append((question, answer))
                if subject and len(pairs) >= wanted:
                    break

            if existing and held is not None:
                seen = {str(e["content"]) for e in existing}
                fresh = [(q, a) for q, a in pairs if f"{q} {a}" not in seen][:wanted]
                if not fresh:
                    print("    nothing new", file=sys.stderr)
                    continue
                start = len(existing)
                for n, (question, answer) in enumerate(fresh, start=start):
                    existing.append(
                        {
                            "id": f"{unit.id}.q1.a{n:02d}",
                            "level": args.level,
                            "concepts": list(unit.teaches),
                            "claim_class": "empirical",
                            "content": f"{question} {answer}",
                            "provenance": {"source_claim": f"topic:{unit.id}"},
                        }
                    )
                path.write_text(
                    render_book(book_head(held), existing), encoding="utf-8"
                )
                written += 1
                print(
                    f"    added {len(fresh)}, now {len(existing)} spreads",
                    file=sys.stderr,
                )
                continue

            if not subject:
                print("    no subject definition survived", file=sys.stderr)
                continue
            pairs = pairs[:wanted]
            if not pairs:
                print("    no usable exchange", file=sys.stderr)
                continue

            records: list[dict[str, object]] = [
                {
                    "id": f"{unit.id}.q1.d00",
                    "level": args.level,
                    "concepts": list(unit.teaches),
                    "claim_class": "formal",
                    "content": subject,
                    "provenance": {"source_claim": f"topic:{unit.id}"},
                    "defines": {"kind": "topic", "target": unit.id},
                }
            ]
            for n, (word, said) in enumerate(sorted(got_words.items()), start=1):
                records.append(
                    {
                        "id": f"{unit.id}.q1.d{n:02d}",
                        "level": args.level,
                        "concepts": [defined[word]],
                        "claim_class": "formal",
                        "content": said,
                        "provenance": {"source_claim": f"lexicon:{word}"},
                        "defines": {"kind": "word", "target": word},
                    }
                )
            for n, (question, answer) in enumerate(pairs, start=1):
                records.append(
                    {
                        "id": f"{unit.id}.q1.a{n:02d}",
                        "level": args.level,
                        "concepts": list(unit.teaches),
                        "claim_class": "empirical",
                        # One spread, one exchange: the question and the
                        # answer it turns to.
                        "content": f"{question} {answer}",
                        "provenance": {"source_claim": f"topic:{unit.id}"},
                    }
                )
            head = {
                "id": book_id,
                "level": args.level,
                "title": unit.form.split(".")[0],
                "subject": {"kind": "topic", "target": unit.id},
                "form": "question",
            }
            path.write_text(render_book(head, records), encoding="utf-8")
            already.add(book_id)
            written += 1
            print(
                f"    wrote {len(records)} spreads, {len(pairs)} exchanges",
                file=sys.stderr,
            )
        if written >= args.limit:
            break

    print(f"{written} question book(s), {tally.rejected} line(s) rejected")
    for reason, count in sorted(tally.reasons.items(), key=lambda kv: -kv[1])[:8]:
        print(f"  {count:4}  {reason}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
