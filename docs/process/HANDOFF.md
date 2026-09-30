# Handoff

## Validity check and continuity stamp

Stamped 2026-09-30 at 20:35 Coordinated Universal Time. The verified base is
`7011d61131dab25b84f0ae6b70cda0f41c66ea86`. This is an ancestry anchor,
not the revision containing this document. A later documentation commit
does not invalidate it merely by changing the current revision.

Read `CLAUDE.md` and run these checks before relying on the state below.

    git status --short
    git merge-base --is-ancestor 7011d61131dab25b84f0ae6b70cda0f41c66ea86 HEAD
    git diff --stat 7011d61131dab25b84f0ae6b70cda0f41c66ea86
    .venv/bin/python tools/measure_lexicon_increment.py \
      evals/review/level_2_taste_senses \
      --check evals/review/level_2_taste_senses/measurement.json

Ancestry success and matching content support the recorded lexical state.
Inspect later changes and local edits for changes to the task or its evidence.
If ancestry fails or measurements disagree, report the affected claims as
stale and reconcile them against the tree. Do not require equality with the
anchor. Missing host artifacts make the associated checks unverified rather
than disproved. Use the restart verification below for the full gate.

## Current authority and task status

Read this file with `CURRENT_BRIEF.md` and `COMPLETION_CONDITION.md`.
The brief and condition describe the completed taste-sense increment, not
an instruction to repeat it. Earlier handoffs in `HANDOFF_HISTORY.md` are
historical evidence. Their commands and status statements are not current
instructions. Durable failure analysis is in `PROCESS_STRATEGY.md`.

The latest requested scope is this handoff refresh for post-compaction and
new-session continuity. It adds no lexical or training task. A weekly usage
limit interrupted the refresh before edits. The operator upgraded the plan
and requested resumption. No generation or training job was started for this
refresh, and no background job needs resuming from this session.

After compaction, continue any unfinished explicit user task using the
transcript and the tree. For this refresh, inspect whether documentation
edits, verification or publication remain. The operator has authorized
committing and pushing all non-ignored work in this scope. Preserve ignored
host artifacts. Do not infer publication or cleanliness from this stamp.
Verify the working tree, remote revision and continuous integration result.
If the refresh is complete and no later task exists, report readiness for
the next task. Recommendations below do not initiate another lexical batch.

## Verified publication and evidence

The taste-sense increment was committed and published at the verified base.
Its [continuous integration run](https://github.com/sgeos/epagoge/actions/runs/36530723855)
completed successfully, rechecked on 2026-09-30. This result covers the base,
not future revisions. The last full local gate for that increment passed with
601 tests and no skips, zero type errors or warnings, 96 percent core
coverage and 92 percent reported training coverage. Its disclosure scan
passed. The increment measurement was rechecked against the authoring tree
on 2026-09-30 and matched, including the preservation hashes.

The full local gate also passed on the continuity refresh on 2026-09-30,
including the reference checks and the local disclosure scan. Test and
coverage counts were unchanged. Publication of the refresh must be checked
against its containing revision rather than the base run linked above.

Local and remote checks are separate evidence. Run the full local gate on
changes and inspect its exit status before committing. Check continuous
integration for the actual published revision, including a handoff-only
revision. Continuous integration cannot discharge the local disclosure scan.

## Completed work and next development target

The latest review is `evals/review/level_2_taste_senses/README.md`. The candidate
generator accepts optional explicit senses and parts of speech for exactly
the candidate set. Malformed specifications fail before teacher access.
Prompts and reports retain the specifications and their input hash.

The four-word batch mechanically accepted taste. Agent adaptations admitted
tongue and taste with reviewed noun plurals. Sugar and sweet remain deferred
because their replies define each through the other and the sugar reply lacks
independently distinguishing content. Explicit sense instructions do not
replace semantic review or dictionary-grounding checks.

Level two now admits 966 distinct headwords, leaving 9,034 to the approximate
ten-thousand-word target. Level one remains at 849. Required definition
coverage is 812 of 812 at level one and 929 of 929 at level two. Both
dictionaries remain fully grounded. Preservation hashes match level-one
books, reference weights and all earlier review artifacts.

Earlier repairs remain in place. Fifteen part-of-speech declarations and
fourteen new forms were reviewed in level_2_inflections. Optional defining
words still occupy slots within the existing 700-word list, and the teacher
context remains 4096 tokens. No general acceptance improvement is measured.

The next recommended investigation is independently grounded defining
language for sugar and sweet, with sour as a possible additional taste
candidate. Fruit senses of skin and stone and the noun-and-verb treatment of
crash remain separate unresolved reviews. No new sense is authorized by this
recommendation alone. Independent expert semantic review is unavailable.
Experimental, licensing and later-schedule decisions remain with the operator.

## Starting the next Codex session

The continuity prompt is `docs/process/RESUME_PROMPT.md`. Start a fresh session
in this existing directory so the authoring-host artifacts remain available.
The installed Codex command-line interface was version 0.158.0 when its help
output was checked for these options in the earlier continuity repair. That
version has not been rechecked for this refresh.

    codex --cd /Users/bsechter/projects/python/epagoge \
      --sandbox workspace-write --ask-for-approval on-request \
      "Read docs/process/RESUME_PROMPT.md and carry out its instructions."

This retains the configured model selection. Approval requests remain
available for local teacher access and the package cache. The prompt file is
an instruction for the new session, not a claim that a Stop hook has been
installed. Hook installation was not part of this work.

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

The 2026-09-28 audit verified 523 level-one books, 9,131 records and 330,710
words. The audit measured 954 level-two words before the increment described
above. Re-run the validators before using any count after corpus changes.

The generator requires explicit source evidence, output and report paths.
Its report retains prompts, replies, every candidate outcome and counts.
Teacher responses are nondeterministic. Semantic review remains necessary.

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

The 2026-09-28 audit found the teacher service, its model, local weights and
scan sources present. Service availability has not been rechecked for this
documentation refresh. Metal was visible outside the sandbox. Sandbox
failures must not be reported as missing host capabilities. The teacher
context remains 4,096.
The earlier pre-generation check measured approximately 13.9 GB of swap in
use. That is a historical measurement, not current memory state. Check
current memory before sustained generation or concurrent training.

Run the local gate, inspect its exit status, and check continuous integration
separately for the published revision. Local and remote checks are distinct.
