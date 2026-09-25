#!/usr/bin/env python3
"""Top up short books to the spread standard, without regenerating them.

**A book below the standard is unfinished, not wrong.** Regenerating it
would throw away lines that are already true and admissible, so this asks
the teacher only for the spreads that are missing and appends what passes.

    PYTHONPATH=src:generators python3 generators/extend_books.py --limit 5
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import cast

from generate import ask, well_formed
from generate_books import Tally, admissible_words, keep
from epagoge import prompt as prompts
from epagoge.book import SPREADS, parse_book, render_book
from epagoge.vocabulary import load_vocabulary

ROOT = Path(__file__).resolve().parent.parent


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--level", type=int, default=1)
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--timeout", type=int, default=420)
    parser.add_argument("--attempts", type=int, default=2)
    args = parser.parse_args(argv[1:])

    vocabulary = load_vocabulary(ROOT / "curriculum/vocabulary.json")
    admissible = admissible_words(vocabulary, args.level)
    book_dir = ROOT / f"curriculum/books/level_{args.level}"

    tally = Tally()
    done = 0
    for path in sorted(book_dir.glob("bk.*.md")):
        if done >= args.limit:
            break
        book, records = parse_book(path.read_text(encoding="utf-8"), path.name)
        short = SPREADS - len(book.records)
        if short <= 0:
            continue
        entries = [cast(dict[str, object], r) for r in records]
        existing = "\n".join(str(r["content"]) for r in entries)
        print(
            f"  {book.id}: {len(book.records)} spreads, needs {short}", file=sys.stderr
        )

        added: list[str] = []
        for _attempt in range(args.attempts):
            if len(added) >= short:
                break
            want = short - len(added)
            question = prompts.continue_story(
                book.title, existing, want, args.level, admissible
            )
            raw = ask(question, timeout=args.timeout)
            for line in raw.splitlines():
                text = line.strip().lstrip("-").strip()
                if not text or text.startswith(("STORY", "#")):
                    continue
                if not well_formed(text):
                    continue
                if not keep(text, vocabulary, args.level, tally):
                    continue
                if text in existing or text in added:
                    continue
                added.append(text)
                if len(added) >= short:
                    break

        if not added:
            print("    nothing usable", file=sys.stderr)
            continue
        start = len(entries)
        for offset, text in enumerate(added):
            entries.append(
                {
                    "id": f"{book.id.removeprefix('bk.')}.x{start + offset:02d}",
                    "level": book.level,
                    "concepts": list(cast(list[str], entries[0].get("concepts", []))),
                    "claim_class": "empirical",
                    "content": text,
                    "provenance": {"source_claim": "primitive:things-change"},
                }
            )
        head = {
            "id": book.id,
            "level": book.level,
            "title": book.title,
            "subject": {"kind": book.subject_kind.value, "target": book.subject},
        }
        path.write_text(render_book(head, entries), encoding="utf-8")
        print(f"    added {len(added)}, now {len(entries)}", file=sys.stderr)
        done += 1
    print(f"extended {done} book(s)")
    for reason, count in sorted(tally.reasons.items(), key=lambda kv: -kv[1])[:8]:
        print(f"  {count:4}  {reason}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
