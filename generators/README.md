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

## Open constraint

The verification layer that rejects unsupported claims is specified in
`docs/decisions/OPEN_QUESTIONS.md` item two and is not yet implemented. The
drift finding above is the evidence that it is needed rather than an
assumption that it might be.
