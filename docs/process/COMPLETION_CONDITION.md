# Completion condition

**Ordering is explicitly not a completion criterion.** Any order satisfies
this, and so does any branch, any commit shape and any process. What counts
is the end state of the tree.

## Done when all of the following hold

**A tool exists that turns candidate words into definitions the admission tool
accepts**, and it is runnable from the tree rather than described.

**It was run and words were admitted from its output**, each carrying the
source that proposed it.

**Level two is still self-hosting and its coverage of words needing a
definition did not fall.** No word was admitted without a definition.

**The acceptance rate is recorded**, meaning how many candidates the teacher
could define inside the level's vocabulary against how many were offered, read
from the run rather than estimated.

**The remaining gap is stated as a number**, so nothing implies the lexicon is
close.

**Generated forms were checked, not assumed.** Any admitted noun with no plural
or adjective with no suffixed comparison carries the qualifier that says so,
and no manufactured non-word entered the lexicon.

**A tracked document says what the pipeline is and what judgement it still
requires**, including that archaism is invisible to it.

**No claim rests on a figure the tree cannot reproduce.** Every count in a
tracked document was read from a tool rather than computed by hand.

**No tracked artifact holds the output of a probe** rather than a recorded run,
and any new tool requires an output path rather than defaulting to a tracked
one.

**The gate passes.** `./tools/check.sh` reports all checks passed and exits 0,
with no check weakened or removed to achieve it.

**Continuous integration is green** on the pushed head, checked rather than
assumed.

**The working tree is clean and pushed.**

**Nothing was added beyond what this question needs.**
