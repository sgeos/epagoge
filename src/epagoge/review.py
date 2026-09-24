"""Human review of corpus records.

This is the sampled expert audit from open question two, not only a reading
aid. It produces the measured residual error rate that the project's central
quality claim rests on, and that the collaborative positioning treats as a
credential.

Standard library only.
"""

from __future__ import annotations

import json
import math
import random
from collections.abc import Collection, Iterable, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import Enum
from pathlib import Path
from statistics import NormalDist
from typing import Final, cast

from epagoge.concept_graph import ConceptGraph
from epagoge.record import Record

DEFAULT_CONFIDENCE: Final[float] = 0.95
MIXED_DOMAIN: Final[str] = "mixed"


class Judgment(Enum):
    """A reviewer's verdict on one record."""

    ACCEPT = "accept"
    REJECT = "reject"
    FLAG = "flag"
    """Uncertain. Counted separately, never silently as either."""


@dataclass(frozen=True, slots=True)
class Verdict:
    record_id: str
    judgment: Judgment
    reason: str
    reviewer: str
    at: str

    @staticmethod
    def now(record_id: str, judgment: Judgment, reason: str, reviewer: str) -> Verdict:
        stamp = datetime.now(UTC).isoformat(timespec="seconds")
        return Verdict(record_id, judgment, reason, reviewer, stamp)

    def to_json(self) -> str:
        return json.dumps(
            {
                "record_id": self.record_id,
                "judgment": self.judgment.value,
                "reason": self.reason,
                "reviewer": self.reviewer,
                "at": self.at,
            }
        )


@dataclass(frozen=True, slots=True)
class ErrorRate:
    """A measured rejection rate with its uncertainty.

    The interval matters more than the point estimate. An audit of thirty
    records that rejects three has a rate of ten percent and an interval
    wide enough that quoting ten percent alone would overstate what was
    learned.
    """

    domain: str
    reviewed: int
    rejected: int
    flagged: int

    @property
    def rate(self) -> float:
        return self.rejected / self.reviewed if self.reviewed else math.nan

    def interval(self, confidence: float = DEFAULT_CONFIDENCE) -> tuple[float, float]:
        return wilson_interval(self.rejected, self.reviewed, confidence)


def wilson_interval(
    successes: int, trials: int, confidence: float = DEFAULT_CONFIDENCE
) -> tuple[float, float]:
    """Wilson score interval for a proportion.

    Preferred over the normal approximation because an audit is small and
    the rate is near zero, where the normal approximation gives intervals
    that extend below zero and understate uncertainty.
    """
    if trials < 0 or successes < 0 or successes > trials:
        raise ValueError(f"invalid counts: {successes} of {trials}")
    if not 0.0 < confidence < 1.0:
        raise ValueError(f"confidence must lie in (0, 1), got {confidence}")
    if trials == 0:
        return (0.0, 1.0)
    z = NormalDist().inv_cdf(1.0 - (1.0 - confidence) / 2.0)
    p = successes / trials
    denominator = 1.0 + z * z / trials
    centre = (p + z * z / (2 * trials)) / denominator
    half = (
        z
        / denominator
        * math.sqrt(p * (1.0 - p) / trials + z * z / (4 * trials * trials))
    )
    return (max(0.0, centre - half), min(1.0, centre + half))


def domain_of(record: Record, graph: ConceptGraph) -> str:
    """The single domain a record belongs to, or ``mixed``.

    A record spanning domains is reported separately rather than attributed
    to one, because attributing it would let a rate be moved by a choice of
    attribution rather than by the corpus.
    """
    domains = {
        graph.nodes[c].domain
        for c in record.concepts
        if c in graph.nodes and graph.nodes[c].domain is not None
    }
    if len(domains) == 1:
        only = domains.pop()
        return only if only is not None else MIXED_DOMAIN
    return MIXED_DOMAIN


def error_rates(
    verdicts: Iterable[Verdict], records: Sequence[Record], graph: ConceptGraph
) -> list[ErrorRate]:
    """Per-domain rejection rates. Never aggregated into one number.

    Verifiability varies enormously across domains, so a single rate would
    average a machine-verifiable domain against an interpretive one and
    conceal both. See open question two.
    """
    by_id = {r.id: r for r in records}
    counts: dict[str, list[int]] = {}
    for verdict in verdicts:
        record = by_id.get(verdict.record_id)
        if record is None:
            continue
        key = domain_of(record, graph)
        row = counts.setdefault(key, [0, 0, 0])
        row[0] += 1
        if verdict.judgment is Judgment.REJECT:
            row[1] += 1
        elif verdict.judgment is Judgment.FLAG:
            row[2] += 1
    return [
        ErrorRate(domain=k, reviewed=v[0], rejected=v[1], flagged=v[2])
        for k, v in sorted(counts.items())
    ]


def take_sample(
    records: Sequence[Record], size: int, seed: int, exclude: Collection[str] = ()
) -> list[Record]:
    """A reproducible sample of unreviewed records.

    Reproducible from the seed so that an audit can be repeated exactly, and
    so that a disputed rate can be checked against the same records.
    """
    if size < 1:
        raise ValueError(f"sample size must be positive, got {size}")
    pool = [r for r in records if r.id not in exclude]
    rng = random.Random(seed)
    if size >= len(pool):
        return sorted(pool, key=lambda r: r.id)
    return sorted(rng.sample(pool, size), key=lambda r: r.id)


def load_verdicts(path: Path) -> list[Verdict]:
    if not path.is_file():
        return []
    out: list[Verdict] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        stripped = line.strip()
        if not stripped:
            continue
        parsed: object = json.loads(stripped)
        if not isinstance(parsed, dict):
            raise ValueError(f"{path}:{number}: verdict must be an object")
        body = cast(dict[object, object], parsed)
        out.append(
            Verdict(
                record_id=_require_str(body.get("record_id"), f"{path}:{number}"),
                judgment=Judgment(
                    _require_str(body.get("judgment"), f"{path}:{number}")
                ),
                reason=_require_str(body.get("reason", ""), f"{path}:{number}"),
                reviewer=_require_str(body.get("reviewer", ""), f"{path}:{number}"),
                at=_require_str(body.get("at", ""), f"{path}:{number}"),
            )
        )
    return out


def append_verdict(path: Path, verdict: Verdict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(verdict.to_json() + "\n")


def _require_str(value: object, where: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{where}: expected a string, got {type(value).__name__}")
    return value
