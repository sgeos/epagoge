# Trial 7 review, Part A: the long-tail batch

Reviewer line, Fable model. Edits nothing tracked. Each statement is marked
Fact (observed by a command or a file read), Inference (drawn from facts),
or Judgement (a reading of sense or level that another reader may dispute).

**Stamp.** Fact. HEAD is aae4abe2187fc08289ed6ad85c67d672a84e7970. Working
tree blobs by git hash-object: level-two seed book
f9a6a9b017336e786cb3aefb733ccf2fee2d3caa, level-three seed book
f03ee7bf8d77f49c25afb2425448c4824a36c80f, curriculum/vocabulary.json
26fd70343c9a9193e97d22e2fafa176957f04d56. The same files at HEAD are
29f168d4, 8c2a94e6 and db49acc9. The fourth to sixth trials' batches are
also uncommitted, so differences against HEAD include them, and this review
separates the long-tail batch's share where it can.

## 1. Completion-condition clauses about the batch

| Clause | Command | Result |
| --- | --- | --- |
| A review record for each of the 607 strings, 6 withdrawn as a count | reviewer_checks.py (section 2) | Fact. 607 strings each have exactly one decision across the two review files. pool.json holds 613, pool.txt 607, difference 6. authoring.json records pool_size 607 and operator_withdrawn 6. |
| Each string admitted with one definition, or a reviewed form, or deferred or excluded with a reason | reviewer_checks.py | Fact. 376 admits, 92 defers, 145 excludes at level two; 104 admits at level three. Every admit has one definition; every defer and exclude has a reason. Three exclusions name a headword that does not carry the form, by stated choice (finding F1). |
| Level-three admissions recorded in level_3_long_tail | reviewer_checks.py | Fact. 74 pool strings and 30 citation forms are admitted there, all at level 3 in the vocabulary. |
| Each batch's increment measurement matches the tree | `PYTHONPATH=src .venv/bin/python tools/measure_lexicon_increment.py evals/review/level_2_long_tail --check evals/review/level_2_long_tail/measurement.json` | Fact. Prints "increment measurement matches the tree", exit 0. Level three has no measurement.json, as its README says. The gap the sixth-trial review noted stands. |
| No earlier review decision changes | reviewer_checks.py, all evals/review/*/review.json | Fact. Exactly one key in the batch has an earlier record: bond, admitted as a noun in level_3_agency_05. The batch record is flagged second_sense and the earlier record is unchanged. |
| No existing record in provenance.json or vocabulary.json changes | `python3 tmp/dromon-trial-8/keydiff.py curriculum/provenance.json words senses --changed-only` and `... curriculum/vocabulary.json terms=word,concept --changed-only` | Fact. provenance words 973 added, 0 removed, 0 changed; senses 7 added, 0 removed, 0 changed; vocabulary terms 980 added, 0 removed, 0 changed. The other vocabulary sections are identical to HEAD. thesaurus.json senses=word,concept: 980 added, 0 removed, 0 changed. Inference. 973 plus 7 equals 980, so every added term has a provenance entry. The additions include the fourth to sixth trials. |
| Required coverage complete at levels one and two, closure grounded at one to three | `PYTHONPATH=src .venv/bin/python tools/validate_closure.py curriculum/vocabulary.json curriculum/books/level_N N` for N in 1, 2, 3 | Fact. Level 1: 849 of 849, grounded 853, 815 records, self-hosting yes. Level 2: 3371 of 3371, grounded 3372, 2531 records, yes. Level 3: 3672 of 3672, grounded 3673, 302 records, yes. All exit 0. Note the tool takes the vocabulary path first; the operator's example form without it fails with IsADirectoryError. |
| tools/check.sh exits 0 with no skipped tests | Not run, as instructed. Ran the parts separately. | Fact. `env PYTHONPATH=src .venv/bin/python tools/run_tests.py`: Ran 727 tests in 101.7 s, OK, no skips, exit 0. `.venv/bin/ruff check .` all checks passed. `.venv/bin/ruff format --check .` 823 files already formatted. `.venv/bin/pyright` strict: 0 errors, 0 warnings, 0 informations, exit 0. Coverage floor, graph and corpus validation and the disclosure scan were not run. The worker reports the full gate passed; I did not verify that. |
| No book changed except the two seed books; nothing under generators/ or prompt.py | `git status --short` | Fact. The only paths under curriculum/books in the status are the two seed books. Nothing under generators/ and no prompt.py appears. |
| No teacher loaded, no text fetched | Hashes only | Fact. authoring.json records teacher null. The sixteen source files' sha256 match source_hashes in pool.json, and pool.json, scan_f4.json and pool.txt match the hashes in authoring.json. I did not call the teacher's address, as the line rules forbid it, so the teacher clause is not verified by me. |

## 2. Mechanical checks

Fact. Script tmp/dromon-trial-8/reviewer_checks.py, output saved in
tmp/dromon-trial-8/reviewer_checks_output.txt. Exit 0, FAIL count 0, NOTE
count 3. The first version of the script reported 17 failures, 14 of which
were its own defects: it compared part-of-speech strings by order where the
admit tool sorts them, it matched the past-tense decision names used in
reasons against the present-tense decision field, and it did not parse the
wording for a form of a second sense. The second version corrects those.

What it verified, all Fact:

- Every one of the 607 pool strings has exactly one decision. 110 further
  keys are citation forms added in place of pool inflections, 80 at level
  two and 30 at level three, and every one is an admit.
- 480 admitted records. For each: exactly one vocabulary term with that
  word and concept, at the record's level, with the same part of speech
  set and source; reviewed_forms equals the headword plus the term's forms;
  a seed-book record exists with the identical text; admitted.json agrees;
  a provenance entry exists with this batch's source, in senses for the two
  second senses with the batch path; a thesaurus sense entry exists.
- Every admitted definition passes epagoge.vocabulary.unlicensed at its
  level with the default exact matching. 0 failures.
- 142 form reasons checked. Every exclusion "form of X" names a headword
  that exists, and X's entry lists the form, except the three NOTE cases
  below. Each "admitted in this batch", "admitted in level_3_long_tail" and
  "earlier batch at level three" claim holds. Each deferral "form of X,
  which BATCH deferred or excluded" matches that batch's record.
- Four deferral reasons name a word without an earlier batch (clearer,
  indices, millennia, strung). Read by hand: clear is a level-one verb,
  string a level-one noun, index and millennium are not headwords. The
  reasons are accurate.
- authoring.json hashes and measurement.json artifact hashes match the
  files. Growth 375 equals 376 admitted minus 1 second sense.

NOTE cases. efficiencies, particulates and runups are excluded as the
plural of a mass noun whose entry does not carry the plural, and the reason
says so. See finding F1.

## 3. Hand sample

Concordance script tmp/dromon-trial-8/reviewer_concordance.py, output in
reviewer_concordance.txt, 71 strings, up to five snippets each from the
sixteen sources.

### Fixed sample, pool.txt lines 1, 16, 31 and every fifteenth after (41)

Fact for the decisions and source uses; Judgement for "fits".

Fits, no change proposed (32): absorber (see F3), antibiotics, assessments,
belief, bonded, carriage, chiefly, communicate, cottage, delivery,
doorstep, ecoforecasting, evacuate, fastened, fled, hopefully, inaccurate,
instructions, kelp, lighthouses, mathematics, mist, oak, pad, percolate,
porcelain, propeller, ranking, resilience, sails, seventh, soo,
strengthens, supermassive, unreinforced, voltage, worthy.

Would change (4):

- **dip** (level two, shape, noun). Fact. The sources use the noun (jet
  stream dip, "dips, low spots") and the verb ("Dip a paper towel", "the
  hydrologist just dips a bottle", "the cable dips"). The pool string dips
  is excluded as a form of dip, but the verb sense is not carried.
  Proposed: pos "noun verb", definition "A dip is a place where something
  goes down a little and then up again, and to dip something is to put it
  into a liquid for a short time." Licensed at level two.
- **translates** (excluded as a form of translate). Fact. All six source
  uses are "this translates to more than 14.5 million storms" or "the
  meter translates the voltage difference into pH". None is the language
  sense, which is the only sense translate's definition gives. The brief
  admits a form only where the headword carries its sense. Proposed
  definition for translate: "To translate is to change words from one
  language into another, or to change one thing into another form."
  Licensed at level two.
- **graduate** (level three, knowing, noun). Fact. Four of seven uses are
  "graduate student", "graduate level", "Graduate Program", where the word
  describes study after college. One is "recent graduates". Proposed: "A
  graduate is a person who has finished school or college, and graduate
  study is study done after college." Licensed at level three. Judgement:
  minor.
- **terrace** (level three). Fact. All four uses are marine terraces
  formed by the sea. "cut into a slope" reads as made by people. Proposed:
  "A terrace is a flat step of land on a slope, made by people or by the
  sea, or a flat area beside a building." Licensed at level three.

Comment, Judgement. 41 level-two admissions carry an empty part of speech,
all adverbs or pronoun-like words (chiefly, hopefully, everybody,
whenever). Fact. The vocabulary has no term with pos adverb at or below
level two and 465 terms there without a pos, and the fifth batch did the
same for 32 words. So this is the standing convention, not a defect of
this batch.

### First fifteen level-three admissions

Fact for uses, Judgement for fit. absorber, academic, acidification,
advent, agent, antibiotic, artery, aspect, assessment, baseline, bond,
calibrate, catalyst, certify, characteristic.

- All fifteen definitions match a sense the sources use, and the level
  three placement fits the calibration of entering eighth grade.
- antibiotic and artery have no singular in the sources; the plurals are
  the pool strings, and the singular is the citation form reviewed in its
  place. Correct under the batch's method.
- agent has one singular use, "wetting agent", and the pool plural in
  "possibly-harmful agents". The definition fits the plural use.
- **absorber** (F3). Fact. Four uses are the solar collector's absorber and
  one is "shock absorber". The definition "a dark part of a heater that
  takes in heat from the sun" is narrower than the word. Proposed: "An
  absorber is a part made to take in heat, light or a push instead of
  letting it pass, such as the dark plate of a solar heater." Licensed at
  level three. Judgement: minor, the admitted sense is one the sources
  use.
- **characteristic**. Fact. Two of four uses are the adjective ("is
  characteristic of small streams"). The noun definition is correct for
  the other two. Judgement: acceptable; an adjective sense could be added
  later as a second sense.
- bond. Fact. The sources use the verb for water molecules and atoms
  bonding. The second sense is correctly filed and the noun record is
  unchanged.

### First fifteen deferrals or exclusions not a form, a name or a fragment

Fact for uses, Judgement for fit. antimeridian, aphelion, applicators,
bacterium, barrages, bathypelagic, bibliography, bid, biogeography,
biologic, blest, breeches, buffering, catcher, cinnabar.

- All fifteen decisions fit the stated reason. The technical terms
  (antimeridian, aphelion, bathypelagic, biogeography, buffering,
  cinnabar) are used in the sources only in the specialised sense.
  Judgement: antimeridian and aphelion are defined in the sources' own
  prose for young readers and could be level three or four; deferral
  rather than exclusion leaves that open, which is right.
- bid, blest and breeches are archaic or literary in the McGuffey readers
  ("do as you bid me", "truly blest", "knee breeches"). Deferral follows
  the brief.
- bacterium is deferred because filing the singular would change the
  plural-only entry for bacteria. The reason is accurate.
- applicators, barrages and biologic are set-phrase or variant uses.
  Accurate.
- bibliography and catcher occur only in publication titles or link text.
  Accurate under the fifth pass's interface rule.

## 4. Changes outside the batch directories

- **src/epagoge/inflection.py.** Fact. The diff against HEAD adds, to
  IRREGULAR: bind, cling, rid, transmit, withdraw, fight, flee, overcome,
  submit, underlie; to IRREGULAR_PLURAL: salmon, snowman, tomato, workman,
  basis, catfish, shellfish; to NO_DOUBLE_MULTISYLLABIC: blossom, differ,
  fasten, interpret, lessen, recover, shorten, strengthen, threaten,
  abandon, alter, deliver, inhabit, color. Fact. Every word the README does
  not list (bind, cling, rid, transmit, withdraw, basis, catfish,
  shellfish, abandon, alter, deliver, inhabit, color) is admitted in
  level_2_agency_05 or level_2_stripped_forms, and every word the README
  lists is admitted in this batch. Inference. The batch's share of the
  diff is exactly what its README states.
- **tests/test_candidates.py.** Fact. The diff adds four batch names to
  the stacked-measurement list and relaxes the growth assertion by the
  second-sense count. The sixth-trial Part A review records the
  stripped_forms line and the second-sense relaxation as that trial's.
  Inference. This batch added the level_2_long_tail line only, as its
  README says.
- **Fourteen tracked measurement.json files** (agency, agency_02 to 04,
  one_source, scan_02 to 10). Fact. `git diff -U0` shows the same changed
  lines in each: after.2 2631 to 3372, remaining_gap 7369 to 6628,
  closure.2.defined and required 2630 to 3371, and the two
  validator_output strings, which gain a "records" line and the new
  counts. No other field changes. Inference. These are the fields the live
  headword count and validator output drive, and only those.
- **Three untracked measurement.json files** (agency_05, agency_06,
  stripped_forms). Fact. Modified at 15:21 with the batch. Each now
  reports after.2 3372. No HEAD copy exists to diff. The test
  TestStackedScanMeasurements re-derives every stacked measurement and
  passed in the 727-test run.
- **curriculum/provenance.json _comment.** Fact. One sentence added
  describing the senses section. Inference. This came with the sixth
  trial's word_provenance.py change, modified 13:27, not with this batch.
- **curriculum/thesaurus.json.** Fact. 3945 insertions and 25 deletions in
  the text diff, but 980 added and 0 changed or removed by (word, concept)
  key. Inference. The deletions are re-serialisation of list boundaries.
- Fact. Nothing else in `git status` is attributable to this batch. The
  process documents, tools, src/epagoge/book.py and the new test files
  were modified between 12:26 and 15:01, before the batch wrote at 15:21.

## Findings, ranked

- **F1, decision.** efficiencies, particulates and runups are excluded as
  plurals of mass nouns, but the sources use each as a countable plural
  ("greater efficiencies", "fewer emissions of particulates", "Tsunamis
  with runups over one meter", "Most runups are less than 10 feet"). The
  batch deferred bacterium for the same situation, an entry that would
  have to change. Judgement: these three should be deferred, not excluded,
  with the reason that the sources use a countable plural of a word filed
  as a mass noun and the earlier entry is a separate decision. Exclusion
  with the present wording records them as closed.
- **F2, fix before commit.** translates is recorded as a form of translate
  while the sources use only the "convert or amount to" sense, which the
  headword's definition does not carry. dips is recorded as a form of dip
  while the sources use the verb, which the noun-only entry does not
  carry. Proposed wordings above are licensed at level two.
- **F3, wording.** absorber, graduate and terrace definitions are narrower
  than, or slanted away from, the sources' uses. Proposed wordings above
  are licensed at level three. Minor.
- **Gap, repeated from trial six.** Level-three admissions have no
  measurement check. The closure validator at level three is the only
  mechanical gate on them, and it passed.

## Not checked

- tools/check.sh, the coverage floor, graph and corpus validation and the
  disclosure scan were not run.
- Level judgements for the 480 admissions were read only for the 71
  sampled strings.
- The six withdrawn strings were counted, not read.
