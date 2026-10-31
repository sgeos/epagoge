# Stripped forms of the first agency scan, level two

Recorded 2026-10-30. This pass fetched nothing and did not rescan. It
decides 17 strings from the first agency scan of 2026-10-10, kept at the
ignored `tmp/lexicon-sources/scan_agency.json`, which covers NASA
children's earth pages, a StarChild level 1 sample and USGS Water Science
School pages. No teacher ran.

The first pass recorded its source as public domain. Whether each page is
a work of a federal employee was not checked again here, so the source
recorded on each term in this batch says agency source and does not say
public domain, as in the fifth and sixth passes.

## How the pool was fixed

No pool tool drew this pool. The operator fixed it as the 17 strings that
the fifth trial's review, `docs/process/trials/dromon_trial_5/review-part-a.md`,
found frequent in the first agency scan, admissible at level two only
because the lookup strips a suffix to another headword, and listed in no
reviewed-forms list. They are buildings, colored, cooling, cools,
experiencing, flooding, graphics, mining, oils, organics, peoples, powered,
sampling, soaps, united, waters and wells. The operator screened them, and
there was no pool stop.

The strings are kept as the ignored `tmp/dromon-trial-7/strings.txt`.
`authoring.json` records it as the pool report with its hash, and records
the scan's hash.

## How each string was read

For each string the agent read every use in the three agency sources, the
ignored `tmp/lexicon-sources/src_nasa_kids_earth.txt`,
`tmp/lexicon-sources/src_nasa_starchild_l1.txt` and
`tmp/lexicon-sources/src_usgs_water.txt`. It then looked up which
headword the lookup strips the string to and in which senses that headword
is admitted. A stripped form carries an undecided sense when the source's
sense is not one of those.

## Decisions

Every string has a review decision.

| String | Lookup strips to | Decision |
| --- | --- | --- |
| buildings | build, a verb | Deferred |
| colored | color, a noun | Form of color, a verb admitted as a second sense |
| cooling | cool, an adjective | Form of cool, a verb admitted as a second sense |
| cools | cool, an adjective | Form of cool, a verb admitted as a second sense |
| experiencing | experience, a noun | Form of experience, a verb admitted as a second sense |
| flooding | flood, a noun | Deferred |
| graphics | graphic, an adjective | Deferred |
| mining | mine, a pronoun | Admitted at level two |
| oils | oil, a mass noun | Excluded as a form in the sense oil carries |
| organics | organic, an adjective | Admitted at level three |
| peoples | person | Excluded as a misspelt possessive of the plural people |
| powered | power, a mass noun | Deferred |
| sampling | sample, a noun | Form of sample, a verb admitted as a second sense |
| soaps | soap, a mass noun | Excluded as a form in the sense soap carries |
| united | unit, a noun | Deferred |
| waters | water, a mass noun | Excluded as a form in the sense water carries |
| wells | well, an adverb | Form of well, a noun admitted as a second sense |

Mining is admitted as a mass noun meaning digging rock, metal or coal out
of the ground. The lookup resolved it to the pronoun mine, which is a
different word. Organics is recorded in `evals/review/level_3_stripped_forms/`.

Five second senses are admitted at level two, namely color and cool as
verbs of change, experience as a verb of feeling, well as a noun under
liquid, and sample as a verb of checking. Each word's first sense is
unchanged. A word and concept pair carries one sense, so where a sense's
nearest concept was its first sense's, as heat is for cool and physical
property for color, the next nearest concept was chosen. The six pool
strings that are forms of these senses are excluded as separate headwords
and listed among their reviewed forms.

Oils, soaps and waters are plurals in the sense their headword already
carries, naming kinds of oil or soap or the water of particular places.
Each headword is a mass noun, so the plural is not added to its forms. In
the source, peoples occurs only before uses and needs, where it is a
misspelt possessive of the plural people. The plural meaning nations does
not occur.

Graphics occurs only in a credit heading and in the name of an award.
Powered is frequent only because one news headline repeats in the page
interface. United occurs in the three agency sources only in the name
United States. Buildings is the noun building, which is already a form of
the level-one verb build. A form shared by two different words is refused,
so filing the noun needs a change to the level-one entry for build, and
that is left as a separate decision. Flooding is used in the sources only
as the noun for the event, which is the sense of the noun flood already
admitted at level two, and the sources never use flood as a verb. Filing
flooding as a form of that noun would change an entry from before this
brief, which is also a separate decision.

Experience and sample already had admit decisions, in
`evals/review/level_2_scan_02/`, for their noun senses. Those decisions are
unchanged. The records here are keyed by the same words and decide new
senses, marked `second_sense` in `review.json` and `admitted.json`. No
word with a review decision from before this batch was given a new one.

## The operator's choice and the tool change

