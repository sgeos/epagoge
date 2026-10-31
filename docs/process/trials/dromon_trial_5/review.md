# Review of the sixth agency batch and the level-one and level-two readiness report

**Stamp.** HEAD is aae4abe2187fc08289ed6ad85c67d672a84e7970. Committed level-two seed book blob 29f168d4970649c33613cea29c3f2897d73f8750. Working-tree level-one seed book blob d32c51b14357971b24738b643e0e4c1210e910d4, which equals HEAD. Working-tree level-two seed book blob b291839d07dabd48dc6866f777284aebc2015490. The fifth and sixth batches are both uncommitted on top of HEAD.

**Fact.** I edited nothing tracked, did not commit, did not apply any diff, did not load the teacher, and did not run tools/check.sh or the test suite. Withdrawn strings were counted only, not identified.

## Part A: the sixth batch

### 1. Completion-condition clauses

- **Fact.** `tools/measure_lexicon_increment.py evals/review/level_2_agency_06 --check evals/review/level_2_agency_06/measurement.json` reported that the increment measurement matches the tree and exited 0.
- **Fact.** Closure, run as `PYTHONPATH=src .venv/bin/python tools/validate_closure.py curriculum/vocabulary.json curriculum/books/level_N N`, gives 849 of 849 at level one, 2995 of 2995 at level two and 3192 of 3192 at level three, all 100.0%.
- **Fact.** The level-two review holds 26 records (9 admit, 11 exclude, 6 defer). The level-three review holds 4 admits. Together these match the pool words plus the two citation forms, `dedicate` and `flux`.
- **Fact.** No batch word has an earlier decision under its own name, so no prior decision was changed.
- **Fact.** The 13 new vocabulary entries are the 9 and 4 admitted here. The seed books change by addition only.

### 2. Definitions

- **Fact.** All 13 definitions pass `epagoge.vocabulary.unlicensed` at their level.
- **Fact.** `incompressibility` (level three) is defined as "the property of being incompressible", which only restates the word. The operator has approved the replacement "Incompressibility is how much a substance pushes back when it is squeezed into a smaller space." It passes the ceiling. "resists being squeezed" is rejected because "resists" is not admitted at level three.
- **Fact.** `flux` (level three) gives the water-cycle sense, which is imprecise. The optional replacement "A flux is the amount of something that flows through an area in a given time." passes the ceiling.
- **Inference.** The other eleven definitions are correct and within their levels as far as the ceiling check shows. Their accuracy against source pages is not checked.

### 3. Deferrals and exclusions

- **Fact.** The nine Spanish exclusions cite that the string is not an English headword. The two inflected exclusions, `dedicated` and `fluxes`, cite admitted citation forms. Both are sound.
- **Fact.** The five deferrals cite page-interface use only, as in the fifth batch.
- **Inference.** `abstract` is a common English word, and its deferral rests on the scan's note that it is frequent only in interface text. That reading is reasonable, but it needs a prose sample before a later decision.

### 4. Changes outside the batch

- **Fact.** `src/epagoge/inflection.py` and `tests/test_candidates.py` changed only in the fifth batch's entries and in the new `level_2_agency_06` test entry. This batch changed no table.
- **Fact.** The fourteen measurement files that changed differ only in `after`, `closure` and `remaining_gap`.
- **Fact.** `docs/process/HANDOFF.md` and `docs/process/RESUME_PROMPT.md` are modified, and I did not review them.

### 5. The first-pool accounting

- **Fact.** `tmp/lexicon-sources/pool_agency.json` holds the first pool of 243 strings under the key `pool`. Only `organics` among the seventeen strings listed below is in that pool. The operator confirmed this, and I verified it against the list.
- **Correction.** My Part A review said that the seventeen strings were likely part of the first pool. That inference was wrong. Sixteen of them were never pool words. The README is correct that `organics` is the only undecided pool word without a reviewed-forms entry.
- **Fact.** The sixteen strings are `buildings`, `colored`, `cooling`, `cools`, `experiencing`, `flooding`, `graphics`, `mining`, `oils`, `peoples`, `powered`, `sampling`, `soaps`, `united`, `waters` and `wells`. Each is admissible only through suffix stripping to a headword, and each lacks a review record under its own name.
- **Inference.** The operator has recorded the general point, that a string admissible only by suffix stripping can carry an undecided sense. That point stands even though the sixteen are not pool words, so it is not a completion-condition failure.
- **Fact.** `organics` has no review record and is a pool word, so under the completion condition it still needs a decision. The operator has not decided it.

