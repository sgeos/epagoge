# Handoff Prompt

**Refreshed 2026-09-24, describing `main` at `f7f01ad`.** Session 1 took this
project from nothing to a validated specification and tooling layer, and
then restructured the domain set from seven names to eleven. No corpus is
generated and no model is trained. Read this block, run the validity check,
then stop and wait for the human prompt.

---

## Validity

**Branch**: `main`. No other branches, no remote.

**Before writing anything tracked, read `secret/CODE_NAMES.md`.** Hard
constraint. It holds the disclosure discipline, the banned vocabulary, and
the scan that enforces them. A tracked document naming the deployment domain
is a defect regardless of how true it is.

**Validate by ANCESTRY and by CONTENT, never by a hash match.** A check
requiring `HEAD` to equal a recorded commit claims nothing else ever lands.

**Ancestry**: `main` should contain **`f7f01ad`**, the last commit before
this refresh. If it does not, this file predates a reset and is stale.

**Content** — cheap, independent, each verified on 2026-09-24. Check the
rendered ORDER of this list, not just the next unused number.

1. `./tools/check.sh` reports **ALL CHECKS PASSED** across nine checks.
   Anything red means a statement below needs re-reading before it is
   believed.
2. The suite reports **199** tests.
3. `curriculum/graph/concepts.json` **declares 11 domains** and holds **78**
   nodes, of which **4 domains hold no concept at all** and are awaiting
   content by design. It yields **4** derived transfer edges. A domain
   named `everyday`, `physical_world`, or `communication` means this file
   predates the 2026-09-24 restructure and is stale.
4. `tools/validate_graph.py` reports **0** foundation feeds, now counted
   over `directed_physical_interactions`, `record_keeping`, and
   `agentic_operations`. **That is a known defect, not a target** — see the
   state below. A non-zero value means someone has begun fixing it and this
   file is behind.
5. Vocabulary completeness is **100 percent**, 138 terms, **0** unmapped.
6. `git ls-files secret | wc -l` reports **0**. Anything else: stop, do not
   commit.

## What a resuming session should do first

1. Run the validity check and report the handoff valid, or
   invalid-and-stale, on its outcome.
2. Read `docs/decisions/OPEN_QUESTIONS.md`. Nineteen answered, four
   deferred, two open. Several answers carry corrections that must not be
   re-reverted.
3. Read `evals/PRE_REGISTRATION.md`. **Incomplete by design**, and must be
   complete before the first ablation run.
4. **Wait for the human prompt.** Do not begin corpus generation — see what
   is not yours, below.

## The state

**Green and clean.** Thirty-one commits, nothing uncommitted. Seven
documents in `secret/`, none tracked. Sixteen decision records, seven
specifications, three architecture documents, 199 tests.

**There is now a remote.** `github.com/sgeos/epagoge`, created empty and
**private**, with no local `origin` configured and nothing pushed. The
intended end state is public with everything sensitive quarantined in the
gitignored `secret/`. **An audit must pass before the first push**, and it
has not been run. See the disclosure section below.

**What exists.** A concept graph with prerequisite, instantiation, and
specialisation edges and two reach metrics. A record schema with twelve
enforced rules across four record types. A six-class claim taxonomy. A
primitive register of 34 hand-authored axioms. A per-level vocabulary, fully
mapped. A variance-pilot harness, run. A review tool that is also the
sampled audit. A teacher model pulled and verified.

**What does not exist.** Any generated corpus, any trained model, any
curriculum schedule. The 20-record sample corpus exercises every feature and
is not curriculum.

### The live defect

**The foundation domains found nothing.** Zero prerequisites run from
`physical_world`, `space_and_time`, or `agency` into any other domain, and
only one foundation concept is depended on at all. They carry vocabulary and
contribute no structure.

This was reported twice as the good property "no cross-domain prerequisites"
before being recognised as disconnection. **The property that matters is
narrower**: no prerequisite between the two ablation domains, since that is
what would muddy the contrast. Foundations feeding both is desirable.

### Findings that outlive the session

- **The variance pilot measured a pairing gain of 20.7x seeds, free.**
  Twelve paired seeds beat 246 unpaired. **Its numbers do NOT carry over**,
  because the optimiser and schedule have since changed to Muon with
  warmup-stable-decay.
