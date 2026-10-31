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

## Resume state, 2026-10-30, seventh Dromon trial

The operator directed the session to find a high-value iteration and
complete it through the Dromon harness. The brief in `CURRENT_BRIEF.md`
chose a lexicon batch from the long tail of sources already fetched. The
operator did not ask for a commit, so the work of the fourth to seventh
trials is left in the working tree on top of `8b81d43`. The sixth trial's
brief and condition are preserved in `evals/review/level_2_long_tail/`.
The sixth-trial resume state below is historical.

**Dependencies.** On the same day the operator asked that the Dependabot
alerts be addressed. Fifteen were open, fourteen in filelock and one in
setuptools, both reached only through torch under the training extra.
Commit `8b81d43` upgrades them in `uv.lock` to 4.2.5 and 84.2.1. It was
merged by rebase from a pull request whose continuous integration passed,
and continuous integration on `main` passed. The Dependabot pull request
for filelock alone was closed as superseded. GitHub's dependency graph
lists the new versions. Whether Dependabot has marked the alerts fixed is
recorded below as last observed.

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

## Resume state, 2026-10-30, sixth Dromon trial

The brief opened later on 2026-10-30 in `CURRENT_BRIEF.md` ran a sixth
multi-agent trial of the Dromon harness on the level-two lexicon and
corpus. The operator did not ask for a commit, so the work of the fourth,
fifth and sixth trials is left in the working tree on top of `aae4abe`.
The fifth trial's brief and condition are preserved in
`evals/review/level_2_stripped_forms/`. The fifth-trial resume state below
is historical.

**Lexicon.** Every earlier pool was fully decided, and the operator chose
to decide the 17 strings admissible only by suffix stripping. The batch in
`evals/review/level_2_stripped_forms/` and
`evals/review/level_3_stripped_forms/` admitted mining at level two and
organics at level three, filed second senses of color, cool, experience,
sample and well at level two, recorded the matching strings as their forms,
and deferred buildings, flooding, graphics, powered and united. Level two
rose from 2,996 to 2,997 distinct headwords, measured, because a second
sense adds no headword.

**Second senses.** `docs/decisions/LEXICON.md` allows a word several
senses, but the tools could not file one. The operator chose that the
worker extend them. `tools/admit.py`, `tools/author_definitions.py` and
`tools/measure_lexicon_increment.py` now admit a second sense keyed by word
and concept. `tools/word_provenance.py` records a second sense's origin
under a separate `senses` map, so it no longer overwrites the first
sense's record, which it had done for color, cool and well before the
review. `tools/validate_closure.py` now checks every dictionary record at a
level, not only the first per word. A verb sense of flood was removed
because the sources never use one. The suite holds 727 tests.

**Corpus.** The readiness reports of the third to fifth trials counted the
seed books and missed `curriculum/books/level_1/bk.dictionary.1.md`. The
luna line counted the term entries of `curriculum/vocabulary.json` at
levels one and two instead. No concept in the 26 level-two units without a
book is empty. The thinnest, with one word each, are balance, letter,
reconciliation, right_reason and two_shoulds_at_once. The top five became
r2.measure, p2.matter, p2.force, b2.mending and ac2.flow. A count measures
vocabulary on file, not whether a module can be written. The reports, the
script, the review and the three harness reports are in
`docs/process/trials/dromon_trial_6/`.

**Harness.** One `dromon mail` call timed out while the daemon was busy.
The lines ask for a blocking wait on a named task, a view of how generated
files differ from the last commit by key, which would have shown the
provenance overwrite, a check_disclosure that takes several paths, visible
truncation of command output, and counting rules stated in the brief.

Dromon's running estimates after this trial stood at about 40.25 dollars
for the worker and 1.95 dollars for the reviewer. This trial used about
10.23 dollars of the worker's. No cost is recorded for the Codex line. No
teacher was loaded.

## Resume state, 2026-10-30, fifth Dromon trial

The brief opened later on 2026-10-30 in `CURRENT_BRIEF.md` ran a fifth
multi-agent trial of the Dromon harness on the level-two lexicon and
corpus. The operator did not ask for a commit, so this work and the fourth
trial's are both left in the working tree on top of `aae4abe`. The fourth
trial's brief and condition are preserved in
`evals/review/level_2_agency_06/`. The fourth-trial resume state below is
historical.

