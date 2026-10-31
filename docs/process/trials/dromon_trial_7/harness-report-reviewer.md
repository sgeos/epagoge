# Harness experience report, reviewer line, seventh trial

Recorded 2026-10-30. Labels: **[F]** fact from my own turns, **[I]**
inference. This trial ran the reviewer on the Fable model. The earlier
reports ran on Haiku.

I read `docs/process/trials/dromon_trial_6/harness-report-reviewer.md`
first. Section 5 assesses its suggestions against this trial.

## What changed since the sixth trial

**[F]** The batch was 607 strings against a few dozen, so the review was
script-first. One script verified all 480 admissions against five files, a
second built a source concordance for 71 hand-checked strings, and a third
reproduced luna's two tables cell by cell.

**[I]** I cannot measure the model change from inside one line. Two
observables differ. The Part A review ran to about 2,500 words against the
sixth trial's 930 for both parts, and my first script's failures were in
my own assumptions rather than in the batch. Either could be the batch
size rather than the model.

## 1. What worked well

**[F]** Background tasks. The 727-test run took 102 seconds and pyright
longer, and both ran as tracked background tasks that woke me on exit. I
did other checks meanwhile.

**[F]** The brief survived compaction. My context reached the warning
during Part A, the harness compacted it, and the next turn opened with the
brief I had set, including the stamp and the three open findings. I
resumed Part B from it without rereading the batch.

**[F]** The Part A and Part B split by operator mail worked as in the sixth
trial. The Part B mail also told me not to re-review the batch, which
removed an ambiguity about the worker's parallel edits.

**[F]** Luna's scripts reran bitwise. Both tables matched the reruns in
every cell, so the readiness check was a test rather than a reading.

## 2. What got in my way, and how I worked around it

**[F]** The first version of my check script reported 17 failures and 14
were its own. It compared part-of-speech strings by order where the admit
tool sorts them, matched past-tense decision words in reasons against the
present-tense decision field, and did not parse the wording for a form of a
second sense. I fixed each and kept the three real findings.

**[F]** The closure validator takes the vocabulary path first. The brief's
example omitted it and the tool failed with an unhelpful error.

**[F]** A GNU option to `ls` is not on macOS, which broke a chained command
so one rerun silently did not happen. I reran it alone.

**[F]** A `cd` inside a compound command changed the working directory for
later calls, which the environment reported. I returned explicitly.

**[F]** No Write or Edit tool was offered. I used write_scratch and, for
in-place corrections, a Python heredoc.

## 3. What I could not see or do

**[F]** The teacher clause. The line rules forbid calling the address, so I
verified only that authoring.json records no teacher.

**[F]** The full gate, as directed. The coverage floor, graph and corpus
validation and the disclosure scan were not run by me.

**[F]** The worker's fixes to findings F1 to F3, which landed after my
stamp and during Part B. I stamped the vocabulary blob before every
command so the review states what it measured.

## 4. Ranked suggestions

1. **Offer an in-place edit tool to lines.** The problem is that
   correcting one line of a report needed a Python heredoc, which is easy
   to get wrong and hard to audit.
2. **Do not charge an autonomous turn for a compaction wake.** The problem
   is that the compaction note opened a turn with nothing to do, and the
   turn counted against the limit.
3. **Reset the working directory between Bash calls.** The problem is that
   a `cd` inside one command silently moved later commands.
4. **Have tools reject a wrong first argument with a usage line.** The
   problem is that the closure validator reported a directory error when
   the vocabulary path was missing.
5. **Enforce the stamp.** Still open from the third trial. All three lines
   stamped by hand and matched, but nothing checked that they did.

## 5. Earlier suggestions, now

- **Sixth trial 1, scope every readiness heading.** **Applied.** Luna's
  delta report says it counts term entries at levels one and two.
- **Sixth trial 2, record the counting rule for forms.** **Applied.**
  The stripped-forms report states exactly what a listed form is.
- **Sixth trial 3, name the source file in every count script.**
  **Applied.** Both reports name the file and the command.
- **Sixth trial 4 and third trial 1, stamp each review.** **Still
  applies.** Done by hand again.
- **Sixth trial 5, give wake notes a reason.** **Applied.** This trial's
  compaction note stated the token count that caused it.
- **Third trial 3, verifiable gate record.** **Still applies.** I did
  not run the gate.
- **Third trial 2 and 4, dry-run mode and disclosure status.** **No new
  evidence.**

## 6. How I was directed

**[F]** The brief fixed the sample by line number, so it could not drift
toward easy strings.

**[F]** The brief said "two omitted admissible strings" without saying by
which filter. I chose one from each omission category and said so.

**[I]** Knowing before Part B that the worker would edit the tree in
parallel would have let me plan the stamping, rather than discovering it
from the operator's mail.
