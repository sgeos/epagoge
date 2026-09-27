# Current brief. Build the arm that decides it

**Written 2026-09-27**, replacing the brief that attributed the residual.
That brief's conclusion was withdrawn a tick later and this one exists
because of the withdrawal. Durable practice is in `PROCESS_STRATEGY.md`.

## Why this and nothing else

**Two explanations for the ordering residual are collinear and no analysis
can separate them.** Orders that respect the prerequisite graph also sort
books by length, because a prerequisite-heavy book is placed later and 90
percent of books carry one. Across the arms the two predictors correlate at
-0.76, and within each arm neither varies enough to regress.

**With two groups, everything that differs between them is confounded with
everything else that does.** The fix is a third group, not a cleverer fit.

**The arm to build has the length ordering and not the graph.** If it
reproduces the graph-respecting arm's penalty, the effect is sequence length
and the curriculum interpretation is dead. If it lands with the shuffled
arm, the graph survives as the explanation.

## The trap this brief exists to avoid

**A control is only a control if it matches on the thing it holds fixed.**
The weight that sets how strongly this arm sorts by length has to be tuned
until its length ordering equals the graph-respecting arm's. Tuned wrong,
the arm varies two things again and the tick is wasted.

**Tune against the arm as implemented, not against a reconstruction of
it.** A first attempt tuned against a script that rebuilt the ordering
by hand and came out half again too strong, because the real arm places the
dictionary books differently.

**Tune against the right statistic.** Correlating a book's mean position
across seeds against its length gives +0.311. Correlating within a single
seed gives +0.211. A training run sees one order, so the per-run figure is
the target, and the first tuning used the other one.

## Other wrong turns to avoid

**Do not change what the ablation compares by default.** A fourth arm costs
a third more compute on every run that does not ask this question, and
changing the default comparison is a design decision that belongs to the
operator. Make the arm available.

**Do not conclude from the arm alone.** Report where it falls relative to
both existing arms, and say what a middling result would mean, because a
result between them does not decide anything.

**Do not treat this as the last confound.** Five have now been found, the
most recent in the reasoning rather than the code. Ask what else differs
between the new arm and the ones it is being compared to, before reporting.

**Do not overwrite a tracked artifact**, do not read a count from
arithmetic, and check CI separately.

## What is not this brief's to decide

Items 5, 7 and 10, the level-two lexicon, schedules for levels three to
seven, `sources/` and level seven, the fourteen sense questions, and the
Rust build output. **Announcing the repository is not this brief's either.**
