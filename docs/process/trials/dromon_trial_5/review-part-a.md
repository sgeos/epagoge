# Review of the sixth agency batch, Part A

**Stamp.** HEAD is aae4abe2187fc08289ed6ad85c67d672a84e7970. Committed level-two seed book blob 29f168d4970649c33613cea29c3f2897d73f8750. Committed level-three seed book blob 8c2a94e6956d362c20fedcdfd17c4732ebb6c897. Working-tree level-two blob b291839d07dabd48dc6866f777284aebc2015490. Working-tree level-three blob 930a1259ec30ba6b3b4b15fc031dcb5b23c08d58. The fifth batch and this batch are both uncommitted on top of HEAD. I separated them by comparing the working seed books with HEAD and with the admission records of both batches.

**Fact.** I edited nothing tracked and did not run tools/check.sh.

## 1. Completion-condition clauses

- **Fact.** `tools/measure_lexicon_increment.py evals/review/level_2_agency_06 --check evals/review/level_2_agency_06/measurement.json` printed "increment measurement matches the tree" and exited 0.
- **Fact.** Closure, run as `PYTHONPATH=src .venv/bin/python tools/validate_closure.py curriculum/vocabulary.json curriculum/books/level_N N`: level one 849 of 849 defined, closure 100.0%; level two 2995 of 2995, closure 100.0%; level three 3192 of 3192, closure 100.0%. All self-hosting.
- **Fact.** The level-two review holds 26 records (9 admit, 11 exclude, 6 defer). The level-three review holds 4 admits. Those 30 records equal the 28 pool words plus the 2 citation forms `dedicate` and `flux`.
- **Fact.** No batch word has a decision in an earlier review under its own name, so no prior decision was given a new one.
- **Fact.** Pre-existing vocabulary entries are unchanged. The 13 new entries are the 9 and 4 admitted here. The seed books change by addition only. The 13 headwords appear verbatim in the seed books.

## 2. Definitions

- **Fact.** All 13 definitions pass `epagoge.vocabulary.unlicensed` at their level.
- **Fact.** `incompressibility` (level three) is defined as "the property of being incompressible", which only restates the word. Proposed: "Incompressibility is how much a substance pushes back when it is squeezed into a smaller space." Ceiling ok. "resists" is not admitted at level three, so "resists being squeezed" is rejected.
- **Fact.** `flux` (level three) is defined as "a flow of something", the water-cycle sense the README gives, which is imprecise. Optional proposal: "A flux is the amount of something that flows through an area in a given time." Ceiling ok. This changes the sense, which is the operator's choice.
- **Inference.** The other eleven definitions are correct, grounded and within their levels. `dedicate` is defined in the source's sense, which the README discloses. The sense limit is a judgement the operator may want to review.

## 3. Deferrals and exclusions

- **Fact.** The nine Spanish exclusions cite that the string is not an English headword, which is sound.
- **Fact.** The two inflected exclusions, `dedicated` and `fluxes`, cite their citation forms admitted at level three, which is sound.
- **Fact.** The five deferrals cite page-interface use only, as in the fifth batch.
- **Inference.** The deferrals are sound on the stated rule. `abstract` is a common English word, and its deferral rests on the scan's note that it is frequent only in interface text. That is a reasonable reading, but it should be checked against a prose sample before a later decision.

## 4. Changes outside the batch

- **Fact.** `src/epagoge/inflection.py` and `tests/test_candidates.py` changed only by the fifth batch's entries and by the new `level_2_agency_06` line in the test list. Neither changed in this batch's tables.
- **Fact.** The measurement files that changed (fourteen earlier level-two files) differ only in `after`, `closure` and `remaining_gap`, and `after` now records 2,996.
- **Fact.** `docs/process/HANDOFF.md` and `docs/process/RESUME_PROMPT.md` are modified in the working tree. I did not review them, as they are outside this batch.

## 5. Prior decisions

- **Fact.** No earlier review file changed, and no earlier admitted word changed its entry.

## Issue: the accounting in the README is incomplete

- **Fact.** The README says that of the first pool's 80 undecided strings, 52 are admissible at level two through existing headwords, and that "organics" is the only one in no reviewed-forms list.
- **Fact.** Among the 253 strings the pool rule removed as admissible, 75 have no decision under their own name. Of those, 53 are listed as reviewed forms of a first-pass headword and 5 of a later headword. 17 are listed in no reviewed-forms list. They are `buildings`, `colored`, `cooling`, `cools`, `experiencing`, `flooding`, `graphics`, `mining`, `oils`, `organics`, `peoples`, `powered`, `sampling`, `soaps`, `united`, `waters` and `wells`.
- **Fact.** Each of the 17 is frequent in the first scan, and each is admissible only because the lookup strips a suffix to a headword.
- **Inference.** The 17 are likely part of the first pool, which would make the README's statement that only `organics` is unaccounted for incorrect. I did not verify this, because the first pool's 243 strings are not recorded in the repository. Re-running the first pool rule would settle it.
- **Consequence.** Under the completion condition, a pool word needs an admission, an exclusion or a deferral in a review record. These 17 currently have none. The operator should decide each one, most likely as forms of their citation headwords, and the README should be corrected to match.

## Limits

- I did not run the test suite on this tree.
- The definitions were not checked against source pages.
- I did not reconstruct the first pool, so the 80 and 52 figures are unverified.
