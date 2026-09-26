# Process Strategy

**Written 2026-09-25**, after reviewing the process documents of the
operator's `keleusma` repository, which was this project's reference when
it was set up and has moved a long way since.

This document holds what is **durable**. `CURRENT_BRIEF.md` holds what is
current and is deleted when its completion condition is met, which is why
the lessons below were moved out of it: a list of failure modes filed in a
document marked for deletion is a list that will be deleted.

## Engineering classification

**Research project.** Claims are provisional until measured. The cost of
being wrong is not a crash but a published result that does not replicate,
so the rigour goes into measurement and into saying what has not been
measured, rather than into uptime.

## Verification

**There is one tier, and that is a property of this project rather than a
preference.** The full gate is twenty checks and takes about nine seconds.
Continuous integration takes about a minute. The reference repository
maintains three tiers because its gate takes two and a half hours and its
continuous integration about an hour, which makes the choice of what to
run a real cost. Here it is not, so **run the whole gate every time** and
do not build a fast path whose existence invites skipping the slow one.

**Run the gate, read its exit code, then stop before committing.** Three
commits have landed on a red gate, every one of them because the gate ran
and the commit ran in the same breath. Reading the exit code is not the
control. Not issuing the commit is.

**Continuous integration is NOT a strict superset of the local gate here,
and that inverts the usual advice.** The disclosure scan reads a pattern
this repository does not contain, so on a runner it announces a skip
and returns success. The local gate is therefore load-bearing and cannot be
trimmed. The reference repository can treat its continuous integration as
the authority because containment was checked step by step; this project
cannot, because one check is structurally unable to run there.

**Check continuous integration separately.** A green local gate has twice
meant nothing about the remote one, once for a missing virtual environment
and once for a shallow clone breaking a check derived from history.

**A guard that has not been shown able to fail is not a guard.** Every
check added to the gate is shown failing against a deliberately broken
input before it is trusted. The reference checker was shown failing on an
invented path before it was wired in.

## Failure classes this project actually produces

Each of these has happened here, more than once, and each read as success
at the time. That is what makes them worth naming rather than fixing case
by case.

**Silent partial coverage.** A book ordering that covered thirteen of a
hundred and forty-six. A chunker that kept a quarter of the corpus. A
generator that skipped seven domains. Nine front-matter builders that
would each have erased a field added later. **A tool that returns less
than it was asked for must say so.**

**A CHECK SCANS THE SET IT WAS GIVEN, WHICH IS RARELY THE SET THAT
MATTERS.** The disclosure scan read `git ls-files`, so a new document was
invisible until its first commit and the gate that ran before that commit
could not see it. **Two documents carrying banned vocabulary were committed
and pushed to a public repository with a green gate on either side.** It
also matched line by line, so a banned multi-word phrase wrapped across a
line break was invisible; two files had been carrying one for days, one
since before publication. Both were closed on 2026-09-25. Before trusting
a check, ask what it enumerates and whether the thing you fear would be
inside that set.

**A METRIC COMPARED AT A FIXED TEMPERATURE MEASURES SHARPNESS, NOT
QUALITY.** Distinct-token share and attractor frequency were read as
quality signals when comparing two models. Swept across temperatures, the
better-fit model is less varied at every one and recovers past the worse
model's figure by 1.2, and its attractor frequency falls from 24 to 3 as
temperature rises. **A better model has a sharper distribution**, so at
fixed temperature it looks more repetitive. Neither figure can separate a
worse model from a sharper one. Compare across temperatures or not at all.

**A tool that is right for one job is wrong for another that looks like
it.** `fold_typography` maps a dash to a hyphen because the tokeniser must
split words consistently and never shows the result to anyone. Used on
back-cover prose it turned `things down—like notes` into `down-like`, and
damaged **99 of 246 descriptions** before it was caught. The corpus
validator being more permissive than the lexicon is the same class.

**A COMPARISON IS ONLY AS GOOD AS WHAT IT HOLDS FIXED, and this project
has now got that wrong twice in one day, in two different ways.**

- **A loss figure is comparable only to one measured against the same
  held-out set.** Each sweep holds out the last eighth of its own chunk
  list, so a corpus that has grown holds out different material. Comparing
  across two sweeps produced a scaling rate of 0.199 and a worry that
  filling books added low-value tokens. Measured against one held-out set,
  the same doubling bought 0.316, the largest increment in the series.
