# Agency scan, level two

Recorded 2026-10-10. 151 headwords from a public-domain scan of NASA
children's earth pages, a thin StarChild level 1 sample, and USGS Water
Science School pages were admitted. No teacher ran. Strings in that pool
that were not admitted were left without a review decision.

Level two rose from 2,159 to 2,310 distinct headwords, measured. Coverage
is 2,310 of 2,310 and closure is complete at levels one and two.

    .venv/bin/python tools/measure_lexicon_increment.py \
      evals/review/level_2_agency \
      --check evals/review/level_2_agency/measurement.json
