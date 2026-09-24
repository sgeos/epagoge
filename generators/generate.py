#!/usr/bin/env python3
"""Generate level-one records from the schedule, through the local teacher.

Nothing leaves the machine. The teacher runs under Ollama on Apache-licensed
weights, for the reason in `docs/decisions/OPEN_QUESTIONS.md` item two.

Teacher output is untrusted input. Every line is checked against the record
schema before it is written, and a line that fails is rejected loudly and
counted rather than repaired.

    PYTHONPATH=src python3 generators/generate.py --limit 10 --out tmp/draft.jsonl
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess  # noqa: S404
import sys
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import cast

from epagoge import prompt as prompts
from epagoge import schedule as sched
from epagoge.concept_graph import ConceptGraph
from epagoge.vocabulary import Vocabulary, load_vocabulary, unlicensed

ROOT = Path(__file__).resolve().parent.parent
MODEL = "qwen3:30b-a3b-instruct-2507-q4_K_M"


def teacher_binary() -> str:
    """Resolve the runtime to an absolute path before executing it.

    The argument vector is fixed and no shell is involved, so the only
    variable is which binary the name resolves to. Resolving it here means
    that is decided once and visibly rather than by the caller's PATH at the
    moment of the call.
    """
    found = shutil.which("ollama")
    if found is None:
        raise RuntimeError("ollama is not on PATH; the teacher runs locally")
    return found


@dataclass(frozen=True, slots=True)
class Draft:
    unit: str
    concept: str
    level: int
    text: str
    attempts: int


@dataclass
class Tally:
    """Counts kept so the run reports what it rejected, not only what it kept.

    A generator that silently drops failures reports a clean run whatever
    the teacher did, which is the failure shape this project keeps finding.
    """

    accepted: int = 0
    rejected: int = 0
    retried: int = 0
    fragments: int = 0
    duplicates: int = 0


def admissible_words(vocabulary: dict[str, object], level: int) -> list[str]:
    core = cast(list[str], vocabulary.get("core", []))
    exempt = cast(list[str], vocabulary.get("exempt", []))
    terms = cast(list[dict[str, object]], vocabulary.get("terms", []))
    licensed = [
        cast(str, t["word"])
        for t in terms
        if isinstance(t.get("level"), int) and cast(int, t["level"]) <= level
    ]
    return sorted({*core, *exempt, *licensed})


def load_primitives(path: Path) -> dict[str, str]:
    """Read the register, checking its shape rather than assuming it."""
    parsed: object = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(parsed, dict):
        parsed = cast(dict[str, object], parsed).get("primitives", [])
    if not isinstance(parsed, list):
        raise ValueError("primitive register must be a list, or hold one")
    out: dict[str, str] = {}
    for entry in cast(list[object], parsed):
        if not isinstance(entry, dict):
            raise ValueError("each primitive must be an object")
        fields = cast(dict[str, object], entry)
        key, text = fields.get("id"), fields.get("observation", "")
        if not isinstance(key, str) or not isinstance(text, str):
            raise ValueError(f"malformed primitive entry {entry!r}")
        out[key] = text
    return out


MIN_WORDS = 3
"""Shortest accepted draft.

