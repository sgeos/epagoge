"""Recompute the retained lexicon increment's counts and preservation checks."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import cast

from epagoge.artifacts import digest, file_digest, write_json
from epagoge.book import load_book_dir, word_definitions
from epagoge.vocabulary import load_vocabulary

ROOT = Path(__file__).resolve().parents[1]


def read(path: Path) -> dict[str, object]:
    return cast(dict[str, object], json.loads(path.read_text(encoding="utf-8")))


def measure(batch: Path) -> dict[str, object]:
    before = read(batch / "before.json")
    generation = read(batch / "generation.json")
    candidates = read(batch / "candidates.json")
    review = cast(dict[str, dict[str, object]], read(batch / "review.json"))
    admitted = cast(dict[str, dict[str, str]], read(batch / "admitted.json"))
    if set(candidates) != set(review) or generation["candidates"] != candidates:
        raise ValueError("candidate accounting differs between artifacts")
    if generation["input_hash"] != file_digest(batch / "candidates.json"):
        raise ValueError("candidate input hash differs")
    if generation["vocabulary_hash"] != before["vocabulary_hash"]:
        raise ValueError("generator did not use the recorded baseline vocabulary")
    if generation["accepted_hash"] != digest(generation["accepted"]):
        raise ValueError("generator acceptance hash differs")
    if generation["accepted"] != read(batch / "generated.json"):
        raise ValueError("generated admission proposal differs from the report")
    outcomes = cast(dict[str, str], generation["outcomes"])
    accepted = cast(dict[str, object], generation["accepted"])
    if set(outcomes) != set(candidates):
        raise ValueError("generator outcomes do not cover every candidate")
    accepted_words = {
        w for w, status in outcomes.items() if status == "mechanically_accepted"
    }
    if accepted_words != set(accepted):
        raise ValueError("generator accepted outcomes differ from definitions")
    skipped = sum(status == "already_admitted" for status in outcomes.values())
    computed = {
        "input": len(candidates),
        "already_admitted": skipped,
        "offered": len(candidates) - skipped,
        "mechanically_accepted": len(accepted),
        "deferred": sum(status == "deferred" for status in outcomes.values()),
    }
    if computed != generation["counts"]:
        raise ValueError("generator counts differ from candidate outcomes")
    decisions = {word for word, row in review.items() if row["decision"] == "admit"}
    if decisions != set(admitted) or not decisions:
        raise ValueError("review and admission decisions differ or none were admitted")
    for row in review.values():
        if row["decision"] not in {"admit", "defer"} or not row.get("reason"):
            raise ValueError(
                "every candidate needs an explicit review decision and reason"
            )
    vocabulary = load_vocabulary(ROOT / "curriculum/vocabulary.json")
    level = cast(int, generation["level"])
    books, records = load_book_dir(ROOT / f"curriculum/books/level_{level}")
    definitions = word_definitions(books, [cast(dict[str, object], r) for r in records])
    for word, entry in admitted.items():
        terms = [t for t in vocabulary.senses(word) if t.level == level]
        if len(terms) != 1:
            raise ValueError(
                f"{word} does not have exactly one admitted sense at the level"
            )
        term = terms[0]
        if term.concept != entry["concept"] or term.source != entry["source"]:
            raise ValueError(f"{word} admission provenance or concept differs")
        if definitions.get(word) != entry["definition"]:
            raise ValueError(f"{word} admitted definition differs")
        if set(term.surface_forms()) != set(
            cast(list[str], review[word]["reviewed_forms"])
        ):
            raise ValueError(f"{word} admitted forms differ from reviewed forms")
    preserved = cast(dict[str, str], before["preserved"])
    for name, expected in preserved.items():
        if file_digest(ROOT / name) != expected:
            raise ValueError(f"preservation failed for {name}")
    if {
        str(p.relative_to(ROOT))
        for p in (ROOT / "curriculum/books/level_1").glob("*.md")
    } != {name for name in preserved if name.endswith(".md")}:
        raise ValueError("level-one book membership changed")
    closure: dict[str, object] = {}
    for current in (1, 2):
        result = subprocess.run(  # noqa: S603
            [
                sys.executable,
                str(ROOT / "tools/validate_closure.py"),
                "curriculum/vocabulary.json",
                f"curriculum/books/level_{current}",
                str(current),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        match = re.search(r"defined\s+(\d+) of (\d+)", result.stdout)
        if (
            match is None
            or match[1] != match[2]
            or "closure 100.0%" not in result.stdout
        ):
            raise ValueError(f"level {current} is not completely defined and grounded")
        closure[str(current)] = {
            "defined": int(match[1]),
            "required": int(match[2]),
            "grounded": True,
            "validator_output": result.stdout,
        }
    counts = {
        str(n): len({t.word for t in vocabulary.terms if t.level <= n}) for n in (1, 2)
    }
    old = cast(dict[str, int], before["counts"])
    if counts["1"] != old["1"] or counts["2"] - old["2"] != len(admitted):
        raise ValueError("vocabulary change differs from reviewed admissions")
    return {
        "before": old,
        "after": counts,
        "candidates": len(candidates),
        "generator_counts": generation["counts"],
        "admitted": len(admitted),
        "deferred": len(candidates) - len(admitted),
        "approximate_target": before["approximate_target"],
        "remaining_gap": cast(int, before["approximate_target"]) - counts["2"],
        "closure": closure,
        "preserved_files": len(preserved),
        "preservation_passed": True,
        "artifact_hashes": {
            name: file_digest(batch / name)
            for name in (
                "before.json",
                "candidates.json",
                "generation.json",
                "generated.json",
                "review.json",
                "admitted.json",
            )
        },
        "limits": (
            "One manually themed batch. This does not measure general throughput "
            "or complete level two. Semantic review is agent review, "
            "not independent expert validation."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("batch", type=Path)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--out", type=Path)
    mode.add_argument("--check", type=Path)
    args = parser.parse_args()
    result = measure(args.batch)
    if args.check:
        if read(args.check) != result:
            raise ValueError("recorded measurement differs from the current tree")
        print("increment measurement matches the tree")
    else:
        write_json(args.out, result)
        print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
