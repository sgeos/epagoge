# Completion condition

Judge against the repository tree. **Ordering is explicitly not a
completion criterion.** Any sequence of steps leaving the tree in the
state below is complete. No branch, process or commit-shape requirement.

**A measurement that falls short satisfies this. A good result is not
required and must not be manufactured.**

## Level one, the bootstrapping problem

- Every unit in `curriculum/schedule/level_01.json` has at least one book
  in `curriculum/books/level_1/`, and every book there holds exactly
  sixteen spreads.
- The corpus is **larger in words than the 37,207 measured on
  2026-09-25**, and the tree records the current figure.
- A tool loads trained weights and answers a prompt, refusing rather than
  inventing weights when none exist, and its output for at least one
  prompt is recorded with the loss of the model that produced it.

## Levels two to six, the scheduling problem

- The tree reports, by name and not as a percentage, every concept no
  schedule teaches and every concept taught once and never revisited.
- **The count of concepts taught once and never revisited is lower than
  the 68 measured on 2026-09-25**, or the tree records why it is not.
- Every level-two module names concepts it teaches or revisits, and no
  scheduled concept lacks a word at its level.

## Reference material stays sound

- Every word admitted at a level and not in the seed has a definition
  record under `curriculum/books/level_<n>/`.
- `tools/validate_closure.py` reports closure 100 percent at levels one
  and two, with nothing on the frontier, nothing blocked and no cycles.
- Every sense admitted at a level has a thesaurus entry, and
  `tools/validate_thesaurus.py` exits 0 at both levels.
- `ostensive` in `curriculum/vocabulary.json` holds at most 60 words.
- Every dictionary book is in alphabetical order.

## What a curator can see

- More books carry both `about` and `teaches` than the zero measured on
  2026-09-25, and `tools/validate_books.py --describe` reports how many
  still do not.
- A specification for drafting a book at each level exists in the tree.

## Gate and repository

- `./tools/check.sh` exits 0.
- The working tree is clean and `main` matches `origin/main`.
- Continuous integration is green on the head commit.
- `git ls-files secret` reports 0, and no model weights are tracked.

## Records

- `docs/process/HANDOFF.md` states the current corpus, closure, coverage
  and model figures, and those match what the tools report.
- Any goal left undone is named, with what blocks it.

## Out of scope

Schedules for levels three and above, anything under `sources/`, the
level-two lexicon reaching ten thousand words, and the level-two ablation
are **not** required. The first three are design the operator holds or
work longer than a session; the ablation additionally depends on an
endpoint nobody has fixed.
