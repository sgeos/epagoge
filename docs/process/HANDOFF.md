# Handoff

## Validity check and continuity stamp

Stamped 2026-10-07 at 17:09 Coordinated Universal Time. The verified base is
`336545b5e6cb0327d73614cde23bb5e6c608e6b0`, the multi-source commit.
This is an ancestry anchor, not the revision containing this document. A later documentation commit does not invalidate
it merely by changing the current revision.

At the stamp the full local gate passed on the base with 625 tests and no
skips, zero type errors or warnings, 96 percent core coverage, 92 percent
reported training coverage and a clean disclosure scan. The base is not
pushed, so no continuous integration result exists for it.

Read `CLAUDE.md` and run these checks before relying on the state below.

    git status --short
    git merge-base --is-ancestor 336545b5e6cb0327d73614cde23bb5e6c608e6b0 HEAD
    git log --oneline 336545b5e6cb0327d73614cde23bb5e6c608e6b0..HEAD
    .venv/bin/python tools/measure_lexicon_increment.py \
      evals/review/level_2_multi_source \
      --check evals/review/level_2_multi_source/measurement.json

A passing measurement check means the lexicon counts below match the tree.
It fails by design once any later batch changes the vocabulary, and the
measurements of every earlier batch, including the two earlier batches of
this session, already fail for that reason. A failure then marks the counts
below as stale rather than wrong. Missing host artifacts make the associated
checks unverified rather than disproved.

## Current authority and task status

A self-directed loop ran three scopes on 2026-10-07 and was **cancelled by
the operator** during the third. The third scope was finished before
stopping. No loop, wakeup or background job remains. **No further scope is
open.** `CURRENT_BRIEF.md` and `COMPLETION_CONDITION.md` describe the third
scope and are evidence of delivered work, not instructions to repeat it. The
first two briefs and conditions are preserved as `previous_*.md` in
`evals/review/level_2_food_blockers/` and
`evals/review/level_2_multi_source/`. Earlier handoffs in
`HANDOFF_HISTORY.md` are historical evidence. Durable failure analysis is in
`PROCESS_STRATEGY.md`.

The work was committed locally. **It was not pushed**, because no
authorization to publish was given for these scopes and publication is asked
for separately. Check `git status` and the remote before assuming either.
Continuous integration has therefore not run on these commits.

## What these scopes delivered

**Three agent-authored lexical batches.** No teacher ran in any of them,
because host swap was nearly exhausted when the session began, and each
batch's `authoring.json` records that.

| Batch | Pool | Entries | Admitted | Deferred | Excluded |
| --- | --- | --- | --- | --- | --- |
| `level_2_era_overlap` | Scan words frequent in both eras | 146 | 83 | 20 | 43 |
| `level_2_food_blockers` | Blockers of retained rejections | 57 | 36 | 13 | 8 |
| `level_2_multi_source` | Scan words frequent in two sources | 183 | 100 | 68 | 15 |

Measured on the final tree, level two admits 1,185 distinct headwords, up
from 966 at the start of the session, leaving 8,815 to the approximate
ten-thousand-word target. Level one remains at 849. Required definition
coverage is 812 of 812 at level one and 1,148 of 1,148 at level two, with
complete closure at both. All level-one books, the reference checkpoint and
every earlier review artifact match their recorded hashes.

**Tools for lexical growth.** The measurement tool accounts for a batch that
declares no teacher ran. `tools/blocking_words.py` ranks words outside a
level by the retained rejected definitions they blocked.
`tools/candidate_pool.py` selects a pool from a scan report by stated rules,
records every removal, and counts without naming words withheld by the
private disclosure pattern. Tests cover all three.

**Prompts no longer ban admitted words.** `substitutions_at` drops a
substitution key admissible at the prompted level, and every generator now
uses it. `tools/check_substitutions.py` reports the remaining contradictions
in the gate without failing.

**The disclosure scan had three holes, now closed.** It missed plurals of
withheld terms, its second pass was case-sensitive, and it printed clean over
no files when its temporary file could not be created. Each fix was shown
failing on a probe. `PROCESS_STRATEGY.md` records the lesson.

**Inflection tables.** Strike, lay, ride, send and occur are irregular. Offer,
scatter and travel do not double. Species and potato have their plurals
recorded. Each was found by the gate or by the rule producing a wrong form.

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
4. **Level-one entries without a part of speech.** Sky and man declare none,
   so skies and men are not admissible anywhere.
5. **Technical deferrals.** The multi-source batch deferred 44 technical
   words by agent judgement, pending a level-two schedule unit that needs
   them. Whether any belong at level two is a curriculum decision.
6. **Publication** of the local commits.

## Recommended next work

All three pools used in this session are exhausted. `tools/candidate_pool.py`
can produce the next one by relaxing the source rule to one source, which
leaves roughly 1,800 words that need much heavier archaism and technicality
judgement. A different, unmeasured route is to draft level-two books, since no
level-two book uses any word admitted in this session and the coverage rule
is therefore unmet at level two. Drafting needs the teacher, so check host
memory first. Neither throughput nor the semantic quality of agent-authored
definitions has been measured.

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
