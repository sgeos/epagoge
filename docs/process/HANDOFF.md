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

## Resume state, 2026-10-23

No implementation scope is open. Do not repeat the admission brief of
2026-10-09, and do not admit further words from the seven-source pool, the
agency pool, or the long tail.

Local `HEAD` is `bb1790162b98ca9dfa3354bef3bc260a71432526`, message
"Admit the scanned level-two pool and count forms under one citation".
Before this handoff edit the working tree was clean. The only expected
uncommitted files are this handoff, `RESUME_PROMPT.md`, `CURRENT_BRIEF.md`,
and `COMPLETION_CONDITION.md`. Leave them in place. Do not commit or push
them unless the operator asks.

The remote-tracking ref `origin/main` is
`50de0749fab5da632352cc029f91e7359d4db117`. A push of the local commit was
attempted on 2026-10-11 and failed because host key verification could not
read the SSH known-hosts file. The GitHub CLI token was invalid the same
day. Publication of `bb17901` was not confirmed, and the remote was not
fetched again on 2026-10-23. Determine publication from git and the remote.
Ask before pushing.

The full local gate passed on the tree that became `bb17901`, before the
commit, with 678 tests, no skips, 96 percent core coverage, and a clean
disclosure scan. Continuous integration has not run for that commit. On
2026-10-23 `tools/validate_closure.py` reported level two at 2,310 of
2,310, self-hosting yes, with a 267-word seed. The measurement check named
above exits with "recorded measurement differs from the current tree".
That failure means the 2026-10-07 counts are stale. It is not a defect to
repair.

`epagoge.lexeme` and `tools/analyse_lexemes.py` are in the committed tree.
The vocabulary check is unchanged. A grouping is a proposal and admits
nothing.

On 2026-10-14 the operator asked how Space Bunny Alpha compares with the
teacher and whether its terms allow that use. The reading given that day
was that they do not, that the OpenRouter listing was absent, and that the
local Apache checkpoint remains the teacher. The reading was not added to
`OPEN_QUESTIONS.md`. Do not switch the teacher on the strength of it.

Ollama was not listening on `127.0.0.1:11434` on 2026-10-11. That was not
rechecked on 2026-10-23. Do not load the teacher for this handoff.
Confirmatory training remains blocked.

Grok Build on this host is still 1.0.46. The launch command in `AGENTS.md`
was rechecked against its help output on 2026-10-23. Do not pass
`--sandbox` on this host.

## Current authority and task status

On 2026-10-07 a self-directed loop ran three lexical scopes and was
cancelled by the operator. The operator then decided the six open items it
left. That scope is delivered. Its brief and condition are preserved as
`previous_*.md` in `evals/review/level_2_one_source/`. Earlier handoffs in
`HANDOFF_HISTORY.md` are historical evidence. Durable failure analysis is
in `PROCESS_STRATEGY.md`.

**Scope opened 2026-10-09 and closed by the resume state above.** The
operator directed that the remaining
level-two scan candidates be admitted, because the lexicon is far under
its approximate target. The brief and the completion condition in this
directory describe that work. The first batch, 24 McGuffey words, is
recorded in `evals/review/level_2_one_source/`. A second
batch in `evals/review/level_2_scan_02/` admits 432 and excludes 7. A third
batch in `evals/review/level_2_scan_03/` admits 71 and excludes 3.
`level_2_scan_04/` admits 67. `level_2_scan_05/` admits 20 and excludes
10. `level_2_scan_06/` admits 25 and excludes 12. `level_2_scan_07/`
admits 72 and excludes 191. `level_2_scan_08/` admits 72.
`level_2_scan_09/` admits 72. `level_2_scan_10/` admits 72 and defers
thee, thy, thine and unto. The scan batches and the agency batches named
below are committed with the lexicon they changed. Measured
after the tenth, distinct headwords through level two are 2,159, and a
fresh selection from the same scan prints an empty pool. On 2026-10-10 a
separate scan of three public-domain agency sources admitted 151 further
level-two headwords, recorded in `evals/review/level_2_agency/`, and 16
level-three headwords, recorded in `evals/review/level_3_agency/`.
Distinct headwords through level two are 2,310, measured. The same tree
registers noun, verb, adjective and adverb forms, and `epagoge.lexeme`
counts observed spellings under one citation. The vocabulary check is
unchanged. A grouping is a proposal and admits nothing. The counts in the delivery
table below are the 2026-10-07 tree. Dale-Chall and the New General Service
List are not inputs. The long tail below the scan threshold is outside the
brief. The teacher was not loaded. About 175 megabytes of pages were free
and swap held 10,956 of 12,288 megabytes.

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

The one-source frequent pool from the 2026-09-27 scan is decided. Measured
after `evals/review/level_2_scan_10/`, distinct headwords through level two
were 2,159, and a fresh selection from that scan prints an empty pool. On
2026-10-10 three public-domain agency sources were scanned. The filtered
pool held 243 words. 151 were admitted at level two and 16 at level three.
Distinct headwords through level two are 2,310, measured, leaving 7,690 to
the approximate target of about ten thousand. Strings from that pool that
were not admitted were left without a review decision. The candidate list
in `docs/decisions/AGENCY_SOURCES.md` is not exhausted. Forest Service
readers, further NOAA pages, Energy Information Administration pages, Fish
and Wildlife booklets, Ben's Guide, and National Park Service booklets were
not fetched in this pass, and the StarChild level 1 fetch was a thin
sample. Grade 8 remains level three. A word too advanced for level two is
scheduled higher rather than dropped. Alternates for each class are in
`docs/decisions/WORD_FORMS.md`. Check host memory before loading the
teacher. Neither throughput nor the semantic quality of agent-authored
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
