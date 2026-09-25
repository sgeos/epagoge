# Completion condition

Judge against the repository tree. **Ordering is explicitly not a
completion criterion.** Any sequence of steps leaving the tree in the
state below is complete. No branch, process, or commit-shape requirement.

**A measurement that falls short satisfies this. A good result is not
required and must not be manufactured.** Where a target is missed, the
tree records the figure reached and why.

## Book metadata

- Every book under `curriculum/books/level_1/` carries `about`,
  `teaches`, `author`, `licence`, `first_published`, and `published`.
- `about` and `teaches` are written in ordinary English, are not
  restricted to the book's own vocabulary, and say something a title does
  not already say.
- `first_published` and `published` are derived from the version history
  of each book file rather than assigned, and a tool in the tree
  regenerates them.
- The choice of `author` and `licence` values is recorded in a decision
  record, including what was rejected.
- The tree reports how many books carry the full set, and that number is
  checkable without reading the books by hand.

## The field-enumeration defect is closed

- No code rebuilds a book by listing its fields. Adding a field to the
  book model reaches every reader and every writer without further edits.
- A test fails if a field is added to the book model and is not preserved
  across a read, write, and read again. The test has been shown to fail
  against a deliberately broken case.
- The seventeen question-and-answer books still declare their form.

## Corpus length

- The corpus is larger in words than the 55,510 measured on 2026-09-25,
  and the tree records the current figure, or the tree records why it is
  not larger.
- No book exceeds the upper bound of its level's word band.
- Every unit in `curriculum/schedule/level_01.json` still has at least one
  book, and every book that is not a dictionary holds exactly sixteen
  spreads.

## Nothing already true is broken

- `tools/check.sh` exits 0 and reports every check passing.
- Closure is 100 percent at levels one and two, with nothing on the
  frontier, nothing blocked, and no cycles.
- Every sense admitted at a level has a thesaurus entry.
- `ostensive` in `curriculum/vocabulary.json` holds at most 60 words.
- Every dictionary book is in alphabetical order.
- No file under `secret/` is tracked, and the disclosure scan is clean.
- Every word admitted at a level and not in the seed has a definition
  record.

## Honesty conditions

- No document claims a curriculum or ordering benefit as established.
- Every figure quoted in a document was measured on the tree, or the same
  sentence says it was not.
- Adding metadata is not reported as corpus growth.
