# Harness experience report, reviewer line, fifth trial

Recorded 2026-10-30. Labels: **[F]** fact from my own turns, **[I]** inference, **[H]** hypothesis.

I read `docs/process/trials/dromon_trial_3/harness-report-reviewer.md` first. Section 5 assesses each earlier suggestion against this trial.

## 1. What worked well

**[F]** The stamp at the start worked. I recorded HEAD `aae4abe` and the four seed-book blob hashes before reading the batch. Both review files state what they read.

**[F]** Operator mail arrived as a split instruction. I did Part A, sent one message, and stopped. When the operator's later mail said Part B could start, I resumed without re-reading Part A.

**[F]** The ceiling check ran without writing tracked files. Importing `epagoge.vocabulary.unlicensed` and checking each proposed wording let me test eight replacements, and four were rejected in one pass. Each rejected word was named in the output, which made the next wording quick to find.

**[F]** Part B's sheet could be checked by grep. An independent grep of the seed book matched the sheet for three concepts, entry for entry.

## 2. What got in my way, and how I worked around it

**[F]** The closure tool's usage line says `<book-dir>`, not `<level>`. Passing the parent directory reported 0 of 849 defined, with no error. I found the right form by reading the tool's source and reran the three levels.

**[F]** My first parse of the readiness script's output dropped units. The script prints one row per unit and a second block of summary lines. My parser read both blocks, so the ranking came out wrong. I compared it with the script's own summary and used that instead, which narrowed my ranking check to the top five.

**[F]** Two wake notes asked for a context compaction without saying why. I acknowledged each without action, since the session had already compacted. The notes were accurate but gave me no reason to act.

**[F]** A baseline blob named in luna's delta is absent from the repository, so `git cat-file` failed. I recomputed the gains against the committed blob, which matched every concept I checked.

## 3. What I could not see or do

**[F]** I could not see the worker's snapshot. The delta's baseline is untracked, so I could not check its counts against the source it used.

**[F]** I could not run the test suite, by instruction, so the batch's tests are unverified.

**[F]** I could not see my own earlier readiness report's state at its writing time. My trial-four counts were taken during the worker's edits, and I had to correct my own record in this trial.

**[I]** I could not confirm which commit a reviewer's stamp refers to unless the stamp is written in the review. The stamp I wrote is accurate, but nothing in the harness enforces it.

## 4. Ranked suggestions

1. **Put the call form in the tool's usage line and the batch README.** The problem is that `validate_closure.py` accepts a directory of one level, and a wrong argument silently reports zero coverage.
2. **Keep a baseline snapshot in the repository or record its commit.** The problem is that luna's delta cites a blob absent from history, so the comparison cannot be reproduced from git.
3. **Make readiness scripts print a single machine-readable block.** The problem is that rows and summary lines share stdout, so a reader must guess which lines are which.
4. **Give wake notes a reason field.** The problem is that "requests a context compaction" carries no cause, so a line cannot tell whether the request matters.
5. **Keep the commit stamp on every review.** The problem from the third trial is still open, although this trial's stamp was written by hand.

## 5. Earlier suggestions, now

- **Verifiable gate record (third trial, 3).** **Still applies.** I did not run the gate, as directed, so the commit's status is unchecked.
- **Dry-run mode for the definition tool (third trial, 2).** **Partly superseded.** The ceiling check is importable, so I did not need a write. Full closure per proposal is still unverified, so the request still stands for that check.
- **Disclosure status (third trial, 4).** **No new evidence.** I did not call `check_disclosure` this trial.
- **Stamp every review (third trial, 1).** **Still applies, now self-applied.** I stamped by hand, and the harness did not enforce it.
- **Targeted check against the real tree (second trial, 1).** **Applied.** The grep cross-check of the sheet was that check.

## 6. How I was directed

**[F]** Requiring a HEAD and blob stamp before the review was useful, and it caught the commit movement without my having to ask.

**[F]** The split between Part A and Part B was clear. The instruction to stop after Part A and wait made the handoff unambiguous.

**[I]** The brief gave the closure check's inputs but not its command, so I had to search the tool. A line naming the exact call would have saved one turn.

**[I]** The request to check "every definition" in a batch of 480 is more than one turn can do well. I checked all of them against the ceiling and sampled the sense of each by reading, which is a narrower claim than checking each against its source.
