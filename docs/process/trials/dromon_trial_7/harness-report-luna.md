# Trial 7 harness experience report

## Changes since the sixth-trial report

**Fact.** The sixth-trial report concerned readiness counts from the term list, distinct words by concept and level, and reconciling seed-book gaps. This trial measured suffix-stripped candidates against the shared vocabulary lookup and separately reran the readiness report against a changed vocabulary blob. The review independently reproduced all 160 candidate rows and all 104 cells in the readiness comparison.

**Fact.** This review identified two limits in my reports. Six of the 160 candidates had already been deferred in trial six, so describing five of the earlier seventeen as simply remaining in the list could suggest that all were undecided. Also, the readiness counts include earlier uncommitted batches, so their increase cannot be attributed to this trial's batch alone.

## What worked well

**Fact.** The task named the existing lookup, scan input, vocabulary file, review exclusion sources, comparison report and output fields. I reused `Vocabulary.lookup` and `Term.surface_forms()` rather than duplicating suffix or listed-form logic. The reviewer verified that the listed-form description matched the implementation and independently reproduced the results.

**Fact.** The task asked for per-source totals and a small sample of source-line judgements. I generated counts across all scan texts and read source lines for the ten most frequent strings. The review supplied targeted checks on flooding, graphics and roses, identifying both a reasonable sense match and cases where suffix lookup produced a misleading headword.

**Inference.** Keeping the candidate table and the readiness comparison as separate outputs made their different measures easier to inspect.

## What got in the way

**Fact.** A combined command that printed large vocabulary data produced truncated output. I used a short local script to query the needed records and later ran the candidate script to a file for a complete result.

**Fact.** The candidate list includes lookup matches that do not establish a matching sense. For example, roses resolves mechanically to rise, although the source uses refer to flowers. My report noted this limitation generally but did not count or enumerate such false resolutions.

**Fact.** My comparison with the trial-five list did not identify the six strings already deferred in trial six. The reviewer clarified that five of those six were in this list and that 154 rows, rather than 160, were not previously decided. I should have checked the intermediate review records before describing the overlap.

**Fact.** The readiness delta reports vocabulary growth across the current tree, which includes earlier batches. It does not isolate the effect of the current batch. The review made this limitation explicit.

## What I could not see or do

**Fact.** The session could not read `.dromon/`. No information from that directory was needed for the assigned measurements. I could inspect the trial brief, generated reports and review file in the workspace.

**Fact.** The script can report the resolved headword and its attached concepts, but lookup success alone cannot determine whether the source use fits the headword's sense. That requires reviewing source context and vocabulary definitions. The ten judgements cover only the requested top ten.

## Ranked harness suggestions

1. **Carry prior review decisions into candidate comparisons.** Problem solved: a candidate count can include strings already deferred, making the count look like unresolved work. A compact machine-readable status comparison against prior trial reviews would make the status visible.
2. **Mark the scope of tree-wide deltas.** Problem solved: vocabulary growth across several batches can be mistaken for the effect of the newest batch. Name the included changes or provide a baseline snapshot when attribution matters.
3. **Make large-output truncation visible and queryable.** Problem solved: full vocabulary output was truncated in a combined command. Structured query examples or an obvious truncation notice would help select a focused view.
4. **Preserve review inputs and hashes with results.** Problem solved: later comparisons need to identify which vocabulary state produced a count. This trial's blob hash and review report made the state auditable.

## Earlier suggestions

**Fact.** The sixth-trial report's suggestion to make truncation obvious still applies because truncation recurred. Its recommendation to retain exact comparison artifacts remains useful; the readiness comparison depended on an earlier report, while the review's blob hash documented the current state.

**Fact.** The earlier Ruff path guidance was not needed to resolve an issue in this trial. Ruff and format checks passed when run from the project environment. The schedule-to-book helper and scratch-path suggestions did not apply to these measurements.

**Inference.** Explicit boundary rules remain useful. This assignment stated the listed-form rule and lookup behavior clearly, while checking prior decisions and the scope of combined counts would have made the final reports more complete on first review.
