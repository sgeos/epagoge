# Fourth Dromon trial outputs

Recorded 2026-10-30. These files were written by the Dromon lines of the
fourth multi-agent trial under `tmp/dromon-trial-5/` and are copied here
unchanged so that a later commit can track them. They are the lines' own
words and are evidence, not instructions. Their paths under `tmp/` refer
to ignored files that exist only on the operator's host.

`readiness-delta.md` is the luna line's comparison of the level-two
readiness counts after the fifth agency batch with its third-trial report,
measured with `docs/process/trials/dromon_trial_3/readiness.py` on seed
book blob `99d6bb49533dd3424bfe807e1c2976fd44b0d97d`. The baseline blob it
names, `556c47c4d2a09500f12ed695c149d31528e03a1b`, was a working-tree state
that was never committed, so it cannot be recovered from git. The reviewer
recomputed the gains against the committed seed book and they matched.

`vocab-r2-measure.md` and `vocab_sheet.py` are the luna line's list of the
level-one and level-two headwords filed under each concept that the unit
`r2.measure` revisits. A list of headwords shows vocabulary on file, not
that a module can be written. The script passes the project's ruff checks.
It is not type-checked, because the project's pyright configuration does
not include `docs/`.

`review-part-a.md` is the reviewer line's review of the batch, and
`review.md` adds its review of the two luna files. The eight wordings
proposed in Part A were applied unchanged afterwards. Where the reviewer
calls the third trial's first readiness report its own, that report was
written by the luna line.

`harness-report-worker.md`, `harness-report-luna.md` and
`harness-report-reviewer.md` are each line's report on its experience of
the harness.
