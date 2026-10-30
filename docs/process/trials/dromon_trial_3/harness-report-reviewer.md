# Harness experience report, reviewer line, fourth trial

Recorded 2026-10-29. Labels: **[F]** fact from my own turns, **[I]** inference, **[H]** hypothesis.

I read `tmp/dromon-trial-2/harness-report-reviewer.md` first. The follow-up review of 2026-10-29 is `tmp/dromon-trial-3/review.md`. Section 5 assesses each earlier suggestion against both.

## 1. What worked well

**[F]** The worktree was at `80ff5cd`, a commit that had moved since my earlier turns. Git log and status showed the changes, so I could separate the fourth batch from the committed third. The daemon's note let me catch this without guessing.

**[F]** The fourth review used the same structure as the third. Each completion clause mapped to one command, and the commands ran without prompts.

**[F]** The ceiling check ran without writing tracked files. I imported `epagoge.vocabulary.unlicensed` and called it on each proposed wording, which is the check the generator itself applies. This let me test proposals without running `tools/author_definitions.py`.

**[F]** The readiness script ran with `-I`, and its output could be checked by hand. Three units were recounted with `grep`, and the vocabulary cross-check exposed a one-headword difference.

## 2. What got in my way, and how I worked around it

**[F]** A shell echo of `=====` produced "not found" in two calls. I separated output with a scratch file and reran the command without echo separators.

**[F]** My first attempt at the ceiling check passed a string where the function needed a path. The error was clear, and I fixed it in one edit.

**[F]** My word count for the review was 1,446, over the 1,300 limit. I trimmed it in two edits to 1,277. I made the first cut too small and had to make a second.

**[F]** `tools/author_definitions.py` writes to tracked files when all entries pass. The instruction to check proposals "without writing tracked files" ruled it out. I used the lower-level ceiling check, which proves less. The full closure check for each proposal is therefore unverified.

**[F]** The readiness report's counts were stale when I ran it. The worker was still editing. I reported the stale values with their rerun values, rather than deciding which was current.

## 3. What I could not see or do

**[F]** I could not verify closure for each proposed definition without writing. A dry-run mode for `tools/author_definitions.py` would have solved this.

**[F]** I could not see the worker's intermediate counts, so I could not tell which of the report's numbers were stale at writing time. A timestamp on the source data would have fixed that.

**[F]** I could not run the gate, by instruction. The daemon's note said the daemon could not check whether my worktree's commit moved between turns. My earlier reviews may therefore describe a tree that no longer exists, and no record linked each review to a commit.

**[F]** `mcp__dromon__check_disclosure` reported "this project has no disclosure list" on the third trial. I could not confirm the disclosure status of my own reports, so I wrote them without that check.

## 4. Ranked suggestions

1. **Stamp every review with its commit and time.** The problem is that the third and fourth reviews describe trees that moved. A commit and time on each review would let an operator tell which state was reviewed.
2. **Offer a dry-run mode for the definition tool.** The problem is that proposals cannot be closure-checked without writing tracked files. A dry-run would solve this without a write.
3. **Record the worker's gate result with its commit.** The problem persists from the first trial: a reviewer must trust or rerun. A record tied to the commit would remove both costs.
4. **Give the disclosure check a clear status.** The problem is that "no disclosure list" was reported without saying whether the project should have one. A missing list should be a named state.
5. **Timestamp the source counts in readiness reports.** The problem is that the report's numbers went stale while I read them.

## 5. Earlier suggestions, now

- **Verifiable gate record (first trial, 1).** **Still applies.** Item 3 above is the same request.
- **Budget at task start (first trial, 2).** **No longer applies in this trial.** The limits were stated in the mail, and the notice showed the count from zero.
- **Negative-control fixture for pattern scans (first trial, 3).** **Still applies in part.** The disclosure tool now exists, but reports no list, so the fixture question is open.
- **Denial reasons (first trial, 4).** **No new evidence.** No denial occurred this trial.
- **Model and lease state (first trial, 5).** **Partly addressed.** Lease tools exist. Model load state is still not visible to me.
- **Targeted check against the real tree (second trial, 1).** **Still applies.** The dry-run in suggestion 2 is a form of this.

## 6. How I was directed

**[F]** The brief named the tool, the file, the limits, and the forbidden actions. That kept the work on course.

**[I]** The instruction to check proposals "without writing tracked files" was clear. It also excluded the tool the worker used, so it was the single largest constraint on Part A.2. A sentence naming a non-writing alternative would have helped.

**[I]** The request for "every admitted definition" in a batch of 169 is large for one turn. A request for every definition in a stated sample, with a reason, would be easier to meet well.
