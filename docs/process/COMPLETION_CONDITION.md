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
- `about` and `teaches` are ordinary English, not restricted to the book's
  own vocabulary, and say something a title does not.
- The two dates are derived from each file's version history by a tool in
  the tree, not assigned.
- A decision record gives the `author` and `licence` values and what was
  rejected.
- A check reports how many books carry the full set.

## The field-enumeration defect is closed

- No code rebuilds a book by listing its fields. Adding a field to the
  book model reaches every reader and every writer without further edits.
- A test fails if a field is added to the book model and is not preserved
  across a read, write, and read again. The test has been shown to fail
  against a deliberately broken case.
- The seventeen question-and-answer books still declare their form.

## The capacity question is settled either way

- The tree records a model-size sweep at level one that includes widths
  below 128, run on one frozen corpus, with training loss, held-out loss
  and the gap for every point.
- Its report names the corpus size it ran against and does not compare
  its figures to a sweep on a different corpus.
- It says which conclusion the evidence supports: that a smaller model
  generalises better on the same tokens, or that it does not and the
  recorded corpus limit survives. **A negative result satisfies this.**
- Any surviving claim that corpus rather than training is the limit is
  either supported by that sweep or marked as not separated from model
  size.
- The earlier diagnosis file is still present and still names the corpus
  it describes.

## Corpus length

- The corpus is larger in words than the 55,510 measured on 2026-09-25,
  and the tree records the current figure, or the tree records why it is
  not larger.
- Fewer than 203 of the 244 sixteen-spread content books sit below the
  level-one word band, or the tree records why not.
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
