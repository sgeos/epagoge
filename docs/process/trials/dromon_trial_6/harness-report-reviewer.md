# Harness experience report, reviewer line, seventh trial

Recorded 2026-10-30. Labels: **[F]** fact from my own turns, **[I]** inference, **[H]** hypothesis.

I read `docs/process/trials/dromon_trial_5/harness-report-reviewer.md` first. Section 5 assesses each earlier suggestion against this trial.

## 1. What worked well

**[F]** The stamp held. I recorded HEAD `aae4abe` and the vocabulary blob before reading the batch, and both review files state them.

**[F]** Part A and Part B were separated by the operator's mail. I finished Part A, sent one message and stopped. The Part B mail arrived in a later turn and I resumed from the saved file.

**[F]** Luna's script ran unchanged with `python3 -I` and matched the report's tables, which made the readiness check a direct test rather than a reading.

## 2. What got in my way, and how I worked around it

**[F]** The sandbox does not provide `timeout`, and pytest is not installed in `.venv`. I ran the two relevant test files with unittest and did not install pytest.

**[F]** A compaction left a tool-result dump in my context at the start of one turn. I did not act on it. I checked the mailbox before doing anything else.

**[F]** My first draft of Part A had a wrong count and a mislabelled heading. I corrected both by string replacement before sending.

## 3. What I could not see or do

**[F]** I did not run tools/check.sh, as directed, and the full test suite was not run.

**[F]** I could not confirm the worker's fixes for findings A, C and D, because they came after my stamp.

**[F]** The fifth-trial readiness report depends on seed books that a later trial's term file no longer matches. I could check the counts only against the files as they stand at HEAD.

## 4. Ranked suggestions

1. **Scope every readiness heading to the levels it counts.** The problem is that the term-based report counts levels one and two only, and its heading does not say so.
2. **Record the counting rule for forms.** The problem is that a word and its inflection are two term entries, so counts inflate by one for each such pair, and the report does not say whether forms count as coverage.
3. **Name the source file in every count script.** The problem is that the fifth-trial count read only the seed books, and its zeros came from that file set.
4. **Stamp each review with HEAD and the source blob.** Still open from earlier trials, and handled by hand again here.
5. **Give wake notes a reason.** The problem is that compaction notes carry no cause.

## 5. Earlier suggestions, now

- **Verifiable gate record (third trial, 3).** **Still applies.** I did not run the gate, so the commit's status is unchecked.
- **Dry-run mode for the definition tool (third trial, 2).** **Partly applied.** The ceiling check is importable and needs no write. Full closure per proposal is still unverified.
- **Disclosure status (third trial, 4).** **No new evidence.** I did not call `check_disclosure` this trial.
- **Stamp every review (third trial, 1).** **Still applies.** I stamped by hand, and the harness did not enforce it.
- **Targeted check against the real tree (second trial, 1).** **Applied.** Each check ran against HEAD and the working tree.
- **Test membership against the named list (fifth trial, 3).** **Applied.** I checked forms against the term entries' `forms` field and the `word` field separately.
- **Record removal categories (fifth trial, 1).** **No new evidence.** This trial did not use the pool file.

## 6. How I was directed

**[F]** The brief named the exact clauses, and the operator's Part B mail named the forms question. Both made the checks specific.

**[F]** The operator's split instruction let me stop after Part A without ambiguity.

**[I]** The harness report's six-section form works for a second readiness review, but its section 5 suggestions are mostly restated from earlier trials. Retiring the ones already applied would shorten it.
