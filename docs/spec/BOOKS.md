# Books

A record teaches a concept. **A book is where a reader is told what the
words mean before they are used**, and where the material that uses them
runs as one thread rather than as unconnected assertions.

Implemented in `../../src/epagoge/book.py`, gated by
`../../tools/validate_books.py`.

## Why the corpus needs them

The first measured generation runs produced records like these, every one
true, admissible, on-concept, and lifeless.

```
[presence]           The cup is here.
[emptiness]          The cup is empty.
[household_object]   The cup is on the table, and it stays there.
[direction]          She moves forward.  It goes forward.  It moves forward.
```

**Nothing connects one sentence to the next, so the generator has no reason
to vary them.** Three near-identical lines for `direction` are not a bug in
the teacher. They are what a prompt with no context produces.

A book gives the variation a reason. An empty cup filled with different
liquids and emptied different ways covers emptiness, liquid, containment,
quantity, action and causation in one thread, and the repetition is the
pedagogy rather than an artifact.

## Shape

Three parts, in order.

1. **The subject is defined.** The domain or the topic the book is about.
2. **The words are defined.** Each in the vocabulary of its own level.
3. **The story uses them.**

That ordering is the whole point. A definition with nothing following it is
a glossary. A story with no definitions in front of it assumes vocabulary
the reader does not have.

## Definitions live on records, not on books

A book is an ordering of records. A definition belongs to the sentence that
makes it, so a record carries an optional `defines` of a kind and a target.

| Kind | Target |
| --- | --- |
| `word` | a vocabulary term |
| `domain` | a declared domain |
| `topic` | a schedule unit, the smallest thing a book can be about |

## Rules the validator enforces

1. A book holds at least one record, and every record it names exists.
2. Every record in a book is at the book's level.
3. No record is in two books.
4. **A book defines its own subject.** A book about a thing that never says
   what the thing is leaves the reader to infer it, which is the failure
   this shape exists to fix.
5. **No definition after the material that uses it.** A word defined after
   the story is a glossary at the back.
6. Every definition target exists in its own namespace.

## The closure property, which the lexicon was not authored for

**Every definition is written in the vocabulary of its own level.** At
level one that means about seven hundred words defining themselves.

Ogden's Basic English was designed for exactly this and selected its 850
words so that anything could be said in them. **This lexicon was authored
concept by concept and was never tested for definitional closure.** Some
words may not be definable in the remaining vocabulary, and that is a
property of the lexicon rather than of any particular book.

It has not been tested. The first book defines six words.

## Coverage is reported, never gated

A word with no definition is not a defect in an unfinished corpus, and it
is one in a finished level. `validate_books.py` prints the fraction defined
for words, domains and topics at each level, and fails on none of them.

## What the claim taxonomy does not have

**A definition is not one of the six claim classes.** It is not formal by
proof, not empirical, not an attributed position, not a conditional result,
and not normative. Definitions are stipulative.

The first book uses `formal` with a `lexicon:` or `domain:` source claim,
which is the nearest fit and is not a good one. **Recorded as a gap in
`../decisions/OPEN_QUESTIONS.md` territory rather than solved here**, since
adding a class to the taxonomy touches the validator, the generator and
every record already written.
