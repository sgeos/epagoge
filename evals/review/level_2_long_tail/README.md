# Long tail of sixteen sources, level two

Recorded 2026-10-30. This pass fetched nothing. It decides a pool drawn
from a scan at a threshold of four of the sixteen source texts that earlier
batches scanned, which are the four McGuffey readers of the first batch and
twelve texts from sites that `docs/decisions/AGENCY_SOURCES.md` lists as
candidates. No teacher ran.

Whether each agency page is a work of a federal employee was not checked
again here, so the source recorded on each term names the scan and does
not say public domain, as in the fifth and sixth passes.

## How the pool was drawn

`tools/scan_lexicon.py` counted the sixteen texts at a threshold of four.
`tools/candidate_pool.py` then selected the pool at level two with the
private term list applied and a minimum of one source, the rule every
earlier agency pass used. The pool held 613 strings. The operator withdrew
6 of them before any decision was made, recorded here as a count only, and
the remaining 607 are listed in the ignored `tmp/dromon-trial-8/pool.txt`.
There was no pool stop.

The scan and the pool are kept under the ignored
`tmp/lexicon-sources/longtail/`. `authoring.json` records the hash of the
scan, the pool report and the list of 607 strings, and records
`operator_withdrawn` as 6.

## How each string was read

For each string the agent read its uses in the sixteen texts, looked up
whether the string or a word it is a form of is already a headword at any
level, and looked up any review decision from an earlier batch on the
string or the word it is a form of. Every definition was checked against
the level's vocabulary before admission.

## Decisions

Every string in the pool has a review decision. 296 pool words were
admitted at level two and 74 at level three. Where the pool held only an
inflected form, the citation form was reviewed and admitted in its place,
and the inflected form is excluded as one of its reviewed forms. That added
80 citation forms at level two and 30 at level three, and 129 inflected
forms are excluded on that ground. 95 strings are deferred and 13 more are
excluded, each with a reason in `review.json`.

Two of the admissions are second senses of words already admitted in
another sense, filed by word and concept as the sixth trial's tool change
allows. Empty is admitted here as a verb under liquid, because the sources
use empties for a river flowing into the sea and for a basin losing its
water, while empty was admitted only as an adjective. Bond is admitted at
level three as a verb, recorded in `evals/review/level_3_long_tail/`,
because the sources use bonded for atoms joined together, while an earlier
batch admitted bond at level three only as a noun.

Dip is admitted as a noun and a verb in one entry, because the sources use
it for a low place, as in a dip in the jet stream, and for putting
something into a liquid, as in dipping a paper towel. So dips is one of its
reviewed forms in either use.

Translate was reviewed in place of the pool string translates. The sources
use translates only for converting one thing into another or amounting to,
as in a meter that translates a voltage difference into pH, so the
definition gives that sense as well as the sense of changing words from one
language into another.

Thirty-three deferred strings are technical terms used in the sources only
in a specialised sense past level three, such as antimeridian, dryline,
eutrophic, isotachs, mesocyclone, penstock and xylem.

Fourteen are frequent only in page interface text, in link text or in the
titles of linked pages. Most of these are the titles of linked questions
in one ocean source, such as kelp, seamount and turtle. The scan gives no
prose evidence for them, so they are deferred as interface strings were in
the fifth pass, even where the word itself is common.

Fourteen are used in the McGuffey readers mainly in an archaic or literary
sense, and are deferred as the brief directs. They are bid, blest, breeches,
contrived, counsel, cunning, dwell, keen, quay, queer, recollect, rill,
whatsoever and woe.

Eight are forms of words that earlier batches deferred or excluded, and
those decisions are not reopened. They are accumulates, dimensions,
flashing, individuals, posters, prayed, presented and prevents, the last
of which is a form of a word an earlier batch excluded. Efficiencies,
particulates and runups are used in the sources as countable plurals, as in
fewer emissions of particulates, of words filed earlier as mass nouns, and
changing those entries is a separate decision, as for bacterium below.
Lbs, quads and vol are abbreviations, and as in the fifth pass whether such
a form is a headword is left to a separate decision.

Applicators, barrages, conterminous, crispy, preserver, rogue, strider,
striders, sulfuric and theorem occur only in a specialised sense, in a
joined name or in a loose use. Biologic and hydroenergy are a variant and
a rare synonym. Bacterium, indices and millennia are singular or irregular
plural forms tied to words whose entries would have to change or are not
admitted. Clearer is the comparative of the adjective clear, which is
admitted only as a verb under the concept the adjective would need, and
strung is the past of a verb sense of string that is not admitted. Grind
would give the past form ground, which is already a headword. Goatskin
cannot be defined inside the level, because goat is not admitted. Liquor
is used for a strong drink and for a waste liquid from paper mills, and
whether the drink belongs at level two is left to a separate decision.

Seven excluded strings are fragments of pronunciation markup. Clinkerty
and twee are sound words from poems, edna is a name, and grey is a
spelling of gray. Infiltrated and lipids are a form and a plural of words
an earlier batch admitted at level three, which is not reopened.

So this batch admitted 375 headwords and one second sense at level two.
The 103 level-three headwords and one level-three second sense are recorded
in `evals/review/level_3_long_tail/`.

No word that had a review decision before this batch was given a new one.
Bond, which an earlier batch admitted as a noun, gains a record for a
second sense that the earlier decision did not cover, and that decision is
unchanged. This was checked for the added citation forms as well as for
the pool.

## Measured

Level two rose from 2,997 to 3,372 distinct headwords, measured.
Required definition coverage is 849 of 849 at level one and 3,371 of 3,371
at level two, and closure is complete at both. The validator also reports
one definition of a function word at level two, which it does not count as
required, grounds all 3,372, and finds every one of the 2,531 dictionary
records at level two inside the level and grounded.

    .venv/bin/python tools/measure_lexicon_increment.py \
      evals/review/level_2_long_tail \
      --check evals/review/level_2_long_tail/measurement.json

## Changes outside the lexicon

The derived forms of nine words were wrong or missing. Fight, flee,
overcome and underlie are now listed in `IRREGULAR` in
`src/epagoge/inflection.py`, and submit is listed there because it doubles
its final consonant. Salmon, snowman, tomato and workman are listed in
`IRREGULAR_PLURAL`. Blossom, differ, fasten, interpret, lessen, recover,
shorten, strengthen and threaten end consonant, vowel, consonant with an
unstressed final syllable, so they are listed in `NO_DOUBLE_MULTISYLLABIC`,
which the corpus validator requires of every such verb.

The measurements of the earlier level-two batches that record the live
headword count were recorded again. This batch was added to the test that
checks those measurements. The full test suite was run on a simulated copy
of the tree before admission.

## Limits

The level of each word was judged by the agent against the calibration in
`docs/decisions/LEVEL_CALIBRATION.md`, and that judgement has not been
reviewed independently. The pool is the largest yet, so each definition was
kept short, and several give one common sense without the detail a later
level would add. Where a word has several senses, the definition gives the
one the sources use most, so cord is defined as a thick string and not as
a measure of wood, and attractive as pulling things together.

Strings whose only evidence is in the titles of linked pages were deferred
even when the word is common, which keeps the rule of the fifth pass but
leaves some easy words, such as turtle, for a later batch.

`previous_CURRENT_BRIEF.md` and `previous_COMPLETION_CONDITION.md` are the
brief and condition met earlier on 2026-10-30, retained as historical
evidence.
