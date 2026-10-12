# Reference-source scan, fifth batch

Recorded 2026-10-09. Twenty headwords from the frequent group of the
2026-09-27 scan were admitted, and ten candidates were excluded. The
exclusions are fragments that are not English headwords, or inflected forms
whose singular or base is not in the frequent pool. No teacher ran.

Behold takes the past beheld. Consider does not double its final consonant.
Cast keeps the same form in the past.

Level two rose from 1,826 to 1,846 distinct headwords, measured. Coverage
is 1,846 of 1,846 and closure is complete at levels one and two. A fresh
selection then left 550 words in the pool.

    .venv/bin/python tools/measure_lexicon_increment.py \
      evals/review/level_2_scan_05 \
      --check evals/review/level_2_scan_05/measurement.json
