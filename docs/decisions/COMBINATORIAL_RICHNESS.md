# Repetition should raise combinatorial richness, not repeat combinations

**Decided 2026-09-26, operator direction**, prompted by an observation from
an external model: eight hundred words is not many, but the space of
combinations it can express is vast, and the same holds for combined-concept
books and for vocabulary.

**The corpus was spending its repetition on the same combinations**, and the
measurement is worse than the principle suggests.

## What was measured

Over the 244 sixteen-spread content books at level one:

| | |
| --- | --- |
| Concepts appearing in a content book | 124 |
| Concept pairs possible | 7,626 |
| **Pairs realised in some book** | **109, which is 1.4 percent** |
| Pairs realised inside a single record | 50 |
| Records carrying exactly one concept | 3,047 of 3,904, which is 78 percent |

**The structure is worse than the count.** Every concept's partners were
exactly its own unit-mates, because a book is about a unit and a variant
repeats that unit. `giving_a_reason` had appeared beside `agreeing` and
`disagreeing` and nothing else, the three being one unit. `right_reason` had
**no** partner at all.

So `.v2`, `.v3` and `.v4` multiplied the corpus without multiplying its
combinations. They were the cheapest growth available and they bought less
than their word count suggests.

## The rule

**A concept met again should be met beside something different.** Repetition
that reuses a combination adds tokens; repetition that makes a new
combination adds structure.

**The same applies to vocabulary.** A concept should be taught with
different words where the lexicon allows it, and a different partner concept
pulls in different words as a side effect, which is why the two halves of
the rule are one intervention rather than two.

**It does not licence arbitrary pairing.** A pair has to make a story that
is true and readable at the level. The pairings written first ground a
**poorly retained abstract** concept in a **well retained concrete** one,
because that is both a new combination and a pedagogically defensible one.

## Why this is not merely tidiness

`../../evals/pilot/LEVEL_ONE_POSITIONS_AND_RETENTION.md` measured what the
model retains. The worst-retained concepts are the epistemic ones this
project exists to teach: `giving_a_reason`, `disagreeing` and `agreeing` at
loss 4.011, against 2.017 for `emptiness`. **Those are the concepts with one
book and no partner but their unit-mates**, and concepts taught by a single
book are retained worse, mean loss 3.028 against about 2.65 for two or more.

**The correlation is modest and confounded** and that record says so. But
the direction agrees with the combinatorial argument, and the intervention
is the same either way.

## How it is done

`generators/cross_books.py` writes a book that is a **variant of the target
concept's own unit**, so the schema does not change: the subject is a
scheduled topic and a record in the book defines it. What differs is that
every story record carries the partner concept as well.

The first eleven pair each worst-retained concept with a different
well-retained one, and all eleven pairs are new:

| Concept | Partner |
| --- | --- |
| `giving_a_reason` | `emptiness` |
| `disagreeing` | `presence` |
| `agreeing` | `finished_or_not` |
| `keeping_your_claim` | `goal` |
| `changing_your_mind` | `who_said_it` |
| `not_both` | `household_object` |
| `if_then` | `material` |
| `all_some_none` | `shape` |
| `settling_it` | `liquid` |
| `finding_out` | `air` |
| `right_reason` | `force` |

## Three defects in the tooling that this work found

**`generate.ask` bounded the context and never bounded the output.** A
whole-book prompt the same size as a spread-fill prompt, which answers in
three to six seconds, timed out at ninety seconds and then at two hundred
and forty. Asked for sixteen sentences under a hard word list the teacher
generates until it decides to stop, and under a constraint it cannot satisfy
it does not stop. Capped, the same call answers in fourteen seconds. **A
bounded failure beats an unbounded wait.**

**`prompt.book` misled when given no words to define.** It printed "one WORD
line for each of these words" and then listed none, immediately above the
admissible vocabulary, so the teacher read that list as the words to define
and returned definitions for all 845 of them and no story. A book that
recombines concepts already taught defines nothing new, which is a case the
prompt had never met.

**A concept name is not a word.** A subject form reading "told through
emptiness" produced three subject lines containing `emptiness`, which is a
concept id and absent from the lexicon, so all three were rejected and the
book was discarded despite twenty-three usable story spreads. The teacher is
now given the words that teach a concept, since words are the only thing it
can write with.

## What to check next time

**Pairs realised, before and after.** It is one number and it says whether
a round of writing bought structure or only tokens.

**Whether the eleven concepts move.** Retrain and re-run
`tools/retention.py`. If retention does not respond, the combinatorial
argument is right about the corpus and wrong about the model, and that is
worth knowing.
