# Agency scan, second pass, level two

Recorded 2026-10-28. This pass scanned the Energy Information
Administration elementary pages and the Ben's Guide pages for ages 4 to 8,
both fetched on 2026-10-28. No teacher ran.

## How the pool was drawn

`tools/scan_lexicon.py` counted each source separately at a threshold of
five. `tools/candidate_pool.py` then selected the pool at level two with the
private term list applied. A word frequent in one source was enough, which
is the rule the first agency pass used. The scan found 442 frequent words.
Nine were frequent in Ben's Guide and four in both sources, so the default
of two sources left this pool empty. The pool held 237 strings, and two of
them, colonies and vote, came from Ben's Guide.

The scan and the pool are kept under the ignored `tmp/lexicon-sources/agency2/`.
`authoring.json` records the hash of each.

## Decisions

Every string in the pool has a review decision. 105 pool words were admitted
at level two and 28 at level three. Where the pool held only an inflected
form, the citation form was reviewed and admitted in its place, and the
inflected form is excluded as one of its reviewed forms. That added 48
citation forms at level two and 4 at level three. 90 inflected forms are
excluded on that ground. Six further strings are excluded as an
abbreviation, a Latin phrase, a clipped form, a prefixed category label, an
inflected form of a word filed at level six, and an inflected form of a word
outside the pool. Eight are deferred with a reason in `review.json`.

So this batch admitted 153 headwords at level two. The 32 level-three
headwords are recorded in `evals/review/level_3_agency_02/`.

No word that had a review decision before this batch was given a new one.
That was checked for the added citation forms as well as for the pool.

## Measured

Level two rose from 2,310 to 2,463 distinct headwords, measured. Coverage
is 2,463 of 2,463 and closure is complete at levels one and two.

    .venv/bin/python tools/measure_lexicon_increment.py \
      evals/review/level_2_agency_02 \
      --check evals/review/level_2_agency_02/measurement.json

## Changes outside the lexicon

Control, transfer and offset end consonant-vowel-consonant, so their
doubling cannot be derived from spelling. Each is now listed in
`IRREGULAR` in `src/epagoge/inflection.py`. The measurements of the eleven
earlier scan batches were recorded again, because each records the live
headword count. Only the after counts, the remaining gap and the level-two
closure output changed in them. This batch was added to the test that
checks those measurements.

## Limits

The level of each word was judged by the agent against the calibration in
`docs/decisions/LEVEL_CALIBRATION.md`, and that judgement has not been
reviewed independently. Several level-two words, such as biodiesel and
quadrillion, sit near the boundary. The energy pages use some common words
in a narrow technical sense. Generation and carrier are defined here in a
general sense that covers the source's use.

`previous_CURRENT_BRIEF.md` and `previous_COMPLETION_CONDITION.md` are the
brief and condition met on 2026-10-25, retained as historical evidence.
