# Completion condition

**Ordering is explicitly not a completion criterion.** Any order satisfies
this, and so does any branch, any commit shape and any process. What counts
is the end state of the tree.

## Done when all of the following hold

**Batch composition under each arm is measured and recorded**, not asserted.
A record states, per arm, how homogeneous a training batch is under some
stated measure, and says how many batches the figure rests on.

**A control exists that preserves the curriculum sequence while changing
batch composition**, and the record states how far it moves each of those
two quantities, so a reader can see it is a control and not a second
shuffled arm.

**That control has been trained and compared against the uncontrolled
baseline** at the same endpoint and the same number of seeds, and the
comparison is recorded with the per-arm means and the seed count.

**The record states which mechanism the result supports**, in the form of
what the arm difference is attributable to, and says plainly if the answer
is that the two cannot be separated by this experiment.

**Every ordering figure this harness has produced is marked with whether it
survives the answer.** If the arm difference turns out to be attributable to
batch composition, any record presenting an ordering effect says so before
its numbers.

**No ordering verdict is presented as settled.** Reporting which mechanism
explains the arm difference is in scope. Declaring which ordering is better
for the curriculum hypothesis is not, because the endpoint and the minimum
effect are unchosen and belong to the operator.

**Every figure says how many seeds it rests on.**

**The gate passes.** `./tools/check.sh` reports all checks passed and exits
0, with no check weakened or removed to achieve it.

**Continuous integration is green** on the pushed head, checked rather than
assumed.

**The working tree is clean and pushed**, with no tracked evaluation
artifact holding the output of a probe rather than a recorded run.

**Nothing was added beyond what this question needs.** A control arm and the
measurement that justifies it are in scope. A new token, generator, training
objective or corpus is not.
