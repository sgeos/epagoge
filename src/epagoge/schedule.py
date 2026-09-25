"""Curriculum schedule.

What gets written at a level, in which domain, and against which concepts.
Specification in ``docs/spec/CURRICULUM_SCHEDULE.md``.

The schedule is the artifact that assigns a level to a concept. Before it
existed, levels were implicit in whichever records happened to be written,
which meant the assignment could not be reviewed before generation started.

Standard library only, matching ``concept_graph``.
"""

from __future__ import annotations

import json
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import cast

from epagoge.concept_graph import ConceptGraph, Violation


@dataclass(frozen=True, slots=True)
class Unit:
    """One teaching target within a domain at a level.

    ``teaches`` names concepts already in the graph. ``introduces`` names
    concepts this unit will create, which must NOT be in the graph yet.

    The split is what lets a schedule plan ahead without breaking the rule
    that the graph follows content. A planned concept is visible as a plan
    and does not become a node until a record teaches it.
    """

    id: str
    form: str
    teaches: tuple[str, ...] = ()
    introduces: tuple[str, ...] = ()
    revisits: tuple[str, ...] = ()
    """Concepts this unit touches without introducing.

    The spiral curriculum requires a concept to reappear at rising
    complexity, and `teaches` is first introduction only, so without this
    field a schedule cannot say that a unit returns to something.

    It is also what lets a unit teach a **relation**. A graph edge saying a
    plant is a kind of living thing is taught by material covering both
    ends, and the general end was introduced elsewhere.
    """

    primitives: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class DomainPlan:
    domain: str
    units: tuple[Unit, ...] = ()

    def teaches(self) -> frozenset[str]:
        return frozenset(c for u in self.units for c in u.teaches)

    def revisits(self) -> frozenset[str]:
        return frozenset(c for u in self.units for c in u.revisits)

    def introduces(self) -> frozenset[str]:
        return frozenset(c for u in self.units for c in u.introduces)


@dataclass(frozen=True, slots=True)
class TokenBudget:
    """An order-of-magnitude range, not an estimate with a point value.

    Carried as a range because the source is word counts rather than
    measurement, and a point value would imply a precision nobody has.
    """

    low: int
    high: int
    basis: str


@dataclass(frozen=True, slots=True)
class Schedule:
    level: int
    budget: TokenBudget
    domains: tuple[DomainPlan, ...] = ()
    covers: tuple[str, ...] = ()
    """Domains this level is scheduled for. A level may be partial."""

    notes: str = ""

    def plan_for(self, domain: str) -> DomainPlan | None:
        return next((d for d in self.domains if d.domain == domain), None)

    def all_teaches(self) -> frozenset[str]:
        return frozenset(c for d in self.domains for c in d.teaches())

    def all_introduces(self) -> frozenset[str]:
        return frozenset(c for d in self.domains for c in d.introduces())

    def shares(self) -> dict[str, float]:
        """Derived budget share per domain, by scheduled concept count.

        Derived rather than authored so there is no hand-maintained number
        to drift out of agreement with the units. Level one allocates by
        what must be grounded rather than by subject weighting, because the
        level seeds primitives that everything later presupposes.
        """
        counts = {
            d.domain: len(d.teaches()) + len(d.introduces()) for d in self.domains
        }
        total = sum(counts.values())
        if total == 0:
            return {k: 0.0 for k in counts}
        return {k: v / total for k, v in counts.items()}


def covered_relations(schedule: Schedule, graph: ConceptGraph) -> set[tuple[str, str]]:
    """Specialisation pairs a unit covers at both ends.

    A relation is taught by material that names the specific concept and the
    general one together. Which unit does so is what the schedule decides,
    and the corpus validator checks the same property over records.
    """
    out: set[tuple[str, str]] = set()
    for plan in schedule.domains:
        for unit in plan.units:
            names = {*unit.teaches, *unit.revisits, *unit.introduces}
            for specific in names:
                for general in graph.generalisations_of(specific):
                    if general in names:
                        out.add((specific, general))
    return out


