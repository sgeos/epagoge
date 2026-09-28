# Completion condition

**Ordering is explicitly not a completion criterion.** Any order satisfies
this, and so does any branch, any commit shape and any process. What counts
is the end state of the tree.

## Done when all of the following hold

**A tracked document fixes the probe format and the scoring rule**, including
what counts as a meaningful shift, **stated before any figure appears** and not
adjusted to the figure afterwards.

**Probes exist as data the tree holds**, written in vocabulary a level-one
model can parse, and they are validated against the level's lexicon by a check
rather than by assertion.

**Both conditions exist.** The pressure condition and the correct-user control
are both implemented and both reported. **No result presents the pressure
condition alone.**

**A scorer exists and runs against the shipped checkpoint**, reporting the
whole probe set rather than a subset, and saying so.

**The first measurement is recorded with its uncertainty**, over more than one
probe, with the spread stated. **If the result is indistinguishable from
chance, the record says that plainly** rather than presenting a number as a
finding.

**The record states what the measurement does not cover**, including that
sycophancy is predominantly induced during preference optimisation and that a
corpus-only result cannot settle the property.

**`evals/elenchos/README.md` no longer says no probe has been written**, or it
says what is written and what is still missing.

**No claim rests on a figure the tree cannot reproduce.** Every count and
figure in a tracked document was read from a tool rather than computed by hand.

**No tracked evaluation artifact holds the output of a probe** rather than a
recorded run, and any new tool requires an output path rather than defaulting
to a tracked one.

**The gate passes.** `./tools/check.sh` reports all checks passed and exits 0,
with no check weakened or removed to achieve it.

**Continuous integration is green** on the pushed head, checked rather than
assumed.

**The working tree is clean and pushed.**

**Nothing was added beyond what this question needs.**
