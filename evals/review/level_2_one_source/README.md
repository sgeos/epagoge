# One-source frequent pool, first batch

Recorded 2026-10-09. The operator directed that remaining level-two
candidates be admitted, because the lexicon is far under its approximate
target of about ten thousand words. Capacity is not a reason to hold one
back. A definition that stays inside the level is still required.

## What this batch did

The pool was the frequent group of the 2026-09-27 scan at threshold five,
kept when a word is frequent in at least one source. At the start of the
batch that pool held 1,300 words after the mechanical filters. This batch
admits 24 of them, all frequent in one McGuffey reader. No word is deferred
or excluded here. The saved `pool.json` is the pool after the admission and
holds 1,276.

No teacher ran. About 175 megabytes of pages were free and swap held 10,956
of 12,288 megabytes, and the teacher needs about eighteen gigabytes
resident. The definitions were written by the agent.

## Measured outcome

Level two rose from 1,232 to 1,256 distinct headwords through level two,
leaving 8,744 to the approximate target. Level one remains at 849. Required
definition coverage is 849 of 849 at level one and 1,256 of 1,256 at level
two, with complete closure at both.

Curious is compared with more and most. Childhood, courage, darkness,
coffee and bark take no plural. Borrow does not double its final letter.

## Evidence and verification

`candidates.json`, `authoring.json`, `review.json`, `admitted.json`,
`before.json` and `measurement.json` follow the earlier agent-authored
batches. `pool.json` is the remainder.

    .venv/bin/python tools/measure_lexicon_increment.py \
      evals/review/level_2_one_source \
      --check evals/review/level_2_one_source/measurement.json

## Limits

One agent-authored batch. It does not finish the pool, and it does not
measure general throughput. Semantic review is agent review, not
independent expert validation. Several definitions state one elementary
sense and leave other senses unadmitted. Bark is the cover of a tree.
