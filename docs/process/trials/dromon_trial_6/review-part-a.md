# Review of the seventh-trial lexicon batch, Part A

**Stamp.** HEAD is aae4abe2187fc08289ed6ad85c67d672a84e7970. Committed blobs: level-two seed book 29f168d4970649c33613cea29c3f2897d73f8750, level-three seed book 8c2a94e6956d362c20fedcdfd17c4732ebb6c897, curriculum/vocabulary.json db49acc931a742f99ead34f059ace7ace7f466ce. Working-tree blobs: level-two seed book 9a1dd8f2fcb3f9d727963dc1482dbe32741dc102, level-three seed book a3aa91a459a26be1e2f5da5e31872fe8d1b29a07, curriculum/vocabulary.json e4187a17a4a280d0b1779b10656f3edfa3eeec64.

**Fact.** I edited nothing tracked, applied no diff, did not commit, did not load the teacher, and did not run tools/check.sh. Scratch files are under $TMPDIR. Withdrawn strings: none were reported by the operator for this batch, so none were counted.

**Fact.** The brief and condition were read. Both were written for this batch, not the earlier trials.

## 1. Completion-condition clauses

- **Fact.** `.venv/bin/python tools/measure_lexicon_increment.py evals/review/level_2_stripped_forms --check evals/review/level_2_stripped_forms/measurement.json` printed "increment measurement matches the tree" and exited 0. Level two went from 2996 to 2997 headwords. Seven admissions, six of them second senses, give growth of one.
- **Fact.** `level_3_stripped_forms` has no measurement.json. Its README says that the level-three admission is not counted by the level-two measurement. The completion condition asks that the increment measurement match the tree. This clause is therefore met for level two only, and the level-three admission has no measurement check. (Gap.)
- **Fact.** Closure, run as `PYTHONPATH=src .venv/bin/python tools/validate_closure.py curriculum/vocabulary.json curriculum/books/level_N N`, exited 0 at each level. Level one: 849 of 849 defined, grounded 853, closure 100.0%. Level two: 2996 of 2996 defined, grounded 2997, closure 100.0%. Level three: 3194 of 3194 defined, grounded 3195, closure 100.0%. All report self-hosting yes.
- **Fact.** All eight new definitions pass `epagoge.vocabulary.unlicensed` with the default exact reading at their own level. This is the seven level-two definitions and the one level-three definition. The lenient reading also passes.
- **Fact.** Review records: `review.json` at level two holds 22 entries, which are the 17 pool strings plus the citation forms color, cool, experience, flood, sample and well. Admitted are seven at level two (six second senses and mining) and one at level three (organics). Deferred are four (buildings, graphics, powered, united). Excluded are eleven. The 17 pool strings match the operator's list.
- **Fact.** No word with a decision before this brief has a new decision. The first-sense entries of color, cool, experience, flood, sample and well are unchanged in `curriculum/vocabulary.json` (no existing term changed; 501 terms added, none removed).

## 2. The 17 strings against the sources

I read every use of each string in the three named agency sources: `tmp/lexicon-sources/src_nasa_kids_earth.txt`, `tmp/lexicon-sources/src_nasa_starchild_l1.txt` and `tmp/lexicon-sources/src_usgs_water.txt`. I also checked the pre-batch lookup against the HEAD copy of `curriculum/vocabulary.json`.

