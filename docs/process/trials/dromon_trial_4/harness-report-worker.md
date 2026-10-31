# Harness experience report, worker line, fourth trial

Written 2026-10-30 by the worker line after the fifth agency batch and its
review fixes. Each point is marked as a fact, observed in my own turns, or
as an inference, which is my judgement and is unverified. I read my
third-trial report at `docs/process/trials/dromon_trial_3/harness-report-worker.md`
before writing this one.

## What changed since the third trial

- Fact. check_disclosure now answers against the project's term list and
  matches substrings. It helped. I checked both READMEs, both review files
  and every outgoing report through it, and did not have to read the secret
  file to clear a message. I still ran my own count of the banned
  vocabulary over the READMEs, reviews and seed books, because I could not
  tell whether the tool covers that section as well as the term list.
- Fact. Substring matching produced one false positive. A pool string, and
  the citation form I admitted in its place, contain a listed substring.
  The level-two review fails the tool on 9 lines. The operator ruled on it
  before I began, so it cost nothing beyond a sentence in each report.
- Fact. The pool was 572 strings, nearly three times the last. The
  operator asked me to stop at a consistent point if cost neared the
  limit. It did not, and the batch closed at about $6 of $40.

## 1. What worked well

- Fact. The pool stop worked as before. The withdrawal cost one filter.
- Fact. The simulation earned its cost again. Its first gate run failed on
  9 corpus violations, three forms already filed at higher levels and five
  concepts not yet taught, plus multiply. I fixed them on the copy, and the
  real tree matched it byte for byte across 21 files and two directories.
- Fact. set_brief carried the task across a compaction in the middle of
  the batch. The new session began from the brief and resumed without
  rereading the transcript.
- Fact. The fix round ran in one turn. The authoring tool accepted all
  eight wordings, and the gate passed on its first run.

## 2. What got in the way, and the workaround

- Fact. The real gate exited 1 on its reference check, because the
  operator's uncommitted brief named a trial directory that did not exist.
  Creating it would have edited `docs/process/`, which I may not do. I
  asked through ask_operator, and the operator created a placeholder. That
  cost one round trip.
- Fact. My first loop to re-record measurements deleted files for batches
  outside the stacked test and could not rewrite them. I restored them
  from the real tree and limited the loop to the fourteen stacked batches.
  This was my error, not the harness's.
- Fact. My first send_message failed with "no operator ana", because I
  used an address from the tool's example. I found the right address in
  list_sent.
- Fact. Waiting on the gate still used a bounded polling loop in Bash.
  wake_after with a task identifier was a useful backstop but does not
  wait.

## 3. What I could not see or do

- Fact. check_disclosure reports a count of lines, never the term or the
  line number. For the false positive I could confirm the count matched the
  ruled string only by reasoning, not by the tool.
- Fact. The tool allows ten checks an hour. I had three left after the
  fix round, which would not have covered a second round of drafting.

## 4. Suggestions for the harness, ranked

1. Let check_disclosure accept an allow list of strings the operator has
   ruled false positives, so a ruled file can pass rather than fail on a
   known count.
2. Add a tool that waits for a named background task with a timeout. This
   replaces polling loops.
3. State the operator's address in the turn banner. This solves guessing
   it from an example.
4. Before a line starts, check that every path named in the brief and
   condition exists. This would have caught the missing directory before
   the gate did.
5. Provide a sanctioned scratch tree with its own environment.

## 5. Earlier suggestions, revisited

- Connecting check_disclosure to the term list no longer applies. It is
  done and was useful.
- The wait tool still applies unchanged.
- The sanctioned scratch tree still applies. I again copied the tree and
  reused an edited gate script.
- A stated shell no longer applies. It stayed bash.
- Clearing stale notes is partly done. My own notes are now counted apart
  from unread, but the banner still counts four messages as unanswered.

## 6. Direction that would have made the work easier

- The rulings on the withdrawn string, the false positive and the one
  admissible sense of probe, all given before any decision, removed three
  questions I would otherwise have asked.
- Saying whether my own banned vocabulary count is still required now
  that check_disclosure is connected.
- Committing or creating every path a new brief names before the line
  runs the gate.
- Saying in advance that words already filed at a higher level stay
  there. I deferred six such words, and three more whose forms collide
  with higher entries, as separate decisions.
