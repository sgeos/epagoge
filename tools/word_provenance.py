#!/usr/bin/env python3
"""When each word entered the lexicon, and under what reason.

**Post-facto analysis needs to answer, for every word, why it is there.**
Most of the lexicon predates any field recording that, so the answer has
to be recovered rather than invented, and the repository's own history is
the only honest source: the commit that first introduced a word says when
it arrived and, in its message, why.

Walks every revision of the vocabulary and records, for each word, the
first commit that contains it. Where a term carries a `source` written at
admission, that is reported alongside and is better evidence, because it
was written when the decision was made rather than reconstructed from it.

**A reconstructed reason is labelled as reconstructed.** A commit subject
is what the commit was about, which is usually but not always why a
particular word was in it.

    PYTHONPATH=src python3 tools/word_provenance.py --out curriculum/provenance.json
"""

from __future__ import annotations

import argparse
import json
import subprocess  # noqa: S404
import sys
from pathlib import Path
from typing import cast

ROOT = Path(__file__).resolve().parent.parent
TRACKED = "curriculum/vocabulary.json"


def git(*args: str) -> str:
    return subprocess.run(  # noqa: S603
        ["git", *args],  # noqa: S607
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout


def words_at(revision: str) -> set[str]:
    """The headwords present in one revision of the lexicon."""
    try:
        blob = git("show", f"{revision}:{TRACKED}")
    except subprocess.CalledProcessError:
        return set()
    try:
        payload = cast("dict[str, object]", json.loads(blob))
    except json.JSONDecodeError:
        return set()
    terms = cast("list[dict[str, object]]", payload.get("terms", []))
    return {str(t["word"]) for t in terms if "word" in t}


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=None)
    # **A provenance record that has drifted is worse than none**, because
    # it reads as evidence. The gate regenerates and compares rather than
    # trusting the file.
    parser.add_argument(
        "--check",
        action="store_true",
        help="compare curriculum/provenance.json against the history",
    )
    parser.add_argument("--top", type=int, default=12)
    args = parser.parse_args(argv[1:])

    history = [
        line.split("\t", 2)
        for line in git(
            "log", "--reverse", "--format=%H\t%ad\t%s", "--date=short", "--", TRACKED
        ).splitlines()
        if line.strip()
    ]
    if not history:
        print("no history for the vocabulary", file=sys.stderr)
        return 2

    sources: dict[str, str] = {}
    current = cast(
        "dict[str, object]",
        json.loads((ROOT / TRACKED).read_text(encoding="utf-8")),
    )
    for term in cast("list[dict[str, object]]", current.get("terms", [])):
        recorded = str(term.get("source", "")).strip()
        if recorded:
            sources.setdefault(str(term["word"]), recorded)

    first: dict[str, dict[str, str]] = {}
    seen: set[str] = set()
    for commit, date, subject in history:
        present = words_at(commit)
        for word in sorted(present - seen):
            first[word] = {
                "commit": commit[:12],
                "date": date,
                "commit_subject": subject,
            }
        seen |= present

    for word, entry in first.items():
        if word in sources:
            entry["source"] = sources[word]
            entry["evidence"] = "recorded at admission"
        else:
            entry["evidence"] = "reconstructed from history"

    recorded = sum(
        1 for e in first.values() if e["evidence"] == "recorded at admission"
    )
    print(f"revisions of the lexicon      {len(history)}")
    print(f"words with a first commit     {len(first)}")
    print(f"  source recorded at admission  {recorded}")
    print(f"  reconstructed from history    {len(first) - recorded}")
    print()
    by_date: dict[str, int] = {}
    for entry in first.values():
        by_date[entry["date"]] = by_date.get(entry["date"], 0) + 1
    print("words first seen, by date")
    for date in sorted(by_date):
        print(f"  {date}  {by_date[date]:>5}")

    if args.check:
        path = ROOT / "curriculum/provenance.json"
        if not path.is_file():
            print(f"no {path}", file=sys.stderr)
            return 1
        held = cast("dict[str, object]", json.loads(path.read_text(encoding="utf-8")))
        recorded_words = cast("dict[str, object]", held.get("words", {}))
        missing = sorted(set(first) - set(recorded_words))
        extra = sorted(set(recorded_words) - set(first))
        if missing or extra:
            print(
                f"provenance is stale: {len(missing)} word(s) missing, "
                f"{len(extra)} no longer in the lexicon",
                file=sys.stderr,
            )
            for word in (missing + extra)[:10]:
                print(f"  {word}", file=sys.stderr)
            return 1
        print("provenance matches the history")
        return 0

    if args.out is not None:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(
            json.dumps(
                {
                    "_comment": (
                        "When each word entered the lexicon. 'recorded at "
                        "admission' is evidence written when the decision was "
                        "made. 'reconstructed from history' is the commit that "
                        "first contained the word, which is what the commit was "
                        "about rather than necessarily why that word was in it."
                    ),
                    "revisions": len(history),
                    "words": dict(sorted(first.items())),
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        print(f"\nwrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
