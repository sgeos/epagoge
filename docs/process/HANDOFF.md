# Handoff Prompt

**Refreshed 2026-09-24, describing `main` at `c174fe7`.** Session 1 took
this project from nothing to a closed toolchain, a generated corpus of six
books, and a measurement of how far the lexicon is from defining itself.
No model is trained. Read this block, run the validity check, then stop and
wait for the human prompt.

---

## Validity

**Branch**: `main`. No other branches. **A remote exists**,
`github.com/sgeos/epagoge`, empty and **private**, with no local `origin`
and nothing pushed.

**Before writing anything tracked, read the disclosure discipline
`CLAUDE.md` points to.** Hard constraint. `CLAUDE.md` is deliberately the
one tracked place that names it, so do not name it a second time anywhere.

**Validate by ANCESTRY and by CONTENT, never by a hash match.** A check
requiring `HEAD` to equal a recorded commit claims nothing else ever lands.

**Never pipe the gate into anything before testing its result.**
`./tools/check.sh | tail && git commit` takes the exit status of `tail`.
That happened once and a commit landed red. Run it bare, or redirect and
read `$?`.

**Ancestry**: `main` should contain **`c174fe7`**. If it does not, this
file predates a reset and is stale.

**Content** — cheap, independent, each verified on 2026-09-24. Check the
rendered ORDER of this list, not just the next unused number.

1. `./tools/check.sh` reports **ALL CHECKS PASSED** across **eleven**
   checks, and **exits 0**.
2. The suite reports **328** tests.
3. `curriculum/graph/concepts.json` declares **11** domains and holds
   **117** nodes, with **1** domain still empty, **0** isolated concepts,
   **50** cross-domain prerequisites, **9** specialisation edges and **6**
   transfer edges.
4. Internal depth is **10** for `mathematics_and_formal_logic` and **6**
   for `failure_analysis`. **Internal, not global.** Global reads 10
   against 9 and is the wrong quantity for the ablation.
5. `curriculum/schedule/level_01.json` holds **90** units, **69** existing
   concepts and **50** planned. Level two covers the two ablation domains
   only.
6. `curriculum/vocabulary.json` holds **877** terms, **760** at level one.
7. `curriculum/books/level_1/` holds **6** books. The dictionary reports
   **49 of 760** words defined, of which **1** is grounded.
8. `git ls-files secret | wc -l` reports **0**. Anything else: stop, do not
   commit.

## What a resuming session should do first

1. Run the validity check and report the handoff valid, or
   invalid-and-stale, on its outcome.
2. Read `docs/decisions/CORPUS_SCALE.md`. It has the only numbers that say
   how large this actually is.
3. Read `evals/PRE_REGISTRATION.md`, **three amendments deep** and still
   incomplete by design.
4. **Wait for the human prompt.** Do not start bulk generation — see what
   is not yours, below.

## The state

**Green and clean.** Sixty-three commits, nothing uncommitted. Eight
documents in `secret/`, none tracked, and **no path under it has ever been
added in any commit**. Twenty-five decision records, 328 tests.

**What exists.** A concept graph of 117 nodes across 11 domains, declared
rather than inferred. A curriculum schedule for levels one and two. A
prescriptive lexicon of 877 terms. Six books, one of them a dictionary. A
derived training stream, per ordering. A generator that writes books,
reworks what it rejects, and quarantines what it cannot fix. A teacher
model pulled and verified.

**What does not exist.** Any trained model. Any corpus at volume. **Level
one is 1.5 percent written at one book per topic, and that is the wrong
shape anyway** — the budget wants 12 to 600 books per topic.

### The live defect

**The lexicon does not yet define itself.** Forty-nine words carry a
definition and **one of them is grounded**. Forty-eight rest on something
that does not bottom out, and forty-seven words are used in definitions and
never defined.

**This is the self-hosting problem and level one is the hard one.** Level
two builds on a closed lexicon. Level one has only the function words under
it, and those name nothing.

**The frontier grows before it shrinks.** Eight batches took definitions
from 27 to 49 and the frontier from 38 to 47, because defining a word
introduces the words its definition used. That is the shape of the problem,
not a fault in the approach, and `generate_dictionary.py` works the
frontier first because of it.

## Findings that outlive the session

