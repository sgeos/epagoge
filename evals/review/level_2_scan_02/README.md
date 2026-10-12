# Reference-source scan, second batch

Recorded 2026-10-09. This continues the admission of the frequent group
from the scan of 2026-09-27. The first batch, 24 words, is in
`evals/review/level_2_one_source/`.

## What this batch did

At the start of the batch the one-source pool held 1,276 words. This batch
admits 432 of them and excludes 7. The exclusions are words whose concept
is already used by the same headword at a higher level, or verbs whose past
form is already a headword at a higher level, so the level-two form cannot
be carried. No word is deferred. No teacher ran. The definitions were
written by the agent.

The source string on each admission names the 2026-09-27 reference-source
scan. Dale-Chall and the New General Service List were not inputs.

## Measured outcome

Level two rose from 1,256 to 1,688 distinct headwords through level two,
leaving 8,312 to the approximate target. Level one remains at 849. Required
definition coverage is 849 of 849 at level one and 1,688 of 1,688 at level
two, with complete closure at both. After the batch a fresh selection left
761 words in the pool.

Adjectives of more than one syllable compare with more and most, except
where a suffixed comparison is the ordinary form. Mass nouns take no plural.

## Evidence and verification

    .venv/bin/python tools/measure_lexicon_increment.py \
      evals/review/level_2_scan_02 \
      --check evals/review/level_2_scan_02/measurement.json
