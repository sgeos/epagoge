# Completion condition

**Ordering is explicitly not a completion criterion.** Any order satisfies
this, and so does any branch, any commit shape and any process. What counts
is the end state of the tree.

## Done when all of the following hold

**Held-out loss against training corpus size is measured on the current
corpus**, at three or more sizes spanning at least a fourfold range, with
the held-out set identical at every size and that fact stated.

**More than one step count is run at each size**, and the record says which
figure it reports and why, since the optimal step count moves with corpus
size.

**The record states what the slope means for whether to write more books**,
in terms a reader can act on, and distinguishes what the curve measures
from what it does not.

**`evals/pilot/LEVEL_ONE_SCALING.md` no longer presents only figures taken
before the current corpus**, and a reader meets the current measurement or a
pointer to it before the older one.

**Every figure says how many seeds it rests on**, and any single-seed figure
is labelled as such.

**No claim is made that generation is or is not worthwhile beyond what the
measurement supports.** Token count and concept coverage are different
quantities and the record says which was measured.

**The gate passes.** `./tools/check.sh` reports all checks passed and exits
0, with no check weakened or removed to achieve it.

**Continuous integration is green** on the pushed head, checked rather than
assumed.

**The working tree is clean and pushed**, with no tracked evaluation
artifact holding the output of a probe rather than a recorded run.

**Nothing was added beyond what this question needs.**
