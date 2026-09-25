# Completion condition

Judge against the repository tree. **Ordering is explicitly not a
completion criterion.** Any sequence of steps leaving the tree in the
state below is complete. No branch, process or commit-shape requirement.

**A null or negative measurement satisfies this. A positive result is not
required and must not be manufactured.**

## Level-one corpus

- Every unit in `curriculum/schedule/level_01.json` has at least one book
  in `curriculum/books/level_1/`.
- Every book in that directory holds exactly sixteen spreads.
- `tools/validate_books.py` exits 0 with the spread standard enforced.

## Reference material stays sound, levels one and two

- Every word admitted at that level and not in the seed has a definition
  record under `curriculum/books/level_<n>/`.
- `tools/validate_closure.py` reports closure 100 percent at both levels,
  with nothing on the frontier, nothing blocked and no cycles.
- Every sense admitted at that level has a thesaurus entry, and
  `tools/validate_thesaurus.py` exits 0 at both levels.
- `ostensive` in `curriculum/vocabulary.json` holds at most 60 words.
  Closure bought by enlarging the seed does not count.

## Variance is measured on the level-one corpus

The pilot already ran on a synthetic stream. This asks for the same
measurement on real text.

- A paired multi-seed run over the level-one corpus is recorded in the
  tree, with its seeds, the corpus size in tokens and its per-seed losses.
- The record reports the unpaired spread, the paired spread and their
  correlation, and states how each compares with the synthetic-stream
  figures of 0.0750, 0.0233 and 0.9539.
- `evals/PRE_REGISTRATION.md` reflects what this settles, and any item it
  does not settle still names the dependency that would.

## A trained model exists

- A training run over the level-one corpus has completed, and the tree
  records the corpus size, the configuration and the final loss.
- The record states plainly whether the corpus was large enough for the
  result to mean anything.

## Gate and repository

- `./tools/check.sh` exits 0.
- The working tree is clean and `main` matches `origin/main`.
- Continuous integration is green on the head commit.
- `git ls-files secret` reports 0.

## Records

- `docs/process/HANDOFF.md` states the coverage, closure, corpus,
  training and variance figures, and those match what the tools report.
- Any goal left undone is named, with what blocks it.

## Out of scope

The level-two ablation, schedules for levels three and above, and a
concept-complexity target per level are **not** required. The ablation
depends on a minimum detectable effect justified from the literature and
on an endpoint decision, neither of which is settled.