**Lexicon.** No text was fetched. The worker line drew the pool again from
the first agency scan of 2026-10-10, whose hash matches the recorded one,
and it held 28 strings that still lacked a decision. The operator's session
withdrew none. The batch in `evals/review/level_2_agency_06/` and
`evals/review/level_3_agency_06/` admitted 9 headwords at level two and 4
at level three, excluded 11, mostly Spanish page titles, and deferred 6
page interface words. Level two rose from 2,987 to 2,996 distinct
headwords, measured, with coverage and closure complete at levels one to
three. Of the 243 strings in the first pool, only organics now lacks any
decision. It passes the pool rule because the lookup strips its final
letter to the adjective organic, while the source uses it as a noun.

**Open finding.** A string the pool rule removes as admissible may be
admissible only because the lookup strips a suffix to another headword, so
its own sense may never have been decided. The reviewer line found 17 such
strings frequent in the first scan, among them wells, united and mining.
Whether such strings need their own decision is for the operator.

**Corpus.** The luna line counted headwords at levels one and two together
for the 26 level-two units with no book, because a level-two book may use
level-one words. Only keeping_your_claim, letter, right_reason and
two_shoulds_at_once are empty at both levels. The top five under the third
trial's rule became r2.measure, ac2.flow, p2.matter, b2.mending and
p2.force. A headword count measures vocabulary on file, not whether a
module can be written. The reports, the script, the review and the three
harness reports are in `docs/process/trials/dromon_trial_5/`.

**Harness.** Creating every path the brief names before the lines started
removed the gate failure of the fourth trial. The lines ask for a record of
whether each removed string's sense is decided, kept snapshots of any
report used as a comparison baseline, visible truncation of command output,
and a stated path for project tools such as ruff.

Dromon's running estimates after this trial stood at about 30.02 dollars
for the worker and 1.55 dollars for the reviewer. No cost is recorded for
the Codex line. No teacher was loaded.

## Resume state, 2026-10-30, fourth Dromon trial

The brief opened on 2026-10-29 and restated on 2026-10-30 in
`CURRENT_BRIEF.md` ran a fourth multi-agent trial of the Dromon harness on
the level-two lexicon and corpus. The operator's restated direction did not
ask for a commit, so this work was left in the working tree on top of
`aae4abe`. That commit recorded the operator's merge settings for the
repository in `PROCESS_STRATEGY.md`, and its continuous integration run
succeeded. The third trial's brief and condition are preserved in
`evals/review/level_2_agency_05/`. The resume state below is historical.

**Lexicon.** The operator's session fetched 214 USGS Water Science School
pages beyond the 19 read on 2026-10-10, about 164,900 words, into
`tmp/lexicon-sources/agency5/`. The first crawl was throttled and stopped.
The second waited three seconds between requests and kept each page as it
arrived. Lines repeated from an earlier page were dropped, because the
question and answer pages repeat the same lists of related questions. The
worker line stopped after drawing a pool of 572 strings, and the operator's
session withdrew 1 before any decision and limited probe to one sense. The
batch in `evals/review/level_2_agency_05/` and
`evals/review/level_3_agency_05/` admitted 356 headwords at level two and
124 at level three, excluded 122 forms and deferred 43. Level two rose from
2,631 to 2,987 distinct headwords, measured, with coverage and closure
complete at levels one to three. The reviewer line proposed eight wordings,
and all eight were applied through `tools/author_definitions.py` without
change.

**Corpus.** The luna line reran the third trial's readiness script after
the batch. The 26 level-two units with no book all gained headwords, and 13
of their concepts still have none, among them agreeing, being_wrong and
opinion. It also listed the headwords on file for each concept of
`r2.measure`. A list of headwords shows vocabulary on file, not that a
module can be written. The reports, the sheet, the review and the three
harness reports are in `docs/process/trials/dromon_trial_4/`.

**Harness.** The local Dromon project file now names the private term list
as its disclosure list. The worker reports that this let it clear its
records and messages without reading the list, at the cost of one false
positive, because Dromon matches a term as a substring. The gate first
failed because the brief named the trial directory before it existed, and
the worker asked rather than editing `docs/process/`. The lines ask for an
allow list of ruled false positives, a wait on a named background task, a
check that every path a brief names exists before a line starts, visible
truncation of command output, and a recorded baseline snapshot for any
comparison.

Dromon's running estimates after this trial stood at about 27.00 dollars
for the worker and 1.25 dollars for the reviewer. No cost is recorded for
the Codex line. No teacher was loaded.

## Resume state, 2026-10-29, third Dromon trial