- **The pilot's first run trained 23 epochs**, where ordering effects
  necessarily wash out, inflating the correlation from 0.954 to 0.987. Both
  results are kept because the difference is the finding.
- **An unexplained systematic difference appeared between two orderings that
  should be equivalent**, sign following the ordering and not the execution
  position, marginal at about p = 0.04. It is the shape of a false positive
  and the ablation carries a null arm because of it.
- **The teacher conflates adjacent concepts unless the prompt excludes
  them.** Prompts must carry the concept's nearest graph neighbours as
  explicit exclusions; the graph already holds them.
- **Maximal update parametrization is confound removal, not optimisation.**
  Without it the three scale points carry different optimal hyperparameters,
  so scale-dependence could be a tuning artifact — which lands on this
  project's own proposed mechanism.

## What is YOURS: decisions the operator holds

1. **The curriculum schedule.** Unstarted and non-trivial. Levels are
   authored, capacity and completion are unmodelled, nothing has scheduled
   anything. The largest open design task, and everything downstream waits
   on it.
2. **Whether to connect the foundations**, and how. The defect above is a
   design question, not a bug to patch.
3. **Populating the four empty domains.**
   `history_and_philosophy_of_science`, `institutional_interfacing`,
   `cybernetic_biological_systems`, and `normative_adjudication` are
   declared and hold nothing. The graph follows content, so they fill when
   records teach them and not before.
4. **Whether multi-head latent attention is admissible.** A low-rank
   projection, which `JACOBIAN_SPACE.md` bans in the base model. Measure it
   against the effective-rank floor; do not adopt it on efficiency.
5. **Five manifest topics still have no home.** Game theory, economics,
   modelling and simulation, and policy and governance. Game theory is
   mathematics, and mathematics is frozen until the ablation runs.

## What is NOT yours, and why it stays unstarted

**Corpus generation.** Blocked on the curriculum schedule, not on tooling.
Writing the generator first would encode guesses where changing them is most
expensive.

**The ablation.** Blocked on the pre-registration, itself blocked on
re-measuring variance under the intended optimiser.

**Re-running the variance pilot.** Cheap and unblocked, but useless until
the trainer uses Muon and warmup-stable-decay, which the pilot harness does
not.

## Disclosure, before any push

**Finding A in `secret/AUDIT_ADDENDUM.md` is ACCEPTED, not softened.** Two
independent conjunctions, the hardware constraints and now the eleven
domain names, both point at the same deployment family. That was weighed
and allowed. The threat model is **unintentionally timed disclosure rather
than disclosure**, so reading between the lines is acceptable and lay
readers should see nothing.

**The acceptance is scoped to a quiet public repository.** Discovery
probability scales with attention, not with content. Any launch post,
paper, or deliberate promotion re-opens the decision without a file
changing. Re-read finding A before drawing attention to this work.

**Two gaps in the gate, both currently clean and neither enforced.** The
disclosure scan reads `git ls-files`, so it never sees an untracked file.
**Stage first, then gate**, or a new document passes by not being read.
The scan also never reads commit messages or history at all, and history
is what a push publishes. Both were scanned by hand on 2026-09-24 over all
commit messages and all 197 blobs and both were clean. The pre-push audit
must cover history, not the working tree.

## Governing rules that are easy to lose

- **Run `./tools/check.sh` before any commit.** The static analysis sat
  configured and unexecuted through the initial commit; on first run it
  failed thirty-six ways.
- **A scan returning unexpected volume is presumed broken until its pattern
  is inspected.** An unanchored alternation matched `ore` inside `before`
  and produced output indistinguishable from a clean result, one minute
  after the same failure was recorded as a finding.
- **The vocabulary design was corrected three times, each by running the
  validator rather than by reasoning.** A concept can be taught before its
  name is introduced, so a word's level is authored and the graph bounds it
  from below only.
- **A metric can hide the thing it appears to measure.** A low anchor-reach
  score may mean a concept is not worth teaching or that the graph is
  incomplete. "No cross-domain prerequisites" read as cleanliness and meant
  disconnection. Prefer a metric that can report a zero as a defect.
- **Corrections are kept in place, not deleted.** Several records carry a
  withdrawn claim beside its replacement. Removing one corrupts the record
  of why the replacement is right.
