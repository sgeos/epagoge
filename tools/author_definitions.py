#!/usr/bin/env python3
"""Apply authored dictionary definitions, rejecting any that do not ground.

Reads a JSON object mapping word to definition on stdin or from a file.
**Nothing is written unless every entry passes**, because a partial wave
leaves the dictionary out of self-hosting and the gate then refuses the
commit anyway.

Three checks, in order of cheapness. The word must be a headword, the text
must stay inside the level's vocabulary, and the whole dictionary must
still reduce to the seed with the entry added.

**A value may name a second sense** as an object with ``concept`` and
``definition``. Its record is ``dict.LEVEL.WORD.CONCEPT``, carries that
concept, and is written or replaced on its own, so the word's other
records are never touched by it. A plain string never touches a
second-sense record. The sense must be filed at this level, and it must not
be the word's only sense at or below it. The closure check is keyed by
word and sees one definition per word, so a second sense's text is checked
here, token by token, against what the closure grounds.

    PYTHONPATH=src python3 tools/author_definitions.py [file] [--level N]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import cast

from epagoge.book import (
    Book,
    DefinitionKind,
    book_head,
    dictionary_closure,
    load_book_dir,
    parse_book,
    render_book,
    sense_record_id,
    ungrounded_tokens,
    word_definitions,
)
from epagoge.vocabulary import load_vocabulary, tokenise, unlicensed

ROOT = Path(__file__).resolve().parent.parent

_LEVEL_NAME: dict[int, str] = {
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
}


def new_seed_text(level: int, subject: str) -> str:
    """A dictionary book for a level that does not have one yet.

    Levels three to seven had no book directory, so the first definition
    at those levels could not be written. The subject is a word this file
    is about to define. The licence is recorded because a book that does
    not say cannot be reused.
    """
    if level not in _LEVEL_NAME:
        raise ValueError(f"level {level} is outside 1 to 7")
    if not subject.strip():
        raise ValueError("a new dictionary needs a subject word")
    book = Book(
        id="bk.dictionary.seed",
        level=level,
        title=f"The first words at level {_LEVEL_NAME[level]}",
        subject_kind=DefinitionKind.WORD,
        subject=subject,
        form="reference",
        licence="CC0-1.0",
    )
    return render_book(book_head(book), [])


def write_seed_if_missing(path: Path, level: int, subject: str) -> bool:
    """Create the seed dictionary when the level has never had one."""
    if path.exists():
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(new_seed_text(level, subject), encoding="utf-8")
    return True


def is_sense_record(entry: dict[str, object], level: int, word: str) -> bool:
    """Whether a record is a second-sense record of ``word`` at ``level``."""
    concepts = cast(list[object], entry.get("concepts") or [])
    return any(
        entry.get("id") == sense_record_id(level, word, str(concept))
        for concept in concepts
    )


def split_drafts(
    raw: object,
) -> tuple[dict[str, str], dict[str, tuple[str, str]], list[str]]:
    """Plain drafts, second-sense drafts as concept and text, and problems."""
    if not isinstance(raw, dict):
        return {}, {}, ["input must be a JSON object"]
    plain: dict[str, str] = {}
    senses: dict[str, tuple[str, str]] = {}
    problems: list[str] = []
    for key, value in cast(dict[object, object], raw).items():
        word = str(key)
        if isinstance(value, str):
            plain[word] = value
            continue
        if isinstance(value, dict):
            spec = cast(dict[object, object], value)
            concept = spec.get("concept")
            text = spec.get("definition")
            if (
                set(spec) == {"concept", "definition"}
                and isinstance(concept, str)
                and isinstance(text, str)
                and concept
                and text
            ):
                senses[word] = (concept, text)
                continue
        problems.append(
            f"{word}: a definition is a string, or an object with exactly "
            "a concept and a definition"
        )
    return plain, senses, problems


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", nargs="?", type=Path)
    parser.add_argument("--level", type=int, default=1)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv[1:])
    if not 1 <= args.level <= 7:
        parser.error("level must be from 1 to 7")

    raw = args.file.read_text(encoding="utf-8") if args.file else sys.stdin.read()
    drafts, sense_drafts, problems = split_drafts(json.loads(raw))

    vocabulary = load_vocabulary(ROOT / "curriculum/vocabulary.json")
    seed = set(vocabulary.seed_words())
    headwords = {term.word for term in vocabulary.terms}
    book_dir = ROOT / f"curriculum/books/level_{args.level}"
    # **Level two builds on a closed level one.** Definitions from earlier
    # levels are already grounded, so the closure check has to see them or
    # every level above the first starts from nothing.
    lower_dirs = [ROOT / f"curriculum/books/level_{n}" for n in range(1, args.level)]

    def resolve(token: str) -> str | None:
        found = vocabulary.lookup(token)
        return found.word if found is not None else None

    paths = sorted(book_dir.glob("*.md"))
    parsed = {p: parse_book(p.read_text(encoding="utf-8"), p.name) for p in paths}
    # **Canonical, not whichever record was read last.** Built by
    # assignment order this took the book-embedded definition over the
    # dictionary one, and the book versions are frequently ungrounded, so
    # `shape`, `house` and `bright` all read as ungrounded while the
    # dictionary defines them perfectly well.
    all_books = [book for book, _records in parsed.values()]
    all_records = [
        cast(dict[str, object], r)
        for _book, records in parsed.values()
        for r in records
    ]
    current = word_definitions(all_books, all_records)
    inherited: dict[str, str] = {}
    for lower in lower_dirs:
        if not lower.exists():
            continue
        books, records = load_book_dir(lower)
        inherited.update(
            word_definitions(books, [cast(dict[str, object], r) for r in records])
        )

    for word, text in drafts.items():
        if word not in headwords:
            problems.append(f"{word}: not a headword")
        outside = unlicensed(vocabulary, text, args.level)
        if outside:
            problems.append(f"{word}: outside level {args.level}: {' '.join(outside)}")
    for word, (concept, text) in sense_drafts.items():
        same = [t for t in vocabulary.terms if t.word == word]
        filed = [t for t in same if t.concept == concept]
        if not filed:
            problems.append(f"{word}: no sense under {concept!r}")
        elif filed[0].level != args.level:
            problems.append(
                f"{word}: the sense under {concept!r} is filed at level "
                f"{filed[0].level}, not {args.level}"
            )
        elif not any(t.concept != concept and t.level <= args.level for t in same):
            problems.append(
                f"{word}: {concept!r} is its only sense at or below level "
                f"{args.level}, so it takes a plain definition"
            )
        outside = unlicensed(vocabulary, text, args.level)
        if outside:
            problems.append(f"{word}: outside level {args.level}: {' '.join(outside)}")

    trial = {**inherited, **current}
    trial.update(drafts)
    closure = dictionary_closure(trial, seed, tokenise, resolve)
    for word in drafts:
        if word not in closure.grounded:
            needs = sorted(
                {
                    (resolve(t) or t)
                    for t in tokenise(drafts[word])
                    if (resolve(t) or t) not in closure.grounded
                    and t not in seed
                    and (resolve(t) or t) not in seed
                    and (resolve(t) or t) != word
                }
            )
            problems.append(f"{word}: ungrounded, needs {' '.join(needs[:6])}")
    # **The same rule the gate applies to every record**, shared so the
    # authoring check and tools/validate_closure.py cannot drift apart.
    for word, (_concept, text) in sense_drafts.items():
        needs = ungrounded_tokens(text, word, closure.grounded, seed, tokenise, resolve)
        if needs:
            problems.append(f"{word}: ungrounded, needs {' '.join(needs[:6])}")

    if problems:
        print(f"{len(problems)} problem(s), nothing written:", file=sys.stderr)
        for line in problems:
            print(f"  {line}", file=sys.stderr)
        return 1
    if args.dry_run:
        print(f"{len(drafts) + len(sense_drafts)} would apply cleanly")
        return 0

    patched = 0
    sense_ids = {
        sense_record_id(args.level, w, c): w for w, (c, _t) in sense_drafts.items()
    }
    existing_sense_ids: set[str] = set()
    for path, (book, records) in parsed.items():
        kept: list[dict[str, object]] = []
        changed = False
        for record in records:
            entry = cast(dict[str, object], record)
            defines = cast(dict[str, object], entry.get("defines") or {})
            record_id = str(entry.get("id", ""))
            if record_id in sense_ids:
                entry["content"] = sense_drafts[sense_ids[record_id]][1]
                existing_sense_ids.add(record_id)
                changed = True
                patched += 1
            elif defines.get("kind") == "word":
                target = str(defines["target"])
                if (
                    target in drafts
                    and target in current
                    and not is_sense_record(entry, args.level, target)
                ):
                    entry["content"] = drafts[target]
                    changed = True
                    patched += 1
            kept.append(entry)
        if changed:
            path.write_text(
                render_book(book_head(book), kept),
                encoding="utf-8",
            )

    fresh = {w: t for w, t in drafts.items() if w not in current}
    fresh_senses = {
        w: spec
        for w, spec in sense_drafts.items()
        if sense_record_id(args.level, w, spec[0]) not in existing_sense_ids
    }
    if fresh or fresh_senses:
        seed_path = book_dir / "bk.dictionary.seed.md"
        write_seed_if_missing(seed_path, args.level, min({*fresh, *fresh_senses}))
        book, records = parse_book(
            seed_path.read_text(encoding="utf-8"), seed_path.name
        )
        out = [cast(dict[str, object], r) for r in records]
        for word, text in fresh.items():
            senses = sorted(vocabulary.senses(word), key=lambda s: s.level)
            out.append(
                {
                    "id": f"dict.{args.level}.{word}",
                    "level": args.level,
                    "concepts": [senses[0].concept],
                    "claim_class": "formal",
                    "content": text,
                    "provenance": {"source_claim": f"lexicon:{word}"},
                    "defines": {"kind": "word", "target": word},
                }
            )
        for word, (concept, text) in fresh_senses.items():
            out.append(
                {
                    "id": sense_record_id(args.level, word, concept),
                    "level": args.level,
                    "concepts": [concept],
                    "claim_class": "formal",
                    "content": text,
                    "provenance": {"source_claim": f"lexicon:{word}"},
                    "defines": {"kind": "word", "target": word},
                }
            )
        # **Written back in alphabetical order.** Appending put every new
        # entry at the end, which is authoring order and is meaningful to
        # nobody looking a word up. The gate checks the order, so leaving
        # it to a separate pass makes every admission break the build.
        out.sort(
            key=lambda entry: (
                str(
                    cast(dict[str, object], entry.get("defines") or {}).get(
                        "target", ""
                    )
                ),
                str(entry.get("id", "")),
            )
        )
        seed_path.write_text(
            render_book(book_head(book), out),
            encoding="utf-8",
        )
    print(
        f"patched {patched}, appended {len(fresh) + len(fresh_senses)}, "
        f"total defined {len(trial)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
