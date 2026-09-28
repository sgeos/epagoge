# Completion condition

**Ordering is explicitly not a completion criterion.** Any order satisfies
this, and so does any branch, any commit shape and any process. What counts
is the end state of the tree.

## Done when all of the following hold

**A baseline is measured on the current corpus** at a duration justified by
the twenty-epoch rule, over more than one seed, with the seed spread stated and
with every held-out batch scored. **The stale frontier is not used as the
comparison point**, and any figure carried from before the corpus refresh is
labelled as describing a smaller corpus.

**Warmup-stable-decay exists in the trainer and its effect is measured**
against that baseline, or a tracked document says why it was not adopted.

**Muon exists in the trainer and its effect is measured** against that
baseline, or a tracked document says why it was not adopted. **If it is
implemented, a tracked document names what the implementation was checked
against and states which parameters it is applied to and which are left to the
other optimiser.**

**Whether the two combine is stated from measurement rather than assumed.** If
they do not add, the record says so.

**Maximal update parametrization's status is settled in a tracked document.**
Its superseded justification is kept in place rather than edited away, and the
document says what the technique is still for, if anything, now that a single
scale point is decided.

**No improvement is credited beyond what was run.** Anything measured alone
and not in combination is described as such, and a technique adopted on
reasoning rather than measurement says which it was.

**A reader looking for what to train with can find the current answer** in a
tracked document, with the configuration and the loss it reaches.

**No claim rests on a figure the tree cannot reproduce.** Every count and loss
in a tracked document was read from a tool rather than computed by hand.

**No tracked evaluation artifact holds the output of a probe** rather than a
recorded run.

**The gate passes.** `./tools/check.sh` reports all checks passed and exits 0,
with no check weakened or removed to achieve it.

**Continuous integration is green** on the pushed head, checked rather than
assumed.

**The working tree is clean and pushed.**

**Nothing was added beyond what this question needs.**
