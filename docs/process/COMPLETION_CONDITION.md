# Completion condition

**Ordering is explicitly not a completion criterion.** Any order satisfies
this, and so does any branch, any commit shape and any process. What counts
is the end state of the tree.

## Done when all of the following hold

**A configuration is named as the best measured**, with every setting that
differs from the defaults stated, and with the held-out loss it reaches.

**That configuration was found by a sweep over more than one setting**,
recorded with the full grid rather than only the winner, so a reader can see
what was beaten and by how much.

**Whether the settings combine is stated from measurement**, not assumed.
If two improvements do not add, the record says so.

**The best result rests on more than one seed**, or is labelled as resting
on one, and the seed-to-seed spread is stated so a reader can judge whether
the winner is distinguishable from its neighbours.

**The shipped checkpoint is trained at the named configuration**, loads
through the ordinary loader, and `tools/talk.py` runs against it without
reporting a vocabulary mismatch.

**A reader looking for what to train with can find the answer** in a
tracked document, rather than having to reconstruct it from evaluation
records.

**The frontier is stated as one number with its configuration attached**, so
a later claim has something specific to beat.

**No improvement is credited beyond what the sweep shows.** Anything
measured in isolation and not in combination is described as such.

**The gate passes.** `./tools/check.sh` reports all checks passed and exits
0, with no check weakened or removed to achieve it.

**Continuous integration is green** on the pushed head, checked rather than
assumed.

**The working tree is clean and pushed**, with no tracked evaluation
artifact holding the output of a probe rather than a recorded run.

**Nothing was added beyond what this question needs.**
