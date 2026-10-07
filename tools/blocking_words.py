#!/usr/bin/env python3
"""Rank unadmitted words by how many retained rejected definitions they blocked.

**A word the teacher reached for is evidence about the corpus.** Every
retained generation report records, for each rejected definition, the
tokens outside the level that made it fail. A blocker admitted once unblocks
every later definition that needs it, so this ranking orders candidates by
what they would unblock rather than by how often a source used them.

Counts are per rejected definition, so a token repeated inside one reply
counts once. A token is reported only while it is not admissible at the
level under the exact reading the tokeniser uses.

**A malformed report is refused, not skipped.** A tool that returns less
than it was asked for must say so, and a report silently dropped would make
the ranking look complete when it is not.

    PYTHONPATH=src python3 tools/blocking_words.py --level 2
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import cast

from epagoge.vocabulary import Vocabulary, load_vocabulary, unlicensed

ROOT = Path(__file__).resolve().parent.parent

REJECTED = "outside_vocabulary"
"""The outcome status whose tokens name the words that blocked it."""


@dataclass(frozen=True, slots=True)
class Blocker:
    word: str
    rejections: int
    blocked: tuple[str, ...]
    """Candidate words whose rejected definitions needed this one, sorted."""


@dataclass(frozen=True, slots=True)
class Ranking:
    reports: int
    rejected_definitions: int
    blockers: tuple[Blocker, ...]


def _outcomes(path: Path) -> list[tuple[str, frozenset[str]]]:
    """Every rejected definition in one report, with its blocking tokens."""
    try:
        raw: object = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"{path}: unreadable report ({error})") from error
    if not isinstance(raw, dict):
        raise ValueError(f"{path}: a report must be an object")
    requests = cast(dict[str, object], raw).get("requests")
    if not isinstance(requests, list):
        raise ValueError(f"{path}: requests must be a list")
    found: list[tuple[str, frozenset[str]]] = []
    for r_index, request in enumerate(cast(list[object], requests)):
        if not isinstance(request, dict):
            raise ValueError(f"{path}: request {r_index} must be an object")
        outcomes = cast(dict[str, object], request).get("outcomes", [])
        if not isinstance(outcomes, list):
            raise ValueError(f"{path}: request {r_index} outcomes must be a list")
        for o_index, outcome in enumerate(cast(list[object], outcomes)):
            where = f"{path}: request {r_index} outcome {o_index}"
            if not isinstance(outcome, dict):
                raise ValueError(f"{where} must be an object")
            body = cast(dict[str, object], outcome)
            word, status = body.get("word"), body.get("status")
            if not isinstance(word, str) or not isinstance(status, str):
                raise ValueError(f"{where} needs string word and status")
            if status != REJECTED:
                continue
            tokens = body.get("tokens")
            if not isinstance(tokens, list) or not tokens:
                raise ValueError(f"{where} is rejected but names no tokens")
            if not all(isinstance(t, str) and t for t in cast(list[object], tokens)):
                raise ValueError(f"{where} tokens must be nonblank strings")
            found.append((word, frozenset(cast(list[str], tokens))))
    return found


def rank(reports: list[Path], vocabulary: Vocabulary, level: int) -> Ranking:
    """Blockers still outside ``level``, most rejections first, then by word."""
    if level < 1:
        raise ValueError("level must be at least 1")
    counts: dict[str, int] = {}
    blocked: dict[str, set[str]] = {}
    rejected = 0
    for path in reports:
        for word, tokens in _outcomes(path):
            rejected += 1
            for token in tokens:
                counts[token] = counts.get(token, 0) + 1
                blocked.setdefault(token, set()).add(word)
    still = [
        Blocker(token, n, tuple(sorted(blocked[token])))
        for token, n in counts.items()
        if unlicensed(vocabulary, token, level)
    ]
    still.sort(key=lambda b: (-b.rejections, b.word))
    return Ranking(len(reports), rejected, tuple(still))


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--level", type=int, required=True)
    parser.add_argument("reports", nargs="*", type=Path)
    parser.add_argument(
        "--vocabulary", type=Path, default=ROOT / "curriculum/vocabulary.json"
    )
    args = parser.parse_args(argv[1:])
    reports = cast(list[Path], args.reports) or sorted(
        ROOT.glob("evals/review/*/generation.json")
    )
    if not reports:
        print("no generation reports found", file=sys.stderr)
        return 1
    ranking = rank(reports, load_vocabulary(args.vocabulary), args.level)
    print(
        f"{ranking.reports} reports, {ranking.rejected_definitions} rejected "
        f"definitions, {len(ranking.blockers)} blockers still outside level "
        f"{args.level}"
    )
    for blocker in ranking.blockers:
        print(
            f"  {blocker.rejections:3d}  {blocker.word:16s} {' '.join(blocker.blocked)}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
