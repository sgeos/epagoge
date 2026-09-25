# Completion condition

Judge against the repository tree. **Ordering is explicitly not a
completion criterion.** Any sequence of steps that leaves the tree in the
state below is complete. No branch, process or commit-shape requirement.

## Dictionary

- Every level-one word in `curriculum/vocabulary.json` that is not in the
  seed has a definition record under `curriculum/books/level_1/`. The seed
  is the core list, the exempt list, the ostensive list, and every surface
  form of an ostensive word.
- `tools/validate_closure.py` at level 1 reports closure 100 percent, with
  nothing on the frontier, nothing blocked and no cycles.

## The seed is bounded

- `ostensive` in `curriculum/vocabulary.json` holds **at most 45 words**.
  Closure reached by enlarging the seed does not count.

## Thesaurus

- Every sense admitted at level one has an entry.
- **At least 200 entries carry a synonym.**
- `tools/validate_thesaurus.py` at level 1 exits 0.

## Gate and repository

- `./tools/check.sh` exits 0.
- The working tree is clean and `main` matches `origin/main`.
- `git ls-files secret` reports 0.

## Records

- `CHANGELOG.md` and `docs/process/HANDOFF.md` state the final coverage
  and closure figures, and those figures match what the tools report.
