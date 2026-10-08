# Handoff

## Validity check and continuity stamp

Stamped 2026-10-08 at 17:45 Coordinated Universal Time. The verified base is
`99a9d8ceb86fb27544da7179d4e92807b9fa935a`, the commit that made the gate pass inside agent sandboxes. This is an
ancestry anchor, not the revision containing this document. A later
documentation commit does not invalidate it merely by changing the current
revision.

The base was pushed to `origin/main` and its [continuous integration
run](https://github.com/sgeos/epagoge/actions/runs/37818789022) succeeded.
The full local gate passed on it with 631 tests and no skips, zero type
errors or warnings, 96 percent core coverage, 92 percent reported training
coverage and a clean disclosure scan. It also passed inside the Codex
`workspace-write` and Grok Build `workspace` sandboxes. That evidence covers
the base, not later revisions.

Read `CLAUDE.md` and run these checks before relying on the state below.

    git status --short
    git merge-base --is-ancestor 99a9d8ceb86fb27544da7179d4e92807b9fa935a HEAD
    git log --oneline 99a9d8ceb86fb27544da7179d4e92807b9fa935a..HEAD
    .venv/bin/python tools/measure_lexicon_increment.py \
      evals/review/level_2_operator_decisions \
      --check evals/review/level_2_operator_decisions/measurement.json

A passing measurement check means the lexicon counts below match the tree.
It fails by design once any later batch changes the vocabulary, and the
measurements of every earlier batch already fail for that reason. A failure
then marks the counts below as stale rather than wrong. Missing host
artifacts make the associated checks unverified rather than disproved.

## Current authority and task status

On 2026-10-07 a self-directed loop ran three lexical scopes and was
cancelled by the operator. The operator then decided the six open items it
left, and that scope is described by `CURRENT_BRIEF.md` and
`COMPLETION_CONDITION.md`. **No further scope is open.** The brief and
condition are evidence of delivered work, not instructions to repeat it.
Earlier briefs and conditions are preserved as `previous_*.md` beside the
review records that followed them. Earlier handoffs in `HANDOFF_HISTORY.md`
are historical evidence. Durable failure analysis is in
`PROCESS_STRATEGY.md`.

## Starting the next session

The repository is prepared for Codex and Grok Build. `AGENTS.md` gives the
verified launch commands for both, what a sandboxed agent needs, and what a
fresh clone lacks. Trial sessions of both tools on 2026-10-08 loaded the
instructions, passed the handoff validity checks and passed the full gate
inside their workspace sandboxes, Codex with the network off. Network access
is needed only to publish, and the loopback teacher only to generate. Give a new session
`docs/process/RESUME_PROMPT.md`. Start it in this existing directory, so the
ignored host artifacts under `secret/`, `tmp/` and `evals/pilot/` remain
available.

## Operator decisions of 2026-10-07

1. **All words are shown and defined.** Ostensive words stay grounded by
   showing and now also need a definition. All have one. Sweet and sour are
   admitted at level two as ostensive and defined. **Function words were read
   as outside this decision**, because they cannot be shown and name no
   concept. That reading is the agent's and is open for the operator.
2. **US English.** The curriculum uses color, gray and toward. The
   substitution table points British forms at US forms. Documentation prose
   is still British and was not converted.
3. **Substitution contradictions.** The level-one bans were stale and are
   removed. A key admissible at level one now fails the gate.
4. **Missing parts of speech.** Eighty-three nouns now declare noun or mass
   noun, so skies, men and thirty-eight other plurals are admissible.
   Adjectives, adverbs and inflections filed as headwords were not changed.
5. **Technical words.** Forty-three of the 44 are admitted. Electromagnetic
   waits on electricity and magnet.
6. **Commit and push.** Done for this work. The authorization does not
   extend to later work.

## What the session delivered

| Batch | Pool | Entries | Admitted | Deferred | Excluded |
| --- | --- | --- | --- | --- | --- |
| `level_2_era_overlap` | Scan words frequent in both eras | 146 | 83 | 20 | 43 |
| `level_2_food_blockers` | Blockers of retained rejections | 57 | 36 | 13 | 8 |
| `level_2_multi_source` | Scan words frequent in two sources | 183 | 100 | 68 | 15 |
| `level_2_operator_decisions` | Taste words and technical deferrals | 57 | 48 | 1 | 8 |

No teacher ran in any batch, because host swap was nearly exhausted when the
session began, and each `authoring.json` records that. Measured on the final
tree, level two admits 1,232 distinct headwords, up from 966 at the start of
the session, leaving 8,768 to the approximate ten-thousand-word target. Level
one remains at 849. Required definition coverage, now including ostensive
words, is 849 of 849 at level one and 1,232 of 1,232 at level two, with
complete closure at both.

**Tools.** The measurement tool accounts for a batch that declares no teacher
ran. `tools/blocking_words.py` ranks words by the retained rejected
definitions they blocked. `tools/candidate_pool.py` selects a pool by stated
rules and counts without naming words the private disclosure pattern
withholds. `tools/check_substitutions.py` gates level one and reports level
two. Prompts drop substitution keys admissible at the prompted level.

**The disclosure scan had three holes, now closed.** It missed plurals of
withheld terms, its line-break pass was case-sensitive, and it printed clean
over no files when its temporary file could not be created.

**Inflection tables.** Strike, lay, ride, send and occur are irregular. Offer,
scatter, travel and monitor do not double. Species, potato and axis have their
plurals recorded.

## Open items for the operator

1. **Function words.** Whether the and, of and the other function words should
   also be defined. They have no concept to file a dictionary record under, so
   doing so needs a decision about how such records are classified.
2. **Documentation spelling.** Whether documentation prose should also move
   to US English.
3. **Archaic and other deferrals.** Words deferred as archaic, religious or
   sense-ambiguous remain deferred, each with a reason in its review record.

## Recommended next work

All pools used in this session are exhausted. `tools/candidate_pool.py` can
produce the next by relaxing the source rule to one source, which leaves
roughly 1,800 words needing heavier judgement. A different route is drafting
level-two books, since no level-two book uses any word admitted in this
session and the coverage rule is unmet at level two. Drafting needs the
teacher, so check host memory first. Neither throughput nor the semantic
quality of agent-authored definitions has been measured.

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