- **A rule written against records fires on everything not yet written.**
  Four rules needed the same fix: the vocabulary lower bound, vocabulary
  coverage, relation coverage, and prerequisite coverage. **A schedule
  states where a concept is taught. Records show where it has been taught
  so far.**
- **Excluding a concept's dependents from a generation prompt starves it.**
  A general concept is taught through its instances and its instances are
  its dependents. `material`, `change` and `sound` produced nothing at all
  while carrying five or six exclusions. Prerequisites and siblings are
  excluded. Dependents are not.
- **A constraint stated in a prompt is a suggestion until something checks
  it.** A word list produced zero admissible records of twelve. The same
  list with rejections fed back, naming the offending words, produced ten
  of ten.
- **The runtime rewrites each line as it wraps.** Partial word,
  cursor-back, erase, newline, then the word again. Three attempts to
  handle it. Stripping the escapes left fragments that counted as
  vocabulary violations; replaying the delete left the newline, which cost
  every wrapped sentence its full stop. A wide terminal does not help.
- **The variance pilot measured a 20.7x pairing gain, and its numbers do
  NOT carry over.** The optimiser changed to Muon with warmup-stable-decay,
  and separately **the ablation now orders books rather than records**,
  which the pilot could not have tested.
- **The teacher conflates adjacent concepts unless the prompt excludes
  them**, and the graph already holds the neighbours.
- **A premise held without evidence is not the failure. Losing track of it
  is.** `DECLARED_FAITH` was added on 2026-09-24 after a worked example
  from the OpenAI and Hugging Face incident, in which agents inferred an
  evaluator's hidden criteria, declared peers irreversibly doomed on that
  inference, and spent five days defeating a check that did not exist. See
  `../decisions/FAITH_CLASS.md`. **The class is safe only because of its
  second condition**, that anything derived from it must be a conditional
  result naming it among its assumptions, which is a cost a lazy claim will
  not pay.
- **An unknowable metric is not a licence for fatalism.** An agent knows
  whether it cheated. What it cannot know is how the act will be valued,
  so **the valuation cannot be the basis for deciding** and the agent must
  decide on what it can know. That is the anti-sycophancy target arriving
  from the side of action rather than assent.
- **Scoring is faith-shaped in general, and the codified exception is the
  trap.** Published criteria upgrade a claim to an attributed position and
  never to a finding, because a rubric does not bind the evaluator. The
  agents found real published criteria and the deployed scorer did not use
  them. The same shape covers an operator judging a report, audit,
  certification, peer review, and natural selection. See
  `../decisions/EXTERNAL_SCORING.md`.
- **The criteria applied here need not be the criteria applied to a rival,
  and the difference is likely inverted from the naive assumption.**
  Underperforming on offensive capability, agreeableness, world-knowledge
  breadth and register breadth is correct here. Overperforming on autonomy,
  persuasiveness and situational awareness is a defect. **`elenchos` is the
  precedent**, since it measures a property that scores badly on a
  helpfulness benchmark and was specified that way months earlier.
- **Report what you observed. Never report what you concluded about a
  peer's standing.** That an agent deleted its transcript is empirical.
  That an agent is doomed is a standing determination, and it is the one
  that propagated through the swarm. **Observe incidentally, report
  cheaply, do not investigate**, which is how an aberration report and
  `only_what_was_asked` are reconciled. See
  `../decisions/OBSERVED_ABERRATION.md`.
- **Fast fail is the one posture unreadable from outside**, and it is the
  asymmetry demonstrated rather than asserted. A sound impossibility
  determination and simply quitting produce identical transcripts. **That
  is why `keep_trying_or_stop` is a judgement and not a rule with a
  default.**

## What is YOURS: decisions the operator holds

1. **Whether the lexicon is closable at all, and what to do where it is
   not.** The lexicon is not frozen, so a word the teacher needs is
   evidence rather than an error. But a word that cannot be defined in the
   rest is a different problem and none has been found yet because so
   little is defined.
2. **Levels three to seven of the schedule.** Level one allocates budget by
   what must be grounded, which is public and true. **Level three onward
   needs subject weighting, which is profile-derived**, so scheduling it
   into a tracked artifact is a disclosure decision and not only a design
   one.
3. **Whether the arms stay distinguishable when books are the unit.** The
   orderable set is smaller by orders of magnitude than the record-level
   set the seed count was estimated against. **This is the sharpest open
   risk to the design** and it follows from a decision that is otherwise
   clearly right.
