# Current brief. Finish the metadata, then lengthen the corpus

**Written 2026-09-25**, replacing the three-problems brief, whose items
are carried forward below. Delete when `COMPLETION_CONDITION.md` is met.
Durable practice is in `PROCESS_STRATEGY.md` and is not repeated here.

## The present goals, as the tree reports them

| Goal | State, measured 2026-09-25 |
| --- | --- |
| Level-one book metadata | **0 of 246** books carry any of six fields |
| Level-one corpus length | **229 of 244** content books below the word band |
| Level-one lexicon utilisation | **688 of 2,051** surface forms never used |
| Level-two lexicon | 879 words against a target near 10,000 |
| Schedules for levels three to seven | None exist |
| Level seven | Not started. `sources/` empty, licensing unexamined |
| Ordering ablation | Blocked on an endpoint the operator holds |

The last four are the operator's and are listed in the handoff. They are
not this brief's.

## What to pursue, and why in this order

**First, book metadata, to completion.** It is bounded, finishable in one
sitting, and it has sat at zero across three sessions while the capability
to do it existed. The operator asked for `about` and `teaches` once and
for `author`, `licence`, `first_published` and `published` again later.
This is the project's own rule about unblocking not being authoring,
applied to the one case where the tooling was already built.

**Second, corpus length**, with whatever budget remains. It is the larger
prize, since the corpus is the *measured* limit on model quality, and it
needs no new book. But it is open-ended where the metadata is bounded, and
finishing beats starting.

**Not lexicon utilisation.** Each of the 688 unused forms is a judgement
about whether a module should use it, be drafted for it, or whether
admitting it was a mistake. A loop cannot make that call and should not
pretend to.

## Two defects found before any of this work started

Both were found in the first ten minutes, by reading the tool rather than
running it. Neither would have announced itself.

**`generators/describe_books.py` rebuilds a `Book` by enumerating its
fields.** It passes seven and the dataclass has twelve, so a bulk run
would silently strip `form` from the **17 question-and-answer books**,
along with any of the other four fields already present. This is exactly
the failure `book_head` was written to prevent, and its docstring claims
the problem is solved because one function now writes the front matter.
**The writer side was fixed and the constructor side was not.** Fix it
with `dataclasses.replace` so the set of fields is never enumerated again.

**`src/epagoge/book.py:books_from_json` drops the same five fields on
read.** Any consumer of `load_books` sees books whose form and metadata
are absent rather than empty, and cannot tell the difference.

**Do not run the bulk description pass until both are fixed**, and add a
round-trip test that fails when a field is added to `Book` and not carried
through. A guard that has not been shown able to fail is not a guard.

## Wrong turns to avoid, specific to this work

- **`--limit` defaults to 10.** A bulk run needs an explicit count, and
  the printed total is the check that it did what was asked.
- **Do not apply the vocabulary ceiling to `about` and `teaches`.** They
  are deliberately unrestricted, written for a person and never trained
  on. That is the whole reason this task cannot fail the way corpus
  generation fails.
- **Fold typography.** The first generated description carried a curly
  apostrophe, which lands in the JSON as `’`. The project already
  lost four sentences to curly apostrophes once.
- **`author` and `licence` are decisions, not derivations.** Pick a
  defensible value, record why in a decision record, and do not invent
  something that reads as a claim about authorship the project cannot
  support. `first_published` and `published` *are* derivations, from the
  git history of each book file, and must be derived rather than guessed.
- **Read a sample of the output, not only the count.** Two interventions
  once raised acceptance and moved closure not at all.
- **Metadata is not corpus.** Adding six fields to 246 books changes no
  measured model property. Do not report it as corpus growth.
- **The run is about twenty-five seconds a book**, so 246 books is
  roughly one hundred minutes of teacher time. Run it in the background
  and do something else; do not sit on it.
- **Gate, read the exit code, stop, then commit.** Three commits have
  landed on a red gate by running both in one breath.

## Carried forward from the three-problems brief

The framing in `../decisions/THREE_PROBLEMS.md` still governs. Level one
is bootstrapping and is solved in its essentials. Levels two to six are a
scheduling problem where coverage and consistency bind, not volume. Level
seven is a transition problem that has not started.

The specific wrong turns recorded against lexicon work, generation
acceptance, thesaurus synchronisation and inflection remain in the git
history of this file and in `PROCESS_STRATEGY.md`, which holds the classes
they belong to.
