# Backporting level-two concepts into level-one picture books

**Recorded 2026-09-25.** Operator direction: iterate the same ideas at
different lexical and complexity levels, and backport concepts from the
level-two corpus into the sixteen-spread picture-book format. This records
a trial of three concepts and what it cost.

## Why backport rather than write more variants

The level-one corpus was growing by writing more books about the same
ninety-two units with the same teacher. That raises token count and does
not raise diversity, and the trained model's most visible failure is
looping on its most frequent collocations. **More text about the same
things is the input that produced the problem.**

A backported concept gives a level-one book something new to be about.

## The trial

Six level-two concepts, three sentences each, written to the level-one
ceiling. **Eighteen of eighteen lines are admissible** after the fixes
below, and the first pass was blocked by four words.

| Concept | Blocked by, first pass | After |
| --- | --- | --- |
| `conservation_of_number` | `taken` | clean |
| `causal_chain` | `chain` | clean, by paraphrase |
| `grouping` | `ones`, `ten` | clean |
| `addition` | nothing | clean |
| `natural_number` | `ten` | clean |
| `place_value` | `ones`, `ten` | clean |

**Three of the four blockers were lexicon defects, not conceptual
barriers.**

- **`ten` sat at level two** under `quantity`. `nine` was already at level
  one. A child entering kindergarten counts to ten and the corpus could
  not say the word.
- **`one` carried no plural**, so `ones` was unreachable. `ones` and
  `tens` were themselves headwords at level two under `place_value`,
  which is the fifth and sixth inflected form filed as a base word.
- **`taken` was a headword** at level two under `subtraction`. It is the
  past participle of `take`, which is core.

Only `chain` was a real level-two word, and the level-one book says "the
line of things" instead.

## What a backport costs

**A backported concept needs a level-one word**, because the lexicalisation
check refuses a scheduled concept no word names at its level. Moving the
concept moves part of its vocabulary with it.

Five words were lowered: `group`, `pile` and `set` for `grouping`,
`unchanged` for `conservation_of_number`, and `knock` for `causal_chain`.
**`rearrange` and `chain` stayed at level two**, which is the shape to
keep: the picture book gets the plain words and the module keeps the
precise ones.

## What it produced

Three units at level one, taking it from 92 to 95, and three books at
sixteen spreads. Level two dropped from eight units to five, and the
concepts return there as module material rather than as units, since a
module revisits what a picture book introduced.

Sample from `bk.m1.same_count`:

> The child moved the five apples about on the table. She counted them
> again, just to be sure. There were still five apples, unchanged in
> number.

## What this does not settle

**Three concepts is not a sample.** They were chosen because their graph
prerequisites were already taught at level one, so nothing had to move
with them. A concept whose prerequisites are themselves at level two costs
more and none was tried.

**Whether the diversity gain is real is unmeasured.** The argument for
backporting is that it broadens the distribution the model sees, and that
is an expectation rather than a measurement. It would show up as a rise in
the distinct-token share in `../../evals/pilot/LEVEL_ONE_SAMPLES.md`, and
three books out of 229 will not move it.
