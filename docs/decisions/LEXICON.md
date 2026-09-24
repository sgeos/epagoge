# The level-one lexicon

**Decided 2026-09-24.** `curriculum/vocabulary.json` changes role from
**descriptive** to **prescriptive**. Level-one content words go from 64 to
508.

## The failure that forced it

The first measured generation run accepted **16 of 100**. Eighty-four
drafts were rejected at the vocabulary ceiling.

The file had been derived to describe the words a 28-record sample corpus
happened to use. At level one that was 156 function words and **64 content
words**, and it was never authored as a lexicon a level-one corpus must be
writable in. Thirty concepts cannot be taught distinctly in 64 content
words, and the measured symptom was the teacher returning the same sentence
for different concepts because the vocabulary left it nowhere else to go.

## Why no published list was imported

Four candidates were considered. Ogden's Basic English at 850 words, Dolch
at 315, the New General Service List at 2809, and the roughly 1500-word
vocabulary behind TinyStories.

**Licensing rules out two of them for a CC0 corpus.** The New General
Service List is CC BY-SA 4.0 and the TinyStories dataset is
CDLA-Sharing-1.0. Both are share-alike, which would attach an obligation to
a corpus this project intends to release under CC0. Ogden's 1930
publication is in the United States public domain as of 1 January 2026, and
Dolch is of the same era.

**But licensing is not the decisive argument. The project's own rule is.**
Every content word must map to a concept, and the vocabulary reports full
coverage with zero unmapped. Importing 850 or 2809 words creates several
hundred words naming no concept in the graph. By the recorded rule, an
unmapped word means a missing concept, so a wholesale import forces either
hundreds of speculative concepts into the graph or the abandonment of the
coverage invariant.

## What was done instead

**The standard is adopted as the coverage target and the mappings are
authored.** For each candidate word, the question is whether the graph holds
a concept that licenses it. A word that can be licensed gets a mapping. A
word that cannot is the signal the recorded rule already describes, meaning
either the mapping was not identified or a concept is missing.

**This inverts the usage. The standard tests the graph rather than
supplying the lexicon.** The benchmark survives, the gap analysis comes
free, no share-alike obligation touches a CC0 corpus, and the concept
coverage invariant holds.

## How ownership was resolved

A word maps to exactly one concept. 444 new words were drafted against 48
level-one concepts, and 130 of them were claimed by more than one.

Resolution is a **precedence order over concepts**, most concrete and most
primitive first, plus an **explicit override table** of 25 entries where
the precedence got the answer wrong.

The overrides are a table rather than a reordering of the precedence,
because reordering to fix one case silently moves others. A table states
each judgement where it can be read.

Ninety-five drafted words were already function words in `core` and were
dropped rather than mapped, since a function word names nothing.

## Two rules changed, both for the same reason

The file's role changed, and two checks encoded the old role.

**Coverage is retired.** It required every term admitted at level L to
appear in some level-L record. That could only ever fire on a mistake while
the vocabulary was derived from the corpus, because every admitted word was
used by construction. A prescriptive lexicon is authored ahead of its
corpus, so a licensed word no record has reached is the expected state.
Enforcing it would require a corpus to exhaust its lexicon before the
lexicon could be written.

**Utilisation replaces it as a number, never a violation.** A corpus using
little of its lexicon means either a thin corpus or a padded lexicon, and
the figure does not distinguish them, so it is reported rather than gated.

**The lower bound now tests against the schedule.** A word may not be
introduced before the concept it names is taught. That is right, and
"is taught" was being measured against whichever records happened to exist.
**A schedule states where a concept is taught. Records only show where it
has been taught so far.** Measured against records, a prescriptive lexicon
fails for every word whose corpus is not yet written.

## What is not claimed

The lexicon has not been checked word by word against Ogden's 850. The
coverage test described above is the intended method and has not been run
as a gap analysis, so no claim is made about how much of that standard this
lexicon covers.

Ogden's United Kingdom copyright term was not verified. It turns on his
death year, which was not checked. The point is moot under the decision
above, since nothing was imported.
