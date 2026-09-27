# Completion condition

**Ordering is explicitly not a completion criterion.** Any order satisfies
this, and so does any branch, any commit shape and any process. What counts
is the end state of the tree.

## Done when all of the following hold

**Displacement is measured and recorded for every arm and for each control
point**, so a reader can see which orderings preserve the sequence and which
do not.

**More than one measure of batch diversity is used**, and the record says
how well each fits the control curve and how much of the arm difference each
explains. The residual is reported under the metric that explains the most,
not the least.

**Mechanical confounds are checked rather than assumed**, including whether
the arms differ in how much padding their batches carry, with the figures
recorded.

**The paired difference between the two matched arms is pooled across every
run available**, and the record states how many paired observations it rests
on and how many point the same way.

**The record states what the residual is attributable to and what it is
not**, naming each alternative that was eliminated and how, and naming any
that survive.

**No curriculum verdict is claimed.** Reporting that an ordering property
tracks held-out loss after controls is in scope. Declaring the project's
hypothesis supported or refuted is not, because held-out loss is not the
property the project targets and the minimum meaningful effect is unchosen.

**Anything that would change if a further confound were found is marked as
such**, rather than presented as settled.

**Every figure says how many seeds or observations it rests on.**

**The gate passes.** `./tools/check.sh` reports all checks passed and exits
0, with no check weakened or removed to achieve it.

**Continuous integration is green** on the pushed head, checked rather than
assumed.

**The working tree is clean and pushed**, with no tracked evaluation
artifact holding the output of a probe rather than a recorded run.

**Nothing was added beyond what this question needs.**