The brief opened later on 2026-10-29 in `CURRENT_BRIEF.md` ran a third
multi-agent trial of the Dromon harness on the level-two lexicon and
corpus. The follow-up's brief and condition are preserved in
`evals/review/level_2_agency_04/`. The follow-up resume state below is
historical for the revision and for publication.

**Lexicon.** The operator's session fetched 147 NASA Space Place pages
beyond the eight scanned on 2026-09-27, keeping each article body and
removing credit captions and repeated interface lines, into
`tmp/lexicon-sources/agency4/`. Whether each page is a federal employee
work was not checked page by page. The worker line stopped after drawing a
pool of 213 strings, and the operator's session withdrew 5 before any
decision. The batch in `evals/review/level_2_agency_04/` and
`evals/review/level_3_agency_04/` admitted 151 headwords at level two and
18 at level three, excluded 44 inflected forms and deferred 18. Level two
rose from 2,480 to 2,631 distinct headwords, measured, with coverage and
closure complete at levels one to three. Drive and the plural of
hypothesis were added to `src/epagoge/inflection.py`. The reviewer line
read all 169 definitions, and its eight proposed wordings, led by
astrology, were applied through `tools/author_definitions.py` without
change.

**Corpus.** The luna line measured, for the 25 level-two units with no
book, how many admitted headwords are filed under each concept they teach
or revisit. Its first round was read while the worker was still admitting,
and its ranking did not follow from its stated rule. The second round reads
a recorded seed book blob and prints its ranking from a stated rule. A
headword count measures vocabulary on file, not whether a module can be
written. The report, the review and the three harness reports are tracked
in `docs/process/trials/dromon_trial_3/`.

**Reports.** Stopping the worker at the pool made the withdrawal one filter
of the pool file rather than a rebuild. Dromon's new disclosure check
answers that this project has no disclosure list, so the worker scanned its
records against the banned vocabulary by its own script. The lines ask for
that check to read the project's list, a wait on a named background task,
a dry-run mode for the definition tool, and a commit stamp on each review.

Dromon's running estimates after all three trials and the follow-up stood
at about 19.01 dollars for the worker and 1.00 dollar for the reviewer. No
cost is recorded for the Codex line. No teacher was loaded, and the daemon
was stopped afterwards.

## Resume state, 2026-10-29, second trial follow-up

