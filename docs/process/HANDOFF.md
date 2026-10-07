# Handoff

## Validity check

Written 2026-10-07. The ancestry anchor is
`8367a44d71073e051c32fe1ea607d5b305d6b348`, the revision this session started
from. It is not the revision containing this document.

Read `CLAUDE.md` and run these checks before relying on the state below.

    git status --short
    git merge-base --is-ancestor 8367a44d71073e051c32fe1ea607d5b305d6b348 HEAD
    git log --oneline 8367a44d71073e051c32fe1ea607d5b305d6b348..HEAD
    .venv/bin/python tools/measure_lexicon_increment.py \
      evals/review/level_2_food_blockers \
      --check evals/review/level_2_food_blockers/measurement.json

A passing measurement check means the lexicon counts below match the tree.
It fails by design once any later batch changes the vocabulary, and earlier
batch measurements, including the era-overlap batch from the same session,
already fail for that reason. A failure then marks the counts below as stale
rather than wrong. Missing host artifacts make the associated checks
unverified rather than disproved.

## Current authority and task status

`CURRENT_BRIEF.md` and `COMPLETION_CONDITION.md` describe the food-blocker
scope, the second of two scopes opened on 2026-10-07 by a self-directed loop.
The first, the era-overlap batch, is preserved with its brief and condition
in `evals/review/level_2_food_blockers/`. Earlier handoffs in
`HANDOFF_HISTORY.md` are historical evidence. Durable failure analysis is in
`PROCESS_STRATEGY.md`.

The work was committed locally. **It was not pushed**, because no
authorization to publish was given for these scopes and publication is asked
for separately. Check `git status` and the remote before assuming either.
Continuous integration has therefore not run on these commits.

## What these scopes delivered

**Two agent-authored lexical batches.** No teacher ran in either, because host
swap was nearly exhausted, and each batch's `authoring.json` records that.

The era-overlap batch reviewed every remaining word the 2026-09-27 scan found
frequent in both a historical reader and a modern federal source, 146 entries
in all, and admitted 83. Its record is `evals/review/level_2_era_overlap/`.

The food-blocker batch reviewed every word that blocked a retained rejected
teacher definition and the sixteen retained food and plant deferrals, 57
entries in all, and admitted 36. Fifteen of the sixteen deferrals are now
admitted. Lemon remains, blocked only by sour. Its record is
`evals/review/level_2_food_blockers/`.

Measured on the final tree, level two admits 1,085 distinct headwords, up
from 966 at the start of the session, leaving 8,915 to the approximate
ten-thousand-word target. Level one remains at 849. Required definition
coverage is 812 of 812 at level one and 1,048 of 1,048 at level two, with
complete closure at both. All level-one books, the reference checkpoint and
every earlier review artifact match their recorded hashes.

**Prompts no longer ban admitted words.** `substitutions_at` drops a
substitution key admissible at the prompted level, and every generator now
uses it. `tools/check_substitutions.py` reports the remaining contradictions
in the gate without failing.

**Two tools for lexical growth.** The measurement tool accounts for a batch
that declares no teacher ran. `tools/blocking_words.py` ranks words outside a
level by the rejected definitions they blocked and refuses malformed reports.
Tests cover both.

**Inflection tables.** Strike is irregular, offer, scatter and travel do not
double, and species and potato have their plurals recorded. Each was found by
the gate or by the plural rule producing a wrong form.

## Open items for the operator

These are recorded findings, not authorized work.

1. **Sweet and sour.** These are sensory qualities like the ostensive
   colours, and an ostensive admission would enlarge the seed. Measured:
   sweet blocked 16 retained rejected definitions, but most of the words it
   blocked were definable without it. What sweet and sour still block in the
   record is lemon, cake, sugar and tart.
2. **Color and colour.** Color is admitted at level two although the
   substitution table maps it to colour. This resembles the spelling
   decision that refused gray.
