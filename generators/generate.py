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
import sys
import urllib.error
import urllib.request
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Final, cast

from epagoge import prompt as prompts
from epagoge import schedule as sched
from epagoge.concept_graph import ConceptGraph
from epagoge.vocabulary import Vocabulary, load_vocabulary, unlicensed

ROOT = Path(__file__).resolve().parent.parent
MODEL = "qwen3:30b-a3b-instruct-2507-q4_K_M"


ENDPOINT = "http://127.0.0.1:11434"
"""Where the local teacher answers.

**This used to shell out to `ollama run`, and that was the bug.** The
command line offers no way to say how large a context the work needs, so
every completion inherited whatever the server had loaded. On 2026-09-25
that was **32,768 tokens for prompts of about 1,260**, which is a
key-value cache nineteen times larger than anything asked for. It pushed a
32 GB machine to 9 percent free with swap 92 percent used, and the same
completion that had taken a median of **6.0 seconds went past 300**. The
run that hit it read as the teacher being slow.

Over the endpoint the context is a request parameter, so the project
declares what it needs instead of inheriting a default nobody chose.
"""

NUM_CTX = 4096
"""The context this project asks for.

Measured 2026-09-25: a `fill_spread` prompt is **1,261 tokens** and the
answer runs 180 to 230, so 4,096 leaves better than threefold headroom.
Dropping to it took the server from 21 GB to 18 GB, free memory from 9 to
22 percent, and the completion back to 2.7 to 6.6 seconds.

**Raise it deliberately and re-measure memory**, because the cost is
quadratic in the wrong direction on a machine this size.
"""

RESERVED_FOR_OUTPUT = 768
"""Tokens kept clear of the prompt so the answer is not what gets cut.

The longest answer observed was 228 tokens. This is generous on purpose:
the failure it guards against is silent, and the cost of being generous is
a prompt refused early rather than an answer truncated late.
"""

CHARS_PER_TOKEN = 3
"""Deliberately pessimistic, so the estimate over-counts tokens.

The measured ratio on this project's prompts is about 5.4 characters a
token. Using 3 means the guard fires early rather than late, which is the
right direction for a check whose alternative is silent truncation.
"""


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


def well_formed(line: str) -> bool:
    """Whether a line is shaped like a sentence.

    Three drafts in the second measured batch were accepted while being
    neither capitalised nor terminated, among them "breath lasted long".
    Every word was admissible and the length rule was satisfied, so nothing
    else would have caught them. Shape is not meaning, and this catches only
    the shape.
    """
    if len(line.split()) < MIN_WORDS:
        return False
    return line[:1].isupper() and line.rstrip()[-1:] in ".!?"


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


CSI_RE: Final[re.Pattern[str]] = re.compile(r"\x1b\[([0-9;]*)([A-Za-z])")
"""Terminal control sequences the runtime emits while streaming.

It rewrites each line as it wraps, emitting partial text, then a cursor-back
and an erase, then the corrected text. **Stripping the escape codes alone is
not enough**, because the partial text they were there to erase survives.
The first attempt did exactly that and left fragments like `someth` and `fl`
in the output, which were then counted as words outside the vocabulary.

So the two codes that matter are replayed rather than removed. `CSI n D`
moves the cursor back n places and `CSI K` erases to the end of the line,
and together they mean delete the last n characters.
"""


def strip_terminal_control(raw: str) -> str:
    """Replay cursor-back and erase, and rejoin the line they wrapped.

    The observed sequence is a partial word, `CSI n D`, `CSI K`, a newline,
    and then the word again in full. So the effect is delete the last n
    characters **and join to the next line**, because the newline is the
    wrap that the rewrite exists to undo rather than a real line break.

    The first attempt stripped the escape codes and left the partial word.
    The second replayed the delete and left the newline, which truncated
    every wrapped sentence and cost it its full stop. Setting a wide
    terminal does not help; the runtime wraps regardless.
    """
    out: list[str] = []
    position = 0
    for match in CSI_RE.finditer(raw):
        if match.start() < position:
            continue
        out.append(raw[position : match.start()])
        position = match.end()
        count, final = match.group(1), match.group(2)
        if final == "D":
            back = int(count) if count else 1
            text = "".join(out)
            out = [text[:-back] if back <= len(text) else ""]
        elif final == "K" and raw[position : position + 1] == "\n":
            position += 1
    out.append(raw[position:])
    return "".join(out)


TIMEOUTS = [0]
"""How many completions this process gave up on.

A list of one rather than a bare integer so a caller can read it without
importing the name again after a rebind. **It exists because a run reported
how many books it filled and never how much it lost.** Twenty-six timeouts
at 240 seconds is 104 minutes, which was about two fifths of one run's
wall clock and appeared nowhere in its summary.
"""


def ask(text: str, *, timeout: int) -> str:
    """Run one completion. Loud on failure, but never fatal to a long run.

    **A raised timeout killed a ten-book chunk and lost all of it**, since
    books are written at the end. One slow completion is an ordinary event
    over a run of ninety, so it returns empty and the caller treats it as
    an unusable answer, which is what it is. A non-zero exit still raises,
    because that means the teacher is misconfigured rather than slow.
    """
    budget = NUM_CTX - RESERVED_FOR_OUTPUT
    estimate = len(text) // CHARS_PER_TOKEN
    if estimate > budget:
        raise RuntimeError(
            f"prompt is about {estimate} tokens against a budget of {budget} "
            f"(num_ctx {NUM_CTX} less {RESERVED_FOR_OUTPUT} for the answer). "
            "The server would truncate it silently, so this refuses instead. "
            "Shorten the prompt or raise NUM_CTX deliberately."
        )

    payload = json.dumps(
        {
            "model": MODEL,
            "prompt": text,
            "stream": False,
            "options": {"num_ctx": NUM_CTX},
        }
    ).encode()
    # **The scheme is a literal in this file, not input.** ENDPOINT is a
    # constant naming a loopback address, so there is no user-supplied URL
    # for a `file:` or custom scheme to arrive through.
    request = urllib.request.Request(  # noqa: S310
        f"{ENDPOINT}/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310
            body = cast(dict[str, object], json.load(response))
    except TimeoutError:
        TIMEOUTS[0] += 1
        print(
            f"  teacher timed out after {timeout}s, treating as empty",
            file=sys.stderr,
        )
        return ""
    except urllib.error.URLError as unreachable:
        raise RuntimeError(
            f"the teacher is not answering at {ENDPOINT}: {unreachable}. "
            "It runs locally; start it before a generation run."
        ) from unreachable

    used = body.get("prompt_eval_count")
    if isinstance(used, int) and used > budget:
        print(
            f"  WARNING: the prompt used {used} tokens against a budget of "
            f"{budget}. Part of it was discarded before the model saw it.",
            file=sys.stderr,
        )
    return strip_terminal_control(str(body.get("response", ""))).strip()


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
                        if not well_formed(line):
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
