# generators/

The corpus synthesis pipeline. Executable stages that produce records for
`corpus/` from the specifications in `curriculum/`.

**Status.** `generate.py` runs end to end. **Its output is not yet usable**
and the reason is recorded below.

## Trust boundary

This directory is where untrusted input enters the system. Output from a
teacher model is untrusted by the same standard as any external input.
Every record must be validated against a declared schema before it reaches
`corpus/`, and a record that fails validation must be rejected loudly
rather than repaired silently.

A synthetic corpus inherits the errors and the dispositional biases of
whatever model generated it. The verification layer is the only thing
standing between a teacher model's confident error and the trained model's
confident error, so it is a primary component rather than a convenience.

## Teacher

Chosen and pulled 2026-09-24. See `TEACHER.md`.

## A prompt must carry the concept boundary

Established by the first two generations attempted. Asked to teach that
repeated use wears things out, the model returned sentences about things
breaking and chains snapping, which is sudden failure and a different
concept that the graph deliberately separates.

One negative constraint fixed it.

**A generation prompt therefore supplies the concept, its grounding
primitive and observation, and its nearest graph neighbours as explicit
exclusions.** The graph holds the neighbours already, so exclusions are
derived rather than authored.

The failure this prevents is the expensive kind. Fluent text that blurs the
distinction the curriculum exists to draw, passing schema validation and
reading well, catchable only by a human reading one record at a time.

## First measured run, 2026-09-24

Fourteen level-one concepts, three sentences each, three attempts each.

| | |
| --- | --- |
| Asked for | 100 |
| Accepted | **16** |
| Rejected at the vocabulary ceiling | 84 |
| Retries spent | 24 |

**The pipeline is not the problem. The vocabulary is.**

### The ceiling is enforced, and it works

A first run without the retry loop produced **zero of twelve** admissible
records, with 29 percent of tokens outside the level-one word list. A soft
instruction to stay inside a word list is one the teacher does not follow.

Re-asking with the specific offending words named took that to **ten of
ten**. A generic repeat of the constraint produces a generic repeat of the
violation. Naming the words converts the instruction into one the teacher
can act on.

### The root cause of the 84 percent

**`curriculum/vocabulary.json` is a descriptive artifact being used as a
prescriptive one.** It was derived to describe the words the sample corpus
happens to use, and at level one that is 156 function words and **64 content
words**. It was never authored as a lexicon a level-one corpus must be
writable in.

Thirty concepts cannot be taught distinctly in 64 content words. The
measured symptom is the teacher returning the same few sentences for
different concepts, because the vocabulary leaves it nowhere else to go.

Three ways out, none of them the generator's to choose. Author a real
level-one lexicon. Teach fewer concepts at level one. Or accept surface
repetition and deduplicate at the concept level rather than the sentence
level, which the operator has said the corpus needs anyway.

### Exclusions are correct and drift persists

`duration` correctly excludes `sequence`, and the teacher still returned
"Each drop happens after the one before," which is sequence.

**Vocabulary is now mechanically enforced. Semantics is not.** The
exclusion mechanism reduces conflation and does not eliminate it, so the
verification layer below is load-bearing rather than optional.

### Two defects found by reading the output

**A one-word fragment passed every check.** The ceiling asks whether every
word is admissible and a fragment satisfies that trivially. Caused by a
line splitter that stripped any leading run of digits, dots and dashes,
which ate the first word of a line beginning with a number word. Fixed, and
a minimum length added.

**The same sentence was written for two different concepts.** "The cup is
empty" arrived for both `household_object` and `emptiness`. That attributes
one piece of teaching to two ideas, which is the conflation the exclusions
exist to prevent, arriving as duplication rather than as drift. Deduplicated
across the run.

## Measured runs

| Run | Level-one words | Exclusions | Concepts | Accepted | Rejected | Produced nothing |
| --- | --- | --- | --- | --- | --- | --- |
| 1, no retry loop | 675 | prerequisites, dependents, siblings | 14 | 16 | 84 | — |
| 2, retry added | 675 | prerequisites, dependents, siblings | 14 | 36 | 41 | 0 |
| 3, lexicon expanded | 870 | prerequisites, dependents, siblings | 24 | 57 | 74 | **3** |
| 4, exclusions corrected | 870 | prerequisites, siblings | 24 | **61** | **59** | **1** |

## Excluding dependents starved the general concepts

**Run three produced nothing at all for `change`, `material` and `sound`**,
which were the three concepts carrying the longest exclusion lists at five,
six and five. Every concept carrying one exclusion produced everything
asked of it.

**A general concept is taught through its instances, and its instances are
exactly its dependents.** `material` was forbidden from mentioning metal,
liquid, heat or shape, which leaves almost nothing a material can be said
to be. `change` was forbidden from mentioning anything that changes.

