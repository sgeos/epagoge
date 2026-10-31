# Agency scan, fifth pass, level two

Recorded 2026-10-30. This pass scanned 214 pages of the USGS Water Science
School beyond the 19 pages read on 2026-10-10, fetched on 2026-10-30 from
the article pages linked from its topic pages and the pages those link to
inside the school. Only the first tab of each page was kept, and media
usage lines, credit lines, page interface lines, the site footer and lines
repeated from an earlier page were removed. The text holds 164,856 words as
counted by `wc`. No teacher ran.

Whether each page is a work of a federal employee was not checked page by
page, and the site states that some images are copyrighted while their
captions were kept as text. So the source recorded on each term says agency
source and does not say public domain. `docs/decisions/AGENCY_SOURCES.md`
lists the school as a level-two candidate.

## How the pool was drawn

`tools/scan_lexicon.py` counted the text at a threshold of five.
`tools/candidate_pool.py` then selected the pool at level two with the
private term list applied and a minimum of one source, the rule every
earlier agency pass used. The private term list removed 2 strings, and the
other rules removed 359 more, so the pool held 572. The operator then
withdrew 1 string from the pool before any decision was made, which left
571.

The scan and the pool are kept under the ignored `tmp/lexicon-sources/agency5/`.
`authoring.json` records the hash of each.

## Decisions

Every string in the pool has a review decision. 292 pool words were
admitted at level two and 114 at level three. Where the pool held only an
inflected form, the citation form was reviewed and admitted in its place,
and the inflected form is excluded as one of its reviewed forms. That added
64 citation forms at level two and 10 at level three. 118 inflected forms
are excluded on that ground. 4 more are excluded as forms of words admitted
at level three by an earlier batch, which is not reopened. 43 strings are
deferred with a reason in `review.json`.

Eight deferred strings are frequent only in the site's page interface, in
link text, the titles of linked material or web addresses. They are com,
gallery, https, interactive, podcast, publication, quiz and www. That gives
the scan no prose evidence for them. Confidence is frequent only in the
name of a kind of report, and is deferred on the same ground.

Five are abbreviations, cfs, faqs, mgd, phs and ppm, and coli is the second
part of the two-word name of a bacterium. Lab, labs and tech are clipped
forms. As in the fourth pass, whether such a form is a headword is left to
a separate decision.

Determination, flash, graduated, nervous and tract are used in the source
only in a specialised sense, while a more common sense of each word differs.
Conditioners, pie and stilling occur only inside joined names. Owing occurs
only in the phrase owing to. Hydrates and quantile name senses past level
three.

Six are already in the vocabulary at a higher level without a review
decision, or are tied to a word that is. They are consequence,
consequences, functions, harmless, hazards and structure. Moving a word
down to level two is a separate decision. Courses, conducting, plains and
preventing are forms of words that earlier batches deferred or excluded,
and those decisions are not reopened.

Accumulate, define and induce would each give a form that is already a
headword at a higher level, accumulating at level six and defined and
induces at level five. Admitting them would file one form under two
headwords, so they are deferred, with accumulated and induced, as a
separate decision. Defined was also excluded by an earlier batch. The
first simulated run of the test suite found these collisions.

Multiply is admitted at level three rather than two, because its concept is
first taught at level three. Probe is admitted at level two in one sense only, a tool put into
something to measure it, as the operator directed.

So this batch admitted 356 headwords at level two. The 124 level-three
headwords are recorded in `evals/review/level_3_agency_05/`.

No word that had a review decision before this batch was given a new one.
That was checked for the added citation forms as well as for the pool.

## Measured

Level two rose from 2,631 to 2,987 distinct headwords, measured.
Required definition coverage is 849 of 849 at level one and 2,986 of 2,986
at level two, and closure is complete at both. The validator also reports one
definition of a function word at level two, which it does not count as
required, and grounds all 2,987.

    .venv/bin/python tools/measure_lexicon_increment.py \
      evals/review/level_2_agency_05 \
      --check evals/review/level_2_agency_05/measurement.json

