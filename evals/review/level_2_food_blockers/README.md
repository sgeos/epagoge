# Level-two food blockers

Recorded 2026-10-07. Earlier teacher runs retained every rejected definition
with the words outside the level that made it fail.
`tools/blocking_words.py` ranks those words by the number of rejected
definitions each blocked. Before this batch it read five reports holding 59
rejected definitions and found 34 blockers still outside level two. Its output
is retained in `blocking_words.txt`.

Sixteen earlier deferrals were also still unadmitted, all of them foods or
plants. They are honey, yeast, nut, peach, plum, lemon, onion, carrot, potato,
lettuce, pepper, garlic, cheese, butter, cream and soup. The review covers the
34 blockers, the sixteen deferrals and the bases of inflected blockers, which
is 57 entries.

## Measured outcome

Agent review admitted 36 words, deferred 13 and excluded eight. Twenty-one
admissions are blockers or their bases and fifteen are retained deferrals.
Level two rose from 1,049 to 1,085 distinct headwords, leaving 8,915 to the
approximate target. Level one remains at 849. Required definition coverage is
812 of 812 at level one and 1,048 of 1,048 at level two, and both dictionaries
are completely grounded. All level-one books, the reference checkpoint and
74 earlier review artifacts match their recorded hashes.

**Fifteen of the sixteen retained deferrals are admitted. One remains blocked
only by sour, and that is lemon.** No admitted definition uses sweet, sour or
sugar. After the batch the ranking finds twelve blockers outside level two.
Sweet, sour, sugar and tart wait on the operator. Cakes waits on sweet. The
other seven are not needed by any revised definition.

## What this shows and what it does not

Sweet blocked 16 rejected definitions, more than any other word. Most of the
words it blocked were definable without it. Honey is distinguished by bees and
nectar, peach by its fuzzy outside and plum by its size and colour. The
teacher reached for sweet where a distinguishing property was available, so
the count overstates what sweet is needed for. What sweet and sour still
block in this record is lemon, cake and sugar. That is the measurement offered
for the operator's ostensive decision. It does not show that an ostensive
admission is right.

The ranking counts rejections, not words. A word rejected in several runs
counts once per run, so a heavily retried candidate inflates its blockers.

## How the definitions were written

No teacher ran, for the host-memory reason recorded in `authoring.json`. The
definitions were written by the agent, informed by the retained rejected
replies but not copied from them. They pass the admission tool's licensing and
closure checks. Blockers were defined first in the sense the rejected replies
used, and the deferrals were then defined through them.

Dependencies inside the batch run one way. Honey uses bee and nectar, and
nectar uses bee. Carrot, onion, potato, pepper and soup use vegetable, which
uses root. Garlic uses onion and cook. Butter uses cream. Mixture uses mix.
Vine uses stem. Lettuce uses salad. No pair is defined only through each
other.

Peach and plum avoid the fruit senses of skin and stone, which are recorded
unresolved reviews. Each uses outside and a hard part that holds one seed, as
the admitted cherry does.

## Agent edits and findings

The plural rule gave potatos, so potato was added to the irregular plural
table with potatoes. The past form cooked is not among the forms of cook. It is
already a level-one participial adjective under raw_and_made, paired with raw,
so it stays admissible and the level-one entry is unchanged. Fine was deferred
by the era-overlap batch because the scan's two eras use different senses.
It is admitted here in the particle sense on the strength of corpus evidence.

## Evidence and verification

`candidates.json`, `authoring.json`, `review.json`, `admitted.json`,
`before.json`, `measurement.json` and `preservation.json` follow the
era-overlap batch. Each admitted entry records whether it was a blocker or a
retained deferral.

    .venv/bin/python tools/measure_lexicon_increment.py \
      evals/review/level_2_food_blockers \
      --check evals/review/level_2_food_blockers/measurement.json

## Limits

Agent review without independent expert validation. Several definitions are
introductory simplifications, such as yeast without saying it is a fungus and
garlic without cloves. No level-two book uses any of these words yet. No
throughput claim follows from one batch.
