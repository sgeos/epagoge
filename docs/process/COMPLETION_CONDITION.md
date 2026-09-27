# Completion condition

**Ordering is explicitly not a completion criterion.** Any order satisfies
this, and so does any branch, any commit shape and any process. What counts
is the end state of the tree.

## Done when all of the following hold

**A checkpoint loads.** `evals/pilot/level_1.pt` exists, was written at the
current vocabulary size, and `tools/talk.py --level 1 --prompt "the cup is"`
produces output without an error and without reporting a vocabulary
mismatch.

**The position comparison has been re-measured** at both position schemes
and at least two sequence lengths, on the current corpus, with heads derived
rather than fixed. `evals/pilot/LEVEL_ONE_POSITIONS_AND_RETENTION.md`
carries the new figures and states the corpus size and head derivation they
were taken under.

**The capacity sweep has been re-measured** with derived heads over at least
three widths. `evals/pilot/LEVEL_ONE_CAPACITY.md` carries the new figures.

**Retention has been re-measured** on a checkpoint trained on the current
corpus. A record states whether the epistemic concepts that were worst
retained moved, and states explicitly that the book set changed between the
two measurements so the two rankings are not a controlled comparison.

**Every evaluation record under `evals/pilot/` that still carries a figure
taken before the current corpus, vocabulary or head derivation says so in
that record**, in a form a reader meets before the figure.

**No figure presented as a result rests on one seed.** Anything single-seed
is labelled as such where it appears.

**`docs/process/HANDOFF.md` validity block matches the tree**, including
book count, record count, test count, vocabulary and token counts, and each
asserted number is one that was read from a tool rather than computed by
hand.

**The gate passes.** `./tools/check.sh` reports all checks passed and exits
0, with no check weakened or removed to achieve it.

**Continuous integration is green** on the pushed head, checked rather than
assumed.

**The working tree is clean and pushed**, with no tracked evaluation
artifact left holding the output of a probe rather than a recorded run.

**No new capability was added** beyond what is needed to take these
measurements. A new option, token, generator, or training objective is
outside this condition.
