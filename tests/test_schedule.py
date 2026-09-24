"""Tests for the curriculum schedule.

Weighted toward negative cases, matching the concept graph tests. The
schedule's whole value is catching an ordering or coverage mistake before
generation rather than after, so every rule has a case that breaks it.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from epagoge import schedule as sched
from epagoge.concept_graph import ConceptGraph, Domain, Node, NodeKind

PRIMITIVES = ["p-one", "p-two"]


def concept(node_id: str, domain: str) -> Node:
    return Node(id=node_id, name=node_id, kind=NodeKind.DOMAIN_CONCEPT, domain=domain)


def graph() -> ConceptGraph:
    return ConceptGraph(
        [concept("a", "one"), concept("b", "one"), concept("x", "two")],
        {"b": ["a"]},
        {},
        domains=[Domain("one", "n"), Domain("two", "n")],
    )


def plan(**over: object) -> sched.Schedule:
    base: dict[str, object] = {
        "level": 1,
        "budget": sched.TokenBudget(10, 100, "test"),
        "covers": ("one",),
        "domains": (
            sched.DomainPlan("one", (sched.Unit("u1", "form", teaches=("a", "b")),)),
        ),
    }
    base.update(over)
    return sched.Schedule(**base)  # pyright: ignore[reportArgumentType]


def codes(s: sched.Schedule, earlier: dict[str, int] | None = None) -> set[str]:
    return {v.code for v in sched.validate(s, graph(), PRIMITIVES, earlier)}


class TestSound(unittest.TestCase):
    def test_a_sound_schedule_has_no_violations(self) -> None:
        self.assertEqual(sched.validate(plan(), graph(), PRIMITIVES), [])

    def test_assignment_maps_every_scheduled_concept_to_the_level(self) -> None:
        s = plan(
            domains=(
                sched.DomainPlan(
                    "one", (sched.Unit("u1", "f", teaches=("a",), introduces=("new",)),)
                ),
            )
        )
        self.assertEqual(sched.assignment(s), {"a": 1, "new": 1})


class TestConceptRules(unittest.TestCase):
    def test_teaching_an_absent_concept_is_a_violation(self) -> None:
        s = plan(
            domains=(
                sched.DomainPlan("one", (sched.Unit("u", "f", teaches=("ghost",)),)),
            )
        )
        self.assertIn("unknown-concept", codes(s))

    def test_introducing_a_present_concept_is_a_violation(self) -> None:
        """If it is already in the graph it is taught, not introduced."""
        s = plan(
            domains=(
                sched.DomainPlan("one", (sched.Unit("u", "f", introduces=("a",)),)),
            )
        )
        self.assertIn("already-present", codes(s))

    def test_teaching_a_concept_of_another_domain_is_a_violation(self) -> None:
        s = plan(
            domains=(sched.DomainPlan("one", (sched.Unit("u", "f", teaches=("x",)),)),)
        )
        self.assertIn("wrong-domain", codes(s))

    def test_scheduling_a_concept_twice_is_a_violation(self) -> None:
        s = plan(
            domains=(
                sched.DomainPlan(
                    "one",
                    (
                        sched.Unit("u1", "f", teaches=("a",)),
                        sched.Unit("u2", "f", teaches=("a",)),
                    ),
                ),
            )
        )
        self.assertIn("duplicate-schedule", codes(s))

    def test_an_unregistered_primitive_is_a_violation(self) -> None:
        s = plan(
            domains=(
                sched.DomainPlan(
                    "one",
                    (sched.Unit("u", "f", teaches=("a",), primitives=("p-nope",)),),
                ),
            )
        )
        self.assertIn("unregistered-primitive", codes(s))


class TestPrerequisiteRules(unittest.TestCase):
    def test_a_prerequisite_scheduled_nowhere_is_a_violation(self) -> None:
        s = plan(
            domains=(sched.DomainPlan("one", (sched.Unit("u", "f", teaches=("b",)),)),)
        )
        self.assertIn("prerequisite-unscheduled", codes(s))

    def test_a_prerequisite_scheduled_at_an_earlier_level_is_accepted(self) -> None:
        s = plan(
            level=2,
            domains=(sched.DomainPlan("one", (sched.Unit("u", "f", teaches=("b",)),)),),
        )
        self.assertEqual(codes(s, {"a": 1}), set())

    def test_a_prerequisite_scheduled_at_a_later_level_is_still_a_violation(
        self,
    ) -> None:
        """Earlier means earlier. A forward reference is the bug this catches."""
        s = plan(
            domains=(sched.DomainPlan("one", (sched.Unit("u", "f", teaches=("b",)),)),)
        )
        self.assertIn("prerequisite-unscheduled", codes(s, {"a": 5}))

    def test_a_prerequisite_in_the_same_level_is_accepted(self) -> None:
        self.assertEqual(codes(plan()), set())


class TestCoverage(unittest.TestCase):
    def test_covering_an_undeclared_domain_is_a_violation(self) -> None:
        self.assertIn("unknown-domain", codes(plan(covers=("ghost", "one"))))

    def test_covering_a_domain_with_no_plan_is_a_violation(self) -> None:
        self.assertIn("missing-plan", codes(plan(covers=("one", "two"))))

    def test_a_plan_for_an_uncovered_domain_is_a_violation(self) -> None:
        self.assertIn("unscheduled-plan", codes(plan(covers=())))


class TestShares(unittest.TestCase):
    def test_shares_are_derived_from_scheduled_concept_count(self) -> None:
        s = plan(
            covers=("one", "two"),
            domains=(
                sched.DomainPlan("one", (sched.Unit("u1", "f", teaches=("a", "b")),)),
                sched.DomainPlan("two", (sched.Unit("u2", "f", teaches=("x",)),)),
            ),
        )
        self.assertAlmostEqual(s.shares()["one"], 2 / 3)
        self.assertAlmostEqual(s.shares()["two"], 1 / 3)

    def test_an_empty_schedule_reports_zero_rather_than_dividing_by_zero(self) -> None:
        s = plan(covers=("one",), domains=(sched.DomainPlan("one", ()),))
        self.assertEqual(s.shares(), {"one": 0.0})

    def test_plan_for_returns_none_for_an_absent_domain(self) -> None:
        self.assertIsNone(plan().plan_for("absent"))


class TestParsing(unittest.TestCase):
    def payload(self, **over: object) -> dict[str, object]:
        base: dict[str, object] = {
            "level": 1,
            "token_budget": {"low": 10, "high": 100, "basis": "b"},
            "covers": ["one"],
            "domains": [
                {"domain": "one", "units": [{"id": "u", "form": "f", "teaches": ["a"]}]}
            ],
        }
        base.update(over)
        return base

    def test_a_well_formed_payload_round_trips(self) -> None:
        s = sched.from_json(self.payload())
        self.assertEqual(s.level, 1)
        self.assertEqual(s.budget.basis, "b")
        self.assertEqual(s.domains[0].units[0].teaches, ("a",))
        self.assertEqual(s.notes, "")

    def test_load_reads_a_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "level.json"
            path.write_text(json.dumps(self.payload()), encoding="utf-8")
            self.assertEqual(sched.load(path).level, 1)

    def altered(self, key: str, value: object) -> dict[str, object]:
        """Build a payload with one field replaced.

        Done positionally rather than by keyword because a keyword argument
        named for a budget field trips the hardcoded-secret lint rule, and a
        suppression comment would be a worse answer than not tripping it.
        """
        body = self.payload()
        body[key] = value
        return body

    def test_malformed_payloads_are_rejected_at_the_boundary(self) -> None:
        bad: list[object] = [
            "not an object",
            self.altered("level", "1"),
            self.altered("token_budget", "wide"),
            self.altered("token_budget", {"low": 100, "high": 10, "basis": "b"}),
            self.altered("token_budget", {"low": 1, "high": 2}),
            self.altered("token_budget", {"low": "1", "high": 2, "basis": "b"}),
            self.altered("domains", "one"),
            self.altered("domains", ["one"]),
            self.altered("domains", [{"domain": "one"}]),
            self.altered("domains", [{"domain": "one", "units": "u"}]),
            self.altered("domains", [{"domain": "one", "units": ["u"]}]),
            self.altered("domains", [{"domain": "one", "units": [{"form": "f"}]}]),
            self.altered("covers", "one"),
            self.altered("covers", [1]),
        ]
        for payload in bad:
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                sched.from_json(payload)
