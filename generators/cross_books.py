"""Write books that pair a concept with one it has never appeared beside.

**Measured 2026-09-26: the corpus realises 109 concept pairs out of 7,626
possible, which is one and a half percent.** Every concept's partners are
exactly its own unit-mates, because a book is about a unit and a variant
repeats that unit. `giving_a_reason` has only ever appeared beside
`agreeing` and `disagreeing`, which are in the same unit.

**Eight hundred words is not many, but the combinations are vast**, and the
corpus was spending its repetition on the same combinations. The operator's
direction is that repetition should raise combinatorial richness instead:
the same concept met beside a different partner, and told with different
words.

**It also targets the concepts the model retains worst.**
`evals/pilot/LEVEL_ONE_POSITIONS_AND_RETENTION.md` measured
`giving_a_reason`, `disagreeing` and `agreeing` at loss 4.011 against 2.017
for `emptiness`, and the badly retained ones are the vocabulary of
falsification, which is what this project is for. So each pair grounds a
poorly retained abstract concept in a well retained concrete one.

**The book is a variant of the target's own unit**, so nothing about the
schema changes: the subject is a scheduled topic and a record in the book
defines it. What differs is that the story records carry the partner concept
too.

**Seeds only.** This writes short spreads and `fill_spreads.py` brings them
to the word band, which is the machinery that already works.

    PYTHONPATH=src:generators python3 generators/cross_books.py --spec pairs.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import cast

from epagoge import prompt as prompts
from epagoge import schedule as sched
from epagoge.book import Book, DefinitionKind, book_head, load_book_dir, render_book
from epagoge.vocabulary import Vocabulary, load_vocabulary, unlicensed
from generate import TIMEOUTS, ask
from generate_books import admissible_words

ROOT = Path(__file__).resolve().parent.parent
SPREADS = 16


def readable(concept: str) -> str:
    return concept.replace("_", " ")


def words_for(vocabulary: Vocabulary, concept: str, level: int) -> list[str]:
    """The admissible words that teach a concept.

    **A concept name is not a word and putting one in a prompt costs a
    book.** Measured 2026-09-26: a subject form that said "told through
    emptiness" produced three subject lines containing `emptiness`, which is
    a concept id and not in the lexicon, so every one was rejected and the
    book could not be written despite twenty-three usable story spreads.

    The teacher is given the words instead. It can only write with words, so
    that is what it should be told about.
    """
    return sorted(
        {t.word for t in vocabulary.terms if t.concept == concept and t.level <= level}
    )


def accepted(lines: list[str], vocabulary: Vocabulary, level: int) -> list[str]:
    """Sentences wholly inside the level, one at a time.

    **Never judge a whole reply.** At about half acceptance per sentence a
    fifteen-line passage survives three times in a hundred thousand, which
    is the arithmetic that cost this project a generation round.
    """
    out: list[str] = []
    for line in lines:
        text = line.strip()
        if len(text.split()) < 4:
            continue
        if unlicensed(vocabulary, text, level):
            continue
        out.append(text)
    return out


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--level", type=int, default=1)
    parser.add_argument("--spec", type=Path, required=True)
    parser.add_argument("--attempts", type=int, default=4)
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--max-predict", type=int, default=600)
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args(argv[1:])

    vocabulary = load_vocabulary(ROOT / "curriculum/vocabulary.json")
    admissible = admissible_words(vocabulary, args.level)
    plan = sched.load(ROOT / f"curriculum/schedule/level_{args.level:02d}.json")
    forms = {u.id: u.form for d in plan.domains for u in d.units}
    out_dir = ROOT / f"curriculum/books/level_{args.level}"
    existing, _ = load_book_dir(out_dir)
    taken = {b.id for b in existing}

    spec = cast("list[dict[str, str]]", json.loads(args.spec.read_text()))
    written = 0
    short: list[str] = []
    for entry in spec[: args.limit]:
        target, unit, partner = entry["target"], entry["unit"], entry.get("partner")
        if not (target and unit and partner):
            continue
        book_id = f"bk.{unit}.x_{partner}"
        if book_id in taken:
            print(f"  {book_id}: already written", file=sys.stderr)
            continue
        target_words = words_for(vocabulary, target, args.level)
        partner_words = words_for(vocabulary, partner, args.level)
        if not target_words or not partner_words:
            short.append(f"{book_id}: no admissible words for one of the concepts")
            continue
        form = (
            f"{forms.get(unit, '')} "
            f"Tell it as one story that keeps returning to these words: "
            f"{', '.join(partner_words[:8])}. "
            f"What happens in the story must show why, using these words: "
            f"{', '.join(target_words[:8])}. "
            f"EVERY LINE INCLUDING THE SUBJECT LINE must use only the word "
            f"list at the bottom."
        )
        stories: list[str] = []
        subject_line = ""
        for _ in range(args.attempts):
            reply = ask(
                prompts.book(
                    subject=unit,
                    subject_form=form,
                    words={},
                    level=args.level,
                    admissible=admissible,
                    sentences=8,
                ),
                timeout=args.timeout,
                max_predict=args.max_predict,
            ).splitlines()
            # **The format is a request, not a guarantee, and the parser
            # tolerates drift.** Measured 2026-09-26: the teacher prefixed
            # one line with STORY and wrote the next five as plain prose. All
            # six were usable. Requiring the prefix threw away five sixths of
            # a good reply, and validation is per sentence regardless, so a
            # line that is not a sentence is rejected on its own merits.
            candidates: list[str] = []
            for line in reply:
                text = line.strip()
                if not text or text.startswith("WORD"):
                    continue
                if text.startswith("SUBJECT:"):
                    head = text.split(":", 1)[1].strip()
                    fresh = head and not subject_line
                    if fresh and not unlicensed(vocabulary, head, args.level):
                        subject_line = head
                    continue
                candidates.append(
                    text.split(":", 1)[1].strip() if text.startswith("STORY:") else text
                )
            stories += accepted(candidates, vocabulary, args.level)
            # **Duplicates are the failure this pass exists to avoid.**
            seen: set[str] = set()
            stories = [s for s in stories if not (s in seen or seen.add(s))]
            if subject_line and len(stories) >= SPREADS - 1:
                break
        if not subject_line or len(stories) < SPREADS - 1:
            short.append(
                f"{book_id}: subject {'yes' if subject_line else 'NO'}, "
                f"{len(stories)} of {SPREADS - 1} story spreads"
            )
            continue

        records: list[dict[str, object]] = [
            {
                "id": f"{unit}.x_{partner}.d00",
                "level": args.level,
                "concepts": [target, partner],
                "claim_class": "formal",
                "content": subject_line,
                "provenance": {"source_claim": f"topic:{unit}"},
                "defines": {"kind": "topic", "target": unit},
            }
        ]
        for n, text in enumerate(stories[: SPREADS - 1], start=1):
            records.append(
                {
                    "id": f"{unit}.x_{partner}.s{n:02d}",
                    "level": args.level,
                    "concepts": [target, partner],
                    "claim_class": "empirical",
                    "content": text,
                    "provenance": {"source_claim": f"topic:{unit}"},
                }
            )
        book = Book(
            id=book_id,
            level=args.level,
            # A title is prose for a person and is not vocabulary-checked,
            # so it may name the concepts. Picking a representative word
            # alphabetically gave "and what is clearing" for emptiness.
            title=f"{readable(target).capitalize()}, and {readable(partner)}",
            subject_kind=DefinitionKind.TOPIC,
            subject=unit,
            records=tuple(str(r["id"]) for r in records),
        )
        (out_dir / f"{book_id}.md").write_text(
            render_book(book_head(book), records), encoding="utf-8"
        )
        written += 1
        print(f"  {book_id}: {len(records)} spreads, {target} + {partner}")

    print(
        f"wrote {written} book(s), {len(short)} too short to write, "
        f"{TIMEOUTS[0]} completion(s) abandoned"
    )
    for line in short:
        print(f"  short: {line}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
