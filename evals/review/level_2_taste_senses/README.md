# Explicit taste-sense review

This review evaluates tongue, taste, sugar and sweet from the retained fruit
rejection evidence. The candidate generator now accepts an optional sense
specification file covering exactly its candidate set. Each entry has a
nonblank sense description of at most 240 characters and recognized parts of
speech. The specifications reach the prompt and the report. Their presence
does not license additional words or establish that a reply has the right
meaning. Existing invocations retain their default behavior.

The bounded run used one request with four candidates, a 700-word defining
list and the existing 4096-token context. The memory observation and request
limit are retained in execution.json. No concurrent training was performed.

## Measured outcome

The teacher mechanically accepted taste and rejected the other three replies
for unavailable vocabulary. The taste reply described any feeling in the
mouth during eating or drinking, which failed to separate taste from texture
and temperature. The tongue reply depended on the still unadmitted taste.

Agent review admitted tongue with a definition grounded in movement, eating
and speech, and taste with a definition that uses tongue while excluding
texture and temperature. The concepts remain body_part and physical_property.
Both are count nouns in the selected senses, with tongues and tastes as their
reviewed plurals. No language, preference or sampling-verb sense is admitted.
These are introductory descriptions without independent expert validation.

Sugar and sweet remain deferred. The replies define each through the other,
and describing sugar as white material is not sufficient to identify table
sugar. No white-material shortcut, general pleasantness substitution or seed
expansion was accepted to break that cycle. No forms for either were admitted.

Level two increased from 964 to 966 headwords, leaving 9,034 to the approximate
ten-thousand-word target. Level one remains at 849. Required definition
coverage is 812 of 812 at level one and 929 of 929 at level two. Both
dictionaries are completely grounded. The preservation check matched all
523 level-one books and the reference checkpoint. Earlier review artifacts
remain unchanged, as checked against preservation.json.

## Evidence and verification

candidates.json records manual proposals and proposed concepts. senses.json
records the explicit meanings and parts of speech. generation.json retains
the exact specifications and their file hash, actual defining vocabulary,
prompt, reply and every mechanical outcome. generated.json is the unchanged
mechanical proposal. review.json and admitted.json record semantic decisions,
agent adaptations and actual forms. before.json and measurement.json retain
the measured lexical change.

Verify the final measurement against the authoring tree with

    .venv/bin/python tools/measure_lexicon_increment.py \
      evals/review/level_2_taste_senses \
      --check evals/review/level_2_taste_senses/measurement.json

The specification tests cover malformed data, duplicate keys, mismatched
candidate sets, unknown fields, invalid qualifiers and oversized descriptions.
They also verify prompt delivery, report retention, per-word parts of speech
and the default path without a specification. The full gate remains required.

This result does not measure general throughput or the causal effect of sense
instructions. Semantic correctness remains a review obligation. Sugar and
sweet need independently grounded defining language. Confirmatory training
remains blocked and operator-reserved decisions remain unresolved.

## Final local verification

The full gate passed with 601 tests and no skips, zero type errors or warnings,
96 percent core coverage and 92 percent reported training coverage. The
disclosure scan passed. verification.json records the gate-log hash and the
verified artifact hashes. Remote workflow status is checked separately for
the published commit.
