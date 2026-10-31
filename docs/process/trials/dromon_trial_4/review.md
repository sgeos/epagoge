# Review of the fifth agency batch, the readiness delta and the r2.measure sheet

**Stamp.** HEAD is aae4abe2187fc08289ed6ad85c67d672a84e7970. The batch is uncommitted on top of it. Committed level-two seed book blob 29f168d4970649c33613cea29c3f2897d73f8750. Committed level-three seed book blob 8c2a94e6956d362c20fedcdfd17c4732ebb6c897. Working-tree level-two blob 99d6bb49533dd3424bfe807e1c2976fd44b0d97d. Working-tree level-three blob 4b8e44431f8065da1f38e6f97b1bd046c8294530. I edited nothing tracked and did not run tools/check.sh.

**Fact.** The full Part A review is at `tmp/dromon-trial-5/review-part-a.md`. Its findings are summarised here and not repeated.

## Part A, the batch

- **Fact.** The measurement check printed "increment measurement matches the tree" and exited 0.
- **Fact.** Closure is 100.0% at levels one to three, with 849, 2986 and 3179 of the required words defined. The validator takes one level's book directory. Passing the parent directory reports 0 of 849 defined, so the batch README's usage should name the level.
- **Fact.** All 480 definitions pass `epagoge.vocabulary.unlicensed` at their level.
- **Fact.** The 645 review records equal the 571 pool words plus 74 citation forms. I checked the arithmetic, not each string. No withdrawn string was identified.
- **Fact.** No pre-existing vocabulary entry changed or was removed. No batch word has a decision in another `review.json`.
- **Fact.** Eight definitions have proposed replacements, each checked against the ceiling. The most important are `abundant`, which has no antecedent, `cement`, which says "dry" where the source describes hardening, and `pathogen`, which conflicts with the level-two `virus` entry. The Part A file gives the wording.
- **Inference.** The deferral reasons are sound. Two depend on a separate policy decision that the record states.

## Part B, the readiness delta

- **Fact.** I reran `docs/process/trials/dromon_trial_3/readiness.py` on the working tree. It reports 26 missing units. The delta lists 26 units, and I checked that the sets match.
- **Fact.** The thirteen zero-count concepts in the delta match the rerun exactly.
- **Fact.** The delta's baseline blob, 556c47c4, is not in the repository's history, so the comparison snapshot cannot be recovered from git. I recomputed each gain against the committed level-two seed book, blob 29f168d4. The gains match for all seventeen concepts I checked, including `change` +13, `material` +16, `physical_property` +6, `good_and_bad` +16 and `spatial_position` +19. Every one of the 26 units gains at least one headword on that baseline.
- **Fact.** The script's summary ranks the top five as r2.measure, ac2.flow, a2.plan, b2.keeping_going and b2.mending, which matches the delta. I did not reapply the stated rule to all 26 units. I checked only the top five.
- **Correction to my own earlier record.** The delta compares against the third-trial ranking, which places ac2.flow second. My trial-four readiness report ranked p2.force second. That report was written while the worker was still editing, so its counts do not match the committed baseline. For example, my earlier `change` count was 29, while the committed count is 31. The trial-four report should not serve as a baseline.
- **Inference.** The delta's statement "the ranking change reflects the count rule" is consistent with the data. The delta correctly says counts do not establish ease of writing.

## Part B, the r2.measure sheet

- **Fact.** Rerunning `tmp/dromon-trial-5/vocab_sheet.py` produced 299 headword entries. Its lists match `vocab-r2-measure.md` line for line.
- **Fact.** Level-two counts are cycle 27, how_sure 15, measuring 37, sequence 22, spatial_position 138 and unit 18. These match both the sheet and the rerun readiness table.
- **Fact.** I checked three concepts by an independent grep of the seed book. For `unit`, `how_sure` and `sequence`, the grep matches the sheet entry for entry. The headword lists are correct.
- **Fact.** The sheet's example headwords are filed under the concepts it names. `per`, `ton` and `degree` are under `unit`. `hundred` and `fourth` are under `number_word_order`. `average` and `equivalent` are under `same_amount`. `amount`, `total`, `fraction`, `ratio` and `sample` are under `quantity`. `horizontal` and `vertical` are under `direction`. `hour`, `interval` and `duration` are under `duration`.
- **Inference.** The sheet's first paragraph says a headword list shows vocabulary on file, not that a module can be written. The judgement paragraphs are labelled as judgements. Neither file claims more than a headword list shows, with one caveat. The phrase "comparatively thin" rests on counts alone, and the sheet says so.

## Limits

- I did not check the ranking rule across all 26 units. I checked the top five and the zero-count list.
- I did not verify the baseline snapshot blob, because it is absent from the repository. I used the committed blob instead.
- I did not run the test suite on this tree.
- The definitions were not checked against source pages.
