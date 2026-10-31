Ordering is not a completion criterion.

Met on 2026-10-30 and measured on the working tree. This file is
historical evidence. Do not treat it as an open task.

`evals/review/level_2_long_tail/` holds a review record for each of the 607
strings in `tmp/dromon-trial-8/pool.txt`, drawn from the threshold-four
scan in `tmp/lexicon-sources/longtail/`, and records the 6 strings the
operator withdrew as a count only. Each string is admitted at level two or
three with one definition of a sense the sources use, recorded as a
reviewed form of a headword that carries its sense, or deferred or excluded
with a reason. Level-three admissions, if any, are recorded in
`evals/review/level_3_long_tail/`. Each batch's increment measurement
matches the tree. No word with a review decision from before this brief
changes its decision, and no existing record in `curriculum/provenance.json`
or `curriculum/vocabulary.json` changes except where a review record gives
the reason.

Required definition coverage is complete at levels one and two, and closure
is grounded at levels one to three. `tools/check.sh` exits 0 with no
skipped tests.

`tmp/dromon-trial-8/` holds a report listing the strings of the
threshold-four scan admissible only by suffix stripping and named in no
reviewed-forms list, a readiness comparison with the sixth trial's report,
a review of the batch and the reports, and one harness experience report
from each Dromon line that took part, or the operator is told which line
did not write one and why. Copies of the reports, any scripts, the review
and the harness reports are tracked in `docs/process/trials/dromon_trial_7/`.

No book under `curriculum/books/` changed except the dictionary seed books
at levels two and three. No file under `generators/` or
`src/epagoge/prompt.py` changed. No teacher was loaded and no text was
fetched. The work is in the working tree, and nothing of it is committed or
pushed unless the operator asked for that.

Ordering is not a completion criterion.
