# Current brief. Settle the capacity confound, and keep lengthening

**Written 2026-09-25 and revised the same day** after the metadata goal
was met and a confound was found in the project's central measurement.
Delete when `COMPLETION_CONDITION.md` is met. Durable practice is in
`PROCESS_STRATEGY.md` and is not repeated here.

## The present goals, as the tree reports them

| Goal | State, measured 2026-09-25 |
| --- | --- |
| Level-one book metadata | **Done.** All six fields on all 246 books |
| Is the corpus really the limit? | **Confounded.** Untested below width 128 |
| Level-one corpus length | **203 of 244** content books below the word band |
| Level-one lexicon utilisation | **688 of 2,051** surface forms never used |
| Level-two lexicon | 879 words against a target near 10,000 |
| Schedules for levels three to seven | None exist |
| Level seven | Not started. `sources/` empty, licensing unexamined |
| Ordering ablation | Blocked on an endpoint the operator holds |

The last four are the operator's and are listed in the handoff. They are
not this brief's.

## What to pursue, and why in this order

**First, settle whether the corpus is really the limit.** The project
records that the model is limited by corpus and not by training, and that
conclusion sets every priority downstream of it. It rests on a width sweep
of exactly two points, 1.39M and 4.35M parameters, both far into the
regime where a model memorises its data. **A two-point sweep entirely
inside the memorisation regime cannot separate "the corpus is too small"
from "the model is too big for this corpus."** Nothing below width 128 has
ever been run. Each run costs a minute or two, so this is the cheapest
test of the most load-bearing claim in the project.

It matters beyond tidiness. If a much smaller model generalises better on
the same tokens, then part of what is recorded as a corpus limit is a
capacity choice, and that is fixable today where corpus growth is eleven
hours of teacher time.

**Second, corpus length**, continuously in the background. It is the
larger prize and needs no new book, but it is open-ended.

**Not lexicon utilisation.** Each of the 688 unused forms is a judgement
about whether a module should use it, be drafted for it, or whether
admitting it was a mistake. A loop cannot make that call and should not
pretend to.

## What the teacher said, and what it is worth

Asked to rate `sporos` given the project's maturity, the teacher answered
**extremely disappointing**, and its diagnostics were partly sound: the
model collapses to `the cup is` whatever it is asked, and every answer to a
question begins with `was`. Both are reproducible.

**Its causal reasoning was not sound, and the difference matters.** It
argued that worse-than-chance held-out loss under overtraining "confirms
the corpus is structurally impoverished." It does not. That is the ordinary
signature of overfitting a small dataset, which is a statement about size.
It also called `cup` a dominant subject; measured, `cup` is 1.69 percent of
content-book tokens and appears in 85 of 244 books. Disproportionate among
content words by a factor of 2.7, not dominant.

**And it was judging its own prose.** Treat the verdict as one model's
opinion, and the attractor collapse as the finding worth keeping.

## Three defects found by reading the tools rather than running them

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

**`generators/generate_books.py` was the third and the worst.** It built
front matter from four fields and wrote it to the book's own path, so
regenerating any of the 95 completed units would have erased its form and
all six metadata fields. All three are fixed, a test walks the dataclass
rather than listing names, and the gate now fails on a book missing a
field whatever erased it.

## Wrong turns to avoid on the capacity question

- **Do not compare a new sweep against the recorded 4.789.** That figure
  was measured on a 55,510-word corpus. The corpus is now over 70,000
  words and growing. **Comparisons are valid only within one sweep on one
  frozen corpus**, which is why the fill is suspended while a sweep runs.
- **Do not read held-out loss alone.** A small model can win on held-out
  loss because it underfits everything equally. Read the gap as well; the
  whole point of the diagnosis tool is that the two together separate
  undertrained from out-of-corpus.
- **Do not invoke compute-optimal scaling laws as though they transfer.**
  They were fit at far larger scale for compute-optimal training, not for
  small-data generalisation. The tokens-per-parameter ratio is a reason to
  run the experiment, not evidence about its outcome.
- **A negative result is the result.** If no width below 128 helps, then
  the project's conclusion survives a stronger test and that is worth
  recording plainly. Do not keep widening the grid until something moves.
- **Do not overwrite `evals/pilot/level_1_diagnosis.json`.** It documents
  the old corpus and is cited. A new sweep gets a new file.

## Wrong turns to avoid on the metadata work, kept for the record

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
