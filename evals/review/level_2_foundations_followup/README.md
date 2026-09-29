# Bread and dough follow-up

Recorded 2026-09-28 after the four foundational admissions. The teacher
mechanically accepted neither proposal. Bread used unadmitted yeast and
required it as an ingredient. Dough used unadmitted bread, ingredients,
mixture and sticky. The retained generation.json contains both replies and
every mechanical outcome.

Agent review adapted both definitions. Bread no longer requires yeast and
uses baking as typical rather than universal. Dough describes a shapeable
uncooked flour-and-liquid material without depending on bread. Both use the
existing material concept and mass-noun senses, with no generated plurals.
These introductory definitions are not exhaustive food classifications.
Agent review is not an independent expert audit.

The admission tool accepted both revised definitions with grounded closure.
Level two increased from 959 to 961 words. Across both new batches it increased
from 955 to 961, leaving 9,039 to the approximate ten-thousand-word target.
Required definition coverage is 812 of 812 at level one and 924 of 924 at
level two. Both dictionaries are fully grounded. Preservation hashes match
523 level-one books and the local reference weights.

Reproduce the final batch measurement against this authoring tree with

    .venv/bin/python tools/measure_lexicon_increment.py \
      evals/review/level_2_foundations_followup \
      --check evals/review/level_2_foundations_followup/measurement.json

The foundational-stage measurement is a historical intermediate result.
Its after counts equal this batch's before counts. Each measurement retains
hashes of its candidates, generation, review and admissions. The original
increment artifacts remain unchanged, as checked against execution.json in
the foundational record. The final audit also checked all six admitted
entries against their definitions, source evidence, concepts and forms.

Generation used one sequential request and the existing 4096-token context.
Neither this two-word batch nor the combined six-word increment measures
general throughput or establishes an ordering benefit. The automatic
acceptance result does not demonstrate an improvement. Confirmatory training
remains blocked, and operator-reserved decisions remain unresolved.
