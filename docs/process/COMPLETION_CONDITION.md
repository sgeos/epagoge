# Completion condition

**Ordering is explicitly not a completion criterion.** Any order satisfies
this, and so does any branch, any commit shape and any process. What counts
is the end state of the tree.

## Done when all of the following hold

**No live tracked document asserts a claim the session's measurements have
changed.** Where such a claim appeared in live text, it carries a correction
beside it rather than having been deleted.

**Text inside an accumulated-history section is unedited**, and the
distinction between history and live text is respected wherever a claim
appears in both.

**Where a decision's stated justification no longer holds but the decision
still stands, the record says both**, rather than removing the item or
leaving the dead reason in place.

**The evaluation record that grew through this session opens with its
current state**, so a reader meets the present conclusion before the
sections it replaced, and the superseded sections remain readable.

**The record names what is now the binding constraint** on further progress,
so a reader knows where effort moves something.

**Every figure presented as current says how many seeds or observations it
rests on.**

**No claim is reinstated that the evidence does not support**, and anything
resting on a measurement taken before the current corpus, vocabulary or
controls is marked where a reader meets it.

**The gate passes.** `./tools/check.sh` reports all checks passed and exits
0, with no check weakened or removed to achieve it.

**Continuous integration is green** on the pushed head, checked rather than
assumed.

**The working tree is clean and pushed**, with no tracked evaluation
artifact holding the output of a probe rather than a recorded run.

**Nothing was added beyond what this question needs.** No new arm, option,
token, generator or training objective.
