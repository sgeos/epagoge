# Completion condition

**Ordering is explicitly not a completion criterion.** Any order satisfies
this, and so does any branch, any commit shape and any process. What counts
is the end state of the tree.

## Done when all of the following hold

**The learning rate is settable from a tool that trains**, so a run can state
what rate it used rather than inheriting one.

**A sweep over the learning rate is recorded for AdamW**, with the full set of
points rather than only the winner, at the duration the twenty-epoch rule
implies.

**A sweep over the learning rate is recorded for Muon**, on the same terms.

**The optimiser comparison is restated with each optimiser at its own best
measured rate**, over more than one seed, with the seed spread given. **The
record says plainly whether the previously published 0.117 nats survives**, and
if it does not, the earlier figure is corrected in place rather than edited
away.

**The width ranking's status is settled in a tracked document.** Either a
measurement at per-width rates is recorded, or the document states why it could
not be settled and leaves the ranking provisional with that reason.

**Every figure carried from before this work is labelled with what it was
measured under**, so a reader cannot mistake an untuned figure for a tuned one.

**No comparison presents a tuned arm against an untuned one as a comparison of
methods.**

**No claim rests on a figure the tree cannot reproduce.** Every count and loss
in a tracked document was read from a tool rather than computed by hand.

**No tracked evaluation artifact holds the output of a probe** rather than a
recorded run.

**A reader looking for what to train with can find the current answer** in a
tracked document, with the configuration and the loss it reaches.

**The gate passes.** `./tools/check.sh` reports all checks passed and exits 0,
with no check weakened or removed to achieve it.

**Continuous integration is green** on the pushed head, checked rather than
assumed.

**The working tree is clean and pushed.**

**Nothing was added beyond what this question needs.**
