# Completion condition

Judge against the repository tree. **Ordering is explicitly not a
completion criterion.** Any sequence of steps leaving the tree in the
state below is complete. No branch, process or commit-shape requirement.

A run that completes and reports honestly satisfies this. **A positive
result is not required and must not be manufactured.**

## Reference material, levels one and two

- Every word at that level which is not in the seed has a definition
  record under `curriculum/books/level_<n>/`. The seed is the core,
  exempt and ostensive lists plus every surface form of an ostensive word.
- `tools/validate_closure.py` at that level reports closure 100 percent,
  with nothing on the frontier, nothing blocked and no cycles.
- Every sense admitted at that level has a thesaurus entry, and entries
  carry both synonyms and antonyms.
- `tools/validate_thesaurus.py` exits 0 at that level.

## The seed is bounded

- `ostensive` in `curriculum/vocabulary.json` holds **at most 60 words**
  across all levels. Closure bought by enlarging the seed does not count.

## Level-one corpus

- **Every unit in `curriculum/schedule/level_01.json` has at least one
  book** in `curriculum/books/level_1/` teaching a concept that unit
  names.
- **Every book holds exactly sixteen spreads**, which is the thirty-two
  page trade standard, and the gate enforces that rather than reporting it.
- `tools/validate_books.py` exits 0.
- `tools/build_corpus.py` produces a stream under both orderings.

## A trained model exists

- A training run over the level-one corpus has completed, and its result
  is recorded in the tree with the corpus size, the configuration and the
  final loss.
- The record states plainly whether the corpus was large enough for the
  result to mean anything.

## Ablation

- `evals/PRE_REGISTRATION.md` has no item left marked pending or
  incomplete.
- An ablation run over level one and level two is recorded, including a
  null arm, with per-seed numbers and the pre-registered effect threshold.
- **The record states the outcome even when it is null**, and says whether
  the arms were distinguishable at the corpus size actually used.

## Gate and repository

- `./tools/check.sh` exits 0.
- The working tree is clean and `main` matches `origin/main`.
- `git ls-files secret` reports 0.

## Records

- `CHANGELOG.md` and `docs/process/HANDOFF.md` state the final coverage,
  closure, corpus, training and ablation figures, and those match what the
  tools report.
