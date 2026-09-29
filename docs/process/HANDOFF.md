# Handoff

Updated after the Codex continuity repair and bounded lexicon increment on
2026-09-28.

## Current authority

Read `CLAUDE.md`, then this file and `CURRENT_BRIEF.md`. Earlier handoffs are
preserved in `HANDOFF_HISTORY.md` as historical evidence. Their commands and
status statements are not current instructions. Durable failure analysis is
in `PROCESS_STRATEGY.md`.

## State being handed over

The operator authorized publication of the accumulated continuity repairs,
lexical increments and subsequent bounded reviews on 2026-09-28. They form one
publication scope. Earlier descriptions of this work as uncommitted refer to
the earlier sessions. Check the actual git status and remote revision before
assuming a later session has the same tree.

The local gate most recently passed with 601 tests and no skips, zero type
errors or warnings, 96 percent core coverage and 92 percent reported training
coverage. The disclosure scan passed. Remote continuous-integration status
must be checked separately for the published revision.

The current brief and completion condition describe this bounded review and
publication scope. Establish a new brief and condition for later work.

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

The suggested prompt is `docs/process/RESUME_PROMPT.md`. Start a fresh session
in this existing directory so the authoring-host artifacts remain available. The installed Codex command-line interface was version 0.158.0
when its help output was checked for these options.

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

The recorded increment can also be checked against the current authoring tree

    .venv/bin/python tools/measure_lexicon_increment.py \
      evals/review/level_2_taste_senses \
      --check evals/review/level_2_taste_senses/measurement.json

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

The audit found the teacher service, its model, local weights and scan sources
present. Metal was visible outside the sandbox. Sandbox failures must not be
reported as missing host capabilities. The teacher context remains 4,096.
The latest pre-generation check measured approximately 13.9 GB of swap in use. Check current memory
before sustained generation or concurrent training.

Run the local gate, inspect its exit status, and check continuous integration
separately for the published revision. Local and remote checks are distinct.
