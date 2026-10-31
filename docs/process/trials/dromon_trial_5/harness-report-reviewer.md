# Harness experience report, reviewer line, sixth trial

Recorded 2026-10-30. Labels: **[F]** fact from my own turns, **[I]** inference, **[H]** hypothesis.

I read `docs/process/trials/dromon_trial_4/harness-report-reviewer.md` first. Section 5 assesses each earlier suggestion against this trial.

## 1. What worked well

**[F]** The stamp worked again. I recorded HEAD `aae4abe` and the seed-book blob hashes before reading the batch, and both parts of the review state them.

**[F]** The split instruction was clear. I finished Part A, sent one message and stopped. When the operator's mail said Part B could start, I resumed from the saved Part A file.

**[F]** The operator's correction arrived with a check I could run. I tested the claim that only `organics` is in the first pool against the pool file's `pool` list, and the claim held.

**[F]** An independent recount in `$TMPDIR` matched the report's counts for three units and reproduced its ranking. This was a direct check, not a reading of the report.

## 2. What got in my way, and how I worked around it

**[F]** My earlier check of the pool file was wrong. I tested membership against the top-level keys of the JSON object rather than the `pool` list, and reported a false positive. I caught it on rerunning, before the review relied on it, and the operator's correction stood on the corrected test.

**[F]** My Part A review inferred from an unverified assumption that the seventeen strings were pool words. It was wrong for sixteen of them. I corrected this in `review.md` rather than leaving Part A as the record.

**[F]** Two wake notes requested compaction without a reason. I acknowledged each without action, as in earlier trials.

## 3. What I could not see or do

**[F]** I did not run the test suite, as directed, and I did not check definitions against source pages.

**[F]** The fourth-trial readiness report is not in the repository. Only its delta file is, so the report's list of seventeen zero-concept strings can only be checked against that delta.

## 4. Ranked suggestions

1. **Record, for each removal category, whether a removed string's sense is decided.** The problem is that the pool file records removals by category, and an admissible removal can still carry an undecided sense, which the category does not show.
2. **Keep every readiness report's source snapshot in git or cite its commit.** The problem is that the fourth-trial zero list cannot be checked against the report it describes.
3. **Test membership against the named list in any pool check.** This is a note on my own method, but the harness's tool usage could name the list field to prevent this error.
4. **Give wake notes a reason.** The problem is that compaction notes carry no cause.
5. **Keep the commit stamp on every review.** Still open from earlier trials, and handled by hand again here.

## 5. Earlier suggestions, now

- **Verifiable gate record (third trial, 3).** **Still applies.** I did not run the gate, so the commit's status is unchecked.
- **Dry-run mode for the definition tool (third trial, 2).** **Partly applied.** The ceiling check is importable and needs no write. Full closure per proposal is still unverified.
- **Disclosure status (third trial, 4).** **No new evidence.** I did not call `check_disclosure` this trial.
- **Stamp every review (third trial, 1).** **Still applies.** I stamped by hand, and the harness did not enforce it.
- **Targeted check against the real tree (second trial, 1).** **Applied.** The recount and the membership test both ran against the tree.

## 6. How I was directed

**[F]** The brief named the fourth-trial report as the comparison, and I could open it directly. That made the zero-list check possible.

**[F]** The operator's correction gave a specific check and a specific wording for the review. That made the fix quick and avoided a dispute.

**[I]** Splitting a trial over two operator turns worked, but a line that stops after Part A depends on the operator's next message arriving promptly.
