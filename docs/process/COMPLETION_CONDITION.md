# Completion condition

**Ordering is explicitly not a completion criterion.** Any order satisfies
this, and so does any branch, any commit shape and any process. What counts
is the end state of the tree.

## Done when all of the following hold

**Variance has been re-measured on the current corpus at more than one
endpoint.** A record under `evals/pilot/` carries, for each endpoint, the
seed-to-seed standard deviation, the paired standard deviation, the
correlation between arms, and the number of paired observations each rests
on.

**The cost of each endpoint is stated as seed counts.** For each endpoint
measured, the record gives the paired and unpaired seeds required to detect
at least two different target effect sizes.

**No ordering verdict appears anywhere.** Nothing added in this work states
or implies which arm won, because the endpoint that would fix the sign is
unchosen and belongs to the operator. Reporting spread, correlation and
seed counts is in scope; reporting which arm was better is not.

**Item 6 of `evals/PRE_REGISTRATION.md` carries the current figures and is
still marked provisional**, with the reasons it remains so named
explicitly: the endpoint is unchosen, and the adopted optimiser and
schedule are not implemented.

**`evals/pilot/LEVEL_ONE_VARIANCE.md` no longer presents superseded figures
as current**, and a reader meets the current measurement or a pointer to it
before any older number.

**Whether pairing still pays is stated as a measured claim**, with the
current gain given rather than the older one repeated.

**Every figure presented says how many seeds it rests on**, and anything
resting on fewer observations than the estimator's own minimum is labelled
as such rather than presented as an estimate.

**The gate passes.** `./tools/check.sh` reports all checks passed and exits
0, with no check weakened or removed to achieve it.

**Continuous integration is green** on the pushed head, checked rather than
assumed.

**The working tree is clean and pushed**, with no tracked evaluation
artifact holding the output of a probe rather than a recorded run.

**No new capability was added** beyond what is needed to take these
measurements. A new option, token, generator, or training objective is
outside this condition.
