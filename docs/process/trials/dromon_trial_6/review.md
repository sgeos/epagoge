# Trial 7 review: Part A summary and Part B readiness terms

**Stamp.** Reviewed at HEAD aae4abe2187fc08289ed6ad85c67d672a84e7970. Vocabulary blob e4187a17a4a280d0b1779b10656f3edfa3eeec64, hashed with git hash-object. The worker's fixes to findings A, C and D and the peoples wording are not yet in this stamp, so they are not reviewed here.

## Part A

The full Part A review is in tmp/dromon-trial-7/review-part-a.md. Its open findings still stand at this HEAD.

- **Finding A (decision).** flooding is excluded as a form of the new verb flood. The sources use it as the noun, which the lookup already resolved to the admitted noun flood.
- **Finding C (fix before commit).** curriculum/provenance.json gives color, cool and well the 2026-10-10 agency scan as their origin, overwriting the first senses' origins.
- **Finding D (decision).** The closure gate keys by word, so the experience, flood and sample second-sense texts are not in its map. They are grounded, so this is a coverage gap, not a current failure.
- **Gap.** The level-three admission (organics) has no measurement check, since its batch has no measurement.json.

## Part B

### Commands and clauses checked

- **Fact.** python3 -I tmp/dromon-trial-7/readiness_terms.py "$PWD" exited 0. Its printed unit counts, ranking and thinnest-concept list agree with the report's tables.
- **Fact.** The script reads only term entries at levels 1 and 2, and counts each word once per concept. It ignores the forms field.

### Hand checks against curriculum/vocabulary.json

- **keeping_your_claim.** Two level-one entries, hold and holds, each with no forms list. Count 2 at L1, 0 at L2, combined 2. Matches. Level-one entries with no level-two entry.
- **balance.** One level-two entry, balance (forms balanced, balances, balancing). Count 1 at L2. Matches. The concept also has three level-three entries (equilibrium, neutralize, offset), which the count excludes.
- **letter.** One level-one entry, letter (forms letters). Count 1 at L1. Matches.

### Ranking across all 26 units

- **Fact.** No unit has a zero concept at levels 1 and 2 combined. The four concepts the fifth trial called empty all have level-one entries, so the zero column reads 0 throughout.
- **Fact.** The script's top five is r2.measure, p2.matter, p2.force, b2.mending, ac2.flow. The report's table gives the same order.

### Reconciliation with the fifth trial

- **Fact.** The fifth-trial script, readiness_l12.py, counts records only in curriculum/books/level_1/bk.dictionary.seed.md and curriculum/books/level_2/bk.dictionary.seed.md (its lines 54 and 55).
- **Fact.** The four words hold, holds, letter, right and hard are defined in curriculum/books/level_1/bk.dictionary.1.md (dict.1.hold and so on) and not in the seed book.
- **Inference.** The fifth-trial zeros came from the seed-book file set, not from the vocabulary. The report's explanation is correct, and the stated reconciliation is supported.

### Forms and inflation (your question)

- **Fact.** The script counts only the word field. Forms lists do not add counts, so forms entries do not inflate other concepts.
- **Fact.** Separate entries for inflected words do inflate counts. keeping_your_claim counts hold and holds as two words, and folding gives one. The concept's count is 2 raw and 1 folded.
- **Inference, heuristic.** A suffix test over all 135 concepts flagged seven words that may be forms of another entry in the same concept: holds, parking, interesting, living, curved, shoes and textured. Only holds is a clear inflection. The others need a check by hand.
- **Fact.** Folding the seven flagged words changes three units by one or two: p2.matter 543 to 541, p2.force 513 to 512, r2.measure 325 to 324. keeping_your_claim changes, but its unit (i2.reason) is not in the top five.
- **Fact.** The ranking does not change under folding. The top five stay in the same order.

### Level restriction (not stated in the report)

- **Fact.** The script and report use only levels 1 and 2. The vocabulary file also holds 198 level-three entries and 55 at levels 4 to 6, which both are excluded.
- **Fact.** Including level three changes the top five's order. It gives r2.measure, ac2.flow, p2.matter, p2.force, b2.mending. Two concepts, balance and claim_under_test, have level-three entries and would count higher.
- **Judgement.** The restriction may be right for level-two readiness. The report should say so in its heading.

### Does the report claim more than a count shows?

- **Claim checked.** "A count measures vocabulary on file, not whether a module can be written." This is correctly hedged.
- **Claim checked.** "The term list gives the broadest basis for this task." This is wrong as written. The term list is narrower than the file, because it excludes levels three to six. The report should say "the level-one and level-two term entries".
- **Claim checked.** "Its counts ... do not assess coverage quality or writing readiness." Correct.
- **Concern.** The ranking rule is an agent-chosen sort. Ties and the minimum-count rule have no justification in the report beyond the script's code. The report labels it as a rule, which is adequate.
- **Concern.** The report calls the ranking "readiness" in its title. The counts measure file contents, so the heading overstates. The body disclaims it.

## Recommendations

1. Scope the readiness report's headings to levels one and two.
2. Replace "broadest basis" with the actual scope.
3. Decide whether forms-only words count as covered, and state the rule.
4. Check the six non-holds heuristic flags before any count is used in a decision.
5. Resolve Findings A, C and D before commit, as listed in Part A.

## Not checked

- The full test suite was not run. Part A ran two test files with unittest.
- tools/check.sh was not run, as instructed.
- The worker's fixes to A, C, D and peoples were not reviewed.
