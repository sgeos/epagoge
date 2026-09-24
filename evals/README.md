# evals/

Evaluation suites. A curriculum that cannot be evaluated by its own stated
standard has not met that standard.

**Status.** Empty. No suite has been written.

## The pre-registration

`PRE_REGISTRATION.md` is the document that fixes every choice which could
otherwise be adjusted after results are seen. **It is incomplete and must
be complete before the first ablation run.** Items are marked fixed or
pending with the dependency that unblocks them.

## Required before any training run

A falsification criterion. The project must state in advance what measured
outcome would count as failure. Without that fixed beforehand, any result
can be narrated as a success after the fact, which is the failure mode this
project exists to avoid.

## Contents

- `elenchos/` holds the anti-sycophancy and calibration probes.
- Capability and knowledge benchmarks belong here as they are adopted.
- The flat-order control comparison belongs here, since the ordering
  hypothesis is the project's central claim and the control is what makes
  it falsifiable.

## Decontamination

Any benchmark used for evaluation must be excluded from the corpus. The
corpus is synthetic, which reduces but does not eliminate the risk, because
a teacher model may reproduce benchmark items from its own training.
Decontamination is a required pass, not an optional one.

## Seed variance is a precondition, not a refinement

Verified 2026-09-23. Neither PyTorch nor JAX offers bitwise determinism on
graphics processing units. Levanter's guarantee is scoped to Tensor
Processing Units, and PyTorch states that complete reproducibility is not
guaranteed across releases, commits, or platforms.

The consequence for this project is direct. The ordering ablation cannot be
settled by comparing one curriculum-ordered run against one flat-order run,
because an observed difference smaller than seed-to-seed variance carries
no information. The published ordering literature reports small and
inconsistent effects, so a small observed difference is the expected case
rather than the unlikely one.

What this requires.

- Multiple seeds per condition, with the count fixed before the runs.
- Reported variance, not point estimates.
- A meaningful-effect threshold declared in advance, so that a result
  cannot be reinterpreted as a success after it is seen.

Neither the seed count nor the threshold has been chosen. See
`../docs/decisions/OPEN_QUESTIONS.md` item eleven.
