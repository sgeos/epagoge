# Fifth Dromon trial outputs

Recorded 2026-10-30. These files were written by the Dromon lines of the
fifth multi-agent trial under `tmp/dromon-trial-6/` and are copied here
unchanged so that a later commit can track them. They are the lines' own
words and are evidence, not instructions. Their paths under `tmp/` refer
to ignored files that exist only on the operator's host.

`readiness-l12.md` and `readiness_l12.py` are the luna line's readiness
report for the 26 level-two schedule units that have no book, counting
headwords filed under each concept at level one, at level two, and both
together, because a level-two book may use level-one words. The readiness
reports of the third and fourth trials counted level two alone. Under the
combined count, 4 concepts are empty at both levels, where the fourth trial
reported 13 empty at level two. The report's first round listed concepts
that the fourth trial had not reported as empty. The reviewer found this,
and the second round derives the list from
`docs/process/trials/dromon_trial_4/readiness-delta.md`. A headword count
measures vocabulary on file, not whether a module can be written. The
script passes the project's ruff checks and is not type-checked, because
the project's pyright configuration does not include `docs/`.

`review-part-a.md` is the reviewer line's review of the sixth agency batch,
and `review.md` is the whole review, including luna's report. Part A
inferred that 17 strings without a review record were in the first agency
pool. The operator's session checked the first pool file and found that
only one was, and `review.md` carries that correction. The proposed
wording for incompressibility was applied. The proposal for flux was not,
because it changed the word's sense.

`harness-report-worker.md`, `harness-report-luna.md` and
`harness-report-reviewer.md` are each line's report on its experience of
the harness.