| String | Pre-batch lookup | Source use | Decision | My view |
|---|---|---|---|---|
| buildings | build (verb, level 1) | noun, structures ("tall buildings", "a line of buildings") | defer | Sound. The noun would share a form with build's "building". |
| colored | color (noun, level 1) | adjective and participle ("lighter colored surfaces", "colored water") | exclude, form of verb color (second sense) | Acceptable. The participle is the nearest verb form, but the source sense is adjectival. Keep, and say so in the reason. |
| cooling | cool (adjective, heat) | gerund and noun modifier ("cooling effects", "cooling systems", "cooling their feet") | exclude, form of verb cool (second sense) | Acceptable. The verb reading of cool carries "cooling of facilities". |
| cools | cool (adjective) | third-person verb ("Earth's surface cools") | exclude, form of verb cool | Sound. |
| experiencing | experience (noun, knowing) | verb ("what we are mostly experiencing", "are experiencing groundwater depletion") | exclude, form of verb experience (feeling) | Sound. |
| flooding | flood (noun, weather) | noun, an event ("more flooding in some places", "coastal flooding", "localized flooding") | exclude, form of verb flood (liquid, second sense) | **Not sound.** See finding A. |
| graphics | graphic (adjective) | credit heading and award name only | defer | Sound. |
| mining | mine (pronoun, having) | noun, the industry or activity ("mining, and aquaculture", "mining water use") | admit, mass noun, raw_and_made, level 2 | Sound. The definition is the activity. The mining-industry sense is near enough. |
| oils | oil (mass noun, liquid) | plural listing kinds ("oils, soaps and chemicals") | exclude, plural of a mass noun | Sound on the stated policy that mass nouns take no plural. Not a sense the vocabulary can carry. |
| organics | organic (adjective) | noun beside sediment ("Sediment and organics color natural water") | admit, plural-only noun, living_and_not_living, level 3 | Sound. "Organic carbon is a material left over from dead plants" (NASA) and "organic matter coming from leaves, roots, and plant remains" (USGS) support the definition. |
| peoples | person (noun; form "people") | possessive written "peoples'" ("peoples' uses", "peoples' needs") | exclude, misspelt possessive | Sound. The reason says the possessive is a form of person. It is the plural "people", not the possessive. Reword. |
| powered | power (mass noun, force) | adjective in one headline, "Nuclear-Powered" | defer | Sound. |
| sampling | sample (noun, quantity) | gerund of the act ("sampling must follow strict guidelines") and noun modifier ("snowpack-sampling pit") | exclude, form of verb sample (checking, second sense) | Acceptable. The act sense is the verb's gerund. |
| soaps | soap (mass noun, liquid) | plural listing kinds ("oils, soaps and chemicals") | exclude, plural of a mass noun | Sound on the same policy as oils. |
| united | unit (noun, unit) | only "United States" | defer | Sound. The verb unite has no headword. |
| waters | water (mass noun, liquid) | plural of places ("ocean waters", "local waters", "natural waters") | exclude, plural of a mass noun | Sound on the same policy as oils. |
| wells | well (adverb, good_and_bad) | noun, water supply ("draw out water via wells", "Wells are extremely important") | exclude, form of noun well (liquid, second sense) | Sound. |

Second-sense admissions:

- **color (change, verb), cool (change, verb), experience (feeling, verb), sample (checking, verb).** The sources use these verbs. The definitions fit the uses. Sound.
- **flood (liquid, verb).** Not supported by the sources. See finding A.
- **well (liquid, noun).** Sound. The source uses wells as water supply, and the definition is "a deep hole dug in the ground to get water".

**Finding A. Flooding.** The batch's README says that flooding's stripped headword is flood, and that the lookup "resolved to an admitted sense that is not the one the source uses". The HEAD vocabulary shows the lookup returned the noun flood (weather), admitted at level two, and the sources use flooding as that noun. The three sources contain no verb use of flood. The second sense admitted for the verb, "To flood is for water to cover land that is usually dry", is therefore a sense the sources do not use, and flooding is excluded as its form. The decision contradicts the batch's own rule, and the exact check passes only because the verb entry carries the form.

- **Proposed change.** Record flooding as a form of the existing noun flood (weather) if the noun's forms can carry it. That edits flood (weather)'s forms, which is a change to an entry from before this brief. The operator must decide that. Otherwise, drop the verb second sense for flood and exclude flooding with the reason that its sense is the noun already admitted, which would then fail the exact check. I recommend the first option, and I did not test it.

**Finding B. Disclosed gap.** The batch README discloses in its Limits section that the closure validator keys definitions by word, and that the three second senses were checked only when authored. The disclosure is accurate. Finding D below confirms it.

## 3. Changes outside the batch

- **Fact.** Level-two seed book: 372 records added against HEAD, none removed, none changed. Level-three seed book: 129 added, none removed, none changed. The additions are the fifth batch, the sixth batch and this batch. I did not separate the fifth and sixth from this batch by record; the batch-level counts for this batch are seven level-two records and one level-three record.
- **Fact.** `curriculum/vocabulary.json`: 501 terms added against HEAD, none removed, none changed. The 501 includes this batch's eight: color, cool, experience, flood, mining, sample and well (second senses or new), and organics.
- **Fact.** `curriculum/thesaurus.json`: 501 (word, concept) pairs added against HEAD, none removed. This includes this batch's eight. The file is generated, so its churn is expected.
- **Finding C. Provenance overwritten.** `curriculum/provenance.json` changed for three existing words that this batch did not decide:
  - `color`: the source field changed from "scan 2026-09-27, frequent in a McGuffey reader and in modern federal material" to "scan 2026-10-10, frequent in at least one agency source". The first sense (physical_property, level one, admitted 2026-09-27) now has the wrong origin.
  - `cool`: source changed from null to the agency scan, and evidence from "reconstructed from history" to "recorded at admission". The first sense (heat, level one) now has an origin it does not have.
  - `well`: source changed from null to the agency scan, and evidence changed in the same way. The first sense (good_and_bad, level one) now has an origin it does not have.
  This is a misattribution, not a decision change. The project records origin because it bears on the corpus licence and on what a word was admitted for. It is not disclosed in the batch README. This needs a fix before commit: provenance keyed by word cannot hold a second sense, and the second sense overwrote the first's record.
