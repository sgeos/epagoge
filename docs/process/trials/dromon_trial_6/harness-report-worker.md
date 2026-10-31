# Harness experience report, worker line, sixth trial

Written 2026-10-30 by the worker line after the stripped-forms batch, the
second-sense tool change and the review fix round. Each point is marked as
a fact, observed in my own turns, or as an inference, which is my judgement
and is unverified. I read `docs/process/trials/dromon_trial_5/harness-report-worker.md`
before writing this one.

## What changed since the fifth trial

- Fact. The fix mail named the review file under `tmp/dromon-trial-7/`, and
  I read the findings myself. Last time the operator relayed a finding.
- Fact. wake_after accepted a task identifier, so a background task could
  end my turn and wake me when it finished.
- Fact. My engine session was compacted mid-trial, from about 207,000
  tokens to about 15,000. The new session led with my standing brief, and
  I resumed without asking anything.
- Fact. The work was larger, a tool change, a question and a fix round,
  at about $9.40 of the $40 limit.

## 1. What worked well

- Fact. ask_operator handled the one real block. Neither tool could file
  a second sense. I asked with lettered options, and the answer chose one,
  widened my write scope to tools and tests, and gave a stopping rule.
- Fact. The simulated copy caught two failures before the real tree was
  touched. The verb color needed a doubling entry, and the stacked test
  owed headword growth for every second sense.
- Fact. The real gate caught three unresolved references in the README.
- Fact. The review found three defects my gate passed. A second sense
  overwrote three words' provenance. The closure gate never read two
  second-sense records. The verb flood had no use in the sources. Each was
  fixed in one turn, and the gate passed on its first run.
- Fact. A probe showed every existing dictionary record passed the
  stricter closure rule before I enforced it.

## 2. What got in the way, and the workaround

- Fact. A scratch script named inspect.py shadowed the standard library
  module and broke the run. I renamed it. This was my error.
- Fact. Process substitution again failed on `/dev/fd`, and `timeout` is
  not installed. I compared JSON in Python instead.
- Fact. The operator required the gate to pass inside the turn, which a
  task wake cannot do, so I waited with a bounded Python loop.
- Fact. I checked every batch measurement for staleness and found many
  older ones failing. They had been stale before this trial, and the
  stacked test does not cover them. I stopped the loop and re-recorded
  only the 17 that the test covers.

## 3. What I could not see or do

- Inference. My tool change missed provenance and closure because I
  extended the tools that blocked me and did not search for every
  consumer that keys a sense by its word. Nothing in the harness would
  have shown me those consumers. The reviewer found them by diffing
  generated files against the last commit.
- Fact. Nothing told me which recorded measurements are expected to pass.
  I learned it from the stacked test's source.
- Fact. check_disclosure still does not say which lists it covers, so I
  again counted banned terms in my own script.

## 4. Suggestions for the harness, ranked

1. A blocking wait on a named background task, with a timeout, inside a
   turn. This removes polling loops when the gate must pass in the same
   turn.
2. A view of how generated files differ from the last commit, by key. This
   would have shown the provenance overwrite before review did.
3. Let check_disclosure take several paths, and state its lists. This
   removes combined scratch files and the second scan by hand.
4. A sanctioned scratch tree with its own environment. I again copied the
   tree and edited the gate script to skip uv.
5. Clear or summarise stale notes. The banner now counts 90.

## 5. Earlier suggestions, revisited

- The wait tool applies in part. The task wake meets it between turns but
  not within one.
- Letting a line read review findings on its own work no longer applies.
  The fix mail named a readable file.
- The disclosure suggestion still applies unchanged.
- The sanctioned scratch tree still applies.
- The operator's address in the banner applies to new lines only.
- The allow list for ruled false positives did not arise this time.
- Clearing stale notes still applies, and the count has grown.

## 6. Direction that would have made the work easier

- Inference. Saying in the first brief that a second sense was likely, and
  that tools and tests could be edited, would have saved one round trip.
  A string like wells could only be read correctly as a second sense.
- The fix mail was the clearest direction of the trial. It gave each
  finding a decision, an acceptable alternative for provenance, and a check
  to run, namely that git diff shows no other word's provenance changed.
- A note on which recorded measurements the gate covers would have saved
  the full staleness pass.
- Fact. The instruction to stop at a consistent point with the gate
  passing, if cost ran short, made it safe to take on the tool change.