- **Never train toward being selected** by other models, and never let quirk
  absorb a negative result. Both are recorded with reasoning.
- Irreversible or outward-facing actions need confirmation. Nothing is
  published; publication needs explicit in-session authorisation.

---

## EVERYTHING BELOW THIS LINE IS ACCUMULATED HISTORY

History records what was true at an increment. It is not stale, and
rewriting it corrupts the record. New sessions append; they do not edit.

### Superseded live block, written 2026-09-24 at `71b01ff`

Kept for its findings. Its content checks named `78` nodes without the
domain count, and it predated the `everyday` split and the foundation-feed
defect.

## Validity

**Branch**: `main`. There are no other branches and no remote.

**Before writing anything tracked, read `secret/CODE_NAMES.md`.** Hard
constraint. It holds the disclosure discipline, the banned vocabulary, and
the scan that enforces them. A tracked document that names the deployment
domain is a defect regardless of how true it is.

**Validate by ANCESTRY and by CONTENT, never by a hash match.** A check
requiring `HEAD` to equal a recorded commit claims nothing else ever lands.

**Ancestry**: `main` should contain **`71b01ff`** (accounting added), the
last commit before this was written. If it does not, this file predates a
reset and is stale.

**Content** — cheap, independent, each verified on 2026-09-24. Check the
rendered ORDER of this list, not just the next unused number.

1. `./tools/check.sh` reports **ALL CHECKS PASSED** across nine checks. It
   gates lint, format, strict typing, tests, a 95 percent coverage floor,
   graph and corpus validation, and the disclosure scan. Anything red means
   a statement below needs re-reading before it is believed.
2. The suite reports **192** tests. A lower number means this file predates
   work; a much higher one means it postdates this refresh.
3. `curriculum/graph/concepts.json` holds **78** nodes across **seven**
   domains and yields **4** derived transfer edges. If there is a domain
   named `everyday`, this file predates the 2026-09-24 split and is stale.
4. Vocabulary completeness is **100 percent**, 138 terms and **0** unmapped.
   A non-zero unmapped count means concepts are missing from the graph, not
   that the words are ordinary.
5. `git ls-files secret | wc -l` reports **0**. If it reports anything else,
   stop and do not commit.

## What a resuming session should do first

1. Run the validity check and report the handoff valid, or
   invalid-and-stale, on its outcome.
2. Read `docs/decisions/OPEN_QUESTIONS.md`. Nineteen answered, four
   deferred, two open. The answers carry their reasoning and several carry
   corrections that must not be re-reverted.
3. Read `evals/PRE_REGISTRATION.md`. It is **incomplete by design** and
   must be complete before the first ablation run.
4. **Wait for the human prompt.** Do not begin corpus generation on your
   own — see what is not yours, below.

## The state

**Green and clean.** Twenty-five commits, nothing uncommitted, nothing
unpushed, no remote. Seven documents in `secret/`, none tracked.

Fourteen decision records, seven specifications, three architecture
documents, 192 tests at 98 percent coverage.

**What exists.** A concept graph with prerequisite, instantiation, and
specialisation edges and two reach metrics. A corpus record schema with
twelve enforced rules across four record types. A claim taxonomy of six
classes. A primitive register of 34 hand-authored axioms. A per-level
vocabulary. A variance-pilot harness, run. A review tool that is also the
sampled audit. A teacher model pulled and verified.

**What does not exist.** Any generated corpus, any trained model, any
curriculum schedule. The 20-record sample corpus is a demonstration that
exercises every feature; it is not curriculum.

### Findings that outlive the session

- **The variance pilot measured a pairing gain of 20.7x seeds, free.**
  Twelve paired seeds beat 246 unpaired. The original five-seed unpaired
  design was off by two orders of magnitude in efficiency. Its numbers do
  **not** carry over, because the optimiser and schedule have since changed
  to Muon with warmup-stable-decay.
- **The pilot's first run was wrong in an instructive way.** It trained 23
  epochs, where ordering effects necessarily wash out, inflating the
  correlation from 0.954 to 0.987. Both results are kept because the
  difference is the finding.
- **An unexplained systematic difference appeared between two orderings
  that should be equivalent**, seven of eight pairs in one direction, sign
  following the ordering and not the execution position. Marginal at about
  p = 0.04. It is the shape of a false positive, and the ablation now
  carries a null arm because of it.