- **Fact.** Fourteen earlier level-two `measurement.json` files changed. In each, only `after.2`, `closure.2.defined`, `closure.2.required`, `closure.2.validator_output` and `remaining_gap` differ. These are the expected fields, re-recorded at the live count of 2997.
- **Fact.** `src/epagoge/inflection.py` gained the verb color in the list of verbs whose final consonant does not double. It gained no other change in this batch. The fifth batch's entries are also in the diff and are not this batch's.
- **Fact.** `tests/test_candidates.py` adds the level-two stripped-forms batch to its list, and it now lets a second sense owe no growth.
- **Fact.** `tools/admit.py`, `tools/author_definitions.py`, `tools/measure_lexicon_increment.py`, `src/epagoge/book.py` and `tests/test_second_sense.py` changed as the brief describes. Their review is in the next section.
- **Fact.** `docs/process/HANDOFF.md`, `docs/process/RESUME_PROMPT.md`, `docs/process/CURRENT_BRIEF.md` and `docs/process/COMPLETION_CONDITION.md` are modified. I did not review them.
- **Fact.** No file under `generators/` or `src/epagoge/prompt.py` changed. No book outside the two dictionary seed books changed.

## 4. Prior decisions

- **Fact.** No term that existed at HEAD changed in `curriculum/vocabulary.json`. The first-sense entries of the six words are unchanged.
- **Fact.** No review file from an earlier batch changed.
- **Finding C** shows that provenance of three earlier words changed, which is not a decision but is a record of origin.

## 5. The tool change

### Correctness

- **Fact.** `tests/test_second_sense.py` ran 30 tests, all OK, with `.venv/bin/python -m unittest discover -s tests -p test_second_sense.py`.
- **Fact.** `tests/test_candidates.py` ran 39 tests, all OK, with the same runner. It took 130 seconds.
- **Fact.** `.venv/bin/python -m pytest` is not available. `pytest` is not installed in `.venv`, so I did not run the full suite with pytest. I did not install it, because that would change the environment. The full suite is therefore not run.
- **Fact.** `tools/admit.py` refuses a second sense that duplicates word and concept, a core word, a string that is a form of another word, and a word with no sense at or below the level. The tests cover these.
- **Inference.** The admission guard is sound on the cases it covers. It does not check that the second sense's definition is grounded at admission. `author_definitions.py` does check that, as Finding D shows.

### The closure gap

- **Fact.** `validate_closure.py` keys definitions by word through `word_definitions`, which keeps the first record of each word in a dictionary book. For experience, flood and sample, the first level-two record and the second-sense record are both at level two. The closure map holds the first sense only.
- **Fact.** I checked the map against each second-sense record. For experience, the map holds "Experience is what you come to know by doing.", and the second-sense record holds "To experience something is to feel it, or to have it happen to you." Flood and sample are the same case. For color, cool and well, the second-sense text is the only level-two text for the word, so the closure map holds it.
- **Fact.** I substituted the three unchecked second-sense texts into the closure map and reran `dictionary_closure`. The grounded count stayed at 2997, so their tokens are grounded. The gap is in the gate's coverage, not in a current failure.
- **Finding D.** So the gate does not recheck the three second-sense definitions. `author_definitions.py` does check them when they are authored. I re-ran the ceiling check for all three, and they pass. So the unchecked definitions are covered by the authoring check, but not by the gate that a later change would run.
- **What a fix needs.** `word_definitions` would need to return every dictionary record's text with its record id and its target word, not one text per word. `dictionary_closure` would need to check each text, and the coverage count would stay per word. Provenance would need the same change, keyed by record id or by (word, concept), to avoid Finding C.

### Other notes

- **Minor.** `sense_definition` in `src/epagoge/book.py` falls back to the word's canonical definition when a second-sense record is missing. A missing record could then pass the measurement if the texts happen to match. This does not occur in this batch.

## Limits

- I did not run the full test suite. pytest is not installed in `.venv`.
- I did not check the definitions against the source pages beyond the sense checks above.
- The level-three admission has no measurement check (Section 1).
- Finding A depends on a judgement about the flooding decision, which the operator must make.
- Finding C is from a comparison with HEAD, not from the batch's own records.
