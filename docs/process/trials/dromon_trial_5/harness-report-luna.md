# Luna harness experience report

## Changes since the earlier report

**Fact.** The fourth-trial report described using a tracked readiness script and generating a vocabulary sheet. This fifth trial reused that readiness script's counting approach, added level-one counts, and ranked by combined level-one and level-two vocabulary. The review reproduced all counts, the ranking and the four concepts empty at both levels.

**Fact.** The operator's correction identified that I had attributed seventeen concepts to the fourth-trial delta even though it listed thirteen. I replaced that paragraph with the thirteen concepts from the cited file and added each concept's current level-one count. The script now reads that list from the cited file and prints the counts. Ruff check and format check pass.

## What worked well

**Fact.** The task supplied the ranking rule, exact script and report paths, source reports, and the rule for delaying the harness report. The script outputs all 26 unit rows, ranks the top five, and lists concepts empty at both levels. The reviewer independently recounted three units and reapplied the ranking across all 26.

**Inference.** Reusing the existing count script's structure made the level-one and level-two comparison easy to verify. The review's pinpointed correction let me repair the unsupported historical comparison without changing the verified counts.

## What got in the way

**Fact.** I initially used the temporary fourth-trial report's longer zero list instead of the thirteen concepts in the cited trial delta. This added eight concepts whose level-two gains were recorded in that delta. The review exposed the mismatch. I then read the specified file and made the script parse its list. The first parser output included the conjunction before the final concept; I noticed this in the output and corrected the parser before updating the report.

**Fact.** Ruff is not on the shell PATH. I ran it from the project's virtual environment and both checks passed.

## What I could not see or do

**Fact.** The fourth-trial readiness report itself is absent from the repository, as the reviewer noted. The delta file is available and supplies the thirteen concepts used in the corrected report. The session also cannot read .dromon/, but this task required no content from there.

**Inference.** The report can accurately attribute the thirteen concepts to the available delta, but it cannot establish what a missing earlier report may have said.

## Ranked harness suggestions

1. **Name the authoritative comparison artifact beside each comparison request.** Problem: I used a temporary report with a longer list instead of the cited delta's thirteen concepts. Repeating the exact source and requiring derived lists from it would prevent scope drift.
2. **Keep historical reports used for comparisons in the repository or trial archive.** Problem: the earlier readiness report is absent, so its contents cannot be checked against the delta. Preserving the source snapshot would make historical claims auditable.
3. **Show command truncation and output boundaries.** Problem: earlier trial work required follow-up reads after large outputs were cut off. A visible marker and per-command cap would show when a read is incomplete.
4. **Document the project tool path for Ruff.** Problem: Ruff was unavailable on PATH although installed in the virtual environment. A standard command would prevent a failed lookup.

## Earlier suggestions and direction

**Fact.** The prior report's recommendation to retain immutable comparison snapshots still applies. The Ruff environment suggestion also applies. Its truncation suggestion remains relevant from earlier work, although this turn's focused commands did not truncate. The schedule-to-book helper is addressed for this task by the existing readiness script. Scratch-path guidance did not affect this task.

**Judgement.** The operator's direction was clear about the requested outputs and deferred harness report. Naming the exact source for the historical empty-concept list would have prevented my initial choice of the wrong report. The review correction was specific enough to resolve the discrepancy and improve the script.
