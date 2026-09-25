#!/usr/bin/env python3
"""Apply authored dictionary definitions, rejecting any that do not ground.

Reads a JSON object mapping word to definition on stdin or from a file.
**Nothing is written unless every entry passes**, because a partial wave
leaves the dictionary out of self-hosting and the gate then refuses the
commit anyway.

Three checks, in order of cheapness. The word must be a headword, the text
must stay inside the level's vocabulary, and the whole dictionary must
still reduce to the seed with the entry added.

    PYTHONPATH=src python3 tools/author_definitions.py [file] [--level N]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import cast

from epagoge.book import dictionary_closure, parse_book, render_book
from epagoge.vocabulary import load_vocabulary, tokenise, unlicensed

ROOT = Path(__file__).resolve().parent.parent


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", nargs="?", type=Path)
    parser.add_argument("--level", type=int, default=1)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv[1:])

    raw = args.file.read_text(encoding="utf-8") if args.file else sys.stdin.read()
    drafts = cast(dict[str, str], json.loads(raw))

    vocabulary = load_vocabulary(ROOT / "curriculum/vocabulary.json")
    seed = set(vocabulary.seed_words())
    headwords = {term.word for term in vocabulary.terms}
    book_dir = ROOT / f"curriculum/books/level_{args.level}"

    def resolve(token: str) -> str | None:
        found = vocabulary.lookup(token)
        return found.word if found is not None else None

    paths = sorted(book_dir.glob("*.md"))
    parsed = {p: parse_book(p.read_text(encoding="utf-8"), p.name) for p in paths}
    current: dict[str, str] = {}
    for _book, records in parsed.values():
        for record in records:
            entry = cast(dict[str, object], record)
            defines = cast(dict[str, object], entry.get("defines") or {})
            if defines.get("kind") == "word":
                current[str(defines["target"])] = str(entry["content"])

    problems: list[str] = []
    for word, text in drafts.items():
        if word not in headwords:
            problems.append(f"{word}: not a headword")
        outside = unlicensed(vocabulary, text, args.level)
        if outside:
            problems.append(f"{word}: outside level {args.level}: {' '.join(outside)}")

    trial = dict(current)
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

    if problems:
        print(f"{len(problems)} problem(s), nothing written:", file=sys.stderr)
        for line in problems:
            print(f"  {line}", file=sys.stderr)
        return 1
    if args.dry_run:
        print(f"{len(drafts)} would apply cleanly")
        return 0

    patched = 0
    for path, (book, records) in parsed.items():
        kept: list[dict[str, object]] = []
        changed = False
        for record in records:
            entry = cast(dict[str, object], record)
            defines = cast(dict[str, object], entry.get("defines") or {})
            if defines.get("kind") == "word":
                target = str(defines["target"])
                if target in drafts and target in current:
                    entry["content"] = drafts[target]
                    changed = True
                    patched += 1
            kept.append(entry)
        if changed:
            path.write_text(
                render_book(
                    {
                        "id": book.id,
                        "level": book.level,
                        "title": book.title,
                        "subject": {
                            "kind": book.subject_kind.value,
                            "target": book.subject,
                        },
                    },
                    kept,
                ),
                encoding="utf-8",
            )

    fresh = {w: t for w, t in drafts.items() if w not in current}
    if fresh:
        seed_path = book_dir / "bk.dictionary.seed.md"
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
        seed_path.write_text(
            render_book(
                {
                    "id": book.id,
                    "level": book.level,
                    "title": book.title,
                    "subject": {
                        "kind": book.subject_kind.value,
                        "target": book.subject,
                    },
                },
                out,
            ),
            encoding="utf-8",
        )
    print(f"patched {patched}, appended {len(fresh)}, total defined {len(trial)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
