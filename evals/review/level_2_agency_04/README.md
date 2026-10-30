# Agency scan, fourth pass, level two

Recorded 2026-10-29. This pass scanned 147 NASA Space Place pages beyond
the eight articles scanned on 2026-09-27, fetched on 2026-10-29 with games
and videos left out. Only the article body of each page was kept. The text
holds 68,600 words as counted by `wc`. No teacher ran.

Whether each page is a work of a federal employee was not checked page by
page, so the source recorded on each term says agency source and does not
say public domain. `docs/decisions/AGENCY_SOURCES.md` lists the site as a
candidate.

## How the pool was drawn

`tools/scan_lexicon.py` counted the text at a threshold of five.
`tools/candidate_pool.py` then selected the pool at level two with the
private term list applied and a minimum of one source, the rule every
earlier agency pass used. The scan found 384 frequent words. The private
term list removed 6 strings, and the other rules removed 165 more, so the
pool held 213. The operator then withdrew 5 strings from the pool before
any decision was made, which left 208.

The scan and the pool are kept under the ignored `tmp/lexicon-sources/agency4/`.
`authoring.json` records the hash of each.

## Decisions

Every string in the pool has a review decision. 129 pool words were
admitted at level two and 17 at level three. Where the pool held only an
inflected form, the citation form was reviewed and admitted in its place,
and the inflected form is excluded as one of its reviewed forms. That added
22 citation forms at level two and 1 at level three. 44 inflected forms
are excluded on that ground. 18 strings are deferred with a reason in
`review.json`.

Eight deferred strings are frequent only in page interface text. Articles,
bookmarks, brochure, dimension, informative, postcards, poster and
printable come from the site's description of itself and its catalogue of
downloadable files. That gives the scan no prose evidence for them.

Four are clipped or combining forms. Litho, topo and hex stand in the
source for longer words, and mini occurs only as the first part of a joined
word. Whether such a form is a headword is left to a separate decision.

Coma, mantle and tissue are used in the source only in a specialised
sense, while a more common sense of each word differs. As for net and bill,
which sense to file first is left to a separate decision.

Popsicle and styrofoam are trade names that the source uses as generic
words for craft materials. Whether the dictionary files trade names is
left to a separate decision.

Farthest is a superlative of far. Far was admitted at level one with
further and furthest as its listed forms. Adding farther and farthest would
change an entry decided before this batch, so it is deferred.

So this batch admitted 151 headwords at level two. The 18 level-three
headwords are recorded in `evals/review/level_3_agency_04/`.

No word that had a review decision before this batch was given a new one.
That was checked for the added citation forms as well as for the pool.

## Measured

Level two rose from 2,480 to 2,631 distinct headwords, measured.
Required definition coverage is 849 of 849 at level one and 2,630 of 2,630
at level two, and closure is complete at both. The validator also reports one
definition of a function word at level two, which it does not count as
required, and grounds all 2,631.

    .venv/bin/python tools/measure_lexicon_increment.py \
      evals/review/level_2_agency_04 \
      --check evals/review/level_2_agency_04/measurement.json

## Changes outside the lexicon

The derived forms of two words were wrong. The rule gave drived for drive
and hypothesises for hypothesis. Drive is now listed in `IRREGULAR` and
hypothesis in `IRREGULAR_PLURAL` in `src/epagoge/inflection.py`. Flatten,
focus, gather and transit end consonant, vowel, consonant with an
unstressed final syllable, so they are now listed in
`NO_DOUBLE_MULTISYLLABIC`, which the corpus validator requires of every
such verb. The rule already gave their forms correctly. The measurements of
the thirteen earlier scan batches were recorded again, because each records
the live headword count. This batch was added to the test that checks those
measurements. The full test suite was run on a simulated copy of the tree
before admission.

## Limits

The level of each word was judged by the agent against the calibration in
`docs/decisions/LEVEL_CALIBRATION.md`, and that judgement has not been
reviewed independently. Hypothesis, exosphere and thermosphere were placed
at level two because related words such as predict and mesosphere are
already there, and each sits near the boundary with level three.

After the review changes below, each of crust, fan, film and screen names
one sense. The second senses of button, phone and screen are not defined.
Theory is defined as an explanation that fits the evidence so far and that
new evidence can still overturn.

`previous_CURRENT_BRIEF.md` and `previous_COMPLETION_CONDITION.md` are the
brief and condition met earlier on 2026-10-29, retained as historical
evidence.

## Review changes

Recorded 2026-10-29. The reviewer line read all 169 admitted definitions
and proposed new wording for eight. Each was applied by
`tools/author_definitions.py`, which checks the wording against the level's
vocabulary and the closure of the whole dictionary before it writes
anything. The tool accepted all eight as proposed, so no wording departs
from the reviewer's. No word changed its decision, level, concept or part
of speech. The admitted and review records of this batch and of
`evals/review/level_3_agency_04/` carry the new wording.

**Advanced, level two.** The old definition was "Advanced means more
developed, newer or harder than others of its kind." Harder is not part of
the meaning. The new definition is "Advanced means more developed or more
modern than others of its kind."

**Crust, level two.** The old definition named the outside of bread and the
outer layer of the earth in one sentence. The new definition is "A crust is
the hard outer layer of something, such as the rocky outer layer of the
earth." It names one sense with one example.

**Fan, level two.** The old definition named a machine and a folded paper
that is waved. The new definition is "A fan is a thing that moves air, such
as a machine with turning blades." It keeps the machine as its one example.

**Film, level two.** The old definition named a thin layer and the film of
an old camera. The new definition is "A film is a thin layer or sheet of
something." The camera sense is not defined.

**Screen, level two.** The old definition named a display and a sheet of
wire with small holes. The new definition is "A screen is a flat surface
where pictures are shown, such as the front of a computer or a phone." The
wire sense is not defined.

**Astrology, level two.** The old second sentence was "It is not a science,
because its claims do not rest on evidence." That stated an evaluation as
the dictionary's own claim. The new second sentence is "Most scientists do
not accept it, because its claims have not been shown by evidence." The
first sentence is unchanged.

**Ion, level three.** The old definition was "An ion is an atom or a
particle that has an electric charge." Particle was loose. The new
definition is "An ion is an atom or group of atoms that has an electric
charge." It keeps the electric charge sense alone.

**Laser, level three.** The old definition said the beam is of one color,
which is not strictly true of every laser. The new definition is "A laser
is a machine that makes a narrow, very bright beam of light that is almost
one color."

The headword counts and closure figures are unchanged. The measurement of
this batch was recorded again because it holds a hash of each record file,
and only the hashes of `review.json` and `admitted.json` changed.
