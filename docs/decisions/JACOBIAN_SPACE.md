# Jacobian-space as an architecture objective

**Decided 2026-09-23.** The architecture goal is to maintain healthy
reasoning ability by keeping Jacobian-space adequately unconstrained.

This supersedes an earlier version of this record, which treated the
Jacobian only as instrumentation on the ablation. That version also
contained an error, corrected below.

## Reading of the term

The parameter-to-function Jacobian and the geometry it induces through the
neural tangent kernel. "Adequately unconstrained" means the reachable
function space stays wide enough for reasoning, rather than being collapsed
by deployment-driven constraints.

## CORRECTION. A conflict was recorded as a convergence

The earlier version held that Jacobian awareness served two goals at once,
the ordering mechanism and weight-perturbation tolerance, and called that
convergence.

**It is a conflict.** Fault tolerance wants low sensitivity of the function
to parameter change. Reasoning wants that sensitivity to remain rich. These
are the same quantity pulled in opposite directions.

The verified literature supports the reasoning side against the earlier
framing. Sharpness is better understood as a function-dependent property
than as a reliable indicator of poor generalisation. Sharper minima can
reflect more appropriate inductive biases, particularly under
regularisation, and can coincide with better generalisation, calibration,
and robustness. Training toward flatness is not a free good, and here it
would purchase bit-flip tolerance with the capacity the model exists to
have.

## The objective is measurable, therefore enforceable

"Adequately unconstrained" requires a number or it is a slogan.

**Effective rank of the tangent kernel**, the square of the trace over the
squared Frobenius norm, counts how many eigenvalues are of the order of the
largest. It is described in the literature as a proxy for how wide the
reachable function space is. Full-rank kernels admit a wide variety of
learnable functions. Low-rank kernels limit what the model can express.
Published work uses tangent-kernel metrics to characterise trainability and
expressivity of candidate architectures, and recent work addresses scalable
estimation, which matters because the exact kernel is intractable at scale.

**The rule.** Declare an effective-rank floor. Measure it. Reject any
deployment constraint that pushes the model below it.

The floor value is not yet chosen and belongs in the pre-registration
alongside the effect size and seed count. Choosing it requires the first
measurements, so it is declared as a procedure now and a number later, and
that sequencing must be stated explicitly rather than allowed to become a
post-hoc choice.

## What constrains Jacobian-space, ranked

**Severe.**

- **Ternary quantisation.** Discretises the reachable function space. The
  capability-stratified degradation finding in `OPEN_QUESTIONS.md` item
  15b, where ternary models lose reasoning disproportionately to fluency,
  is direct evidence for this account rather than an unrelated curiosity.
- **Small parameter count.** Effective rank scales with width and the
  deployment envelope caps width.
- **Low-rank parameterisation.** Constrains the Jacobian to a low-rank
  subspace by construction. **Banned outright in the base model.**

**Moderate.**

- Flatness-seeking regularisation and heavy weight decay, which suppress
  the quantity directly.
- Bounded attention, which constrains which inputs may influence which
  outputs.
- Dense rather than mixture-of-experts. The rejection still stands on
  memory-inversion and control-flow grounds, but the cost is now visible.

**Negligible.** Static shapes, standard components.

## Fault tolerance is handled in hardware, not by flattening

Error-correcting codes on weight memory, periodic scrubbing against a
protected copy, and triplication of the small high-precision core already
identified, namely embeddings, normalisation, and the output head.

This is where the concentrate-the-fragility principle in
`MODEL_ARCHITECTURE_CONSTRAINTS.md` actually pays. It spends silicon rather
than capability. Given that flatness is not reliably beneficial in any
case, it is the better engineering answer independent of this objective.

## Positive program

- Width in preference to depth. This also matches the cache recommendation
  in `OPEN_QUESTIONS.md` item 15d, reached for unrelated reasons.
- Deliberate regime placement. How far a network leaves the static kernel
  regime depends on width and learning rate, so hyperparameters are part of
  the architecture objective rather than tuning.
- No low-rank parameterisation anywhere in the base model.
- No sharpness-aware minimisation. Moderate weight decay only.
- Quantisation as mild as deployment tolerates, strengthening four-bit over
  ternary.

## Instrumentation

Measured on runs already budgeted, against a probe set held fixed and
identical across conditions.

| Measure | Purpose |
| --- | --- |
| Tangent-kernel effective rank | The objective itself |
| Relative kernel change from initialisation | Regime position |
| Kernel-target alignment | Whether ordering shapes the kernel toward the task |
| Per-stage gradient cosine alignment | Transfer between curriculum stages, measured directly |
| Empirical weight-perturbation probe | Bit-flip tolerance, measured not assumed |

Subsampling and cheap estimators are assumed throughout. Estimator choice
belongs in the pre-registration.

## Consequences for decisions already recorded

**The quantisation pilot changes purpose.** Measuring effective rank across
the floating-point, four-bit, and ternary arms directly tests whether
ternary crosses the floor. That is a better question than the accuracy
comparison previously specified, and it is the same three runs.

**Open question eighteen acquires a mechanism.** Agentic reliability being
scale-dependent is no longer only an empirical pattern. Reasoning requires
Jacobian richness, richness scales with width, and the deployment envelope
caps width. The account predicts the ceiling rather than discovering it.

## Discipline retained from the earlier version

**Measurement, not intervention, in the primary arms.** Adding Jacobian
regularisation to training would introduce a second variable and confound
the pre-registered ablation. Regularisation, if wanted, is a separate arm
with its own declaration.

**Secondary measures are declared secondary.** They may generate a
hypothesis. They may not rescue an inconclusive primary result.

## The regime hypothesis, retained

Feature learning is the evolution of the tangent kernel during training,
and kernel alignment with the target is its structural signature. How far a
network moves from the static kernel regime depends on width, learning
rate, and task.

If ordering acts by shaping the kernel, it can only help in the
feature-learning regime, and regime position is scale-dependent. That
predicts the ordering effect varies across the three scale points in open
question five, and offers a mechanistic explanation for the inconsistency
of the published ordering literature.

## Sources consulted 2026-09-23

- The Spectral Dimension of NTKs is Constant, with scalable estimation,
  https://arxiv.org/html/2512.00860
- Characterizing Trainability, Expressivity and Generalization with
  Metrics from the Neural Tangent Kernel,
  https://link.springer.com/chapter/10.1007/978-3-032-04558-4_5
- Characterizing the Spectrum of the NTK via a Power Series Expansion,
  https://arxiv.org/pdf/2211.07844
- A Theory of Neural Tangent Kernel Alignment,
  https://arxiv.org/pdf/2105.14301
- A Function Centric Perspective on Flat and Sharp Minima,
  https://openreview.net/forum?id=BeLwO47iNn
- Sharp Minima Can Generalize For Deep Nets,
  https://www.researchgate.net/publication/315096447
- Provable Advantage of Curriculum Learning on Parity Targets,
  https://arxiv.org/pdf/2306.16921
