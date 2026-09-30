# Process Strategy

**Written 2026-09-25**, after reviewing the process documents of the
operator's `keleusma` repository, which was this project's reference when
it was set up and has moved a long way since.

This document holds what is **durable**. `CURRENT_BRIEF.md` holds a bounded
scope and is marked completed when its condition is met. A completed brief
may remain until a new scope replaces it, with the previous brief and
condition preserved beside their review evidence. The handoff identifies
current task status. Durable lessons belong here so replacement of a brief
does not erase them.

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

## Added 2026-09-27, after a session that found six

**Three were in code and three were in reasoning**, and the reasoning ones
were harder to see because nothing failed.

**A TOOL THAT ANNOUNCES ITS OWN TRUNCATION IS ONLY USEFUL IF SOMEONE HEARS
IT.** `diagnose_level.py` printed "held-out loss over 24 of 48 batches" on
every run for a day. **It was read past about forty times**, through four
evaluation records, until an absolute figure was about to be published as a
frontier. Every number that tool produced was 0.25 nats optimistic.
Comparisons survived, because the truncation was identical everywhere, and
absolute values did not. **The announcement was added deliberately, by this
project, for exactly this case, and it still did not work.** A partial
result should be refused or defaulted to whole, not narrated.

**ELIMINATION IS NOT ATTRIBUTION.** An ordering residual was attributed to
the prerequisite graph by ruling out three alternatives and taking the
remainder. A fourth existed, unlooked-for: graph-respecting orders also sort
books by length. **Before concluding from elimination, the question is what
has not been enumerated**, and the answer is never zero.

**A CONTROL IS ONLY A CONTROL IF IT MATCHES ON WHAT IT HOLDS FIXED**, and
that has to be verified after building it rather than assumed from the
construction. One control was tuned against a reconstruction of the arm
rather than the arm, and the real one placed a class of books differently.
The same control was then tuned against the wrong statistic, a correlation
of mean position across seeds rather than within one seed, which differ by
half again. **Both would have produced a control varying two things, and
both looked correct in the write-up.**

**THE SAME QUANTITY COMPUTED THREE WAYS GAVE 88 PERCENT, 0.5 PERCENT AND
3.5 PERCENT.** Pair coverage counting every concept any record mentions
counts the dictionary books, which define the lexicon and form one clique.
Counting only what a schedule unit teaches loses every cross-concept book's
partner. **Two of the three were produced before the right one**, and what
caught it was disagreement with a figure already in the handoff, not
reasoning. **Check a derived quantity against a recorded one before
believing it.**

**A LESSON RECORDED IN ONE FILE GETS RELEARNED IN ANOTHER.** `prompt.py`
carries a comment saying that naming a banned word is not supplying the
replacement. `retitle_books.py` then refused a title four times for a
contraction the lexicon has a substitution for, because its prompt named no
replacement. Separately, `book_head` existed with a docstring asking callers
to use it, and two call sites did not. **Where a lesson can be made
structural it should be**: the second was fixed by a type whose only
constructor is the right one, and the comment had not been enough.

**READ A COUNT FROM THE TOOL.** Four times in one session a number went
into a record from arithmetic when the gate would have supplied it: a test
count in a pushed commit message, a record count, a word count, and a
second word count. **Three were caught by checking and one by the gate.**

**DO NOT PIPE A RUN THROUGH A FILTER AND READ THE EXIT CODE.** It reports
the filter's status. A training run crashed after its first seed and the
shell reported success, and a lint failure was hidden the same way an hour
later, by the same mistake in a different command.

## Added 2026-09-27, later the same day, and it is the sibling of the last one

**DO NOT CHAIN THE GATE TO THE COMMIT.** `check.sh` was run, then the
commit, then the push, in one shell command joined by a semicolon. The gate
failed, the commit ran on the gate's output rather than on its exit code, and
a failing tree reached `origin`. `9a7981c`.

**The rule that says to run the gate, read the exit code, stop, then commit
already existed**, and it was not disobeyed so much as bypassed by the shape
of the command. **Nobody decided to skip the gate.** The decision point was
removed by putting the three steps in one invocation, which is exactly how
the filter-and-exit-code failure above works, one layer up.

**So the gate runs alone and the next command reads its status.** A gate
whose result is not looked at before the next step is a gate that is not
gating.

