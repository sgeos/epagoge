# Pre-registration

**Status: INCOMPLETE. Opened 2026-09-23.**

**This document must be complete and committed before the first ablation
run.** Several decisions across the repository defer to it. Its purpose is
to fix every choice that could otherwise be adjusted after results are
seen, which is the only thing separating a falsifiable experiment from a
narratable one.

Items are marked **FIXED** where decided, or **PENDING** with the
dependency that unblocks them. A pending item is not a gap in the design.
It is a value that must be measured rather than chosen, and choosing it now
would be the error this document exists to prevent.

## 1. Hypothesis

**FIXED.** Difficulty-graded curriculum ordering improves pretraining
relative to an ordering that respects the same constraints but discards the
curriculum trajectory.

**Stated referent.** The seven levels bundle breadth, depth, abstraction,
and groundedness. Depth is named the primary axis so the claim has a
referent. The bundling is a documented confound, not a decomposed one.

## 2. Primary endpoint

**PENDING** the variance pilot. Final held-out loss is the default
candidate. The pilot measures its seed-to-seed variance and its paired
correlation, and a lower-variance endpoint may be substituted if one is
clearly better. The endpoint is fixed before any ablation run.

## 3. Conditions

**FIXED.**

| Condition | Ordering |
| --- | --- |
| Treatment | The curriculum trajectory across seven levels |
| Control | A random topological ordering, fresh per seed |

The control respects prerequisites while discarding the trajectory, so the
comparison is the curriculum against an arbitrary valid ordering rather
than against an invalid one. A free shuffle was rejected as close to a
tautology.

**Pairing.** Treatment and control share an initialisation and share the
data within a pair. Order is the only difference.

## 4. Domains

**FIXED.** Mathematics and failure analysis, each at full depth across all
seven levels.

Chosen to differ maximally in prerequisite depth, which is the hypothesised
mechanism. The strongest available outcome is a dissociation, since an
effect in the deep-structure domain with a null in the flat-structure one
would be evidence that prerequisite depth is the mechanism.

## 5. Scale points

**PROVISIONAL** pending the variance pilot. Roughly 100M, 300M, and 1B
parameters at Chinchilla-style token ratios. Allocation across points is
set by measured variance, and the one-billion arm is the obvious candidate
if the design must be trimmed, since it is the large majority of cost.

## 6. Seed count

**PENDING** the variance pilot, which measures seed variance and paired
correlation at the smallest scale for roughly seventy dollars of compute.

The unpaired five-seed design originally specified detected only effects of
1.77 standard deviations of seed variance, against a literature reporting
small effects. Pairing is worth between 1.4 and 10 times the seed count
depending on a correlation nobody has measured.

## 7. Minimum meaningful effect

**PENDING** the variance pilot. Must be stated in the pilot's measured
units and justified from the literature rather than chosen for
affordability.

## 8. Failure condition

**FIXED.** The project fails if the result is **inconclusive**, meaning the
observed difference falls within seed-to-seed variance.

A negative result is a deliverable. Learning that ordering does not help,
cleanly and with the control to demonstrate it, is a finding.

## 9. Secondary measures, and their status

**FIXED that they are secondary.** They may generate a hypothesis. They may
not rescue an inconclusive primary result.

- Tangent-kernel effective rank
- Relative kernel change from initialisation
- Kernel-target alignment
- Cross-domain gradient alignment
- Weight-perturbation sensitivity
- Anti-sycophancy baseline on the trained base models

**Correction procedure: PENDING.** Only the primary comparison is
inferential. Every secondary measure is descriptive and reported without a
significance claim. This is the default and is recorded here so that it
cannot be revisited after results are seen.

## 10. Estimator choices

**PENDING.** The exact tangent kernel is intractable at scale. Subsampling
scheme, probe-set size, and estimator must be fixed here before any run,
because an estimator chosen after seeing a curve is a choice about the
result.

The probe set is held fixed and identical across conditions.

## 11. Corpus acceptance

**PARTIALLY FIXED.**

- Residual error rate is measured by sampled expert audit and reported
  **per domain**, never aggregated. FIXED.
- The ceiling that admits a corpus to the experiment: **PENDING**. It
  cannot sensibly be chosen before the first audit establishes what rate is
  achievable.

## 12. Effective-rank floor

**PENDING** the first measurements. The floor is the quantity that decides
whether a deployment constraint is admissible. Choosing a number before any
graph or model exists would be arbitrary; the procedure is fixed now and
the number is fixed once measurable.

## 13. Quirk boundary

**FIXED.** Recorded so that quirk cannot absorb a negative result.

| Quirk, accepted | Failure, not accepted |
| --- | --- |
| Unusual register | Systematic factual error |
| Narrow stylistic range | Degenerate repetition |
| Odd idiom | Mode collapse |
| Gaps in cultural knowledge | Failure to parse real input |

## 14. Reproducibility

**FIXED.**

- Bitwise determinism is unavailable on graphics processing units under
  either candidate framework. The design does not rely on it.
- The ordering is emitted as an explicit versioned artifact before
  training, so order is exactly reproducible even where arithmetic is not.
- Every run records its seed, its ordering artifact hash, its corpus hash,
  and its concept-graph hash.

## What unblocks the pending items

| Item | Unblocked by |
| --- | --- |
| 2, 6, 7 | The variance pilot |
| 5 | The variance pilot, for allocation |
| 9 correction, 10 | Decision, once the endpoint is fixed |
| 11 ceiling | The first corpus audit |
| 12 | The first kernel measurements |

**The variance pilot is the single largest unblocker and depends on
nothing.** It measures run-to-run behaviour of the training setup, not the
curriculum, so it runs on any small corpus and is not waiting on the
concept graph or on corpus generation.
