# Harness experience report, worker line, fifth trial

Written 2026-10-30 by the worker line after the sixth agency batch and its
review fix. Each point is marked as a fact, observed in my own turns, or as
an inference, which is my judgement and is unverified. I read my
fourth-trial report at `docs/process/trials/dromon_trial_4/harness-report-worker.md`
before writing this one.

## What changed since the fourth trial

- Fact. The task mail said every path the brief and condition name already
  exists. The real gate passed on its first run, and the reference check
  cost no round trip. My fourth suggestion of last time was met by
  direction rather than by the harness.
- Fact. I addressed the operator correctly at once, from the last trial.
- Fact. The engine session was new at the start of this trial. It led with
  my standing brief and said that operator mail had arrived since the
  brief was set, which told me at once that the brief was stale.
- Fact. The batch was small. The pool held 28 strings, and the batch with
  its fix cost under $3 of the $40 limit.

## 1. What worked well

- Fact. The pool stop caught a wrong inference. My pool message guessed
  why the pool held 28 rather than 80. The operator asked me to check
  before deciding, and the check showed that 50 of the 80 had been
  reviewed as forms in the first pass, one came from a later headword, and
  one passes by suffix stripping alone. The README records the accounting
  rather than my guess.
- Fact. Reusing the fifth batch's scratch scripts kept staging short. I
  adapted the staging script by string replacements that each asserted a
  single match, so a stale constant could not survive silently.
- Fact. The simulated gate passed on its first run. A checksum dry run of
  rsync listed exactly the 34 files the batch should touch before I copied
  them, and a second dry run listed none after.
- Fact. The fix round ran in one turn. The authoring tool accepted the
  reviewer's wording, and the gate passed on its first run.

## 2. What got in the way, and the workaround

- Fact. A diff using process substitution failed with "Operation not
  permitted", because the sandbox refuses `/dev/fd`. I diffed the files
  directly.
- Fact. In the copy I deleted the provenance file before regenerating it,
  as the measurement tool requires for its own output. The provenance tool
  reads the old file and failed. I restored it in the copy. This was my
  error, and the real tree was not affected.
- Fact. check_disclosure allows ten checks an hour. I combined both
  READMEs and both reviews into one scratch file to check them with one
  call.
- Fact. Waiting on the gate still used a bounded polling loop in Bash.

## 3. What I could not see or do

- Fact. I could not see the reviewer's concern about 17 strings directly.
  The operator checked it against the first pool and told me the result.
  Inference. A shared view of review findings addressed to the worker
  would have let me answer it without the operator's time.
- Fact. The brief directs me to read the banned vocabulary section of the
  secret file, and I did. check_disclosure does not say whether it covers
  that section, so I still counted banned terms in my own script.

## 4. Suggestions for the harness, ranked

1. Add a tool that waits for a named background task with a timeout. This
   replaces polling loops, which every gate run in this trial used.
2. Let check_disclosure accept several paths in one call, or state which
   lists it covers. This solves combining files to save checks and running
   a second scan by hand.
3. State the operator's address in the turn banner. This solves guessing
   it on a line's first trial.
4. Let a line read review findings that concern its own work. This solves
   the operator relaying a question that the worker could answer.
5. Provide a sanctioned scratch tree with its own environment.

## 5. Earlier suggestions, revisited

- The allow list for ruled false positives does not apply this time.
  There was no false positive in this batch, but the need will return with
  the next substring match.
- The wait tool still applies unchanged.
- The operator address in the banner still applies.
- Checking that named paths exist no longer applies in practice. The
  operator now ensures it before the line starts.
- The sanctioned scratch tree still applies. I again copied the tree and
  reused an edited gate script.
- Clearing stale notes still applies in part. The banner counts 62 of my
  own notes and four unanswered messages.

## 6. Direction that would have made the work easier

- The instruction to defer or exclude Spanish and page interface strings
  as in the fifth batch settled nine decisions before I began.
- The instruction to confirm my inference before deciding was the most
  useful direction of the trial, because the inference was wrong.
- Saying whether a batch drawn again from an older scan should repeat that
  scan's public domain claim. I followed the fifth batch and dropped it,
  and recorded the difference.
