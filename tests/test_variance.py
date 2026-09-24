"""Tests for the variance pilot analysis.

Two kinds of test. Closed-form cases, where the answer is known exactly, and
recovery cases, where synthetic data is generated with a known sigma and rho
and the estimator must find them.

Recovery testing matters here because an estimator that is merely
self-consistent can still be systematically wrong.
"""

from __future__ import annotations

import math
import random
import unittest

from epagoge.variance import (
    PairedObservation,
    bootstrap_required_seeds,
    detectable_effect,
    estimate,
    required_seeds,
)

Z_SUM = 1.959963985 + 0.841621234  # alpha 0.05 two-sided, power 0.80


def synthetic(
    n: int, sigma: float, rho: float, shift: float, seed: int
) -> list[PairedObservation]:
    """Paired draws with a known within-condition sigma and correlation."""
    rng = random.Random(seed)
    out: list[PairedObservation] = []
    for i in range(n):
        shared = rng.gauss(0.0, 1.0)
        a = rng.gauss(0.0, 1.0)
        b = rng.gauss(0.0, 1.0)
        mix = math.sqrt(max(rho, 0.0))
        rest = math.sqrt(max(1.0 - rho, 0.0))
        treatment = sigma * (mix * shared + rest * a) + shift
        control = sigma * (mix * shared + rest * b)
        out.append(PairedObservation(seed=i, treatment=treatment, control=control))
    return out


class TestClosedForm(unittest.TestCase):
    def test_required_seeds_matches_the_formula(self) -> None:
        for sigma, effect in ((1.0, 1.0), (2.0, 1.0), (1.0, 0.5), (0.05, 0.01)):
            expected = math.ceil((Z_SUM * sigma / effect) ** 2)
            self.assertEqual(required_seeds(sigma, effect), expected)

    def test_unpaired_needs_twice_as_many(self) -> None:
        self.assertEqual(
            required_seeds(1.0, 0.1, paired=False), 2 * required_seeds(1.0, 0.1)
        )

    def test_detectable_effect_round_trips(self) -> None:
        for sigma, effect in ((1.0, 0.3), (0.05, 0.01), (3.0, 2.0)):
            n = required_seeds(sigma, effect)
            self.assertLessEqual(detectable_effect(sigma, n), effect)

    def test_smaller_effects_need_more_seeds(self) -> None:
        counts = [required_seeds(1.0, e) for e in (1.0, 0.5, 0.25, 0.1)]
        self.assertEqual(counts, sorted(counts))

    def test_zero_variance_needs_one_seed(self) -> None:
        self.assertEqual(required_seeds(0.0, 0.1), 1)

    def test_non_positive_effect_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            required_seeds(1.0, 0.0)
        with self.assertRaises(ValueError):
            required_seeds(1.0, -1.0)

    def test_negative_sigma_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            required_seeds(-1.0, 1.0)

    def test_invalid_alpha_or_power_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            required_seeds(1.0, 1.0, alpha=0.0)
        with self.assertRaises(ValueError):
            required_seeds(1.0, 1.0, power=1.0)

    def test_detectable_effect_rejects_zero_seeds(self) -> None:
        with self.assertRaises(ValueError):
            detectable_effect(1.0, 0)


class TestRecovery(unittest.TestCase):
    def test_recovers_a_known_sigma(self) -> None:
        obs = synthetic(4000, sigma=2.0, rho=0.0, shift=0.0, seed=1)
        self.assertAlmostEqual(estimate(obs).seed_sd, 2.0, delta=0.1)

    def test_recovers_a_known_correlation(self) -> None:
        for rho in (0.0, 0.5, 0.9):
            obs = synthetic(4000, sigma=1.0, rho=rho, shift=0.0, seed=2)
            self.assertAlmostEqual(estimate(obs).correlation, rho, delta=0.05)

    def test_recovers_a_known_mean_difference(self) -> None:
        obs = synthetic(4000, sigma=1.0, rho=0.5, shift=0.25, seed=3)
        self.assertAlmostEqual(estimate(obs).mean_difference, 0.25, delta=0.05)

    def test_pairing_gain_tracks_correlation(self) -> None:
        # The identity is gain = 1/(1-rho) under equal variances.
        for rho, expected in ((0.0, 1.0), (0.5, 2.0), (0.8, 5.0)):
            obs = synthetic(4000, sigma=1.0, rho=rho, shift=0.0, seed=4)
            self.assertAlmostEqual(
                estimate(obs).pairing_gain, expected, delta=0.15 * expected
            )

    def test_higher_correlation_lowers_the_paired_sigma(self) -> None:
        low = estimate(synthetic(2000, 1.0, 0.1, 0.0, 5)).paired_sd
        high = estimate(synthetic(2000, 1.0, 0.9, 0.0, 5)).paired_sd
        self.assertLess(high, low)


class TestEstimateGuards(unittest.TestCase):
    def test_one_pair_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            estimate([PairedObservation(0, 1.0, 2.0)])

    def test_constant_condition_yields_undefined_correlation(self) -> None:
        obs = [PairedObservation(i, 1.0, float(i)) for i in range(5)]
        self.assertTrue(math.isnan(estimate(obs).correlation))

    def test_identical_pairs_give_zero_paired_sigma(self) -> None:
        obs = [PairedObservation(i, float(i), float(i)) for i in range(5)]
        est = estimate(obs)
        self.assertEqual(est.paired_sd, 0.0)
        self.assertTrue(math.isinf(est.pairing_gain))


class TestBootstrap(unittest.TestCase):
    def observations(self) -> list[PairedObservation]:
        return synthetic(8, sigma=1.0, rho=0.7, shift=0.0, seed=9)

    def test_conservative_estimate_exceeds_the_point_estimate(self) -> None:
        req = bootstrap_required_seeds(
            self.observations(), effect=0.5, resamples=2000, rng=random.Random(1)
        )
        self.assertGreaterEqual(req.conservative, req.point)
        self.assertGreater(req.understatement, 1.0)

    def test_result_is_reproducible_from_a_seed(self) -> None:
        obs = self.observations()
        a = bootstrap_required_seeds(obs, 0.5, resamples=500, rng=random.Random(3))
        b = bootstrap_required_seeds(obs, 0.5, resamples=500, rng=random.Random(3))
        self.assertEqual(a.conservative, b.conservative)

    def test_a_larger_pilot_narrows_the_gap(self) -> None:
        small = bootstrap_required_seeds(
            synthetic(6, 1.0, 0.7, 0.0, 11), 0.5, resamples=3000, rng=random.Random(2)
        )
        large = bootstrap_required_seeds(
            synthetic(60, 1.0, 0.7, 0.0, 11), 0.5, resamples=3000, rng=random.Random(2)
        )
        self.assertLess(large.understatement, small.understatement)

    def test_invalid_percentile_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            bootstrap_required_seeds(self.observations(), 0.5, percentile=0.4)

    def test_invalid_resample_count_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            bootstrap_required_seeds(self.observations(), 0.5, resamples=0)


if __name__ == "__main__":
    unittest.main()