Dependents were added to the exclusion list on reasoning rather than on
evidence, with the argument that the recorded conflation was between a
concept and its prerequisite so siblings alone would not have caught it.
That argument was right about prerequisites and wrong to generalise.

**Prerequisites and siblings are excluded. Dependents are not.** A
prerequisite is prior knowledge a record may teach instead of its target,
which is the recorded failure. A sibling is coordinate and confusable. A
dependent is built on the target, so using it to illustrate the target is
teaching rather than drift.

**Run four confirms it.** `change` and `material` recovered. `sound` did
not, and `sound` is the one concept still carrying five exclusions, because
its prerequisite `change` has many other dependents which are therefore its
siblings. That is one datum and it is consistent with the count hypothesis
rather than proof of it.

The recorded wearing-out case still holds. `wearing_out` still excludes
`things_break`, which is its prerequisite.

## Book generation, 2026-09-24

`generate_books.py` asks for a whole book in one completion. Sentence-at-a-
time prompting produced true, admissible, lifeless records, because nothing
connected one sentence to the next and the teacher had no reason to vary
them.

**It works.** A first book came back with a subject definition, seven word
definitions and nineteen story lines, 236 words, inside the hundred to
eight hundred range an operator gave for a level-one book. The story has
continuity, and its last line returns to the subject definition unprompted.

### Three defects found by reading the output

**The terminal control codes, which had been corrupting every long
completion.** The runtime rewrites each line as it wraps, emitting a
partial word, a cursor-back, an erase, a newline, and then the word again
in full. Three attempts were needed to handle it. Stripping the escape
codes left the partial word, so fragments like `someth` and `fl` were
counted as words outside the vocabulary. Replaying the delete left the
newline, which truncated every wrapped sentence and cost it its full stop,
so 29 of 40 rejections were "not a sentence". The sequence is now replayed
whole, delete and join. **Setting a wide terminal does not help. The
runtime wraps regardless.**

Every earlier batch was checked for escape bytes and none carried any,
because short lines never wrap. Rejection counts in those runs may still
have been inflated by longer completions that were never inspected.

**The retry discarded good output.** It took the later answer wholesale, so
a worse second attempt replaced a better first one and a book that had
seven usable records came back with two. Definitions now accumulate across
attempts.

**Merging accumulated two different stories.** Definitions stand alone and
may be merged. A story is a sequence and may not. The merged version had a
boy find a book and then, with no transition, look forward to a game. The
longest single attempt is kept.

### What the teacher reaches for and cannot use

Eight book prompts produced 110 distinct words outside the ceiling.
`something` led at fifteen occurrences and was simply absent. Fifty-eight
words were added on that evidence, including `direction` itself, which was
a concept whose own name was not in the lexicon.

**The lexicon is not frozen**, so a word the teacher needs is evidence
rather than an error. One exception was left alone. `part` and `whole`
belong to `component_and_system`, which the schedule places at level two,
and moving it would change the very split the ordering ablation tests.

## A rejected line is input, not waste

**Operator policy, 2026-09-24.** Books are edited rather than discarded
unless the quality is so poor that inclusion would be unwise. A rejected
line is a sentence the teacher wanted to write and could not, so **either
the words belong in the lexicon or the sentence needs different words**,
and a counter cannot tell those apart.

The pipeline is therefore three steps rather than one.

**Rework.** A line rejected for vocabulary is asked again, naming the words
it may not use. What survives enters the book. This recovered subject
lines, definitions and story lines that the earlier version dropped.

**Withhold.** A book whose subject definition does not survive is not
written into the corpus, because a book about a thing that never says what
the thing is fails the book rules. The whole book goes to quarantine with a
reason rather than being deleted.

**Triage.** Whatever the rework could not fix is written to a quarantine
file, and `tools/triage_quarantine.py` ranks the offending words and says,
for each, whether it is already licensed at some higher level or absent
from the lexicon entirely. **A word high on that list and absent is a
candidate for addition. A word already licensed above the level is working
as intended** and the sentence using it needed rewording.

Books are written one file each into `curriculum/books/level_1/`, records
inline, so a book is a single artifact a reviewer can read before deciding
whether it belongs.

### Three defects this exposed in my own pipeline

**Reworked records were created and then dropped**, because nothing added
them to the book they came from. A record outside every book is not in the
corpus.

**Subjects were excluded from rework**, which was exactly backwards. The
subject is the one line a book cannot be valid without.

**Reworked records carried no concept**, because the concepts were threaded
into one of the three collection points and not the other two. A record
with no concept now cannot be reworked into the corpus at all.

## Open constraint

The verification layer that rejects unsupported claims is specified in
`docs/decisions/OPEN_QUESTIONS.md` item two and is not yet implemented. The
drift finding above is the evidence that it is needed rather than an
assumption that it might be.