The brief opened on 2026-10-29 in `CURRENT_BRIEF.md` applied the
reviewer's findings on the third agency batch and had the luna line fix
its generator draft. Its condition was met, and the work was committed as
`80ff5cd`, whose [continuous integration
run](https://github.com/sgeos/epagoge/actions/runs/40968241645) succeeded.
The second trial's
brief and condition are preserved in
`evals/review/level_2_agency_03_followup/`. The second trial's resume state
below is historical for the revision and for publication.

**Lexicon.** The worker line changed four definitions, meteor, volcano and
tribe at level two and quasar at level three, and moved volcano from shape
to spatial position. Radio keeps reporting. The reviewer's wording for
meteor used streak, which is not admitted at level two, so the applied
wording says a bright line of light. A test in `tests/test_vocabulary.py`
asserts spun and volcanoes. The changes and reasons are recorded in
`evals/review/level_2_agency_03_followup/README.md`. No word changed its
decision and the headword counts did not change. The reviewer line
confirmed each change, the increment measurement and closure at levels one
to three. The new wording has had no review outside the Dromon lines.

**Generator draft.** Luna's revised draft is in the ignored
`tmp/dromon-trial-3/generator-draft.diff` and is not applied, as the
operator chose. Its repeat check now splits the preceding spread with the
acceptance code's own splitter and compares sentences without their final
punctuation, which the reviewer confirmed with sentences ending in a period
and a question mark. The record rule reaches only units covering ledger,
keeping_count or written_record. The offline phrase check was removed after
the reviewer found that it flagged none of seven phrasings from
`bk.ac2.ledger`, so the record limit rests on the prompt rule alone, and
whether a teacher follows it is unverified. In a scratch copy the full
suite passed with 682 tests, and the operator's session confirmed that the
draft applies to the current tree with its 50 generator and prompt tests
passing. The reviewer did not review the second round.

No teacher was loaded, and the Dromon daemon was stopped afterwards.

## Resume state, 2026-10-28, second Dromon trial

The brief opened later on 2026-10-28 in `CURRENT_BRIEF.md` ran a second
multi-agent trial of the Dromon harness on the level-two lexicon and
corpus. Its condition was met, and the work was committed as `91fff84`,
whose [continuous integration
run](https://github.com/sgeos/epagoge/actions/runs/40963904306) succeeded.
The first trial's brief and condition are preserved in
`evals/review/level_2_agency_03/`. The first trial's resume state below is
historical for the revision and for publication.

**Harness.** pydromon `main` was `36e156a`, clean, with its continuous
integration green, and 3,123 of its tests passed outside the socket and
live markers. The same three lines ran from the same local project file,
and the daemon was stopped afterwards. The briefs carried the report
criteria, the cost and turn limits, the pool rule, the measurement
re-recording and the instruction to finish the gate inside the turn from
the start, as the first trial's reports asked.

**Lexicon.** The operator's session fetched 153 StarChild level 1 pages and
two Ben's Guide pages into `tmp/lexicon-sources/agency3/`. The NASA
children's earth pages were not fetched again, because the first agency
pass scanned them. The worker's batch in `evals/review/level_2_agency_03/`
and `evals/review/level_3_agency_03/` decided a pool of 32 strings, after
two were withdrawn by the operator's session before decision. It admitted
17 headwords at level two and 3 at level three, excluded 10 and deferred 7.
Level two rose from 2,463 to 2,480 distinct headwords, measured, with
coverage and closure complete at levels one to three. Spin and the plural
of volcano were added to `src/epagoge/inflection.py`.

**Corpus.** Luna found that 1 of the 26 level-two schedule units has a
book. It drafted a change to the module prompts and acceptance checks in
`tmp/dromon-trial-2/generator-draft.diff`, tested in a scratch copy at 682
tests against a baseline of 678. The draft is not applied. Its first
attempt was an untested outline, and it finished after an ordered recipe.

**Review.** The reviewer confirmed the condition and read every admitted
definition. It proposed new wording for meteor, volcano, quasar and tribe,
a concept check for volcano and radio, tests for the two new inflections,
and a later decision on deferring date. It found by measurement that the
draft's repeat check misses sentences repeated across spreads, because it
splits the previous spread differently from the acceptance code, and that
its phrase list catches one of seven phrasings tested from
`bk.ac2.ledger`. None of these is applied. They await the operator.

**Reports.** Each line wrote a second harness report under
`tmp/dromon-trial-2/`. The worker finished in one turn with no missed
report. Its new risk is that a scratch copy linked to the shared `.venv`
could repoint the real editable install if uv succeeded in the copy, which
did not happen. The lines ask for a wait on a named background task, a
pass or fail term-list check, a record of what a gate run covered, known
negatives for pattern scans, and visible model load state.

Dromon's estimates are running totals over each line's kept session. The
worker stood at about 10.62 dollars and the reviewer at about 0.21 dollars
after both trials. No cost is recorded for the Codex line. No teacher was
loaded.

## Resume state, 2026-10-28, Dromon trial

The brief opened on 2026-10-28 in `CURRENT_BRIEF.md` ran a multi-agent
trial of the Dromon harness on the level-two lexicon and corpus. Its
condition is met on the working tree and is uncommitted until the operator
asks. The sandbox-fix brief and its condition are preserved in
`evals/review/level_2_agency_02/`. Earlier resume states are historical for
the revision and for publication.

**Harness.** pydromon `main` was `d8673c7`, clean, with its continuous
integration green, and 2,977 of its tests passed outside the socket and
live markers. The daemon ran from that editable install, outside the
sandbox, from the local `.dromon/` project file, and was stopped afterwards.
Three lines took part. `worker` ran Claude Opus 5.5 and wrote tracked
files. `reviewer` ran Claude Haiku 5.5 and wrote only under the ignored
`tmp/dromon-trial/`. `luna` ran GPT-6-Luna under Codex and wrote only there.
Dromon's cost estimates were about 5.24 dollars for `worker` and 0.06
dollars for `reviewer`. The second looks low for the work done and may be
incomplete. Dromon records no cost for Codex lines.

**Lexicon.** The operator's session fetched 39 Energy Information
Administration elementary pages and 4 Ben's Guide pages for ages 4 to 8,
two candidates from `docs/decisions/AGENCY_SOURCES.md`, into
`tmp/lexicon-sources/agency2/`. The worker's batch in
`evals/review/level_2_agency_02/` and `evals/review/level_3_agency_02/`
decided all 237 pool strings, drawn with one source sufficient as in the
first agency pass. It admitted 153 headwords at level two and 32 at level
three, excluded 96 and deferred 8. Level two rose from 2,310 to 2,463
distinct headwords, measured, with coverage and closure complete at levels
one to three. It also made control, offset and transfer irregular in
`src/epagoge/inflection.py`, added the batch to the stacked measurement
test, and re-recorded the eleven earlier level-two measurements, as
`bb17901` did. The sandbox refused its `git checkout`, and it restored five
files through `git show` and a copy, which it disclosed.

**Review.** The reviewer confirmed the condition clause by clause and read
43 definitions. It proposed changes to ten, among them a circular
definition of environmental and overconfident definitions of engine,
battery and fracking. On the operator's direction the worker applied all
ten through `tools/author_definitions.py`, with two concept changes, for
battery and biofuel, synced into the thesaurus. For intensive it gave the
general sense of much work or care beside the energy-use sense, not the
physical-property sense the reviewer named, and it wrote its own wording
for cryogenic and alcohol, where the reviewer gave none. The counts and
closure were unchanged.
Its one term-list hit was a substring inside a longer word, and the
project's scan is clean.

**Corpus.** Luna reviewed `bk.ac2.ledger` in
`tmp/dromon-trial/review-ac2-ledger.md`. It measured three spreads of 617
words against a module of 64 spreads and at least 12,800 words, found
repeated sentences and claims that a record cannot be wrong, and separated
findings for the book from findings for the generator. No book other than
the two dictionary seed books changed, and no teacher was loaded.

**Reports.** Each line wrote a harness experience report under
`tmp/dromon-trial/`. They name a missed report after a background gate, a
turn the engine began by itself and Dromon interrupted, mail that reaches a
line only between turns, denials given without a reason, late visibility of
cost and turn limits, and the lack of a pass or fail check against the
private term list.

**Gate.** After the definition changes, `tools/check.sh` exited 0 inside
the sandbox with 678 tests, no skips, 96 percent core coverage and a clean
disclosure scan.

## Resume state, 2026-10-25, sandbox fixes

The brief opened on 2026-10-25 in `CURRENT_BRIEF.md` applies two sandbox
fixes found when Claude Code first resumed this tree. Its condition is in
`COMPLETION_CONDITION.md`. The closed brief of 2026-10-09 and its condition
are preserved in `evals/review/level_2_scan_10/`. The earlier resume state
of 2026-10-25 below is historical for the revision and for publication. Its
other findings remain.

The session began on `7cd961fe14c0d84267b3efe1632e5a058ba85aab`, message
"Prepare the handoff for Claude Code". Local `HEAD`, the stored
`origin/main` and `git ls-remote origin main` all named that commit, so
the three commits earlier recorded as unpublished and the handoff commit
were on the remote. Its [continuous integration
run](https://github.com/sgeos/epagoge/actions/runs/40216991736) succeeded.
`gh auth status` reported a valid keyring login for `sgeos` in this
session. The measurement check named above still fails as expected.

On that commit the full gate exited 1 inside the Claude Code 2.1.310
sandbox and 0 outside it. A bare `mktemp` ignored `TMPDIR` and wrote under
`/var/folders`, and the sandbox denies writes to `.git/config` and
`.git/hooks` at any depth, which broke `git init` in the provenance test.
Each `mktemp` in `tools/check.sh` and `tools/scrub_scan.sh` now names an
explicit template, and the test selects a git directory named `history`
through `GIT_DIR` and `GIT_WORK_TREE`. With those changes the gate exited 0
both inside the sandbox and outside it on 2026-10-25, with 678 tests, no
skips, 96 percent core coverage, 92 percent training coverage and a clean
disclosure scan over 957 files. uv ran normally inside the sandbox.
On the operator's request these changes were committed as
`abca3af79f348e24b0b99dd679270dd3d7782242` and pushed to `origin/main`
over HTTPS without force. `git ls-remote origin main` then named that
commit, and its [continuous integration
run](https://github.com/sgeos/epagoge/actions/runs/40219585326) succeeded.
That evidence covers `abca3af`, not the later commit that records it.
Commit and push only when the operator asks.

## Dromon dogfooding review, 2026-10-25

On the operator's request this session reviewed the Python prototype of
the Dromon harness, `~/projects/python/pydromon`, for dogfooding on this
project. No implementation scope was opened, and no tracked file of either
repository changed for the review.

Dromon keeps its project file at `.dromon/dromon.toml`, which is local to
this host and excluded through `.git/info/exclude`, so the disclosure scan
does not read it. `dromon config` reported it valid. It declares the
teacher named in `generators/TEACHER.md` at a context of 4096, with
autostart off, and Claude Code lines that read `CLAUDE.md` and the
operator's global rules, run their shell in the sandbox, and are refused
`git commit` and `git push`. `dromon teacher status` reported the model
pulled and not loaded. About one gigabyte of pages was free and about
twelve gigabytes inactive.

Pydromon `HEAD` was `f1543c1`, and its continuous integration run
succeeded. A clean archive of that commit passed 805 tests outside the
socket and live markers, with ruff and pyright strict clean. The socket and
live tests were not run. Its working tree held uncommitted changes from its
own session, and two tests failed on that tree. Its editable install runs
the working tree, so the review supports dogfooding `f1543c1` and not that
tree.

These points are unverified. Whether this project's gate passes inside a
Dromon line's sandbox has not been measured. The commit and push refusal is
a pair of command patterns and may not match forms such as
`git -C . commit`, and the sandbox does not itself prevent a commit. A
Codex line runs read-only and cannot run the gate. Notes for the pydromon
session were left in its ignored `tmp/epagoge-dogfooding-notes.md`.

## Resume state, 2026-10-25

Superseded for the revision and for publication by the sandbox-fix resume
state above.

No implementation scope is open. Do not repeat the admission brief of
2026-10-09, and do not admit further words from the seven-source pool, the
agency pool, or the long tail. The resume state of 2026-10-23 is historical
for the revision and for publication. Its lexicon findings remain, and the
measurement check below is still expected to fail.

Before this edit, local `HEAD` was
`eb2fb3cda63cf9e22a4ecbe1ef87ff30b4f5b5c0`, message "Record the 2026-10-23
handoff and close the admission brief". The working tree was clean. The
commits not on `origin/main` were `bb17901`, `583548d` and `eb2fb3c`. This
edit leaves `AGENTS.md`, `docs/process/HANDOFF.md` and
`docs/process/RESUME_PROMPT.md` uncommitted until the operator commits them.

The stored `origin/main` is
`50de0749fab5da632352cc029f91e7359d4db117`. On 2026-10-25 `git fetch origin`
over HTTPS exited 0 and printed nothing. `git push origin main` from the
Grok session on 2026-10-24 and again on 2026-10-25 exited 128 with
"fatal: could not read Username for 'https://github.com': terminal prompts
disabled". `gh auth status` in that session reported the stored token for
account `sgeos` as invalid. No `GH_TOKEN` or `GITHUB_TOKEN` variable was
set. A read-only keychain lookup for service `gh:github.com` and account
`sgeos` exited 44 and said the item could not be found. The SSH denial
stays in place. The remote URL is HTTPS. Do not force-push. Publication
from the Grok session was not completed. Determine publication from git
and the remote.

The full local gate passed on 2026-10-24, before `eb2fb3c`, with 678 tests,
no skips, 96 percent core coverage, and a clean disclosure scan. The same
gate passed on this edit on 2026-10-25, again with 678 tests, no skips, 96
percent core coverage, and a clean disclosure scan. uv fell back to the
lockfile check because it could not create its cache temporary file.
Continuous integration has not run for the unpublished commits. The measurement check
named above still exits with "recorded measurement differs from the current
tree". That failure is expected. It is not a defect to repair.

Claude Code 2.1.310 is installed at `~/.local/bin/claude`. Its help output
was checked on 2026-10-25. It starts in the current directory and reads
`CLAUDE.md` unless `--bare` is passed. Do not pass `--bare` or
`--dangerously-skip-permissions`. The launch command is in `AGENTS.md`.
Confirmatory training remains blocked. Do not load the teacher for this
handoff.

## Resume state, 2026-10-23

Superseded for the revision and for publication by the resume state of
2026-10-25. No implementation scope is open. Do not repeat the admission
brief of 2026-10-09, and do not admit further words from the seven-source
pool, the agency pool, or the long tail.

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

The repository is prepared for Codex, Grok Build and Claude Code.
`AGENTS.md` gives the verified launch commands, what a sandboxed agent
needs, and what a fresh clone lacks. Trial sessions of Codex and Grok Build
on 2026-10-08 loaded the instructions, passed the handoff validity checks
and passed the full gate inside their workspace sandboxes, Codex with the
network off. Claude Code was not part of that trial. On 2026-10-25 a
Claude Code session launched with the command in `AGENTS.md` loaded the
instructions, ran the handoff validity checks, and passed the full gate
inside its sandbox after the fixes recorded above. Network access is needed only to publish, and the loopback teacher
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
