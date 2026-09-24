"""Tests for review and audit.

The interval arithmetic is checked against known values, because an audit
that reports a rate without a correct interval overstates what was learned,
which is the failure this module exists to prevent.
"""

from __future__ import annotations

import math
import tempfile
import unittest
from pathlib import Path

from epagoge.concept_graph import ConceptGraph, Node, NodeKind
from epagoge.record import ClaimClass, Provenance, Record
from epagoge.review import (
    ErrorRate,
    Judgment,
    Verdict,
    append_verdict,
    domain_of,
    error_rates,
    load_verdicts,
    take_sample,
    wilson_interval,
)


def graph() -> ConceptGraph:
    return ConceptGraph(
        [
            Node("m1", "m1", NodeKind.DOMAIN_CONCEPT, "mathematics"),
            Node("m2", "m2", NodeKind.DOMAIN_CONCEPT, "mathematics"),
            Node("f1", "f1", NodeKind.DOMAIN_CONCEPT, "failure_analysis"),
        ],
        {},
        {},
    )


def rec(record_id: str, concepts: tuple[str, ...] = ("m1",)) -> Record:
    return Record(
        id=record_id,
        level=1,
        concepts=concepts,
        claim_class=ClaimClass.EMPIRICAL,
        content="text",
        provenance=Provenance(source_claim="s"),
    )


class TestWilson(unittest.TestCase):
    def test_zero_rejections_still_bounds_above_zero(self) -> None:
        low, high = wilson_interval(0, 30)
        # Exactly zero in exact arithmetic; floating point leaves a residue
        # around 1e-18, which is why this is not an equality assertion.
        self.assertAlmostEqual(low, 0.0, places=12)
        self.assertAlmostEqual(high, 0.1135, delta=0.002)

    def test_a_small_audit_gives_a_wide_interval(self) -> None:
        low, high = wilson_interval(3, 30)
        self.assertAlmostEqual(low, 0.0346, delta=0.002)
        self.assertAlmostEqual(high, 0.2562, delta=0.002)
        self.assertGreater(high - low, 0.2, "10% from 30 records is not a measurement")

    def test_more_evidence_narrows_the_interval(self) -> None:
        narrow = wilson_interval(10, 1000)
        wide = wilson_interval(1, 100)
        self.assertLess(narrow[1] - narrow[0], wide[1] - wide[0])

    def test_interval_never_leaves_the_unit_range(self) -> None:
        for successes, trials in ((0, 5), (5, 5), (1, 3), (0, 1)):
            low, high = wilson_interval(successes, trials)
            self.assertGreaterEqual(low, 0.0)
            self.assertLessEqual(high, 1.0)

    def test_no_trials_yields_total_ignorance(self) -> None:
        self.assertEqual(wilson_interval(0, 0), (0.0, 1.0))

    def test_impossible_counts_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            wilson_interval(5, 3)
        with self.assertRaises(ValueError):
            wilson_interval(-1, 3)

    def test_invalid_confidence_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            wilson_interval(1, 10, confidence=1.0)


class TestDomainAttribution(unittest.TestCase):
    def test_a_single_domain_record_is_attributed(self) -> None:
        self.assertEqual(domain_of(rec("a", ("m1", "m2")), graph()), "mathematics")

    def test_a_spanning_record_is_reported_as_mixed(self) -> None:
        self.assertEqual(domain_of(rec("a", ("m1", "f1")), graph()), "mixed")

    def test_unknown_concepts_do_not_attribute(self) -> None:
        self.assertEqual(domain_of(rec("a", ("ghost",)), graph()), "mixed")