A one-word line passed the vocabulary ceiling on the first real batch and
was written as a record. The ceiling check asks whether every word is
admissible, and a fragment satisfies that trivially. Length is the cheapest
available proxy for being a sentence at all.
"""


def split_lines(raw: str) -> list[str]:
    """Split a completion into candidate sentences.

    List markers are stripped only from the very front of a line, and only
    when a marker is actually there. The earlier version stripped any
    leading run of digits, dots, dashes and spaces, which ate the first word
    of a line beginning with a number word and produced a fragment that
    then passed every later check.
    """
    out: list[str] = []
    for line in raw.splitlines():
        stripped = line.strip()
        marker = re.match(r"^\s*(?:[-*\u2022]|\d+[.)])\s+", stripped)
        if marker:
            stripped = stripped[marker.end() :].strip()
        if stripped:
            out.append(stripped)
    return out


def ask(text: str, *, timeout: int) -> str:
    """Run one completion. Raises on a non-zero exit so failure is loud."""
    done = subprocess.run(  # noqa: S603
        [teacher_binary(), "run", MODEL],
        input=text,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=True,
    )
    return done.stdout.strip()


def drafts_for(
    plan: sched.Schedule,
    graph: ConceptGraph,
    primitives: dict[str, str],
    vocabulary: Vocabulary,
    words: list[str],
    tally: Tally,
    *,
    limit: int,
    count: int,
    timeout: int,
    max_attempts: int,
) -> Iterator[Draft]:
    """Yield drafts that pass the vocabulary ceiling, retrying those that do not.

    Only `teaches` targets are generated. A concept the schedule marks as
    `introduces` is not in the graph, so its neighbours cannot be derived and
    the exclusion list that makes generation work cannot be built. Those need
    their nodes authored first, which is a separate step.

    A rejected line is re-asked with its offending words named. A generic
    repeat of the constraint produces a generic repeat of the violation.
    """
    emitted = 0
    seen_text: set[str] = set()
    for domain in plan.domains:
        for unit in domain.units:
            for concept in unit.teaches:
                if emitted >= limit:
                    return
                emitted += 1
                target = prompts.target_for(
                    graph, concept, unit.form, primitives, unit.primitives
                )
                text = prompts.build(target, plan.level, words, count=count)
                wanted = count
                for attempt in range(1, max_attempts + 1):
                    lines = split_lines(ask(text, timeout=timeout))
                    bad: list[str] = []
                    kept = 0
                    for line in lines:
                        offending = unlicensed(vocabulary, line, plan.level)
                        if offending:
                            bad.extend(offending)
                            continue
                        if len(line.split()) < MIN_WORDS:
                            tally.fragments += 1
                            continue
                        key = line.rstrip(".").casefold()
                        if key in seen_text:
                            # The same sentence arrived for a different
                            # concept. Keeping both would attribute one piece
                            # of teaching to two ideas, which is the
                            # conflation the exclusions exist to prevent,
                            # arriving as duplication rather than as drift.
                            tally.duplicates += 1
                            continue
                        seen_text.add(key)
                        yield Draft(unit.id, concept, plan.level, line, attempt)
                        kept += 1
                    tally.accepted += kept
                    wanted -= kept
                    failed = len(lines) - kept
                    print(
                        f"  {unit.id}/{concept} try {attempt}:"
                        f" {kept} kept, {failed} rejected",
                        file=sys.stderr,
                    )
                    if wanted <= 0 or attempt == max_attempts:
                        tally.rejected += failed
                        break
                    tally.retried += 1
                    tally.rejected += failed
                    rejected_lines = [
                        line
                        for line in lines
                        if unlicensed(vocabulary, line, plan.level)
                    ]
                    text = prompts.retry(
                        target, plan.level, words, rejected_lines, bad, count=wanted
                    )


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--level", type=int, default=1)
    parser.add_argument("--limit", type=int, default=5, help="concepts to generate for")
    parser.add_argument("--count", type=int, default=3, help="sentences per concept")
    parser.add_argument("--timeout", type=int, default=300)
    parser.add_argument("--attempts", type=int, default=3, help="tries per concept")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv[1:])

    graph = ConceptGraph.load(ROOT / "curriculum/graph/concepts.json")
    plan = sched.load(ROOT / f"curriculum/schedule/level_{args.level:02d}.json")
    primitives = load_primitives(ROOT / "curriculum/primitives.json")
    vocabulary_path = ROOT / "curriculum/vocabulary.json"
    raw_vocabulary = cast(
        dict[str, object], json.loads(vocabulary_path.read_text(encoding="utf-8"))
    )
    vocabulary = load_vocabulary(vocabulary_path)
    words = admissible_words(raw_vocabulary, args.level)

    print(f"teacher {MODEL}", file=sys.stderr)
    print(f"level {args.level}, {len(words)} admissible words", file=sys.stderr)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    tally = Tally()
    written = 0
    with args.out.open("w", encoding="utf-8") as handle:
        for draft in drafts_for(
            plan,
            graph,
            primitives,
            vocabulary,
            words,
            tally,
            limit=args.limit,
            count=args.count,
            timeout=args.timeout,
            max_attempts=args.attempts,
        ):
            handle.write(
                json.dumps(
                    {
                        "unit": draft.unit,
                        "concept": draft.concept,
                        "level": draft.level,
                        "content": draft.text,
                        "attempts": draft.attempts,
                    }
                )
                + "\n"
            )
            written += 1
    print(
        f"wrote {written} drafts to {args.out}."
        f" accepted {tally.accepted}, rejected {tally.rejected},"
        f" fragments {tally.fragments}, duplicates {tally.duplicates},"
        f" retries {tally.retried}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
