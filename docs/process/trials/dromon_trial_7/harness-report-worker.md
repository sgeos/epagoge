# Harness experience report, worker line, seventh trial

Written 2026-10-30 by the worker line after the long-tail batch and the
Part A fix round. Each point is marked Fact, observed in my own turns, or
Inference, which is my judgement and is unverified. I read
`docs/process/trials/dromon_trial_6/harness-report-worker.md` first.

## What changed since the sixth trial

- Fact. keydiff.py met the need I described, a by-key diff of generated
  files against the last commit. I ran both commands in the copy and in the
  tree, before and after the fixes, and each time they reported 0 changed
  and 0 removed. The reviewer got the same numbers.
- Fact. It meets the need only in part. It compares against HEAD, and the
  fourth to sixth trials are uncommitted, so its 980 added terms cannot
  separate this batch from the earlier ones. The reviewer noted the same
  limit.
- Fact. check_disclosure now takes several paths. I checked the README and
  both review records in one call.
- Fact. After compaction and later an idle close, I resumed from the
  standing brief without asking.

## 1. What worked well

- Fact. Checking the tree before acting caught a wrong premise. Item 3 of
  the fix mail said an earlier batch decided translate. No earlier
  review.json names it. I asked with three options, applied the other three
  items in the copy meanwhile, and the answer chose my recommendation.
- Fact. The simulated copy caught five words filed under two untaught
  concepts before the tree was touched.
- Fact. author_definitions.py served as a checked write path. All five new
  definitions passed licensing and grounding on the first attempt.
- Fact. `rsync -rcn` showed exactly the nine files the fixes should touch,
  and the gate passed on its first run.

## 2. What got in the way, and the workaround

- Fact. `ps` is not permitted and list_processes refuses on this platform,
  so I could not tell whether my chain was still running. I read the tail
  of its log instead.
- Fact. When the translate answer arrived mid-run, its edit would change
  hashed batch files, so I stopped the chain and ran it again in full.
- Fact. My batch script rebuilds the copy from the tree and admits the
  batch, so it cannot run once the batch is applied. I wrote a targeted
  fix script instead, which is a second path to keep correct.
- Fact. The batch brief required the gate inside the turn, so I again
  waited with a bounded Python loop. Process substitution and `timeout` are
  still unavailable.
- Fact. The batch of 607 strings took my context to about 348,000 tokens,
  past the warning of 150,000, before compaction ran in the next turn.

## 3. What I could not see or do

- Fact. No tool answers which batch decided a word. I searched every
  review.json by hand. Inference. The premise error suggests the same gap
  on the operator's side.
- Fact. I could not see my own processes, as above.
- Fact. review.md, the combined review, records that translates is
  deferred. That was the first decision, which the operator later replaced
  with widening translate. The two records now disagree.

## 4. Suggestions for the harness, ranked

1. A lookup of every review decision on a word or form across batches,
   open to lines and the operator. This would have prevented the item 3
   question and replaces my repeated searches.
2. Let keydiff take a saved base, such as a snapshot taken before a batch,
   or print the added keys. This isolates one batch while earlier ones are
   uncommitted.
3. Process visibility on this platform. This answers whether a long run is
   alive without reading its log.
4. A blocking wait on a background task inside a turn. This removes
   polling loops when the gate must pass in the same turn.
5. A sanctioned snapshot before a batch is applied. This lets the full
   pipeline be rerun for fixes, not a second, hand-written path.
6. A notice inside a long turn when context passes the warning. This
   would let a line set its brief and stop at a clean point.

## 5. Earlier suggestions, revisited

- The by-key diff is met by keydiff.py, with the base limit above.
- Several paths for check_disclosure is met. Its description now says it
  covers one list configured for the project.
- The blocking wait still applies, for the same reason as before.
- The sanctioned scratch tree still applies, and now also covers reruns.
- Clearing stale notes is met in part. The banner counts my own notes
  apart from unread mail.

## 6. Direction that would have made the work easier

- Fact. The fix mail gave exact wordings and a fallback rule for a wording
  that failed closure. That made the round a single pass.
- Fact. The batch brief named both keydiff commands and the outcome they
  must show, which gave a clear acceptance check.
- Inference. A fix mail that cites the record behind each premise, such as
  the batch that decided a word, would let a line verify it in seconds.
- Inference. A rule in advance for strings attested only in titles of
  linked pages would have removed my largest judgement call. I applied the
  fifth pass's interface rule, which defers some common words.
