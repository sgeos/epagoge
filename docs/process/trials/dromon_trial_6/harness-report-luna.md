# Luna harness experience report

## Changes since the earlier report

**Fact.** The sixth-trial report described combined seed-book counts and a correction to a historical zero-concept list. This trial switched the measure to the authoritative term list, counted distinct words by concept and level, and reconciled seed-book gaps with the separate level-one dictionary book. The reviewer reproduced the unit counts, ranking and hand checks.

**Fact.** The review requested explicit scope for levels one and two, a stated rule for inflections that have separate term entries, and a correction to the phrase “broadest basis.” I made those changes and added the reviewer's finding that folding flagged inflections does not change the top-five order.

## What worked well

**Fact.** The operator identified the authoritative source, listed the fields to count, specified how to treat multiple concept entries, and named the comparison report. The script prints per-unit counts, the ranking and the ten lowest-count scheduled concepts. Ruff check and format check passed.

**Fact.** The reconciliation located hold, holds, letter, right and hard in the separate level-one dictionary book. This explained why the fifth-trial seed-book measure reported four scheduled concepts as empty even though the vocabulary manifest contains terms for them.

**Inference.** Naming both the source file and the distinct-word rule made this measure more reproducible than the earlier seed-record count.

## What got in the way

**Fact.** Reading the entire vocabulary manifest in a combined command produced truncated output. I switched to a short script that reads the JSON and prints only the requested counts and words.

**Fact.** The first Ruff check flagged modern type-alias syntax and a long output label. I changed the aliases and split the label, then Ruff check and format check passed.

**Fact.** My initial report did not explicitly say that levels three through six were excluded or describe how separately listed inflections count. The operator's review identified both omissions. I updated the report to state that levels three and higher are excluded, the forms field adds no words, and separate word entries count separately.

## What I could not see or do

**Fact.** The session cannot read .dromon/. No information there was needed for this task. The full manifest did not fit usefully in command output, but the local script could read it directly.

**Inference.** No unavailable information blocked the count. The specific meaning of whether an inflected word with its own term entry counts separately was not fully explicit in the first task note, so I applied the distinct-word rule literally and stated that choice for review.

## Ranked harness suggestions

1. **Make large command truncation obvious and offer structured file queries.** Problem: dumping the full vocabulary manifest hid most of the output. A truncation marker plus a simple JSON query pattern would direct work toward relevant fields.
2. **State the boundary rules for counts in the task prompt.** Problem: the first report omitted higher levels and did not explain separately listed inflections. Naming the allowed levels, word field and forms treatment at assignment time would prevent a review round for measurement semantics.
3. **Keep review source files and computed outputs together.** Problem: prior trials exposed ambiguity when a referenced historical report was absent or differed from a temporary report. An archived source and its hash make later comparisons auditable.

## Earlier suggestions and direction

**Fact.** The earlier report recommended retaining exact comparison artifacts, showing truncation, and documenting the Ruff path. Truncation recurred. Ruff was available in the project environment and passed when invoked there, so the path guidance remains useful. Exact snapshots were not needed for this current-state count, but remain useful for historical comparisons.

**Fact.** Earlier suggestions for a schedule-to-book helper and scratch-path setup no longer apply to this task. The current script's assignment did not require checking book presence manually, and the requested scratch directory worked.

**Judgement.** The task named the authoritative file and comparison report clearly. Explicitly stating the level boundary and how to treat term entries that are inflections would have made the final report complete on the first review.
