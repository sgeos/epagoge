# Completion condition

Judge against the repository tree. **Ordering is explicitly not a
completion criterion.** Any sequence of steps leaving the tree in the state
below is complete. No branch, process, or commit-shape requirement.

**A measurement that falls short satisfies this. A good result is not
required and must not be manufactured.** Where a target is missed, the tree
records the figure reached and why.

**The level-one condition below was met on 2026-09-26.** It is kept because
a condition that is deleted once met leaves nothing to check a regression
against. Anything that would break a clause here is a regression.

## Level one

- Every book under `curriculum/books/level_1/` carries `about`, `teaches`,
  `author`, `licence`, `first_published` and `published`, and a check
  reports how many do.
- The two dates are derived from each file's version history by a tool in
  the tree, not assigned. A decision record gives the `author` and
  `licence` values and what was rejected.
- Every sixteen-spread content book is inside the level-one word band.
  None is above it.
- Every unit in `curriculum/schedule/level_01.json` has at least one book,
  and every book that is not a dictionary holds exactly sixteen spreads.
- No code rebuilds a book by listing its fields, and a test fails if a
  field added to the book model is not carried through a read, a write and
  a read again. The test has been shown to fail against a broken case.
- The seventeen question-and-answer books still declare their form.

## Measurement is reproducible and honest

- A model-size sweep and a corpus-fraction sweep at level one are both in
  the tree, each naming the corpus it ran against, and a tool in the tree
  reproduces both.
- No figure is compared against one measured with a different held-out set,
  a different temperature, or a different corpus, unless the text says so.
- Distinct-token share and attractor frequency are not presented as
  quality measures.
- Every superseded claim is corrected beside itself rather than deleted.

## Nothing already true is broken

- `tools/check.sh` exits 0 and reports every check passing.
- Closure is 100 percent at levels one and two, nothing on the frontier,
  nothing blocked, no cycles.
- Every sense admitted at a level has a thesaurus entry, and every word
  admitted and not in the seed has a definition record.
- `ostensive` in `curriculum/vocabulary.json` holds at most 60 words.
- Every dictionary book is in alphabetical order.
- No file under `secret/` is tracked, and the disclosure scan reports that
  it covered tracked and untracked files, line by line and with whitespace
  collapsed.

## Honesty conditions

- No document claims a curriculum or ordering benefit as established.
- Every figure quoted was measured on the tree, or the same sentence says
  it was not.

## What would need authorising before a further condition applies

Level two is a scheduling problem, not a writing one. **A condition for it
cannot be written until the lexicon allocation from 879 words toward ten
thousand exists**, because a corpus written before that allocation would be
invalidated by it.
