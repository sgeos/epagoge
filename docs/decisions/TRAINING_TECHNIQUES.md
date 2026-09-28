# Training techniques

**Decided 2026-09-24.** What to adopt from current practice, and why.

## Adopted

### Maximal update parametrization. Mandatory, and not for efficiency

μP specifies weight initialisation and learning-rate scaling such that
hyperparameters tuned on a small model remain optimal on a large one.

It is normally adopted for convenience. **Here it removes a confound in the
project's central claim.**

Without μP the three scale points in open question five have different
optimal hyperparameters. Training 100M, 300M, and 1B with one learning rate
leaves at least two mis-tuned, and **any observed scale-dependence in the
ordering effect could then be an artifact of mis-tuning rather than a
property of scale.**

That lands directly on the mechanism in `JACOBIAN_SPACE.md`, which holds
that curriculum effects appear only in the feature-learning regime and that
regime position depends on **width and learning rate**. Without μP the
learning rate does not scale correctly with width, confounding exactly the
variable the hypothesis concerns.

μP is therefore what makes the three-scale design interpretable, not an
optimisation on top of it.

### Amended 2026-09-28. The reason above is superseded and the adoption stands

**The justification above rests on the three scale points, and item 5 dropped
them.** `../../evals/PRE_REGISTRATION.md` item 5 was decided on 2026-09-27 as
a single scale point, with rescaling as a fallback if scale-dependence is ever
wanted. **With one scale point there is no cross-scale confound to remove**,
so the sentence above is no longer a reason for anything.

**The superseded text is kept in place** rather than edited away, because the
reason it gives was the reason at the time.

**This is the shape of the item 10 finding.** A claim inherited from an
earlier plan, still standing after a later decision removed its premise,
because nobody propagated the change. That is now twice.

**But the adoption survives, for a confound that is live inside one scale
point.** μP's statement is that the optimal learning rate scales with width.
**No tool in this repository exposes the learning rate.** Every run it has
ever done used the trainer's default of 3e-4, across widths 16 to 1,024.

**So the width sweep held fixed the one hyperparameter μP says must move with
width**, and it produced a published conclusion:
`../../evals/pilot/LEVEL_ONE_CAPACITY.md` reports width 1,024 reaching 4.525
and the later re-measurement withdrew the width ranking. **Whether width 1,024
is worse, or is merely mis-tuned at a rate chosen for a model a fourth its
width, is not separable from the runs that exist.**

**That is precisely the confound μP was adopted to remove**, appearing within
a single scale point rather than across three. The original reason is gone and
a better one is in the tree.

**What follows, and none of it is done.** The learning rate needs to be
reachable before μP can be implemented or the confound measured, and the width
ranking should be treated as provisional until it is. **Neither is claimed
here and neither was run.** μP remains adopted and unimplemented, now with a
reason that this corpus supports.

### Muon optimiser

Reported to expand the Pareto frontier over AdamW on the compute-time
tradeoff, and to retain data efficiency at large batch sizes well beyond the
critical batch size. Work exists on making Muon principled under μP
specifically, so the combination is studied rather than improvised.

### Warmup-stable-decay schedule

Replaces the cosine decay in the pilot harness. It is what recent
small-model pretraining protocols use, and the stable phase can be extended
with decay applied later, so a run can be lengthened without restarting.
That suits a project whose compute budget is not fixed.

### Multi-token prediction

A training-objective change that improves data efficiency, with the extra
heads discarded at inference or reused for speculative decoding. Costs
nothing at deployment. Directly useful to a project that is token-limited
by open question twenty.

### FP8 mixed precision, when the hardware supports it

Reported to roughly halve training cost, validated at scales comparable to
a small dense model over about a trillion tokens, so it is not purely a
frontier technique. It carries a brittleness risk and needs capable
accelerators, so it does nothing locally and applies when the ablation
moves to rented hardware.

## Considered and not adopted

### Multi-head latent attention. Check, do not assume

Compresses keys and values by low-rank joint projection, substantially
reducing cache size.

**`JACOBIAN_SPACE.md` bans low-rank parameterisation in the base model
outright**, because it constrains the Jacobian to a low-rank subspace by
construction. MLA compresses the attention representation rather than the
parameter-to-function map, so it is not obviously the same object, but it
is close enough that it **must be measured against the effective-rank floor
rather than adopted on its efficiency merits.**

### Mixture of experts. Closed

Rejected on two independent grounds in `../architecture/MODEL_ARCHITECTURE.md`.
Its bargain spends memory to buy compute, inverting the deployment's binding
constraint, and routing is data-dependent control flow.

## Perspective worth keeping

At one hundred million to one billion parameters on a single node, most
published efficiency work targets problems this project does not have. The
large savings come from multi-node communication and memory pressure at
frontier scale.

**The variance pilot already found a larger lever than anything here.**
Pairing was worth twenty times the seeds at no cost, which dwarfs a fifty
percent arithmetic saving.

## Consequence for the pilot

The pilot measured variance under AdamW with cosine decay. **Changing the
optimiser and schedule changes the training dynamics, so sigma and rho do
not carry over and must be re-measured** under μP with Muon and WSD before
the seed count is fixed. The harness exists and the pilot is cheap, so this
is a small cost, but the numbers are not transferable as they stand.

## A caveat on a widely quoted figure

The training cost most often cited for a recent large open model was the
final run's accelerator rental, excluding research, failed runs, data
acquisition, infrastructure, and people. It is not a total cost and should
not be used to estimate one.
