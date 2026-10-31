# Review of the fifth agency batch, Part A

**Stamp.** HEAD is aae4abe2187fc08289ed6ad85c67d672a84e7970. Blob hashes: committed level two seed book 29f168d4970649c33613cea29c3f2897d73f8750, committed level three seed book 8c2a94e6956d362c20fedcdfd17c4732ebb6c897, working level two seed book 99d6bb49533dd3424bfe807e1c2976fd44b0d97d, working level three seed book 4b8e44431f8065da1f38e6f97b1bd046c8294530. The batch is uncommitted on top of HEAD. Commits since the last turn: 1ff7add and aae4abe.

**Fact.** I edited nothing tracked and did not run tools/check.sh.

## 1. Completion-condition clauses

- **Fact.** `tools/measure_lexicon_increment.py evals/review/level_2_agency_05 --check .../measurement.json` printed "increment measurement matches the tree" and exited 0.
- **Fact.** Closure, run as `PYTHONPATH=src .venv/bin/python tools/validate_closure.py curriculum/vocabulary.json curriculum/books/level_N N`, reported: level one 849 of 849 defined, closure 100.0%; level two 2986 of 2986, closure 100.0%; level three 3179 of 3179, closure 100.0%. All self-hosting. The tool expects the single level's book directory. Passing `curriculum/books` reports 0 of 849 defined, so the usage message matters. I did not check its exit code in that run.
- **Fact.** Counts: 356 level-two admissions, 124 level-three, 122 exclusions, 43 deferrals. Those 645 records equal the 571 pool words plus the 74 citation forms the README reports. I checked the arithmetic, not each pool string against the candidate file, and I did not identify any withdrawn string.
- **Fact.** Zero pre-existing vocabulary entries changed or were removed against HEAD. No word in the batch has a decision in another `review.json`.
- **Inference.** Prior decisions are unchanged, as the completion condition requires.

## 2. Definitions

- **Fact.** All 480 definitions pass `epagoge.vocabulary.unlicensed` at their level, with zero violations.
- **Fact.** Level two, `cement`: "left to dry" conflicts with the source's account of hardening. Proposed: "Cement is a gray powder that becomes as hard as stone when mixed with water and left to set." Ceiling ok. Whether the source supports "dry" was not checked against the page, so this is an inference from the general sense of cement.
- **Fact.** Level two, `abundant`: "there in large amounts" has no antecedent. Proposed: "Abundant means found in large amounts." Ceiling ok. "present" is a level-five headword, so it cannot be used at level two.
- **Fact.** Level two, `gypsum`: "used to make walls and powder" is unclear. Proposed: "Gypsum is a soft, white mineral used to make walls." Ceiling ok.
- **Fact.** Level two, `kilogram`: "a unit for measuring weight" uses the everyday sense the README discloses. Proposed: "A kilogram is a unit for measuring how heavy something is. It is one thousand grams." Ceiling ok. This is a choice for the operator, since the README already states the limit.
- **Fact.** Level three, `multiply`: "to add it to itself a given number of times" is ambiguous at one and zero. Proposed: "To multiply a number by another is to add the first to itself as many times as the second says." Ceiling ok.
- **Fact.** Level three, `chlorine`: "green gas" is imprecise. Proposed: "Chlorine is a chemical element. It is a yellow-green gas, and it is used to make water safe to drink." Ceiling ok. This rests on general chemistry, not the source.
- **Fact.** Level three, `pathogen` conflicts with level two, `virus`. The level-two definition calls a virus "a very small thing", while `pathogen` says "a very small living thing, such as a virus". Proposed: "A pathogen is a very small thing, such as a virus, that causes disease." Ceiling ok. "bacterium" and "germ" are not admitted at a level that permits them here.
- **Fact.** Level three, `evapotranspiration`: the definition names water, not the process. Proposed: "Evapotranspiration is the movement of water into the air from land, water and plants together, by evaporation and transpiration." Ceiling ok.
- **Inference.** The remaining definitions read as faithful to their stated sources. I did not check them against the source pages, which the worker's README does not require.

## 3. Deferrals and exclusions

- **Fact.** Reasons cite one of a small set of grounds: an inflected form of a headword admitted or decided elsewhere, a headword already filed at a higher level, a site-interface-only sense, an abbreviation or clipped form awaiting a separate decision, or a sense past level three.
- **Inference.** These reasons are sound. Two cases depend on prior policy, namely the handling of clipped forms and joined names, and the record states that each is a separate decision.

## 4. Changes outside the batch

- **Fact.** Tracked changes are the two seed books, `provenance.json`, `thesaurus.json`, `vocabulary.json`, the process brief and condition, 14 `measurement.json` files, `src/epagoge/inflection.py` and `tests/test_candidates.py`. The brief and condition changed in the working tree.
- **Fact.** The seed book diffs contain additions only. In each measurement file the changed keys are `after`, `closure` and `remaining_gap`, which are the expected fields.
- **Fact.** `inflection.py` adds five irregular verbs, three irregular plurals and four entries in `NO_DOUBLE_MULTISYLLABIC`. Each carries a comment naming its basis.
- **Unverified.** I did not run the test suite on this tree.

## 5. Prior decisions

- **Fact.** No pre-existing entry changed. The seed books changed by addition only.
- **Inference.** Consistent with the completion condition.

## Concerns outside the checked scope

- The pool string-by-string coverage was not checked, only the arithmetic.
- The definitions were not checked against source pages.
- The test suite was not run.
