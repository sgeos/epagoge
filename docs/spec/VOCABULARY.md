# Per-level vocabulary

**Specified 2026-09-24.** Implementation in `../../src/epagoge/vocabulary.py`.

Level seven is unrestricted. Levels one to six are bounded.

## Two rules

**Ceiling.** A record at level L uses no word admitted above L.

**Coverage.** Every word admitted at level L appears in at least one level-L
record. **Admitting a word is a commitment to teach it.** A word admitted and
never used was never taught, and the level's vocabulary would be a claim the
corpus does not support.

## Three categories, because two were not enough

| Category | Level | Licensed by |
| --- | --- | --- |
| **core** | 1 | Nothing. Function words name no concept |
| **unmapped** | Holding pen, should stay empty | Nothing yet. Awaiting a concept |
| **terms** | **Authored**, bounded below by the graph | The concept the word names |

### Two corrections, in sequence

**First.** An earlier design held that the whole vocabulary could be derived
from the graph. The validator showed otherwise, since forcing a licence on
every word assigned twenty-four of them to levels where they never appeared.
The tiers were introduced in response.

**Third, and it corrects the second.** The level was then derived from the
concept, on the reasoning that a word's level is where its concept is
taught. **That was wrong, because a concept can be taught before its name is
introduced.** The level-one record teaching causation never uses the word
"cause", and children grasp causation long before they say it. Deriving
equality admitted thirty-three words at levels where nothing used them.

A word's level is **authored**, and the graph supplies only a lower bound:
a word may not be introduced before the concept it names is taught. The
placement above that bound is a scheduling decision, which is what
`ENABLING_CONCEPTS.md` describes and what the kanji schedule is.

**Second, and it corrects the first.** Those tiers were then described as a
permanent category, on the model of Basic English and the Dolch lists.
**That was also wrong.** A content word names something. "Shoe", "crayon",
"swing", and "cup" each name a concept, and a word that maps to nothing
means either the mapping was not identified or a concept is missing from the
graph.

**The unmapped tier is therefore a holding pen for unfinished work**, and
its size is a measure of how incomplete the graph is. Only function words
genuinely name nothing. `completeness` reports the fraction of content words
carrying a concept, and it should rise toward one.

At the time of writing it stands at 8.4 percent, with 131 words awaiting a
concept against 12 that have one.

### A word qualifies as a term only if it is used at its concept's level

A word that resembles a concept name but appears elsewhere is general
vocabulary. Treating it as a term would assign it a level the corpus does
not support, which is the same error in a smaller form.

## Inflection

Surface forms group under a lemma. Matching tries the form directly, then
strips a short list of suffixes, then retries with a restored silent *e*.

**Deliberately crude.** A real stemmer conflates distinct words silently,
and a vocabulary check that quietly accepts the wrong word is worse than one
that reports a form it does not recognise. An entry may list explicit
`forms`, which override the suffix rules entirely.

## Exemptions

Numerals are always admissible. Proper nouns, units, and source identifiers
are listed in `exempt` and sit outside the level system.

## What this does and does not catch

**Catches.** Lexical complexity above the level. A level-two record reaching
for a level-five word is reported with both levels named.

**Does not catch.** Conceptual error. The word "broken" is unambiguously
level-one vocabulary, so a record teaching that wear is the same as sudden
breaking passes the vocabulary check while teaching the wrong thing. That
failure is real and was observed in the first generation attempted.

**Vocabulary constrains how simply a thing is said. It says nothing about
whether the thing is right.** Both checks are needed and neither substitutes
for the other.

## Why this matters beyond simplicity

**It makes level assignment mechanically checkable**, which was the design's
weakest point. A level is authored, and prerequisite coverage was the only
thing constraining it, so a disagreement about whether a record is level
three or four had nothing to appeal to. The vocabulary ceiling is a second,
independent, automatic check.

## A concept with no word cannot be taught

**Added 2026-09-24.** `concept-unlexicalised` fires when a concept the
schedule places at level L has no term licensed at or before L.

**Nothing caught this until it was asked about**, and twenty-eight concepts
had accumulated without a word. The other rules here run the opposite
direction. A word must name a real concept, and a word may not be
introduced before its concept. **Neither fires when a concept has no word**,
because an unlexicalised concept breaks no rule as written. It is simply
unwritable, and the generator is constrained to the level's word list so it
cannot write about what that list does not name.

Restricted to concepts the graph holds. A term must name a graph concept,
so planning a concept and lexicalising it are the same step, and the rule
would otherwise fire on every plan.

**A word may still be introduced after its concept**, which is the design
recorded above and was nearly destroyed while satisfying this check. The
first attempt lowered every term to its concept's level, which would have
flattened deliberate authoring across 40 terms. Only the absence of any
word at or below the level is a defect. A late word alongside an early one
is not.

## Prior art

Restricted-vocabulary corpora are established rather than speculative.
TinyStories constrained generation to the lexicon of three-to-four-year-olds,
roughly fifteen hundred words, and models of three million parameters
produced coherent English. Successors extend the approach with progressively
simpler language environments and elementary-school filtering.
