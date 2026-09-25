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

## A book is a Markdown file, not JSON

**Changed 2026-09-24, on the ratio.** A level-one book of 173 words
occupied **260 lines** of JSON structure. The same book is now 81 lines
with the prose readable at the bottom.

**The project's own sequence makes reading the corpus the step that decides
whether generation continues.** `CURRICULUM_LEVELS.md` step three is a
hundred records generated, validated, and read, and if they are bad
everything downstream is bad. A format that obstructs reading obstructs the
one check nothing automates.

It also gets worse with level, which is the argument that settles it rather
than the ratio. A level-five record is a paragraph. A level-seven one draws
on real literature. Neither survives being escaped into a JSON string
field, and choosing the format for the level we happen to be writing is how
a decision becomes expensive later.

### The shape

Front matter between `---` lines, holding the book and one compact line per
record annotation. Then the prose, in blocks marked by the record
identifier.

```
---
{
  "id": "bk.cup",
  "level": 1,
  "title": "The Cup",
  "subject": {"kind": "domain", "target": "directed_physical_interactions"},
  "records": {
    "bk.cup.d01": {"concepts": ["change"], "claim_class": "formal", ...}
  }
}
---

[bk.cup.d01]
Things do what they do. You can make a thing do other things.
```

**Blocks are marked, not positional.** Positional matching is silent when
an insertion shifts everything by one, which is the failure shape this
project keeps finding in its own checks. A block with no annotation, an
annotation with no block, and a repeated identifier are all rejected.

A block runs to the next marker, so a multi-paragraph record needs nothing
special.

## The metadata a book carries about itself

Six fields beyond the subject, all optional in the schema and all present
on every level-one book as of 2026-09-25. `book_head` writes them and
omits any that is empty, so an absent field means nobody has got to it
rather than that it is blank.

| Field | What it is |
| --- | --- |
| `about` | What the book is about, for a curator |
| `teaches` | What a reader should come away knowing |
| `author` | Who the book is by. `docs/decisions/BOOK_ATTRIBUTION.md` |
| `licence` | The SPDX identifier for the corpus licence |
| `first_published` | Date of the earliest commit touching the file |
| `published` | Date of the latest |
| `form` | `question` for a question-and-answer book, else absent |

**`about` and `teaches` are the one place a level's vocabulary ceiling
does not apply.** They are written in ordinary English for a person
choosing books, and are not text a model trains on. A description
restricted to the book's own words would say what the title already says.

**The two dates are derived, never written.** `tools/stamp_books.py`
reads them from the commit log in one pass and is idempotent, and its
`--check` mode fails when a committed book's `published` field disagrees
with its own history.

**NEVER REBUILD A BOOK BY LISTING ITS FIELDS.** Use `book_head` to write
one and `dataclasses.replace` to change one. Two constructions each
dropped five fields by enumerating them, and one would have stripped
`form` from every question-and-answer book in a single bulk run. A test
walks the dataclass and fails if a field added later is not carried
through a read, a write and a read again.

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
