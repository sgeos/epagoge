# Completion condition

**Ordering is explicitly not a completion criterion.** Any order satisfies
this, and so does any branch, any commit shape and any process. What counts
is the end state of the tree.

## Done when all of the following hold

**The level-one corpus holds more books than it did**, and every book in it
meets the standards the gate enforces, with none admitted by weakening a
check.

**Concept pair coverage is recorded before and after**, computed as the
union of concepts across each content book's own records with the
dictionary books excluded, and the record states which counting method was
used and why the other two are wrong.

**Every new book carries its metadata fields and a date consistent with
version history**, as the gate's own checks report.

**No new book uses a word outside the level**, as the corpus validator
reports.

**Any book the generator produced that did not meet the standard is either
brought to standard or absent**, and the record says how many were refused
or discarded rather than reporting only what succeeded.

**A round that bought tokens rather than structure is reported as such.**
If pair coverage did not move, the record says so plainly instead of
reporting the book count alone.

**The gate passes.** `./tools/check.sh` reports all checks passed and exits
0.

**Continuous integration is green** on the pushed head, checked rather than
assumed.

**The working tree is clean and pushed**, with no tracked evaluation
artifact holding the output of a probe rather than a recorded run.

**No claim about model behaviour is made from this work.** Adding books
changes the corpus; whether it changes the model is a separate measurement
and is not part of this.
