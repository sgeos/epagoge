# Completion condition

**Ordering is explicitly not a completion criterion.** Any order satisfies
this, and so does any branch, any commit shape and any process. What counts
is the end state of the tree.

## Done when all of the following hold

**An ordering exists that carries the length gradient without respecting the
prerequisite graph**, and it is available to the trainer.

**Its length gradient is shown to match the graph-respecting arm's**, and
its batch diversity is shown to match the graph-ignoring arm's, both by
measurement recorded alongside the arms they are matched against. A reader
can see it is a control rather than a fourth variable.

**The statistic used for that match is stated**, and whether it is computed
per run or across runs, because the two differ by half again for these
orderings.

**The arm has been trained against both existing arms** at the same
endpoint and seed count, with per-arm means and the seed count recorded.

**The record states what the result implies for the residual**, including
what a result falling between the two existing arms would mean, and states
plainly if the design cannot decide.

**The default set of arms the trainer compares is unchanged**, so that
adding this control does not silently alter what an ordinary run measures.

**Any claim that the residual is attributable to a named cause is either
supported by this experiment or absent.** The previously withdrawn
attribution is not reinstated without the evidence this arm provides.

**Every figure says how many seeds it rests on.**

**The gate passes.** `./tools/check.sh` reports all checks passed and exits
0, with no check weakened or removed to achieve it.

**Continuous integration is green** on the pushed head, checked rather than
assumed.

**The working tree is clean and pushed**, with no tracked evaluation
artifact holding the output of a probe rather than a recorded run.

**Nothing was added beyond what this question needs.**
