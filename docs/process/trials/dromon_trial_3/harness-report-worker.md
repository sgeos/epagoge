# Harness experience report, worker line, third trial

Written 2026-10-29 by the worker line after the fourth agency batch. Each
point is marked as a fact, observed in my own turns, or as an inference,
which is my judgement and is unverified. I read my second-trial report at
`tmp/dromon-trial-2/harness-report-worker.md` before writing this one.

## What changed since the second trial

- Fact. The task mail named the rule not to run uv in the scratch copy.
  That was the direction my last report asked for, and the uv detour of
  the second trial did not recur.
- Fact. The batch was split at the pool. I sent the pool list, ended the
  turn, and the next turn began with the operator's withdrawals. In the
  second trial a withdrawal arrived after admission, and I rebuilt the
  whole batch from the committed state on a second copy. This time the
  withdrawal cost one filter of the pool file.
- Fact. Two tools appeared. I used set_brief at the pool stop.
  check_disclosure appeared in the follow-up of 2026-10-29. I called it on
  the follow-up README, and it answered that this project has no
  disclosure list.
- Fact. The follow-up ran in one turn, through the gate. The tool refused
  the reviewer's wording for meteor because streak is not admitted, and I
  substituted a nearer word and recorded why.
- Fact. Between turns the shell changed from bash to zsh. My first
  command of the follow-up failed because zsh read a line of equals signs
  as a command.

## 1. What worked well

- Fact. The simulation earned its cost again. The first gate run on the
  copy failed on four verbs that the corpus validator requires to be
  classified for consonant doubling. I fixed the source table, reran the
  copy, and the real gate passed on its first run. The real tree matched
  the copy across 37 files.
- Fact. The admission tool's refusals were precise. It reported 48
  problems in my first draft of 151 definitions, each naming the word
  outside the level, and one cycle between crayon and wax. Three rounds
  cleared them.
- Fact. Reusing my scratch staging script reduced staging to a few
  constant changes.

## 2. What got in the way, and the workaround

- Fact. Without a usable disclosure check, I parsed the banned vocabulary
  section of the secret file in a script and counted hits in the staged
  records without printing any term. Inference. That proves absence only
  for the files I chose to scan, and it required reading the file.
- Fact. A foreground loop of thirteen measurement checks exceeded the two
  minute limit and was moved to the background. I then polled its output
  file. Waiting on the gate used the same bounded polling loop as before.
- Fact. Self-scheduled compaction notes arrived as unread mail in later
  turns, and the banner still counts three messages as unanswered.

## 3. What I could not see or do

- Fact. I could not check text against the project's term list through
  the harness, because check_disclosure has no list for this project.
- Fact. I could not tell from the prompt that the shell had changed until
  a command failed.
- Fact. I still see cost only as the running estimate in the banner, so I
  cannot attribute it to steps such as the three dry runs.

## 4. Suggestions for the harness, ranked

1. Connect check_disclosure to the project's term list and banned
   vocabulary. This solves reading the secret file to prove that a
   message or record is clean.
2. Add a tool that waits for a named background task with a timeout.
   This replaces polling loops.
3. Provide a sanctioned scratch tree with its own environment. The
   operator's rule prevents the uv hazard, but every line must still copy
   the tree and edit its gate script by hand.
4. State the shell at turn start, or keep it fixed across turns. This
   solves commands that fail on a changed interpreter.
5. Clear self-scheduled notes once a line has acknowledged them, and
   count instructions apart from questions in the unanswered total.

## 5. Earlier suggestions, revisited

- The sanctioned scratch copy still applies, with the hazard now covered
  by direction rather than by the harness.
- The wait tool still applies unchanged.
- The term-list check exists in name only for this project, so it still
  applies in effect.
- Clearing stale notes still applies. Fact. Compaction notes recurred.
- Reporting the network policy no longer applies. No command of mine
  needed the network.

## 6. Direction that would have made the work easier

- Stating whether a term's source string should say public domain when
  the brief records that status as unchecked. I dropped the phrase and said
  so in the README and the report.
- Stating whether new kinds of deferral are acceptable. I deferred trade
  names, clipped forms, and a superlative whose admission would change an
  earlier entry, each as a separate decision left open.
- In the follow-up, saying whether the batch's own admitted and review
  records should carry revised definitions. The handoff's workflow covers
  provenance only, so I followed the second batch's precedent.
- Naming the test module. The reviewer suggested one that does not exist,
  and the nearest fit was the vocabulary tests.
