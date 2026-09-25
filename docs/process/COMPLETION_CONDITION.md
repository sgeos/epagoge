# Completion condition

Judge against the repository tree. **Ordering is explicitly not a
completion criterion.** Any sequence of steps leaving the tree in the
state below is complete. No branch, process or commit-shape requirement.

**A measurement that falls short satisfies this. A good result is not
required and must not be manufactured.**

## A model can be interacted with

- A tool in the tree loads trained weights and answers a prompt, and
  refuses rather than inventing weights when none exist.
- Its output for at least one prompt is recorded in the tree.
- The record states the held-out loss or perplexity of the model that
  produced it, so the reader can tell how much to trust what they see.

## The corpus is growing and sound

- Every unit in `curriculum/schedule/level_01.json` has at least one book
  in `curriculum/books/level_1/`, and every book there holds exactly
  sixteen spreads.
- The corpus is **larger in tokens than the 45,547 measured on
  2026-09-25**, and the tree records the current figure.
- `tools/validate_books.py` exits 0 with the spread standard enforced.

## Reference material stays sound, levels one and two

- Every word admitted at that level and not in the seed has a definition
  record under `curriculum/books/level_<n>/`.
- `tools/validate_closure.py` reports closure 100 percent at both levels,
  with nothing on the frontier, nothing blocked and no cycles.
- Every sense admitted at that level has a thesaurus entry, and
  `tools/validate_thesaurus.py` exits 0 at both levels.
- `ostensive` in `curriculum/vocabulary.json` holds at most 60 words.

## The limit on model quality is named with evidence

- The tree records a measurement separating undertrained from
  out-of-corpus, reporting training and held-out loss for more than one
  configuration.
- The tree records what corpus size would be needed for a better model,
  with the measurements it was derived from and the reasons it may be
  wrong.

## Gate and repository

- `./tools/check.sh` exits 0.
- The working tree is clean and `main` matches `origin/main`.
- Continuous integration is green on the head commit.
- `git ls-files secret` reports 0, and no model weights are tracked.

## Records

- `docs/process/HANDOFF.md` states the current corpus, closure and model
  figures, and those match what the tools report.
- Any goal left undone is named, with what blocks it.

## Out of scope

The level-two ablation, schedules for levels three and above, and a
concept-complexity target per level are **not** required. Reaching a
corpus of 10^6 tokens is **not** required, because at the observed rate
it is many times longer than a session.
