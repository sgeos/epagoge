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

## The gap analysis, run for the first time on 2026-09-24

The section above describes testing the graph against a published standard
and records that it had not been run. **It has now been run from the other
end**, driven by what the dictionary generator actually failed on rather
than by a word list, which is the better method and was not the one
planned.

### What the dictionary was blocked by

Two runs produced fifteen definitions from 144 word-requests. **Every
rejection classified was the same cause**, a definition reaching outside
the level's vocabulary, and the offending words were not a long tail. The
same handful recurred in every batch. `amount`, `part`, `last`,
`position`, `present`, `center`, `length`, `location`.

Checked against the 56 words a dictionary definition runs on.

| | Count | Examples |
| --- | --- | --- |
| Available at level one | **37** | `piece`, `kind`, `way`, `thing`, `place`, `side`, `end`, `middle`, `shape`, `same` |
| Present but **above** level one | **5** | `part` L2, `amount` L2, `last` L2, `group` L5, `position` L6 |
| **Absent from the lexicon** | **14** | `bit`, `sort`, `type`, `center`, `form`, `surface`, `area`, `length`, `width`, `location`, `similar`, `act`, `event`, `state` |

### The finding

**The lexicon was selected by what a preschooler knows. A self-hosting
dictionary needs what you write definitions with.** Those are different
criteria. The overlap is large and **the gap is exactly what blocks
closure**.

There is no level-one way to say what an arm is without `part`. Three of
the twelve words in the first classified batch wanted that one word.

**This is the first concrete evidence on whether the lexicon is closable**,
and it is more tractable than that question sounded, because the missing
set is small, stable, and identifiable by running the generator rather than
by judgement.

### The two classes need different remedies

**Above level one** is a curriculum question, not a lexicon one. A word may
not be introduced before the concept it names is taught, so promoting
`part` means scheduling `component_and_system` at level one. That is a
schedule change with consequences for the ablation domains.

**Absent entirely** is the signal the section above already describes,
meaning either the mapping was not identified or a concept is missing.
Several look licensable against concepts the graph already holds, and
`state` and `event` do not.

**Neither is applied here.** Both change the lexicon's selection principle
rather than repairing an error in it.

### A caution on the obvious fix

Adding the blockers will unblock these definitions and **will produce a new
blocker list**, since the added words then need defining themselves. The
question the next run answers is whether that list is shorter than this
one. **If it is not, the lexicon is not closable by addition** and the
answer is a smaller defining subset rather than a larger lexicon, which is
what a controlled defining vocabulary is.

## One word, several senses, recorded 2026-09-25

**Operator correction.** A dictionary gives more than one definition, and
a level-one preschool dictionary cannot avoid it either. The model held
**one concept per word**, so admitting a word silently asserted that it
meant one thing.

### The inflection check found it before the argument did

Marking verbs exposed `set`, which is the noun under `correspondence` at
level one and whose plural `sets` is the noun under `grouping` at level
two, while the verb demands `sets` as its third person. **One word, two
parts of speech, and the rule could not hold both.** The verb marking was
withdrawn at the time. It has now been restored properly.

### What changed

A word may carry several senses, each with its own concept, level and part
of speech. Three rules follow.

- **A form shared by two senses of one word is ordinary.** `sets` is the
  plural of the noun and the third person of the verb.
- **A form shared by two different words is still rejected**, because
  nothing can then decide which concept the token carries. `saw` as the
  tool and `saw` as the past of `see` would be that case.
- **Admissibility asks whether any sense is reachable.** A generator at a
  level can use a form as soon as one of its senses is admitted, which is
  why `lookup` returns the earliest and `senses` returns all of them.

### Only admitted senses are listed, and that is the point

**The absence of a sense is a statement.** `ground` is the earth and it is
also the past of `grind`. `swallow` is an action and it is also a bird.
Neither second sense is level-one material, so neither is listed, and the
lexicon thereby says so.

That is a better answer than a completeness rule would give, because
**completeness over senses would drag in exactly the material the level
excludes.** The operator's phrasing is the test worth keeping. Grinding
swallows is probably not a level-one concept.

### Six senses added

Each is a second sense of a word already admitted, and each was missing in
a way that mattered.

| Word | Held | Added | Why it mattered |
| --- | --- | --- | --- |
| `set` | the noun | the verb, to put down | The case that forced this |
| `kind` | being kind | a kind of thing | **Definitions need it**, as in a kind of container |
| `right` | the direction | correct | **The four moves need it**, as in that is right because |
| `like` | resembling | to enjoy | Ordinary preschool sense, absent |
| `mean` | to signify | unkind | Ordinary preschool sense, absent |
| `watch` | to look | the thing telling time | Ordinary preschool sense, absent |

### The dictionary now writes one entry per sense

`prompt.definitions` takes a sequence of senses rather than a mapping from
word to concept, **which was silently dropping one of every pair**. The
generator batches by sense and the prompt shows the concept beside each,
so the teacher is asked for the sense rather than for the word.

## The dictionary and thesaurus are reference material, 2026-09-25

**Operator direction.** Both are lexicon analysis tools during authoring
and **level-one reference material afterwards**. The second role is what
sets the requirements, and it is stricter than the first.

| Requirement | Follows from |
| --- | --- |
| The dictionary defines every word in words the level admits | Self-hosting. Already enforced at the generator boundary |
| The thesaurus covers **every dictionary sense** | Reference material with holes is not reference material |
| Both are written in level-one words | A reader at level one has nothing else |

### Antonymy belongs to a sense

The thesaurus was a flat list of word pairs, which cannot hold `right`,
since it opposes `left` as a direction and `wrong` as a judgement. **This
is the same failure the lexicon had**, where one concept per word could
not hold `set`, and it was found the same way, by a case rather than by
reasoning.

It is now one entry per lexicon sense. 834 entries covering all 815
level-one senses.

### Coverage is required, an antonym is not

**A sense with no entry is a sense nobody has looked at**, so an uncovered
sense fails the gate. **An entry with no antonym is not a failure**,
because most nouns oppose nothing and requiring one would invent
oppositions to satisfy a check.

### A core word may hold an entry with no concept

`up` against `down`, `yes` against `no`, `here` against `there`. These
name nothing, so they have no sense and no concept, and **dropping them
would make the reference material worse in order to serve the analysis
tool**. Eighteen core words carry an entry.

### Antonymy is symmetric, between licensed words

If one names the other, the other must name it back. The rule is confined
to licensed terms, since a core word has no entry obliged to exist.

### What is emitted

`build_corpus.py` writes the thesaurus after the dictionary, as sentences
in the level's own vocabulary. **Only entries carrying a relation are
emitted**, since a line recording that a noun opposes nothing teaches a
reader nothing. 101 relations, phrased with `opposite` and `mean the
same`, both already admitted.

### Still open

**No synonyms are recorded.** The structure holds them and the check
enforces their reachability, and nothing has been authored. Synonym sets
are the larger half of a thesaurus and are authoring work rather than
analysis.

## What is not claimed

The lexicon has not been checked word by word against Ogden's 850. The
coverage test described above is the intended method and has not been run
as a gap analysis, so no claim is made about how much of that standard this
lexicon covers.

Ogden's United Kingdom copyright term was not verified. It turns on his
death year, which was not checked. The point is moot under the decision
above, since nothing was imported.