- **Sampling one seed across different prompts measures the seed, not the
  prompt.** Six prompts at `--seed 1` all began with `was`, which was
  recorded as a learned trigger on the question mark and shown to the
  teacher as a measurement. Over eight prompts at eight seeds the same
  checkpoint begins with `was` once. **The teacher then built a theory on
  it**, which is what a fabricated regularity costs downstream.

Both read as findings. Neither was. **Before reporting a difference, say
what was held fixed and check that it was.**

**A by-name list is correct the day it is written.** Prefer a pattern that
matches to an enumeration that remembers. `curriculum/books/level_*/exclude/*`
in `.gitignore` covers a level that does not exist yet; a line per level
would not. A hand-written bound is the same defect wearing different
clothes.

**A metric that cannot fail measures nothing.** The corpus once reported
one hundred percent of sampled tokens admissible, which was true by
construction because the tokeniser is built from the lexicon. Before
reporting a figure, ask what value would have been alarming.

**Two numbers that should differ.** A token count was overstated by a
quarter by reporting the sum of chunk identifiers as the corpus size. The
two quantities were both available and neither was labelled.

**A check more permissive than the thing it guards.** The corpus validator
accepted a word by stripping suffixes while the tokeniser did not, so
eleven forms reached books in shapes the lexicon does not carry. A
generation-time check must ask the question the consumer asks.

**Unblocking is not authoring.** Fifty-one concepts were made authorable
and no book was written. Reporting enabling work as delivery is the error
the concept record exists to avoid.

**A destructive tool's input format is not what you assume.** A
`git-filter-repo` replacement file has no comment syntax. A comment line
in one replaced every `#` in every file in history. Read the format, take
a mirror clone first, and verify the head tree hash afterwards.

## Autonomy boundaries

**Proceed** without asking on anything bounded and already on the roadmap.
Choosing among bounded tasks is not a fork. Cost asymmetry between
candidates is an ordering input, not a decision point.

**Stop and ask** when a decision would change what the curriculum claims,
when an action is irreversible or outward-facing, when the answer requires
information only the operator holds, or when a budget is reached.

**The operator holds** the endpoint and estimator that fix the sign of any
ordering result, the licensing questions, the schedules for levels three
to seven, and anything under `sources/`. These are listed in the handoff
and are not the loop's to settle.

**A prior authorisation does not extend to the next outward-facing
action.** Publishing, deleting, force-pushing, and tagging are each asked
for separately.

## Ordering work

**Minimise context switching first, then take the higher-value task.**
Several increments in one area is cheaper and less error-prone than
alternating. Switch only when the area is exhausted.

**Finishing beats starting.** A fill run that spends its budget on new
books leaves the short ones short.

## The record

**Corrections are kept in place.** A wrong claim in a pushed commit is
corrected by the next commit, not amended away. `CHANGELOG.md` is exempt
from the reference check for the same reason: an entry naming a file
deleted afterwards is historical, not wrong.

**Do not describe a property the tree does not have yet.** This has been
caught twice, both times by checking rather than by remembering.

**Bounded currency matters more than bounded size.** The reference
repository split one channel in two when it reached 362 KB and watched the
replacement accrete back to the same shape, because sessions prepend
rather than rewrite. The property worth defending is that a reader can
tell what is true **now**. `HANDOFF.md` is rewritten rather than
prepended, and it opens with a validity check to be run before any of it
is believed.

## What was deliberately not adopted from the reference repository

Recorded so that the omissions read as decisions rather than oversights.

**The release-branch model**, with a version branch, feature branches, and
no-fast-forward merges. This project has one operator, commits directly to
`main`, and has no releases. A branch is cut when a change might turn the
gate or continuous integration red, which is what happened for the
workflow refresh, and that is the whole of the model here.

**Three communication channels.** A task log, a forward prompt, and a
reverse prompt serve a project with sprints and milestones. Here
`HANDOFF.md` and `CURRENT_BRIEF.md` carry the same load at a fraction of
the maintenance.

**Tiered verification and a pre-push hook.** A nine-second gate does not
need tiers, and a hook that duplicates it buys nothing.

**Conventional commit scopes.** The house style is an imperative subject
describing what the commit does, with no prefix. One hundred and
fifty-three commits are consistent in it.