**What it had caught was real.** The reference check resolves file names
mentioned in prose against the tree, and the text named a toolchain file that
exists elsewhere on this machine and not in this repository. **A second
defect in the same replacement text was not something the gate could
catch**, a pin count written from a half-remembered list where the grep was
still available, which is the count-from-arithmetic failure for the fifth
time.

**A LOCAL GATE CAN PASS ON FILES THE REPOSITORY DOES NOT HAVE.** The fourth
divergence between the local gate and continuous integration, and a mechanism
distinct from the three before it. The reference check resolves a named path
three ways, and the third is the working filesystem. A record naming seven
scan sources under ignored `tmp/` resolved locally **because the files were
sitting there**, and failed in the runner's clone, which has the `.gitignore`
but not the files.

**The check was right both times.** What differed was which of its three
resolution paths answered. Writing the full ignored path rather than the
basename makes `git check-ignore` answer instead, and that works in any
clone because `.gitignore` is tracked.

**The general form is worth more than the instance.** A check that consults
the filesystem passes on untracked state, so a green local gate says nothing
about a clone whenever the thing being checked is a path. **The three earlier
divergences all had this shape** and were each diagnosed as their own
specific cause.

## Added 2026-09-28, and it is one class with three instances in a day

**A HYPERPARAMETER WITH ONE NAME IS NOT NECESSARILY ONE QUANTITY.** Three
confounds in a single day, each invisible because the parameter had a single
name.

**The learning rate across widths.** Every run this project has ever done used
the trainer's default of 3e-4, because no tool exposes it, and width was swept
from 16 to 1,024 against that fixed value. Maximal update parametrization's
whole claim is that the optimal rate moves with width. **So the published
width ranking is not separable from mis-tuning**, and it is now marked
provisional.

**The learning rate across two optimisers.** Muon at its reference default of
0.02 against AdamW at 3e-4. Those are not comparable numbers, so the measured
0.117 nats is a comparison of two configurations rather than of two
optimisers, and one of them could not be adjusted at all.

**The weight decay across two optimiser groups.** Muon's shrinkage is coupled
to its own rate, so one shared value applied about sixty-seven times the
per-step shrinkage to the matrices as to everything else. A sweep of that
value measured the coupling and not the decay.

**What caught the third one was the training loss moving the wrong way.** More
decay lowered training loss, which regularisation cannot do. **Nothing caught
the first two; they were reasoned out afterwards from what the code could and
could not express.**

**So the check is mechanical rather than attentive.** Before reporting the
effect of varying a named parameter, ask what quantity the name resolves to in
each condition being compared, and whether anything else moves with it. **A
parameter that is not reachable from a tool has never been held fixed
deliberately**, only by default, and a default is not a control.

## Added 2026-09-28. A recorded property is not a guard

**The provenance record is derived from git history**, so it cannot be
regenerated before the commit that changes the lexicon: the new words have no
first commit yet, and the commit gives them one. **That property was recorded
twice** and then walked into anyway, by running the regeneration in the same
breath as the commit. The gate passed locally and continuous integration
failed on the pushed head.

**Three of this session's recurring failures have the same shape.** A warning,
then a per-caller fix, then finally a change that makes the failure impossible:
the tracked output default, the truncated evaluation, and now this. **In every
case the note was written before the recurrence and did not prevent it.**

**So the rule is about where a lesson goes, not whether it is learned.** A
property a caller must remember at the right moment is a property that will be
forgotten at the wrong one. `word_provenance.py` now refuses to write when the
lexicon holds words no commit contains, and says to commit first.

**The test of whether a lesson has been made structural is whether the next
person can fail the same way.** If they can, it was documentation.

## Added 2026-09-28. A filtered view is not a sample

**A rule was written from evidence the filter had constructed.** The question
was whether dictionary entries lead with the word. A grep for lines matching a
capitalised word followed by "is" returned eight, all of that shape, and the
rule followed. **The pattern could not have returned anything else.**

**Measured properly, 551 of 795 entries do not lead with the word and 244 do**,
so the rule imposed a minority convention on the majority and rejected every
definition in the next run.

**The check is to ask what the query could not have returned.** A search for
confirmation returns confirmation. This is a different failure from reading a
count off arithmetic, because the number was real and the population was
wrong.

**It cost one run and was caught by the result being absurd**, at zero
acceptances where the previous run had two thirds. **A less extreme error would
have survived**, which is the reason to record it rather than the cost.

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