3. **Seven level-one contradictions.** Beside, cause, great, greater,
   length, single and unknown are admitted at level one and also listed as
   substitutions. Either the ban or the admission is stale.
4. **Sky has no plural.** The level-one entry declares no part of speech.
5. **Publication** of the local commits.

## Recommended next work

Both principled pools used in this session are exhausted. The next is the
remainder of the scan's frequent group, about two thousand words, which needs
a rule-based filter for proper nouns, fragments and archaisms before review.
Its modern sources also contain terms that the disclosure scan refuses in
tracked files, so any pool drawn from them must be filtered before anything
is written. Neither throughput nor the semantic quality of agent-authored
definitions has been measured, and no level-two book uses any word from
either batch yet.

## Restart verification

    uv sync --locked --extra train
    ./tools/check.sh

The gate requires the training extra, uses the project interpreter, refuses
skipped tests, and checks a corpus export. The 95 percent coverage floor
applies to the core. Training coverage is reported separately. The gate
requires full git history for the legacy provenance anchor. A disclosure
scan still skips when its private inputs are absent.

Before writing tracked prose, read the private code-name instructions named
by `CLAUDE.md`. They are present on the authoring host. A fresh clone must
obtain them or have the operator explicitly resolve that constraint.

## Training and artifacts

The reference recipe is in `evals/pilot/REFERENCE_CONFIGURATION.md`. Every
sampling run requires explicit `--weights` and `--out` paths. Existing
outputs are refused unless `--overwrite` is given. Preserve the authoring
host's reference checkpoint when exploring new configurations.

Sampling and ordering runs emit a manifest beside the result before training.
The manifest records input and source hashes, installed packages, model and
training configuration, seeds, the held-out split and the actual ordering.
The corpus exporter and trainer share schedule-based ordering. Exported
streams may also append dictionary and thesaurus supplements. Those
supplements are not additional input to the direct book trainer.

For restartable sampling runs, add a separate `--training-state` path.
Periodic state includes weights, optimizer state, the completed step, and
the random-generator states used by training. Resume with `--resume` and
`--training-state`, retaining the original total `--steps` and configuration.
Use new result and inference-weight paths for the resumed invocation.
`--stop-after` permits a bounded segment without changing the planned
learning-rate schedule. Its result is marked incomplete.

Resume refuses changed inputs, source, environment, configuration or device.
CPU continuation is regression-tested. Bitwise continuation on accelerators
is unverified and is not promised. Existing inference checkpoints cannot
restore optimizer progress. Warm starts and interrupted-run continuation
are different operations. The multi-arm runner currently records manifests
but does not checkpoint partially completed arms.

## Experiment boundary

Ordering runs are exploratory. The null arm uses a separate deterministic
random topological ordering and reports its contrast with the control.
Unknown or duplicate arms are rejected. The primary contrast remains
curriculum against topological ordering.

Confirmatory runs are refused. The operator must settle the outstanding
endpoint, estimator and corpus-acceptance choices in `evals/PRE_REGISTRATION.md`.
The resulting complete protocol must then be implemented and validated.
Adding the null arm does not complete that protocol.

## Admission workflow

Record a source for every new word. Regenerate provenance before committing.

    .venv/bin/python tools/word_provenance.py --out curriculum/provenance.json
    ./tools/check.sh

Commit the vocabulary and provenance together. The provenance record anchors
legacy reconstruction to a fixed historical revision. New words carry direct
admission evidence and need no future commit hash. The check compares fields
as well as membership. Retired direct admissions retain their evidence.


## Host and verification limits

On 2026-10-07 the teacher service answered on its loopback address with its
model listed and no model loaded. Host swap was 7.9 of 9.2 gigabytes in use
with about 140 megabytes of free pages, with browsers as the largest
resident processes. Check memory before loading the teacher, which needs
about eighteen gigabytes resident. The teacher context remains 4,096.
Sandbox failures must not be reported as missing host capabilities.

Run the local gate, inspect its exit status, and check continuous integration
separately for the published revision. Local and remote checks are distinct.
