# Agency scan, third pass, level two

Recorded 2026-10-28. This pass scanned 153 StarChild level 1 pages and the
two Ben's Guide pages for ages 4 to 8 that the second pass did not reach,
both fetched on 2026-10-28. The two texts hold 32,283 and 341 words as
counted by `wc`. No teacher ran.

## How the pool was drawn

`tools/scan_lexicon.py` counted each source separately at a threshold of
five. `tools/candidate_pool.py` then selected the pool at level two with the
private term list applied and a minimum of one source, the rule both earlier
agency passes used. The scan found 117 frequent words, 112 in StarChild and
5 in Ben's Guide, and none was frequent in both. The private term list
removed 2 strings and the pool held 34. The operator then withdrew 2 strings
from the pool before any decision was made, which left 32.
Bill, law and tribes came from Ben's Guide.

The scan and the pool are kept under the ignored `tmp/lexicon-sources/agency3/`.
`authoring.json` records the hash of each.

## Decisions

Every string in the pool has a review decision. 13 pool words were admitted
at level two and 2 at level three. Where the pool held only an inflected
form, the citation form was reviewed and admitted in its place, and the
inflected form is excluded as one of its reviewed forms. That added 4
citation forms at level two and 1 at level three. 10 inflected forms are
excluded on that ground. Seven are deferred with a reason in `review.json`.

Six of the deferred words are frequent only in page interface text. Each
StarChild page repeats a notice about a scheduled outage and a government
shutdown, and links to an audio version and a text only version of the
page. That gives the scan no prose evidence for audio, date, outage,
scheduled, shutdown or version. The seventh is bill, which the source uses
only for a draft law. Its senses of money owed and of a beak are more
basic, so which to file first is left to a separate decision, as the second
pass did for net.

So this batch admitted 17 headwords at level two. The 3 level-three
headwords are recorded in `evals/review/level_3_agency_03/`.

No word that had a review decision before this batch was given a new one.
That was checked for the added citation forms as well as for the pool.

## Measured

Level two rose from 2,463 to 2,480 distinct headwords, measured. Coverage
is 2,480 of 2,480 and closure is complete at levels one and two.

    .venv/bin/python tools/measure_lexicon_increment.py \
      evals/review/level_2_agency_03 \
      --check evals/review/level_2_agency_03/measurement.json

## Changes outside the lexicon

The derived forms of two words were wrong. The rule gave spinned for spin
and volcanos for volcano, while the source spells volcanoes. Spin is now
listed in `IRREGULAR` and volcano in `IRREGULAR_PLURAL` in
`src/epagoge/inflection.py`. The measurements of the twelve earlier scan
batches were recorded again, because each records the live headword count.
This batch was added to the test that checks those measurements. The full
test suite was run on a simulated copy of the tree before admission.

## Limits

The level of each word was judged by the agent against the calibration in
`docs/decisions/LEVEL_CALIBRATION.md`, and that judgement has not been
reviewed independently. Collision and meteoroid sit near the boundary
with level three. Experiment is defined as a test of an idea
against what happens, and the definition does not say that a test can show
an idea to be right. Radio is defined as a way of sending signals, which
covers the source's use in radio signals and radio waves.

`previous_CURRENT_BRIEF.md` and `previous_COMPLETION_CONDITION.md` are the
brief and condition met earlier on 2026-10-28, retained as historical
evidence.