- **The teacher conflates adjacent concepts unless the prompt excludes
  them.** Asked to teach that use wears things out, it returned two
  sentences in three about things breaking. One negative constraint fixed
  it. Prompts must carry the concept's nearest graph neighbours as explicit
  exclusions; the graph already holds them.
- **Maximal update parametrization is confound removal, not optimisation.**
  Without it the three scale points carry different optimal hyperparameters,
  so any scale-dependence could be a tuning artifact — which lands on this
  project's own proposed mechanism.

## What is YOURS: decisions the operator holds

1. **The curriculum schedule.** Non-trivial and unstarted. Levels are
   authored, capacity per level and completion by the end are unmodelled,
   and nothing has scheduled anything. This is the largest open design task.
2. **Whether to soften the conjunction disclosure.** `secret/AUDIT_ADDENDUM.md`
   finding A. Each tracked constraint is innocuous; their conjunction
   narrows the domain. An option for tighter cover is recorded and not
   applied.
3. **`secret/TOPIC_MANIFEST.md` has never been reviewed by the operator.**
   It was derived by an agent and drives corpus generation.
4. **History as a domain**, recorded as a further addition and not added.
5. **Whether multi-head latent attention is admissible.** It is a low-rank
   projection, which `JACOBIAN_SPACE.md` bans in the base model. It must be
   measured against the effective-rank floor, not adopted on efficiency.

## What is NOT yours, and why it stays unstarted

**Corpus generation.** Blocked on the curriculum schedule, not on tooling.
The generator, the verification layers, and the teacher prompts do not
exist, and writing them before a schedule exists would encode guesses into
the place where changing them is most expensive.

**The ablation.** Blocked on the pre-registration, which is blocked on
re-measuring variance under the new optimiser.

**Re-running the variance pilot.** Cheap and unblocked, but its result is
only useful once the trainer uses the intended optimiser and schedule, which
the pilot harness does not.

## Governing rules that are easy to lose

- **Run `./tools/check.sh` before any commit.** The static analysis was
  configured in the initial commit and had never been executed; on first run
  it failed thirty-six ways.
- **A scan that returns unexpected volume is presumed broken until its
  pattern is inspected.** An unanchored alternation matched `ore` inside
  `before` and produced a hundred lines that would have looked identical to
  a clean result. That happened one minute after recording the same failure
  as a finding.
- **The vocabulary design was corrected three times, each time by running
  the validator rather than by reasoning.** Derivation from the graph was
  wrong twice. A concept can be taught before its name is introduced, so a
  word's level is authored and the graph bounds it from below only.
- **A low anchor-reach score may mean a concept is not worth teaching, or
  it may mean the graph is incomplete.** The metric cannot distinguish them.
  The teddy bear scored zero until its edges were drawn.
- **Corrections are kept in place, not deleted.** Several records carry a
  withdrawn claim beside its replacement. Removing one corrupts the record
  of why the replacement is right.
- **Never train toward being selected** by other models, and never let
  quirk absorb a negative result. Both are recorded with the reasoning.
- Irreversible or outward-facing actions need confirmation. Nothing is
  published, and publication needs explicit in-session authorisation.
rewriting it corrupts the record. New sessions append; they do not edit.

### Domain restructure, 2026-09-24, at `f7f01ad`

Seven domains became eleven. Every name that survived is an activity,
because a domain named for an activity excludes what does not serve it
while a domain named for a bare field admits everything in the field.
Mathematics is the deliberate exception and is frozen by the ablation.

Domains are now **declared** in a registry rather than inferred from node
membership, so that a domain decided upon and not yet written is visible.
Four are declared and empty.

Thirteen candidate names were withdrawn with reasons, all recorded in
`../decisions/DOMAIN_SET.md`, because the reasons constrain future
additions. The sharpest is that four separate candidates for the normative
domain each pre-committed to where obligations come from, when the conflict
between sources is the domain's actual subject.

### Session 1, 2026-09-23/24

Project created from nothing. Pre-planning closed after nineteen questions.
First implementation was the concept graph. The variance pilot ran. The
teacher model was pulled. Vocabulary went from unmapped to fully mapped.

Four corrections worth carrying forward are in the governing rules above.
The full sequence is in `CHANGELOG.md`, which is written for this purpose.
