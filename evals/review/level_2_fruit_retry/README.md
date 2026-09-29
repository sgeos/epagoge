# Fruit review with selected defining words

Recorded 2026-09-28. This scope repaired a measured selection gap in the
candidate generator and reviewed six earlier fruit candidates. The starting
selection omitted all six headwords admitted by the previous foundational
increment. The new optional defining-word selection retains licensed words
inside the existing 700-word list. Mandatory vocabulary remains present, and
the teacher context remains 4096 tokens. Existing default selection is retained.

## Result

The teacher mechanically accepted cherry and deferred grape, lemon, peach,
pear and plum. Agent review admitted cherry, grape and pear after adapting
their definitions. Lemon, peach and plum remain deferred with explicit
reasons. The actual admitted plurals are cherries, grapes and pears.

Level two increased from 961 to 964 words, leaving 9,036 to the approximate
ten-thousand-word target. Level one remains at 849. Required definition
coverage is 812 of 812 at level one and 927 of 927 at level two. Both
dictionaries are fully grounded. The measurement verified hashes for all
523 level-one books and the reference checkpoint.

## Semantic findings

Fruit appeared in the actual teacher list. The replies nevertheless used
unavailable taste vocabulary and other words. The list selected bunch, but
bunches is not currently licensed. Selecting a headword does not create its
forms. That is a future inflection-review candidate, not permission to bypass
the current validator.

The dictionary currently defines stone as a rock and skin as a body covering.
Although mechanically licensed, those words do not establish the senses used
for fruit. None of the admitted definitions uses those unrecorded senses.
Cherry gained a description of its central hard part enclosing one seed.
Grape gained its climbing-plant habit and a thin outer cover without a colour
restriction. Pear uses a qualified common shape with the narrow end at the
top. These are introductory definitions, not exhaustive identification keys.

Lemon still needs an informative taste account. Peach and plum need more
suitable distinguishing vocabulary and explicit review of fruit-related
senses. The authoring agent performed the review. There is no independent
expert validation. These limitations are not discharged by closure checks.

## Evidence

candidates.json records manual proposals derived from earlier rejections.
generation.json records the requested defining words, actual 700-word list,
prompt, reply and every mechanical outcome. generated.json is the unchanged
mechanical proposal. review.json and admitted.json distinguish agent edits,
semantic decisions and final admissions. before.json and measurement.json
record the measured boundary. execution.json records host memory and bounded
single-request generation. baseline_audit.json records hashes of earlier
review artifacts, which remain unchanged. The previous brief and completion
condition are retained alongside this record.

Verify the final measurement against the authoring tree with

    .venv/bin/python tools/measure_lexicon_increment.py \
      evals/review/level_2_fruit_retry \
      --check evals/review/level_2_fruit_retry/measurement.json

Earlier exact-tree measurements are historical following these admissions.
This one batch does not isolate a causal effect of the selection change or
establish general throughput. No curriculum benefit is claimed. Level two
remains incomplete and confirmatory training remains blocked.

## Final verification

The full repository gate passed with 599 tests and no skips, zero type errors
or warnings, 96 percent core coverage and 92 percent reported training
coverage. The disclosure scan passed. final_audit.json records the measured
result, source hashes and gate-log hash. The final measurement matches the
current tree. No commit or publication was performed.
