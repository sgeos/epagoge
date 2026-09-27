# Completion condition

**Ordering is explicitly not a completion criterion.** Any order satisfies
this, and so does any branch, any commit shape and any process. What counts
is the end state of the tree.

## Done when all of the following hold

**Batch homogeneity is measured from the real chunk assignment**, not from
a proxy for it, and a record says so.

**The earlier homogeneity figures, which came from a wrong proxy, are
corrected everywhere they appear**, with the correction visible rather than
silently substituted, and with a statement of what the error did and did not
change.

**A curve of held-out loss against batch homogeneity exists**, measured at
three or more block sizes with the curriculum sequence held fixed, recorded
with the seed count per point.

**Each block size is recorded with both quantities it affects**: how
homogeneous batches become, and how far books move from their curriculum
position. A reader can see which block sizes are controls and which are not.

**The record states where the shuffled arm falls relative to that curve**,
and therefore what the residual is attributable to, or states plainly that
the design cannot tell.

**Any extrapolation beyond the measured range is labelled as one.** If the
shuffled arm's homogeneity lies outside the range the curriculum arm covers,
the record says so where the conclusion is drawn.

**No curriculum effect is claimed as established.** Reporting what the
residual is attributable to is in scope. Declaring that ordering helps or
harms is not.

**Every figure says how many seeds it rests on.**

**The gate passes.** `./tools/check.sh` reports all checks passed and exits
0, with no check weakened or removed to achieve it.

**Continuous integration is green** on the pushed head, checked rather than
assumed.

**The working tree is clean and pushed**, with no tracked evaluation
artifact holding the output of a probe rather than a recorded run.

**Nothing was added beyond what this question needs.**