## Changes outside the lexicon

The derived forms of eight words were wrong. The rule gave binded, clinged,
ridded, transmited and withdrawed, and the plurals basises, catfishes and
shellfishes. Bind, cling, rid, transmit and withdraw are now listed in
`IRREGULAR`, and basis, catfish and shellfish in `IRREGULAR_PLURAL`, in
`src/epagoge/inflection.py`. Abandon, alter, deliver and inhabit end
consonant, vowel, consonant with an unstressed final syllable, so they are
now listed in `NO_DOUBLE_MULTISYLLABIC`, which the corpus validator requires
of every such verb. The rule already gave their forms correctly. The
measurements of the earlier level-two batches that record the live headword
count were recorded again. This batch was added to the test that checks
those measurements. The full test suite was run on a simulated copy of the
tree before admission.

## Limits

The level of each word was judged by the agent against the calibration in
`docs/decisions/LEVEL_CALIBRATION.md`, and that judgement has not been
reviewed independently. The pool is nearly three times the size of the last
one, so each definition was kept short, and several give a common sense
without the technical detail a later level would add. Kilogram is defined
as a unit for measuring how heavy something is, which is the everyday sense
rather than the physical one.

Dowsing is defined with the statement that scientists have not found
evidence that it works, which follows the source. Septic and transpire are
defined in the source's sense, which differs from another common sense of
each. Findings is admitted as a plural-only noun, because finding is a form
of find. The rule gives radiuses as the plural of radius, which is a
standard plural, so radii is not listed.

`previous_CURRENT_BRIEF.md` and `previous_COMPLETION_CONDITION.md` are the
brief and condition met earlier on 2026-10-29, retained as historical
evidence.

## Review changes

Recorded 2026-10-30. The reviewer line read all 480 admitted definitions
and proposed new wording for eight. Each was applied by
`tools/author_definitions.py`, which checks the wording against the level's
vocabulary and the closure of the whole dictionary before it writes
anything. The tool accepted all eight as proposed, so no wording departs
from the reviewer's. No word changed its decision, level, concept or part
of speech. The admitted and review records of this batch and of
`evals/review/level_3_agency_05/` carry the new wording.

**Cement, level two.** The old definition ended "left to dry". Cement
hardens by setting rather than by drying, so the new definition is "Cement
is a gray powder that becomes as hard as stone when mixed with water and
left to set."

**Abundant, level two.** The old definition was "Abundant means there in
large amounts." The word there had no antecedent. The new definition is
"Abundant means found in large amounts."

**Gypsum, level two.** The old definition said gypsum is used to make walls
and powder, which was unclear. The new definition is "Gypsum is a soft,
white mineral used to make walls."

**Kilogram, level two.** The old first sentence was "A kilogram is a unit
for measuring weight." The new first sentence is "A kilogram is a unit for
measuring how heavy something is." The second sentence is unchanged. The
definition still gives the everyday sense, as the limits above record.

**Multiply, level three.** The old definition was "To multiply a number is
to add it to itself a given number of times." It was ambiguous when the
second number is one or zero. The new definition is "To multiply a number
by another is to add the first to itself as many times as the second says."

**Chlorine, level three.** The old definition called chlorine a green gas.
The new definition calls it a yellow-green gas and is otherwise unchanged.
This rests on general chemistry rather than the source.

**Pathogen, level three.** The old definition called a pathogen a very
small living thing, such as a virus. The level-two definition of virus does
not call a virus living. The new definition is "A pathogen is a very small
thing, such as a virus, that causes disease."

**Evapotranspiration, level three.** The old definition named the water
rather than the process. The new definition is "Evapotranspiration is the
movement of water into the air from land, water and plants together, by
evaporation and transpiration."

The headword counts and closure figures are unchanged. The measurement of
this batch was recorded again because it holds a hash of each record file,
and only the hashes of `review.json` and `admitted.json` changed.
