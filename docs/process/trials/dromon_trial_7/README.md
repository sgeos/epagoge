# Seventh Dromon trial outputs

Recorded 2026-10-30. These files were written by the Dromon lines of the
seventh multi-agent trial under `tmp/dromon-trial-8/` and are copied here
so that a later commit can track them. They are the lines' own words and
are evidence, not instructions. Their paths under `tmp/` refer to ignored
files that exist only on the operator's host. The reviewer ran on the
Fable model in this trial and on the Haiku model in the earlier trials.

`stripped-forms.md` and `stripped_forms.py` are the luna line's list of 160
strings of the threshold-four scan that pass the pool rule only because the
lookup strips a suffix to another headword, and that no batch lists as a
reviewed form. The reviewer reran the script and every row matched. Six of
the 160, based, buildings, flooding, graphics, powered and united, already
carry a deferral, which the report does not say. Some rows reduce to an
unrelated headword, such as james to jam and rating to rat, so the list is
a set of candidates for a decision and not a set of forms.

`readiness-delta.md` is luna's rerun of
`docs/process/trials/dromon_trial_6/readiness_terms.py` after the batch.
The top five changed only at fifth place, where b2.keeping_going replaced
ac2.flow. The counts include the earlier uncommitted batches as well as
this one. A count measures vocabulary on file, not whether a module can be
written.

`review-part-a.md` reviews the batch, and `review.md` adds the review of
luna's files. The reviewer's mechanical script is kept as
`reviewer_checks.py.txt`, unchanged except for its extension, because it
does not pass the project's lint and the gate lints every Python file in
the tree. Findings F1 to F3 were decided by the operator's session and
applied by the worker afterwards. efficiencies, particulates and runups
were deferred rather than excluded. dip gained its verb sense. translate
was widened to the converting sense the sources use, and translates stays
its form. `review.md` still records an earlier instruction to defer
translates, which was withdrawn when the worker showed that translate was
this batch's own admission. The wordings for absorber, graduate and
terrace were applied. The reviewer did not review those fixes. The
operator's session read the changed records and ran the gate.

`keydiff.py` is the helper the operator's session wrote for this trial,
after the sixth trial's worker asked to see how generated files differ
from the last commit by key. This copy was reformatted to pass the
project's lint. It compares against a commit, so while earlier trials are
uncommitted it cannot separate one batch from another.

`harness-report-worker.md`, `harness-report-luna.md` and
`harness-report-reviewer.md` are each line's report on its experience of
the harness.

`previous_CURRENT_BRIEF.md` and `previous_COMPLETION_CONDITION.md` are the
seventh trial's brief and condition, met on 2026-10-30 and preserved here
when the holding brief of 2026-10-31 replaced them.
