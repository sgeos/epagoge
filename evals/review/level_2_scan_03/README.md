# Reference-source scan, third batch

Recorded 2026-10-09. This continues the admission of the frequent group
from the scan of 2026-09-27.

## What this batch did

At the start of the batch the one-source pool held 761 words. This batch
admits 71 of them and excludes 3 plurals whose singular is not in the
frequent pool. No word is deferred. No teacher ran. The definitions were
written by the agent.

The source string on each admission names the 2026-09-27 reference-source
scan. Dale-Chall and the New General Service List were not inputs.

Verbs whose past is not regular, including beat, broadcast, burst, seek,
shoot, split and swear, take the listed forms. Develop, harbor, quarrel
and visit do not double the final consonant. Aircraft, analysis and
gentleman take the listed plurals.

## Measured outcome

Level two rose from 1,688 to 1,759 distinct headwords through level two,
leaving 8,241 to the approximate target. Level one remains at 849. Required
definition coverage is 849 of 849 at level one and 1,759 of 1,759 at level
two, with complete closure at both. After the batch a fresh selection left
663 words in the pool.

## Evidence and verification

    .venv/bin/python tools/measure_lexicon_increment.py \
      evals/review/level_2_scan_03 \
      --check evals/review/level_2_scan_03/measurement.json
