# Trial 7 review: Part A summary and Part B, luna's reports

Reviewer line, Fable model. Edits nothing tracked. Each statement is marked
Fact, Inference or Judgement.

**Stamp.** Fact. HEAD aae4abe2187fc08289ed6ad85c67d672a84e7970. Working
tree blobs by git hash-object at the time of every command below:
curriculum/vocabulary.json 26fd70343c9a9193e97d22e2fafa176957f04d56,
level-two seed book f9a6a9b0, level-three seed book f03ee7bf. The operator
reports that the worker is applying the decisions on findings F1 to F3 in
parallel. Those changes had not reached the vocabulary when Part B ran, and
they are not reviewed here.

## Part A, the long-tail batch

The full Part A review is tmp/dromon-trial-8/review-part-a.md.

- **Fact.** Every one of the 607 pool strings has exactly one decision. The
  110 further keys are citation forms admitted in place of pool inflections.
  All 480 admissions agree across review.json, the vocabulary, the seed
  book, provenance and the thesaurus, and every definition passes
  epagoge.vocabulary.unlicensed at its level.
- **Fact.** The measurement check, the closure validator at levels one to
  three, the key-level diff against HEAD, 727 tests, ruff and pyright all
  pass. The full gate, the coverage floor, graph and corpus validation and
  the disclosure scan were not run by me.
- **Findings, with the operator's decisions.** F1: efficiencies,
  particulates and runups were excluded as plurals of mass nouns while the
  sources use them as count plurals. Decision: deferred. F2: the forms
  translates and dips sat under headwords lacking the sense the sources
  use. Decision: dip gains the verb sense, translates is deferred. F3:
  absorber, graduate and terrace wordings. Decision: applied.
- **Gap.** The level-three batch has no measurement.json, so the 104
  level-three admissions have no increment check. This stands from the
  sixth trial.

## Part B, luna's reports

### Reruns

- **Fact.** `python3 -I tmp/dromon-trial-8/stripped_forms.py "$PWD"`
  exited 0 and printed 160 rows. A script of mine compared every row with
  the table in stripped-forms.md: same 160 strings, same headwords, senses,
  totals and per-source counts, and every total equals the sum of its row.
- **Fact.** `.venv/bin/ruff check` and `ruff format --check` pass on the
  script.
- **Fact.** `python3 -I docs/process/trials/dromon_trial_6/readiness_terms.py
  "$PWD"` exited 0. I parsed the sixth-trial table, recomputed every unit's
  rank under the stated rule for the earlier and current counts, and
  compared all four columns of luna's 26-row table. All 104 cells match.
  The top five and the five thinnest concepts match the rerun. Every
  unit's combined sum grew and no concept's combined count fell.

### How the script reads the pool rule

- **Fact.** tools/candidate_pool.py removes a string as admissible when
  `Vocabulary.lookup` returns a term at or below the level. The script
  calls the same method and the same `surface_forms`, which is the word
  field plus the explicit forms field. Luna's statement of what counts as a
  listed form is exact.
- **Fact.** Of the 2,272 frequent strings, 583 are admissible at level two
  and 281 of those resolve to a headword other than themselves. The script
  omits 114 that are listed forms and 7 that a review excludes, leaving
  160. I reproduced the same partition independently.
- **Fact.** The sixth-trial batch level_2_stripped_forms deferred
  buildings, flooding, graphics, powered and united, and
  level_2_multi_source deferred based. All six are in luna's 160. The
  brief asked the script to drop only reviewed forms and exclusions, so the
  script follows the brief. The report does not say that six rows already
  carry a deferral, and its comparison says five of the earlier seventeen
  "remain in this list" without saying they were decided in the sixth
  trial. Judgement. This is the one place the report claims more than its
  count shows. A reader would take 160 as undecided strings, and 154 are.
- **Fact.** Luna's account of the other twelve of the seventeen holds.
  Seven are listed forms or term words, organics is a level-three term,
  and oils, peoples, soaps and waters are excluded under their own names.

### Three listed strings by hand

- **flooding, resolved to flood, weather, L2.** Fact. 141 occurrences, 123
  in the two NOAA and USGS texts, as "flash flooding", "coastal flooding"
  and "severe flooding". The headword is defined as "A flood is when so
  much water comes that it covers the land." Judgement. The source sense is
  the headword's, as luna says. The sixth-trial batch deferred it on the
  same reading rather than listing it as a form, and the report should say
  so.
- **graphics, resolved to graphic, writing, L2.** Fact. 153 of 165
  occurrences are the repeated heading "StarChild Graphics & Music:
  Acknowledgments". The headword is an adjective, "Graphic means given as a
  picture or a drawing." Judgement. The source's noun, meaning images, is
  not a sense the adjective entry carries, so luna's "probably related" is
  generous. The decision on file is a deferral for want of prose evidence,
  which fits.
- **roses, resolved to rise, falling, L1.** Fact. Seven McGuffey
  occurrences, all the flower. The lookup strips the s, finds rose among
  the forms of rise, and returns the verb. Judgement. The headword carries
  no such sense. The row is a correct report of the lookup and a wrong
  resolution, and the table has several like it, such as rating to rat,
  bearing to bear and james to jam. The report's closing inference covers
  this class but does not count it.

### Two omitted admissible strings by hand

- **dips.** Fact. Omitted as a listed form. The term dip, shape, L2 lists
  dips in its forms, and level_2_long_tail excludes dips as an inflected
  form of dip. The sources use it four times as a verb and twice as a noun.
  Judgement. The omission follows the rule. The verb gap is Part A finding
  F2, which the operator has decided.
- **corals.** Fact. Omitted because level_2_scan_06 excludes it as the
  plural of coral. Coral is a mass noun with no forms, so the string is not
  a listed form, and only the exclusion rule drops it. Nine of ten
  occurrences are the linked question titles "What are brain corals?" and
  "What ocean basin has the most corals?". Judgement. The omission is
  correct, and the record is consistent with the batch's treatment of
  mass-noun plurals.

### One actionable row the report does not draw out

- **tornadoes, resolved to tornado, weather, L2.** Fact. 96 occurrences in
  prose, and the term's forms field lists only tornados. Luna's judgement
  that the sense matches is right. Inference. The useful outcome is a
  forms-field addition of tornadoes to the term, not a new headword, and
  the report stops at the judgement.

### Does either report claim more than its count shows

- **stripped-forms.md.** Judgement. Yes, in one respect, the six deferred
  rows noted above. Otherwise the method paragraph states its filters
  exactly, the ten judgements are marked as readings of two or three lines,
  and the closing inference says plainly that a lookup match does not
  establish sense. The count of 160 is reproduced.
- **readiness-delta.md.** Judgement. No. Every number is reproduced, the
  ranking rule is stated, and the report says twice that a count measures
  vocabulary on file and not whether a module can be written. One
  limitation it does not state is that the counts include the sixth
  trial's uncommitted batches as well as this one, so the delta is not
  attributable to the long-tail batch alone.

## Not checked

- The teacher's address, which the line rules forbid me to call.
- The worker's fixes to F1 to F3, which postdate the stamp.
- Luna's judgements on the seven most frequent strings I did not read by
  hand: united, basics, buildings, based, woods, causing and accounted.