class TestRates(unittest.TestCase):
    def verdicts(self) -> list[Verdict]:
        return [
            Verdict("a", Judgment.ACCEPT, "", "t", "now"),
            Verdict("b", Judgment.REJECT, "wrong", "t", "now"),
            Verdict("c", Judgment.FLAG, "unsure", "t", "now"),
            Verdict("d", Judgment.ACCEPT, "", "t", "now"),
        ]

    def records(self) -> list[Record]:
        return [rec("a"), rec("b"), rec("c"), rec("d", ("f1",))]

    def test_rates_are_split_by_domain(self) -> None:
        rates = {
            r.domain: r for r in error_rates(self.verdicts(), self.records(), graph())
        }
        self.assertEqual(set(rates), {"mathematics", "failure_analysis"})
        self.assertEqual(rates["mathematics"].reviewed, 3)
        self.assertEqual(rates["mathematics"].rejected, 1)
        self.assertEqual(rates["mathematics"].flagged, 1)

    def test_flags_are_counted_separately_never_as_either(self) -> None:
        rates = {
            r.domain: r for r in error_rates(self.verdicts(), self.records(), graph())
        }
        maths = rates["mathematics"]
        self.assertEqual(maths.rejected + maths.flagged + 1, maths.reviewed)

    def test_verdicts_for_unknown_records_are_ignored(self) -> None:
        stray = [Verdict("ghost", Judgment.REJECT, "", "t", "now")]
        self.assertEqual(error_rates(stray, self.records(), graph()), [])

    def test_rate_of_an_empty_audit_is_not_a_number(self) -> None:
        self.assertTrue(math.isnan(ErrorRate("m", 0, 0, 0).rate))


class TestSampling(unittest.TestCase):
    def population(self) -> list[Record]:
        return [rec(f"r{i:03d}") for i in range(100)]

    def test_sampling_is_reproducible_from_a_seed(self) -> None:
        a = [r.id for r in take_sample(self.population(), 10, seed=4)]
        b = [r.id for r in take_sample(self.population(), 10, seed=4)]
        self.assertEqual(a, b)

    def test_different_seeds_give_different_samples(self) -> None:
        a = [r.id for r in take_sample(self.population(), 10, seed=1)]
        b = [r.id for r in take_sample(self.population(), 10, seed=2)]
        self.assertNotEqual(a, b)

    def test_already_reviewed_records_are_excluded(self) -> None:
        seen = {f"r{i:03d}" for i in range(90)}
        sample = take_sample(self.population(), 10, seed=1, exclude=seen)
        self.assertTrue(all(r.id not in seen for r in sample))

    def test_asking_for_more_than_exists_returns_everything_available(self) -> None:
        self.assertEqual(len(take_sample(self.population(), 500, seed=1)), 100)

    def test_a_non_positive_sample_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            take_sample(self.population(), 0, seed=1)


class TestPersistence(unittest.TestCase):
    def setUp(self) -> None:
        self._dir = tempfile.TemporaryDirectory()
        self.addCleanup(self._dir.cleanup)
        self.path = Path(self._dir.name) / "verdicts.jsonl"

    def test_absent_file_reads_as_no_verdicts(self) -> None:
        self.assertEqual(load_verdicts(self.path), [])

    def test_verdicts_round_trip(self) -> None:
        original = Verdict.now("r1", Judgment.REJECT, "a reason", "reviewer")
        append_verdict(self.path, original)
        loaded = load_verdicts(self.path)
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0].record_id, "r1")
        self.assertEqual(loaded[0].judgment, Judgment.REJECT)
        self.assertEqual(loaded[0].reason, "a reason")

    def test_verdicts_append_rather_than_replace(self) -> None:
        append_verdict(self.path, Verdict.now("r1", Judgment.ACCEPT, "", "t"))
        append_verdict(self.path, Verdict.now("r2", Judgment.REJECT, "no", "t"))
        self.assertEqual(len(load_verdicts(self.path)), 2)

    def test_a_timestamp_is_recorded(self) -> None:
        self.assertTrue(Verdict.now("r", Judgment.ACCEPT, "", "t").at)

    def test_a_malformed_verdict_line_raises(self) -> None:
        self.path.write_text('["not", "an", "object"]\n', encoding="utf-8")
        with self.assertRaises(ValueError):
            load_verdicts(self.path)


if __name__ == "__main__":
    unittest.main()