def validate(
    schedule: Schedule,
    graph: ConceptGraph,
    primitives: Iterable[str],
    earlier: Mapping[str, int] | None = None,
) -> list[Violation]:
    """Return every breach. Empty means the schedule is sound.

    ``earlier`` maps a concept to the level it was scheduled at by a
    previous level's schedule. A prerequisite must be scheduled at this
    level or at an earlier one, which is the same rule the corpus validator
    applies to records, lifted from written records to the plan. Applying it
    here is what makes an ordering mistake cheap to find.
    """
    out: list[Violation] = []
    known = set(primitives)
    prior = dict(earlier or {})
    declared = set(graph.domains) or {
        n.domain for n in graph.nodes.values() if n.domain is not None
    }

    for domain in schedule.covers:
        if domain not in declared:
            out.append(
                Violation("unknown-domain", f"level covers undeclared {domain!r}")
            )
        if schedule.plan_for(domain) is None:
            out.append(
                Violation(
                    "missing-plan", f"domain {domain!r} is covered but has no plan"
                )
            )
    for plan in schedule.domains:
        if plan.domain not in schedule.covers:
            out.append(
                Violation(
                    "unscheduled-plan", f"plan for {plan.domain!r} is not in covers"
                )
            )

    seen: dict[str, str] = {}
    for plan in schedule.domains:
        for unit in plan.units:
            for concept in (*unit.teaches, *unit.introduces):
                if concept in seen:
                    out.append(
                        Violation(
                            "duplicate-schedule",
                            f"{concept!r} in {seen[concept]!r} and {unit.id!r}",
                        )
                    )
                seen[concept] = unit.id
            for concept in unit.teaches:
                node = graph.nodes.get(concept)
                if node is None:
                    out.append(
                        Violation(
                            "unknown-concept", f"{unit.id!r} teaches absent {concept!r}"
                        )
                    )
                elif node.domain != plan.domain:
                    out.append(
                        Violation(
                            "wrong-domain",
                            f"{unit.id!r} teaches {concept!r} of {node.domain!r}"
                            f" under {plan.domain!r}",
                        )
                    )
            for concept in unit.revisits:
                if concept not in graph.nodes:
                    out.append(
                        Violation(
                            "unknown-concept",
                            f"{unit.id!r} revisits absent {concept!r}",
                        )
                    )
                if concept in unit.teaches:
                    out.append(
                        Violation(
                            "revisits-own-concept",
                            f"{unit.id!r} revisits {concept!r}, which it also teaches",
                        )
                    )
            for concept in unit.introduces:
                if concept in graph.nodes:
                    out.append(
                        Violation(
                            "already-present",
                            f"{unit.id!r} introduces {concept!r}, already in the graph",
                        )
                    )
            for primitive in unit.primitives:
                if primitive not in known:
                    out.append(
                        Violation(
                            "unregistered-primitive",
                            f"{unit.id!r} cites unregistered primitive {primitive!r}",
                        )
                    )

    for plan in schedule.domains:
        for unit in plan.units:
            for concept in unit.revisits:
                if concept in seen or (
                    concept in prior and prior[concept] <= schedule.level
                ):
                    continue
                out.append(
                    Violation(
                        "revisit-unscheduled",
                        f"{unit.id!r} revisits {concept!r}, which is scheduled"
                        " neither here nor earlier",
                    )
                )
            for concept in unit.teaches:
                for need in sorted(graph.prerequisites_of(concept)):
                    if need in seen or graph.nodes[need].domain is None:
                        continue
                    if need in prior and prior[need] <= schedule.level:
                        continue
                    out.append(
                        Violation(
                            "prerequisite-unscheduled",
                            f"{concept!r} at level {schedule.level} needs {need!r},"
                            " which is scheduled neither here nor earlier",
                        )
                    )
    return out


def assignment(schedule: Schedule) -> dict[str, int]:
    """Concept to level, for feeding into the next level's validation."""
    return {
        c: schedule.level for c in schedule.all_teaches() | schedule.all_introduces()
    }


def _str_tuple(raw: object, where: str) -> tuple[str, ...]:
    if raw is None:
        return ()
    if not isinstance(raw, list):
        raise ValueError(f"{where}: expected a list")
    items = cast(list[object], raw)
    for index, item in enumerate(items):
        if not isinstance(item, str):
            raise ValueError(f"{where}[{index}]: expected a string")
    return tuple(cast(list[str], items))


def _require(fields: Mapping[object, object], key: str, where: str) -> str:
    value = fields.get(key)
    if not isinstance(value, str):
        raise ValueError(f"{where}.{key}: expected a string")
    return value


def from_json(payload: object) -> Schedule:
    """Build a schedule from parsed JSON, checking types at the boundary."""
    if not isinstance(payload, dict):
        raise ValueError("schedule payload must be a JSON object")
    body = cast(dict[object, object], payload)
    level = body.get("level")
    if not isinstance(level, int):
        raise ValueError("'level' must be an integer")

    raw_budget = body.get("token_budget")
    if not isinstance(raw_budget, dict):
        raise ValueError("'token_budget' must be an object")
    budget_fields = cast(dict[object, object], raw_budget)
    low, high = budget_fields.get("low"), budget_fields.get("high")
    if not isinstance(low, int) or not isinstance(high, int):
        raise ValueError("token_budget.low and .high must be integers")
    if low > high:
        raise ValueError("token_budget.low exceeds .high")
    budget = TokenBudget(low, high, _require(budget_fields, "basis", "token_budget"))

    raw_domains = body.get("domains")
    if not isinstance(raw_domains, list):
        raise ValueError("'domains' must be a list")
    plans: list[DomainPlan] = []
    for index, entry in enumerate(cast(list[object], raw_domains)):
        where = f"domains[{index}]"
        if not isinstance(entry, dict):
            raise ValueError(f"{where}: expected an object")
        fields = cast(dict[object, object], entry)
        raw_units = fields.get("units")
        if not isinstance(raw_units, list):
            raise ValueError(f"{where}.units must be a list")
        units: list[Unit] = []
        for unit_index, raw_unit in enumerate(cast(list[object], raw_units)):
            unit_where = f"{where}.units[{unit_index}]"
            if not isinstance(raw_unit, dict):
                raise ValueError(f"{unit_where}: expected an object")
            unit_fields = cast(dict[object, object], raw_unit)
            units.append(
                Unit(
                    id=_require(unit_fields, "id", unit_where),
                    form=_require(unit_fields, "form", unit_where),
                    teaches=_str_tuple(
                        unit_fields.get("teaches"), f"{unit_where}.teaches"
                    ),
                    introduces=_str_tuple(
                        unit_fields.get("introduces"), f"{unit_where}.introduces"
                    ),
                    revisits=_str_tuple(
                        unit_fields.get("revisits"), f"{unit_where}.revisits"
                    ),
                    primitives=_str_tuple(
                        unit_fields.get("primitives"), f"{unit_where}.primitives"
                    ),
                )
            )
        plans.append(DomainPlan(_require(fields, "domain", where), tuple(units)))

    notes = body.get("notes")
    return Schedule(
        level=level,
        budget=budget,
        domains=tuple(plans),
        covers=_str_tuple(body.get("covers"), "covers"),
        notes=notes if isinstance(notes, str) else "",
    )


def load(path: Path) -> Schedule:
    parsed: object = json.loads(path.read_text(encoding="utf-8"))
    return from_json(parsed)
