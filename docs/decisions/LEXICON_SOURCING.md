# Sourcing the level-two lexicon

**Recorded 2026-09-25, operator direction.** The level-two lexicon holds
871 words against a target of about ten thousand. This is the pipeline for
closing that, and the reasons it is shaped as it is.

## The pipeline

1. **Seed from three lists plus what exists.** The level-one lexicon,
   Dale-Chall, the New General Service List, and Ogden's Basic English.
2. **Scan every public-domain and CC0 source** identified in
   `READING_LEVEL_RESEARCH.md`.
3. **Accept the frequent words in bulk.**
4. **Inspect the long tail per source**, because that is where a source's
   idiosyncrasies live and where judgement is worth spending.
5. **Remove what has fallen out of the vernacular**, at drafting time.

## Frequency is per source, and that is the load-bearing choice

**A word frequent in one source and absent from the rest is a word that
source needed.** Pooling counts across sources would bury it under the
long tail of everything else, and a book about levers is the only place
`lever` will be common.

So `scan_lexicon.py` counts each source separately and reports two groups:
frequent in at least one source, and long tail in every source. **The two
get different treatment**, which is the whole point of separating them.
The first is bulk work. The second is one word at a time.

## Provenance is recorded at admission

A `Term` now carries a `source`, free text, written when the word is
admitted.

**This corpus is CC0 and two of the three seed lists are not.** Dale-Chall
has no licence anyone could find, and the New General Service List is CC
BY-SA, which a CC0 repository cannot carry. **None of the three is
committed here.** They are supplied as files at scan time, and what the
repository keeps is this project's own definitions of whatever words
survive judgement.

Consulting a list to decide which English words to define is not the same
act as redistributing that list. **That distinction is only auditable if
the origin is written down**, which is what the field is for.

It also separates two different kinds of evidence. A word the teacher
reached for is evidence about the corpus. A word a frequency scan proposed
is evidence about a source. They have been treated alike until now and
they are not alike.

## Archaism is not visible to a counter

**A public-domain source is public domain because it is old.** A word can
be frequent, plainly useful in 1880, and wrong for a child now. No
frequency threshold sees that, and nothing in this pipeline will.

The operator's reservation to remove such words at drafting time is
therefore not a safety net on the pipeline. **It is the only place that
check happens**, and it should be planned for rather than relied on.

## Adapting modules from public-domain works

**Operator direction: it probably makes sense, and the provenance
advantage is real.** A module adapted from a public-domain text is
traceable to a named source in a way a generated one is not, and this
project's thesis is about curation, which is easier to defend when the
material has a history.

**Two cautions, neither fatal.**

The drift caution applies with more force to prose than to vocabulary. A
word can be swapped; a passage carries its period's assumptions in its
structure.

And an adapted module is a derivative work of its source, where an
extracted word list is arguably not. **For a public-domain or CC0 source
that is fine and needs no judgement**, which is another reason to prefer
the Smithsonian and federal material over the licensed textbooks.

## What is not settled

**Whether consulting Dale-Chall and the NGSL is compatible with CC0.** The
engineering is blocked on it either way, and the pipeline is built so that
the answer changes which files are passed in rather than what the tools
do.

**What counts as frequent.** The threshold is a parameter with a default
of five and no measurement behind it. It should be set from what the first
real scan looks like rather than guessed now.

## Every admitted form must be used, and level one does not manage it

**Operator invariant 2026-09-25.** Every word in a level's lexicon must
appear in that level's corpus, and that means every surface form: all
inflections, singular and plural. A corpus using `run` and never `ran` has
not used what the lexicon claims.

**Measured, and the suspicion was right.** Level one admits **2,051
surface forms and uses 1,355**. **696 are never used, a third of the
lexicon**, and thirteen headwords appear in no form at all: `aim`, `boss`,
`cheater`, `depend`, `fact`, `forbidden`, `hook`, `insect`, `judge`,
`palm`, `scab`, `special`, `ten`.

**Most of the gap is inflections rather than words.** Six bases have all
four of their forms unused, and the common shape is a verb whose base
appears and whose past and participle do not. That is the same asymmetry
the project found from the other side, when seven nonsense past tenses
were admissible for several commits: **inflections are admitted
automatically and used only if a writer happens to need them.**

`tools/unused_words.py` reports it and the gate runs it. **It never
fails**, because each unused word is one of three things and no checker
can tell which.

## What an unused word means, and why it is a judgement each time

1. **An existing module should include it.**
2. **A module should be drafted that includes it.**
3. **Admitting it was a mistake and it should be culled.**

**Archaism is not a reason to cull.** A historical account needs the words
of its period to tell it accurately, so an archaic word may be exactly
right somewhere in the curriculum. What archaism implies is that a word is
not needed *now*, which is a question about **which level it belongs at**
rather than whether it belongs at all.

**And that placement may be arbitrary.** A word that has to exist
somewhere and has no natural home gets one chosen for it. Recording that
the choice was arbitrary is worth more than pretending it was derived.

**The order of work matters here.** This list is most useful after a
level's corpus is drafted rather than during. Culling from a half-written
corpus removes words the unwritten half would have used.