## Part B: the readiness report

### 6. Reproduction

- **Fact.** I ran `python3 -I tmp/dromon-trial-6/readiness_l12.py "$PWD"` and it exited 0. The table covers 26 units and the ranking prints. Its output is at `$TMPDIR/l12-out.txt`.
- **Fact.** The report cites the level-one blob d32c51b1 and the level-two blob b291839d, which both match the working tree.

### 7. Hand recount of three units

I wrote a separate recount in `$TMPDIR` that does not reuse the script's functions.

- **ac2.balance.** Recount: balance 0/1/1, reconciliation 0/1/1, same_amount 1/2/3, exchange 8/35/43. The report states the same values.
- **c2.claim.** Recount: claim_under_test 0/2/2, leaving_out 2/2/4, letter 0/0/0, name 2/1/3, saying_what_you_saw 2/8/10, standing_for 10/7/17, story 2/5/7. The report states the same values.
- **b2.mending.** Recount: animal 8/45/53, being_hurt 2/13/15, mending 3/3/6, tending 1/15/16. The report states the same values.

### 8. Ranking across all 26 units

- **Fact.** My recount applies the stated rule: fewest zero concepts, then the highest minimum, then the highest sum, then ascending identifier. It gives r2.measure, ac2.flow, p2.matter, b2.mending, p2.force, then a2.plan. The report's top five matches, and the sixth position is a2.plan.
- **Fact.** The fourth-trial ordering in the report, r2.measure, ac2.flow, a2.plan, b2.keeping_going, b2.mending, matches `docs/process/trials/dromon_trial_4/readiness-delta.md`.

### 9. Concepts empty at both levels

- **Fact.** The recount finds exactly four concepts with zero combined headwords across the 26 units: keeping_your_claim, letter, right_reason and two_shoulds_at_once. This matches the report.

### 10. The "fourth-trial zero" list

- **Fact.** The report lists seventeen concepts as having zero level-two headwords in the fourth-trial report and now having level-one headwords. All seventeen have positive level-one counts, which I verified.
- **Fact.** The fourth-trial delta file lists thirteen concepts scheduled in missing units with no level-two headword. Nine of luna's seventeen are on that list.
- **Fact.** Eight of luna's seventeen are not on that list: correspondence, doing_in_order, enough, judged_by_another, keep_trying_or_stop, name, presence and wearing_out. The delta file records a positive level-two gain for each of them.
- **Inference.** The report's claim that these eight had zero level-two headwords in the fourth trial is not supported by the delta file. The fourth-trial readiness report itself is not in the repository, so the claim cannot be checked against it. The list should either cite that report or be limited to the thirteen concepts.

### 11. Claims beyond a headword count

- **Fact.** The report states that a headword count measures vocabulary on file, not writability, and that a ranking change is not evidence of better curriculum choices. Both caveats are correct.
- **Inference.** The report does not claim that a level-one headword gives the same sense as a level-two use. This is not checked, and the report does not say it is.

## Findings and open items

1. **Organics.** The operator must decide the one undecided pool word, `organics`, under the completion condition.
2. **Sixteen admissible strings.** These need no pool decision. The operator may still review them for undecided senses reached through suffix stripping.
3. **Trial-four list.** The report's list of seventeen zero-concept strings needs its source corrected, or it should be limited to the thirteen concepts in the delta file.
4. **Abstract.** The deferral needs a prose check before a later decision.
5. **Not done.** The test suite was not run. The definitions were not checked against source pages. The completion condition's `tools/check.sh` gate was not run by this line.

**Verdict.** The sixth batch's measurement, closure, ceiling and prior-decision checks pass. The batch is not complete under the completion condition while `organics` is undecided. The readiness report's counts, ranking and both-level list are reproduced. Its trial-four zero list is not supported by the delta file for eight concepts.
