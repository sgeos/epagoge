#!/usr/bin/env python3
"""Bring books to the spread standard, without regenerating them.

**A book off the standard is unfinished, not wrong.** Regenerating it
would throw away lines that are already true and admissible, so a short
book is asked for only the spreads it is missing and a long one is cut
back to sixteen from the end.

**A long book was possible from the first generation run and went
unnoticed until the gate enforced the count.** The book prompt asks for
twice the story it needs, because about half is rejected on vocabulary,
and a run where little was rejected produced books of eighteen,
twenty-five and twenty-eight spreads. Trimming takes story lines from the
end, never the subject statement and never a definition, because those
are what the book shape exists to put first.

    PYTHONPATH=src:generators python3 generators/extend_books.py --limit 5
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import cast

from generate import ask
from generate_books import Reject, Tally, admissible_words, keep
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
    # **Top-up rounds are where most rejection now happens**, and until
    # this was written their evidence went to stderr as a count and was
    # gone. A word the teacher reached for is the reason the quarantine
    # exists, so the pass that reaches hardest must write one.
    parser.add_argument(
        "--quarantine", type=Path, default=ROOT / "tmp/quarantine_extend.jsonl"
    )
    args = parser.parse_args(argv[1:])

    vocabulary = load_vocabulary(ROOT / "curriculum/vocabulary.json")
    admissible = admissible_words(vocabulary, args.level)
    book_dir = ROOT / f"curriculum/books/level_{args.level}"

    tally = Tally()
    quarantine: list[Reject] = []
    done = 0
    for path in sorted(book_dir.glob("bk.*.md")):
        if done >= args.limit:
            break
        book, records = parse_book(path.read_text(encoding="utf-8"), path.name)
        short = SPREADS - len(book.records)
        entries = [cast(dict[str, object], r) for r in records]
        if short < 0:
            keep_first = sum(1 for e in entries if e.get("defines") is not None)
            if keep_first > SPREADS:
                print(
                    f"  {book.id}: {keep_first} definitions, cannot trim to {SPREADS}",
                    file=sys.stderr,
                )
                continue
            trimmed = entries[:SPREADS]
            head_now = {
                "id": book.id,
                "level": book.level,
                "title": book.title,
                "subject": {"kind": book.subject_kind.value, "target": book.subject},
            }
            path.write_text(render_book(head_now, trimmed), encoding="utf-8")
            print(
                f"  {book.id}: {len(entries)} spreads, trimmed to {SPREADS}",
                file=sys.stderr,
            )
            done += 1
            continue
        if short == 0:
            continue
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
                if not keep(
                    text,
                    vocabulary,
                    args.level,
                    tally,
                    book=book.id,
                    slot="story",
                    quarantine=quarantine,
                ):
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
    args.quarantine.parent.mkdir(parents=True, exist_ok=True)
    with args.quarantine.open("w", encoding="utf-8") as handle:
        for reject in quarantine:
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
    print(f"extended {done} book(s), {len(quarantine)} quarantined")
    for reason, count in sorted(tally.reasons.items(), key=lambda kv: -kv[1])[:8]:
        print(f"  {count:4}  {reason}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
