# Handoff

## Validity check and continuity stamp

Stamped 2026-10-31. The verified base is
`8bd4e606095ad9ea40a9c244fc49062cb5700553`, the commit that took the work of
the fourth to seventh Dromon trials into `main`. This is an ancestry anchor,
not the revision containing this document. A later documentation commit
does not invalidate it merely by changing the current revision.

The base was pushed to `origin/main` and its [continuous integration
run](https://github.com/sgeos/epagoge/actions/runs/41165626718) succeeded.
The full local gate passed on it with 727 tests run twice and no skips,
zero type errors or warnings, 96 percent core coverage, 92 percent reported
training coverage and a clean disclosure scan over 1,110 files. That
evidence covers the base, not later revisions. The previous stamp of
2026-10-08 named `99a9d8ceb86fb27544da7179d4e92807b9fa935a`, which remains
an ancestor.

Read `CLAUDE.md` and run these checks before relying on the state below.

    git status --short
    git merge-base --is-ancestor 8bd4e606095ad9ea40a9c244fc49062cb5700553 HEAD
    git log --oneline 8bd4e606095ad9ea40a9c244fc49062cb5700553..HEAD
    .venv/bin/python tools/measure_lexicon_increment.py \
      evals/review/level_2_long_tail \
      --check evals/review/level_2_long_tail/measurement.json

A passing measurement check means the level-two counts below match the
tree. It passed on 2026-10-31. It fails by design once any later batch
changes the vocabulary, and the measurements of every earlier batch already
fail for that reason. A failure then marks the counts below as stale rather
than wrong. No level-three batch records a measurement, so level-three
counts have no such check. Missing host artifacts make the associated
checks unverified rather than disproved.

## Holding state, 2026-10-31

**No implementation scope is open.** On 2026-10-31 the operator asked that
the project be brought into a nominal holding state, that all work be
committed, pushed and merged, and that the concerns needing a decision be
listed with their obvious choices. The holding brief in `CURRENT_BRIEF.md`
records that scope. The seventh trial's brief and condition are preserved
in `docs/process/trials/dromon_trial_7/`. A resuming session waits for the
operator's next task and does not start work from the list of concerns.

**Decisions.** Every concern awaiting the operator is consolidated in
`OPEN_DECISIONS.md`, each with its obvious choices. The list supersedes the
open items once kept in this handoff. Choosing among the options there is
reserved to the operator, and no option is recommended as settled.

**Publication.** The work of the fourth to seventh trials was committed on
the operator's request of 2026-10-30 as the verified base above and pushed
to `main` without force. The holding commit that records this state was
merged by rebase from a pull request. Determine actual publication from git
and the remote. There are no other local or remote branches, no open pull
requests and no other worktrees, as observed on 2026-10-31.

**Dependencies.** On 2026-10-31 GitHub listed all 15 Dependabot alerts of
2026-10-30 as fixed and none open, after `8b81d43` upgraded filelock and
setuptools in `uv.lock`.

**Host.** No Dromon daemon was running for this project, and the teacher
service answered on its loopback address with no model loaded. The local
Dromon project file still carries the seventh trial's settings, with the
reviewer line on the Fable model and the raised cost limits. Its backup
from before that trial is the ignored `tmp/dromon.toml.before-trial-7`.
Whether to restore it is listed in `OPEN_DECISIONS.md`. Earlier resume
states and the stale status sections of 2026-10-07 to 2026-10-10 were moved
to `HANDOFF_HISTORY.md`.

## Resume state, 2026-10-30, seventh Dromon trial

The operator directed the session to find a high-value iteration and
complete it through the Dromon harness. Its brief, now preserved in
`docs/process/trials/dromon_trial_7/`, chose a lexicon batch from the long
tail of sources already fetched. The work of the fourth to seventh trials
was left in the working tree on top of `8b81d43` until the operator asked
for a commit, and it is now the verified base above. The sixth trial's
brief and condition are preserved in `evals/review/level_2_long_tail/`.
This resume state is historical for the revision and for publication.

**Dependencies.** On the same day the operator asked that the Dependabot
alerts be addressed. Fifteen were open, fourteen in filelock and one in
setuptools, both reached only through torch under the training extra.
Commit `8b81d43` upgrades them in `uv.lock` to 4.2.5 and 84.2.1. It was
merged by rebase from a pull request whose continuous integration passed,
and continuous integration on `main` passed. The Dependabot pull request
for filelock alone was closed as superseded. GitHub's dependency graph
lists the new versions. Whether Dependabot has marked the alerts fixed is
recorded in the holding state above.

**Lexicon.** The sixteen source texts already scanned leave 20 undecided
strings at a threshold of five and 613 at a threshold of four. The
operator's session withdrew 6, recorded as a count only. The batch in
`evals/review/level_2_long_tail/` and `evals/review/level_3_long_tail/`
decided the other 607. 296 pool strings were admitted at level two and 74
at level three, 129 were excluded as forms of citation forms admitted in
their place, 95 were deferred and 13 excluded for other reasons. With
those citation forms, 376 words were admitted at level two and 104 at
level three, including second senses of empty and bond. Level two rose
from 2,997 to 3,372 distinct headwords, measured. No existing record in
`curriculum/provenance.json` or `curriculum/vocabulary.json` changed
against `aae4abe`, measured by key.

**Review.** The reviewer line ran on the Fable model, because the
harness does not offer the Sonnet model. Its findings were decided by the
operator's session and applied. An instruction of that session to defer
translates rested on the false premise that an earlier batch decided
translate. The worker found that it did not and asked, and translate was
widened instead. The reviewer found that the term entry for tornado lists
tornados and not tornadoes, which an earlier batch admitted. That is left
open.

**Corpus.** The luna line listed 160 strings of the threshold-four scan
admissible only by suffix stripping and named in no reviewed-forms list,
six of them already deferred. The readiness top five changed only at fifth
place. The reports, the review and the three harness reports are in
`docs/process/trials/dromon_trial_7/`.

**Harness.** The lines ask for a lookup of every review decision on a
word across batches, a saved base for the by-key diff so that one batch
can be isolated while others are uncommitted, process visibility, an
in-place edit tool for read-only lines, and visible truncation. A model
change of a line must go through `dromon rebind`, and the project file
must then name the new model, or the daemon refuses to start.

Dromon's running estimates after this trial stood at about 50.99 dollars
for the worker and 10.62 dollars for the reviewer, so this trial used
about 10.74 and 8.67 dollars. No cost is recorded for the Codex line. No
teacher was loaded and no text was fetched.

## Starting the next session

The repository is prepared for Codex, Grok Build and Claude Code.
`AGENTS.md` gives the verified launch commands, what a sandboxed agent
needs, and what a fresh clone lacks. Trial sessions of Codex and Grok Build
on 2026-10-08 loaded the instructions, passed the handoff validity checks
and passed the full gate inside their workspace sandboxes, Codex with the
network off. Claude Code was not part of that trial. On 2026-10-25 a
Claude Code session launched with the command in `AGENTS.md` loaded the
instructions, ran the handoff validity checks, and passed the full gate
inside its sandbox after the fixes recorded in `HANDOFF_HISTORY.md`. Network access is needed only to publish, and the loopback teacher
only to generate. Give a new session `docs/process/RESUME_PROMPT.md`. Start
it in this existing directory, so the ignored host artifacts under
`secret/`, `tmp/` and `evals/pilot/` remain available.

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

## Open items for the operator

Consolidated on 2026-10-31 in `OPEN_DECISIONS.md`. The three items once
listed here, function words, documentation spelling and archaic deferrals,
are carried there.

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
