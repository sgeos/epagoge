# Level-two multi-source batch

Recorded 2026-10-07. The pool was selected by `tools/candidate_pool.py` from
the frequent group of the 2026-09-27 scan, and its output with every removal
is retained in `pool.json`. The rules remove, in order, words matching the
private disclosure pattern, words already admissible at level two, words with
a decision in an earlier review, words frequent in fewer than two sources,
words shorter than three letters, and words capitalised in at least half of
their occurrences across the source texts. Words removed by the first rule
are counted and never named.

The tool kept 174 words. Nine bases of inflected pool words were added as
candidates, so the review covers 183 entries.

## Measured outcome

Agent review admitted 100 words, deferred 68 and excluded 15. Level two rose
from 1,085 to 1,185 distinct headwords, leaving 8,815 to the approximate
target. Level one remains at 849. Required definition coverage is 812 of 812
at level one and 1,148 of 1,148 at level two, and both dictionaries are
completely grounded. All level-one books, the reference checkpoint and 85
earlier review artifacts match their recorded hashes.

The deferrals are 44 technical words from the modern sources, nine archaic
or dated words, three words used chiefly in a religious sense, nine words
whose senses differ between sources or occur mainly in fixed phrases, and
three single cases. Kitty duplicates cat and kitten, men waits on a finding
about man, and produce is admitted at level five. The exclusions are
fourteen inflected forms of admitted bases and the fragment dee.

The technical deferrals are agent judgement, not a rule. Some, such as
temperature, forecast and climate, were admitted because an early reader
meets them in ordinary speech about weather.

## Defects found and fixed in this batch

**The disclosure scan missed plurals.** It anchored each withheld term at
both ends of a word, so a plural of a withheld term passed. The first pool
output carried one such plural and the widened scan caught it. The scan and
the pool tool now accept an optional plural suffix.

**The disclosure scan reported clean over no files.** Inside a sandbox its
temporary file could not be created, every later step read an empty path,
and it printed clean with a blank file count. It now fails when the file
list cannot be created or is empty.

**The scan's second pass was case-sensitive.** The pass that finds a phrase
broken across lines ignored phrases in another case. It is now
case-insensitive like the first pass.

Each was shown failing on a probe before it was trusted. Probes with a
capitalised plural and an uppercase phrase broken across lines both failed
the widened scan, and the sandboxed run now exits with a failure.

**The closure check caught a cycle in the drafts.** Egg was first defined
through lay and lay through egg. The admission tool refused all one hundred
words and rolled the lexicon back. Egg was rewritten without lay.

**Four verbs needed the irregular table.** The rule gave layed, rided,
sended and occured. Lay, ride, send and occur are now listed.

## Findings outside the batch

Man declares no part of speech at level one, so men is not admissible. This
is the same finding as sky and skies, recorded for the operator.

## Evidence and verification

`pool.json` is the tool output. `candidates.json`, `authoring.json`,
`review.json`, `admitted.json`, `before.json`, `measurement.json` and
`preservation.json` follow the earlier batches.

    .venv/bin/python tools/measure_lexicon_increment.py \
      evals/review/level_2_multi_source \
      --check evals/review/level_2_multi_source/measurement.json

## Limits

Agent review without independent expert validation. The capitalisation rule
is a proxy and the review was responsible for names. No level-two book uses
these words yet. No throughput claim follows from one batch.
