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
| **general** | **Authored**, in tiers | Nothing. Ordinary content words |
| **terms** | **Derived** from the graph | The concept the word names |

### The correction that produced this

An earlier design held that the whole vocabulary could be derived from the
concept graph, with every word licensed by a concept and its level taken
from where that concept is taught.

**That was wrong, and the validator is what showed it.** Most content words
name no concept. "Shoe", "crayon", "account", and "attempting" are ordinary
English, and forcing a licence on them assigned them the level of whatever
concept they happened to resemble. The result was twenty-four words admitted
at levels where they never appeared.

General vocabulary is authored in tiers, exactly as Basic English and the
Dolch lists are. **Derivation applies where it matters**, to the technical
terms, so that the curriculum and its vocabulary cannot drift apart at the
point where drift would do damage.

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

## Prior art

Restricted-vocabulary corpora are established rather than speculative.
TinyStories constrained generation to the lexicon of three-to-four-year-olds,
roughly fifteen hundred words, and models of three million parameters
produced coherent English. Successors extend the approach with progressively
simpler language environments and elementary-school filtering.
