# Agency scan, sixth pass, level two

Recorded 2026-10-30. This pass fetched nothing and did not rescan. It drew
the pool again from the first agency scan of 2026-10-10, kept at the
ignored `tmp/lexicon-sources/scan_agency.json`, whose hash matches the one
recorded in `evals/review/level_2_agency/authoring.json`. That scan covers
NASA children's earth pages, a StarChild level 1 sample and USGS Water
Science School pages. The first pass admitted words from it and left the
rest of its pool without a review decision. No teacher ran.

The first pass recorded its source as public domain. Whether each page is
a work of a federal employee was not checked again here, so the source
recorded on each term in this batch says agency source and does not say
public domain, as in the fifth pass.

## How the pool was drawn

`tools/candidate_pool.py` selected the pool at level two with the private
term list applied and a minimum of one source, the rule every earlier
agency pass used, against the vocabulary as it stood after the fifth pass.
The private term list removed 3 strings. 253 were already admissible at
level two, 75 had a decision in an earlier review, 12 were short and 98
were mostly capitalised. The pool held 28. The operator withdrew no string.

The pool is kept as the ignored `tmp/lexicon-sources/pool_agency_06.json`.
`authoring.json` records its hash and the scan's.

## Why the pool holds 28 and not 80

80 strings of the first pool had no review decision recorded under their
own name in any batch. 28 of them are this pool. The other 52 were removed
as already admissible at level two, and none of the 80 is unaccounted for.
The operator's session confirmed this accounting against the first pass's
pool of 243 in the ignored `tmp/lexicon-sources/pool_agency.json`.

Of the 52, only one, duties, is admissible as a form of a headword admitted
after the first pass, namely duty in `evals/review/level_2_agency_02/`. 50
are forms of headwords that the first pass itself admitted, and its own
review lists each among that headword's reviewed forms. So those 50 were
reviewed in the first pass as forms rather than left undecided, and the
count of 80 counted only review keys.

The remaining string, organics, is listed as a reviewed form in no review.
It is admissible only because the lookup strips its final letter and finds
the adjective organic, which the first pass admitted. The source uses
organics as a noun for organic matter, a sense no batch has decided. This
batch does not decide it, because it is not in the pool.

## Decisions

Every string in the pool has a review decision. 9 pool words were admitted
at level two and 2 at level three. Where the pool held only an inflected
form, the citation form was reviewed and admitted in its place, and the
inflected form is excluded as one of its reviewed forms. That added
dedicate and flux at level three, and dedicated and fluxes are excluded on
that ground.

Nine strings come from Spanish page titles linked from the NASA earth
pages. Seven are Spanish words, and two are fragments of Spanish words that
the scan split at an accented letter. All nine are excluded as not English
headwords, as the scan_05 and agency_02 batches excluded strings that are
not English.

Five deferred strings are frequent only in page interface text, in link
text, the titles of linked material or web addresses. They are abstract,
docs, html, multimedia and publications. That gives the scan no prose
evidence for them, as in the fifth pass. Clip occurs only inside a joined
name and is deferred on the same ground as the fifth pass deferred such
words.

So this batch admitted 9 headwords at level two, namely atomic, definitely,
download, fortunate, illusion, pun, replica, struggle and universally. The
4 level-three headwords are recorded in `evals/review/level_3_agency_06/`.

No word that had a review decision before this batch was given a new one.
That was checked for the added citation forms as well as for the pool.

## Measured

Level two rose from 2,987 to 2,996 distinct headwords, measured.
Required definition coverage is 849 of 849 at level one and 2,995 of 2,995
at level two, and closure is complete at both. The validator also reports one
definition of a function word at level two, which it does not count as
required, and grounds all 2,996.

    .venv/bin/python tools/measure_lexicon_increment.py \
      evals/review/level_2_agency_06 \
      --check evals/review/level_2_agency_06/measurement.json

## Changes outside the lexicon

No table in `src/epagoge/inflection.py` changed. The rule gives the forms
of every admitted word correctly. The measurements of the earlier
level-two batches that record the live headword count were recorded again.
This batch was added to the test that checks those measurements. The full
test suite was run on a simulated copy of the tree before admission.

## Limits

The level of each word was judged by the agent against the calibration in
`docs/decisions/LEVEL_CALIBRATION.md`, and that judgement has not been
reviewed independently. Atomic occurs in the source only in the joined
form atomic-scale, and it is admitted because the scan counts it as a
word and its sense there is the ordinary one. Dedicate is defined in the
sense of keeping something for one purpose, which is the source's use,
rather than in the sense of offering a work to a person. Fortunate is
defined through chance rather than through luck, which is not admitted.

`previous_CURRENT_BRIEF.md` and `previous_COMPLETION_CONDITION.md` are the
brief and condition met earlier on 2026-10-30, retained as historical
evidence.

## Review changes

Recorded 2026-10-30. The reviewer line read all 13 admitted definitions and
proposed new wording for two. No word changed its decision, level, concept
or part of speech.

**Incompressibility, level three.** The old definition was
"Incompressibility is the property of being incompressible." It only
restated the word. The new definition is "Incompressibility is how much a
substance pushes back when it is squeezed into a smaller space." It was
applied by `tools/author_definitions.py`, which accepted it as proposed.
The admitted and review records of `evals/review/level_3_agency_06/` carry
the new wording.

**Flux, level three.** The reviewer offered a definition as an amount that
flows through an area in a given time. That changes the sense, so on the
operator's direction flux keeps its definition as a flow from one place to
another.

The headword counts and closure figures are unchanged. The measurement of
this batch still matches the tree, because no level-two record changed.
