# Completion condition

**Ordering is explicitly not a completion criterion.** Any order satisfies
this, and so does any branch, any commit shape and any process. What counts
is the end state of the tree.

## Done when all of the following hold

**Sources are vendored outside version control and recorded inside it.** At
least four public-domain or CC0 sources were scanned. A tracked record names
each one with its retrieval date, the licence determined at retrieval and a
content hash. **No source body is tracked and no licensed word list is
tracked.**

**Both Victorian and modern sources are among them**, so the two can be
contrasted.

**The frequency threshold is set from the scan rather than defaulted**, with
the distribution that justified it stated, and with the candidate counts at
neighbouring values given so a reader can see what the choice costs. **If it
was chosen by eye the record says so** rather than implying it was derived.

**Candidates are reported per source rather than pooled**, and a word frequent
in one source and absent from the others appears as a candidate rather than as
long tail.

**The archaism problem is measured rather than asserted.** A figure states how
much of the Victorian sources' frequent vocabulary is absent from the modern
sources, and the record says plainly that the figure identifies candidates for
judgement rather than deciding any of them.

**Some words are admitted from the scan and each carries the source that
proposed it.**

**Level two is still self-hosting and its coverage of words needing a
definition did not fall.** No word is admitted without a definition.

**A reader looking for how to extend the lexicon can find the answer in a
tracked document**, including what the scan proposes and what it cannot see.

**Nothing claims the lexicon is complete.** The remaining gap between the
current count and the target is stated as a number.

**No claim rests on a figure the tree cannot reproduce.** Every count in a
tracked document was read from a tool rather than computed by hand.

**The gate passes.** `./tools/check.sh` reports all checks passed and exits 0,
with no check weakened or removed to achieve it.

**Continuous integration is green** on the pushed head, checked rather than
assumed.

**The working tree is clean and pushed.**

**Nothing was added beyond what this question needs.**
