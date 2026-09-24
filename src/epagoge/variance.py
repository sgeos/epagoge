"""Variance pilot analysis.

Turns paired pilot observations into the numbers the pre-registration needs,
namely seed-to-seed variance, paired correlation, and the seed count the
ablation requires. Standard library only.

Specification in ``docs/spec/VARIANCE_PILOT.md``.

The central reason this module exists separately from the training harness is
that the statistics can be verified exactly, against closed-form cases, while
a training run cannot.
"""

from __future__ import annotations

import math
import random
from collections.abc import Sequence
from dataclasses import dataclass
from statistics import NormalDist, correlation, fmean, stdev, variance
from typing import Final

DEFAULT_ALPHA: Final[float] = 0.05
DEFAULT_POWER: Final[float] = 0.80
DEFAULT_BOOTSTRAP: Final[int] = 10_000
MIN_OBSERVATIONS: Final[int] = 2


@dataclass(frozen=True, slots=True)
class PairedObservation:
    """One pilot pair. Both runs share an initialisation and the same data.

    ``treatment`` and ``control`` differ only in ordering, which is what makes
    the pair a pair. A pilot may legitimately use two arbitrary orderings,
    since it measures the behaviour of the training setup rather than any
    property of the curriculum.
    """

    seed: int
    treatment: float
    control: float

    @property
    def difference(self) -> float:
        return self.treatment - self.control


@dataclass(frozen=True, slots=True)
class VarianceEstimate:
    """What the pilot measured."""

    n: int
    seed_sd: float
    """Pooled within-condition standard deviation. The sigma of an unpaired design."""

    paired_sd: float
    """Standard deviation of the within-pair difference. The sigma that matters here."""

    correlation: float
    """Pearson correlation between paired runs. Drives the gain from pairing."""

    mean_difference: float

    @property
    def pairing_gain(self) -> float:
        """Seed-count multiplier that pairing is worth, as a ratio of variances.

        Reported from the measured paired standard deviation rather than from
        the idealised ``1 / (1 - rho)``, because the identity behind that
        formula assumes equal variance in both conditions, which measurement
        need not respect.
        """
        if self.paired_sd == 0.0:
            return math.inf
        return 2.0 * (self.seed_sd**2) / (self.paired_sd**2)


def estimate(observations: Sequence[PairedObservation]) -> VarianceEstimate:
    """Compute the pilot estimates. Raises rather than guessing on too few pairs."""
    if len(observations) < MIN_OBSERVATIONS:
        raise ValueError(
            f"need at least {MIN_OBSERVATIONS} pairs, got {len(observations)}"
        )
    treatment = [o.treatment for o in observations]
    control = [o.control for o in observations]
    differences = [o.difference for o in observations]

    pooled = math.sqrt((variance(treatment) + variance(control)) / 2.0)
    try:
        rho = correlation(treatment, control)
    except (ValueError, ZeroDivisionError):
        # Undefined when either condition is constant across seeds. Reporting
        # zero would assert independence that was not observed.
        rho = math.nan

    return VarianceEstimate(
        n=len(observations),
        seed_sd=pooled,
        paired_sd=stdev(differences),
        correlation=rho,
        mean_difference=fmean(differences),
    )


def _z(alpha: float, power: float) -> float:
    if not 0.0 < alpha < 1.0:
        raise ValueError(f"alpha must lie in (0, 1), got {alpha}")
    if not 0.0 < power < 1.0:
        raise ValueError(f"power must lie in (0, 1), got {power}")
    normal = NormalDist()
    return normal.inv_cdf(1.0 - alpha / 2.0) + normal.inv_cdf(power)


def required_seeds(
    sigma: float,
    effect: float,
    *,
    paired: bool = True,
    alpha: float = DEFAULT_ALPHA,
    power: float = DEFAULT_POWER,
) -> int:
    """Seeds per condition needed to detect ``effect``, in the units of ``sigma``.

    For a paired design ``sigma`` is the standard deviation of the within-pair
    difference. For an unpaired design it is the within-condition standard
    deviation, and the unpaired requirement carries the familiar factor of two.
    """
    if effect <= 0.0:
        raise ValueError(f"effect must be positive, got {effect}")
    if sigma < 0.0:
        raise ValueError(f"sigma must be non-negative, got {sigma}")
    if sigma == 0.0:
        return 1
    factor = 1.0 if paired else 2.0
    return math.ceil(factor * ((_z(alpha, power) * sigma / effect) ** 2))


def detectable_effect(
    sigma: float,
    n: int,
    *,
    paired: bool = True,
    alpha: float = DEFAULT_ALPHA,
    power: float = DEFAULT_POWER,
) -> float:
    """Smallest effect detectable at ``n`` seeds per condition."""
    if n < 1:
        raise ValueError(f"n must be at least 1, got {n}")
    factor = 1.0 if paired else 2.0
    return _z(alpha, power) * sigma * math.sqrt(factor / n)


@dataclass(frozen=True, slots=True)
class SeedRequirement:
    """Required seeds, with the uncertainty that comes from a small pilot."""

    point: int
    """Computed from the point estimate of sigma."""

    conservative: int
    """Upper bootstrap percentile. This is the planning number."""

    percentile: float
    resamples: int

    @property
    def understatement(self) -> float:
        """How far the naive point estimate would have underplanned."""
        return self.conservative / self.point if self.point else math.inf


def bootstrap_required_seeds(
    observations: Sequence[PairedObservation],
    effect: float,
    *,
    percentile: float = 0.90,
    resamples: int = DEFAULT_BOOTSTRAP,
    alpha: float = DEFAULT_ALPHA,
    power: float = DEFAULT_POWER,
    rng: random.Random | None = None,
) -> SeedRequirement:
    """Required seeds with the uncertainty of the pilot's own sigma carried through.

    **Why this is not optional.** A pilot estimates sigma from few runs, and a
    point estimate understates it about half the time. Planning a study from
    that point estimate therefore underpowers it about half the time, which is
    exactly the failure the pilot exists to prevent.

    Resampling the observed differences makes no distributional assumption and
    reports how far the requirement moves under the pilot's own noise. The
    upper percentile is the number to plan with.
    """
    if not 0.5 < percentile < 1.0:
        raise ValueError(f"percentile must lie in (0.5, 1), got {percentile}")
    if resamples < 1:
        raise ValueError(f"resamples must be positive, got {resamples}")

    base = estimate(observations)
    point = required_seeds(
        base.paired_sd, effect, paired=True, alpha=alpha, power=power
    )

    # S311 twice in this module: the bootstrap must be reproducible from a
    # declared seed, which is the property a cryptographic generator lacks.
    draw = rng or random.Random(0)
    differences = [o.difference for o in observations]
    counts: list[int] = []
    for _ in range(resamples):
        # S311: reproducibility from a declared seed is the requirement here,
        # and is precisely what a cryptographic generator does not offer.
        sample = draw.choices(differences, k=len(differences))
        try:
            sigma = stdev(sample)
        except ValueError:
            continue
        counts.append(
            required_seeds(sigma, effect, paired=True, alpha=alpha, power=power)
        )

    counts.sort()
    index = min(len(counts) - 1, int(percentile * len(counts)))
    return SeedRequirement(
        point=point,
        conservative=counts[index] if counts else point,
        percentile=percentile,
        resamples=len(counts),
    )
