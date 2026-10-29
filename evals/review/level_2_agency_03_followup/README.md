# Third agency batch, review follow-up

Recorded 2026-10-29. The reviewer line read the twenty definitions admitted
by the third agency batch in `evals/review/level_2_agency_03/` and
`evals/review/level_3_agency_03/`, and proposed new wording for four of them
and a check of two concepts. This follow-up applies those findings. No
teacher ran. No word changed its admit, exclude or defer decision, and date
stays deferred as the batch decided.

## Definitions changed

Each definition was applied by `tools/author_definitions.py`, which checks
the wording against the level's vocabulary and the closure of the whole
dictionary before it writes anything.

**Meteor, level two.** The old definition was "A meteor is a rock from
space that gets so hot it shines as it falls through the air." It named the
rock, while a meteor is the streak of light the rock makes. The reviewer
proposed "A meteor is a streak of light in the sky made by a rock from space
that burns as it falls through the air." The tool refused it, because
streak is not admitted at level two and the definition would not ground.
The applied wording is "A meteor is a bright line of light in the sky made
by a rock from space that burns as it falls through the air." Line is
admitted at level one, and the sense is the reviewer's.

**Volcano, level two.** The old definition was "A volcano is a mountain or
an opening in the ground where hot melted rock comes up from deep inside the
earth." A volcano is the opening, which is often on a mountain. The applied
wording is the reviewer's, "A volcano is an opening in the ground, often on
a mountain, where hot melted rock comes up from deep inside the earth."

**Tribe, level two.** The old definition was "A tribe is a group of people
and families who share the same old ways, language and leaders." Old ways
is an evaluative claim, and the reviewer judged it contested. The applied
wording is the reviewer's, "A tribe is a group of people and families who
share a language and a way of life, often with their own leaders."

**Quasar, level three.** The old second sentence was "Its light comes from
hot gas falling into a huge black hole in the middle of a galaxy." That
states an explanation as settled. The applied second sentence is the
reviewer's, "Scientists think its light comes from hot gas falling into a
huge black hole in the middle of a galaxy." The first sentence is
unchanged.

The admitted and review records of both batches carry the new wording, so
that they describe what the dictionary holds. The records of the second
agency batch carry the changes of its own follow-up in the same way.

## Concepts checked

Each concept was checked against `curriculum/graph/concepts.json` and
against the concepts of the nearest words already admitted.

**Volcano changes from shape to spatial position.** Shape fitted the old
definition, which began with a mountain, and mountain is filed under shape.
The new definition names an opening in the ground where something happens,
which is a place. Most landforms admitted through level two are filed under
spatial position, among them hill, cave, island, peak, valley, bay, beach,
coast, desert and shore. Mountain, ridge and slope are filed under shape.
The level-one schedule teaches spatial position, so the term stays licensed
at level two. The
thesaurus was synced by `tools/sync_thesaurus.py`.

**Radio stays under reporting.** The reviewer judged reporting doubtful.
The definition is "Radio is a way to send sounds and signals through the
air without wires", which is a way of passing information on. Broadcast and
signal, the two admitted words closest to it, are filed under reporting.
Household object would fit a definition naming the set that receives the
sound, as television and antenna are filed, and component and system would
fit one naming the machine. The definition names neither, so the concept
is kept.

The concept of meteor was not reviewed and is unchanged.

## Derived forms

`tests/test_vocabulary.py` now asserts that the past form of spin is spun
and that the plural of volcano is volcanoes. The batch had listed both in
`src/epagoge/inflection.py`, and no test covered either until now.

## Measured

The headword counts did not change. Level two holds 2,480 distinct
headwords against 2,463 before the batch, measured. Required definition
coverage is 849 of 849 at level one and 2,480 of 2,480 at level two, and
closure is grounded at levels one to three, with 2,531 of 2,531 at level
three.

The measurement of `evals/review/level_2_agency_03/` was recorded again,
because it holds the hashes of the batch's admitted and review records.
Only those two hashes changed. Every other measurement checked by
`tests/test_candidates.py` still matched the tree and was left as it was.
The level-three batch has no measurement.

    .venv/bin/python tools/measure_lexicon_increment.py \
      evals/review/level_2_agency_03 \
      --check evals/review/level_2_agency_03/measurement.json

## Limits

The changed wording and both concept decisions are agent judgements. They
have not been reviewed independently. The replacement for streak keeps the
reviewer's sense in plainer words and is not a measured improvement.

`previous_CURRENT_BRIEF.md` and `previous_COMPLETION_CONDITION.md` are the
brief and condition met on 2026-10-28, retained as historical evidence.