`tools/admit.py` refused any word already admitted at or below the target
level, and `tools/author_definitions.py` filed a new record under the
concept of the word's earliest sense, so no second sense could be filed.
The agent asked the operator, who chose on 2026-10-30 to extend the tools
with tests and to file six senses through them. Review later removed the
verb flood, as recorded under Review changes, so five remain.

`tools/admit.py` now admits a second sense when its entry carries
`"second_sense": true`. The sense is keyed by word and concept and gets its
own level, part of speech and forms. It keeps any form its own word already
carries, as `samples` serves the noun and the verb. Without the flag an
admitted word is refused as before. With it, the same word and concept are
refused at any level, and a word with no sense at or below the level, a
core word or a string that is a form of another word is refused.

`tools/author_definitions.py` accepts a second sense as an object with a
concept and a definition. Its record is `dict.LEVEL.WORD.CONCEPT` and
carries that concept, and it is written or reworded without touching the
word's other records. A plain definition never touches a second-sense
record. A second sense's text is checked against the grounded words when
it is authored, by the same rule the gate now applies to every record.

`tools/measure_lexicon_increment.py` now finds an admitted sense by word,
level and concept, reads a second sense's definition from its own record,
and does not count a second sense toward headword growth. It records
`second_senses` when a batch has any. The record id and the definition
lookup are shared through `src/epagoge/book.py`. The tests are in
`tests/test_second_sense.py` and include negative tests for each refusal.

## Measured

Level two rose from 2,996 to 2,997 distinct headwords, measured, because a
second sense adds no headword. Required definition coverage is 849 of 849
at level one and 2,996 of 2,996 at level two, and closure is complete at
both. Every dictionary record passes the per-record check, 815 at level
one and 2,155 at level two. The measurements of the earlier level-two
batches in the stacked test were recorded again after the review changes,
because the validator output they hold now reports the records checked.

    .venv/bin/python tools/measure_lexicon_increment.py \
      evals/review/level_2_stripped_forms \
      --check evals/review/level_2_stripped_forms/measurement.json

## Changes outside the lexicon

The verb color was added to the list in `src/epagoge/inflection.py` of
longer verbs whose final consonant does not double, so its forms are
colored and coloring. The validator refused the verb until it was listed.
The measurements of the earlier level-two batches that record the live
headword count were recorded again. This batch was added to the test that
checks those measurements, and that test now owes no headword growth for a
second sense, as the measurement does not. The full test suite was run on
a simulated copy of the tree before admission.

## Review changes

A review of this batch, recorded in the ignored
`tmp/dromon-trial-7/review-part-a.md`, made four findings that the
operator decided on 2026-10-30. They were applied as follows.

The sources use flooding only as the noun for the event and never use
flood as a verb. The verb second sense of flood was removed from
`curriculum/vocabulary.json`, the level-two seed book, the thesaurus and
this batch's candidates, review and admission records, and flooding was
deferred with the reason given above. The authoring declaration's input
hash was recorded again for the changed candidates.

The second senses of color, cool and well had replaced their first senses'
origin in `curriculum/provenance.json`, because the generator kept one
source per word and took whichever sense it read last. The three records
were restored to their state at the last commit. `tools/word_provenance.py`
now reads the second senses from the batches' `admitted.json` files, never
lets a second sense's source reach its word's record, and records each
second sense apart under `senses`, keyed by word and concept with its
source and batch. The gate's comparison covers those records. A comparison
with the last commit shows that no word's record changed, and that every
word added is one admitted by this batch or by the fourth and fifth
trials' batches.

The closure gate read one definition per word, so the second senses of
experience and sample, filed at the level of their first records, were
never checked by it. `tools/validate_closure.py` now checks the text of
every dictionary record at the level against that level's vocabulary
ceiling and against the grounded words, while coverage is still counted
per word. Before the change, every existing record was checked by the same
rule at levels one, two and three, and none failed. The grounding rule is
shared with `tools/author_definitions.py` through `src/epagoge/book.py`.

The reason recorded for peoples was reworded to say that the string is a
misspelt possessive of the plural people.

The tests for the provenance and closure changes are in
`tests/test_sense_records.py`. They include a second-sense record at the
level of its word's first record that uses a word not licensed at that
level, which the gate now fails and before the change passed.

## Limits

The level, concept and sense of each word were judged by the agent against
`docs/decisions/LEVEL_CALIBRATION.md` and the sources, and that judgement
has not been reviewed independently. The concept chosen for the verbs of
cool and color is the nearest one free of a first sense, which is a weaker
fit than heat or physical property would be. Which sense of a word is its
second is known to the provenance generator only from the batch records,
so a second sense filed without `"second_sense": true` in its batch's
`admitted.json` would still reach its word's record.

`previous_CURRENT_BRIEF.md` and `previous_COMPLETION_CONDITION.md` are the
brief and condition met earlier on 2026-10-30, retained as historical
evidence.
