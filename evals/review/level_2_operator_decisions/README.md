# Operator decisions of 2026-10-07

Recorded 2026-10-07. The operator answered the six open items left by the
self-directed loop. This record holds the level-two batch those answers
unblocked. The level-one changes are described here and committed
separately, because they are not a lexical batch.

## The decisions and what was done

1. **All words should be shown and defined.** Ostensive words remain
   grounded by showing, so closure is unchanged, but the closure validator
   now counts them as needing a definition. Twenty level-one ostensive
   words had none and are now defined. Sweet and sour are admitted at level
   two as ostensive and defined. Function words such as the and of cannot be
   shown and name no concept, so they were read as outside this decision.
   That reading is the agent's, and it is reported to the operator.
2. **Use US English.** Colour, grey and towards became color, gray and
   toward across the lexicon, forty books, both dictionaries, the thesaurus
   and the sample corpus. The level-two duplicate color merged into the
   level-one entry. The substitution table now points the British forms at
   the US ones. Documentation prose was not converted.
3. **Reconcile the substitution contradictions.** The eight bans on beside,
   cause, causing, great, greater, length, single and unknown were removed,
   since every one is admitted and used in level-one books. A substitution
   key admissible at level one now fails the gate.
4. **Correct the missing parts of speech.** Eighty-three level-one and
   level-two nouns declared none, so forty plurals, skies and men among them,
   were not admissible. Each now declares noun or mass noun.
5. **Technical words probably belong at level two.** See below.
6. **Commit and push.**

## Measured outcome of the batch

The review covers 57 entries. Agent review admitted 48, deferred one and
excluded eight inflected forms. Level two rose from 1,184 to 1,232 distinct
headwords, leaving 8,768 to the approximate target. The baseline of 1,184
reflects the merge of the two color entries. Level one remains at 849.
Required definition coverage, now including ostensive words, is 849 of 849
at level one and 1,232 of 1,232 at level two, with complete closure at both.
All level-one books, the reference checkpoint and 96 earlier review
artifacts match the hashes recorded after the level-one changes.

Six admissions are the taste words. Sweet is defined through honey and
fruit, and sour through spoiled milk, so that sugar, lemon, cake and tart can
depend on them without a cycle. Forty-two admissions cover 43 of the 44
technical deferrals, eight of them through a base form. Electromagnetic is
deferred because an introductory definition needs electricity and magnet,
neither of which is admitted.

## Agent edits

Axis was added to the irregular plural table with axes, and monitor was
classified as not doubling. Two drafts were rewritten to stay inside the
level, debris without knocked and spectrum without split.

## Evidence and verification

`candidates.json`, `authoring.json`, `review.json`, `admitted.json`,
`before.json`, `measurement.json` and `preservation.json` follow the earlier
batches. Each admitted entry records whether the word is ostensive.

    .venv/bin/python tools/measure_lexicon_increment.py \
      evals/review/level_2_operator_decisions \
      --check evals/review/level_2_operator_decisions/measurement.json

## Limits

Agent review without independent expert validation. Several technical
definitions are deliberate simplifications, such as average without
division and atmosphere as the air around the earth. No level-two book uses
these words yet.
