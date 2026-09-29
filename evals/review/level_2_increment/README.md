# Level-two lexicon increment

Recorded 2026-09-28. The retained generation and review artifacts describe a
bounded batch of manually proposed common food and plant nouns. No licensed
candidate list was used. The local teacher used the existing context limit
and at most two attempts for each group of twelve candidates.

## Measured result

The run offered 24 candidates. Mechanical validation accepted 1 and deferred
23. Semantic review admitted 1 after editing its definition and deferred 23.
These are different acceptance stages even though their counts agree here.

The admitted word is cabbage, assigned to the plant concept. Its original
proposal described a green plant with thick leaves. Review replaced that
broad description with food use and a qualified description of its usual
head shape. The regular plural cabbages was reviewed and admitted. The final
definition is a reviewed adaptation of teacher output, not an unchanged
teacher definition.

The level-two lexicon increased from 954 to 955 distinct admissible words.
The numerical gap to the approximate ten-thousand-word target is 9,045.
Level one remains at 849. Definition coverage is complete at both levels,
with 812 of 812 required words defined at level one and 918 of 918 at level
two. Both dictionaries are grounded without blocked definitions or cycles.
The preservation check covers 523 level-one books and the reference weights.

## Evidence and reproduction

`candidates.json` records the manual proposals and concept assignments.
`generation.json` retains the prompts, replies, validation outcomes and
mechanical counts. `generated.json` is the mechanically accepted proposal.
`review.json` accounts for every candidate, including semantic concerns and
deferrals. `admitted.json` is the reviewed admission input. `before.json`
records the measured baseline and preservation hashes. `measurement.json`
is the recomputed result.

Reproduce the measurement against the current authoring tree with

    .venv/bin/python tools/measure_lexicon_increment.py \
      evals/review/level_2_increment \
      --check evals/review/level_2_increment/measurement.json

The preservation check needs the local reference checkpoint. Its absence in
a clone is a verification limitation, not evidence that it was preserved.
The measurement deliberately fails when the tree no longer matches this
record. Later lexical growth requires its own record rather than rewriting
this one to appear current.

## Interpretation and remaining work

The low acceptance rate is a finding about this batch. It is not an estimate
of general pipeline throughput. Many definitions relied on unadmitted words
such as fruit, sweet, flour and bread. Several replies also contained semantic
errors or ambiguous senses. Vocabulary validity alone would not establish
correctness.

The next useful investigation is a reviewed set of foundational defining
words and their senses, followed by another measured batch. Do not simply
relax the vocabulary constraint or accept all words the teacher requests.
Semantic review here was performed by an agent and has not received an
independent expert audit. Concept assignment, archaism, sense selection and
inflection review remain judgement tasks. Level two remains incomplete.