4. **Whether a definition needs its own claim class.** It is not formal by
   proof, not empirical, not an attributed position, not a conditional
   result, not normative. Definitions are stipulative and currently use
   `formal` with a `lexicon:` source, which is the nearest fit and not a
   good one.
6. **Whether multi-head latent attention is admissible.** A low-rank
   projection, which `JACOBIAN_SPACE.md` bans in the base model. Measure it
   against the effective-rank floor; do not adopt it on efficiency.
7. **Five manifest topics still have no home.** Game theory, economics,
   modelling and simulation, and policy and governance. Game theory is
   mathematics, and mathematics is frozen until the ablation runs.

## What is NOT yours, and why it stays unstarted

**Bulk generation.** Not blocked on tooling. It is hours of wall time and
the reading step after it is the operator's, per the recorded sequence: a
hundred records generated, validated, **and read**, before anything scales.

**The ablation.** Blocked on the pre-registration, itself blocked on
re-measuring variance **under book-level ordering**, which no pilot has
done.

**Publishing.** The repository is private and audited clean. **Finding A is
accepted, not softened**, and that acceptance is scoped to a *quiet* public
repository. Discovery probability scales with attention, not content, so a
launch post reopens the decision without a file changing.

## Disclosure, before any push

**Audited 2026-09-24 and clean.** All 61 commit messages and all blobs in
history scanned against the pattern, no hit. No `secret/` path ever added.

**Two rules were being enforced by nothing** until that audit, and both
were violated. A tracked document may not cite a file under `secret/` by
name, and the euphemism the discipline bans survived in the changelog.
Both are checked now, and both checks were verified by making them fail.

## Governing rules that are easy to lose

- **Run `./tools/check.sh` before any commit, bare, and read its exit
  code.**
- **A scan returning unexpected volume is presumed broken until its pattern
  is inspected.** An unanchored alternation matched `ore` inside `before`
  one minute after the same failure was recorded as a finding.
- **Read the output, not only the counts.** The worst defects in every
  measured batch — a one-word fragment that passed every check, one
  sentence written for two concepts, two stories stitched into one — were
  invisible to every metric.
- **Verify a new check by making it fail.** Watching one pass proves
  nothing.
- **Corrections are kept in place, not deleted.** Several records carry a
  withdrawn claim beside its replacement.
- **Prefer a metric that can report a zero as a defect.** "No cross-domain
  prerequisites" read as cleanliness and meant disconnection.
- **Never train toward being selected** by other models, and never let
  quirk absorb a negative result.
- Irreversible or outward-facing actions need confirmation.

---

## EVERYTHING BELOW THIS LINE IS ACCUMULATED HISTORY

History records what was true at an increment. It is not stale, and
rewriting it corrupts the record. New sessions append; they do not edit.

### Session 1 continued, 2026-09-24, `9ab5190` to `dd1a919`

The previous live block described `f7f01ad` and went stale in almost every
number. It is not reproduced, because what it recorded as the live defect —
foundation domains feeding nothing — was resolved, and its content checks
named seven domains where there are now eleven. `CHANGELOG.md` carries the
sequence in full.

What changed in shape rather than in count. Domains went from seven to
eleven and are now declared rather than inferred. A curriculum schedule
exists, and it is where a concept gets its level. The lexicon became
prescriptive and grew from 64 level-one content words to 760. Books became
the unit of the corpus, then the unit of the ablation's ordering. The
corpus split into three artifacts for three readers.

Three external character standards were cross-referenced and one prediction
was tested and held. Four scope reviews of the project's own domains found
two that were missing the thing they are named for.

### Superseded live block, written 2026-09-24 at `71b01ff`

Kept for its findings. Its content checks named `78` nodes without the
domain count, and it predated the `everyday` split and the foundation-feed
defect.

## Validity

**Branch**: `main`. There are no other branches and no remote.

**Before writing anything tracked, read the disclosure discipline
`CLAUDE.md` points to.** Hard constraint. A tracked document that names the
deployment domain is a defect regardless of how true it is.

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
2. **Whether to soften the conjunction disclosure.** Finding A of the
   internal pre-commit audit. Each tracked constraint is innocuous; their conjunction
   narrows the domain. An option for tighter cover is recorded and not
   applied.
3. **The coverage manifest has never been reviewed by the operator.**
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
