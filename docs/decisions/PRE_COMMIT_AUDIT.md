# Pre-commit adversarial audit

**Conducted 2026-09-23**, on the design and the tracked documentation,
before the initial commit. Adversarial in intent. Findings are recorded
whether or not they reflect well on the work.

Three findings were blocking, meaning each invalidated part of the design
rather than merely weakening it. **All three were resolved on 2026-09-23**
and the resolutions are recorded in place beneath each finding. The
findings are retained rather than deleted, since the reasoning that
produced them is what justifies the resolutions.

## Blocking

### 1. The ablation is underpowered to the point of self-defeat

**Measured, not estimated.** At five seeds per condition the standard error
of the difference of means is 0.632 standard deviations of seed variance,
so the smallest detectable effect at a 0.05 threshold and 0.8 power is
**1.77 sigma**.

The published ordering literature reports small and inconsistent effects.
An effect of 1.77 sigma of seed variance would already be unambiguous
there. Question four defines an inconclusive result as project failure.

**The design therefore has a high prior probability of returning the
failure outcome by construction rather than by finding.**

| Seeds per condition | Smallest detectable effect |
| --- | --- |
| 5 | 1.77 sigma |
| 10 | 1.25 sigma |
| 20 | 0.89 sigma |
| 30 | 0.72 sigma |

### RESOLVED 2026-09-23. Pair the design, pilot the variance, then allocate

**Design error corrected.** The experiment is naturally paired and was
specified unpaired. Both conditions can share an initialisation and share
the data, with order as the only difference. Pairing cancels the
between-seed variance that dominates the unpaired standard error, and it is
free.

| Seeds per condition | Unpaired | Paired, rho=0.5 | Paired, rho=0.8 | Paired, rho=0.9 |
| --- | --- | --- | --- | --- |
| 5 | 1.77 | 1.25 | 0.79 | 0.56 |
| 30 | 0.72 | 0.51 | 0.32 | 0.23 |

Pairing alone is worth between 1.4 and 10 times the seed count depending on
the paired correlation, at no additional compute.

**The correlation is unmeasured, and the whole benefit depends on it.**

**Resolution.** Pair the design. Then run a variance pilot at the smallest
scale, several paired 100M runs at roughly seventy dollars of compute, to
measure seed variance and paired correlation directly. Set the seed count
and the allocation across scale points from the measured values. Only then
pre-register.

This converts the project's central design parameter from an assumption
into a measurement, which is the methodology the project claims for itself.

**Allocation costs, computed for reference once the pilot returns.**

| Allocation | Ideal | With 2.5x overhead |
| --- | --- | --- |
| Original, n=5 at three scales | $3,667 | $9,167 |
| n=30 at three scales | $22,000 | $55,000 |
| n=30/30/5 unequal | $5,333 | $13,333 |
| Drop 1B, n=30 at two scales | $2,000 | $5,000 |

The one-billion arm dominates. Dropping it and running thirty seeds at the
two cheaper scales is both better powered and cheaper than the design
originally specified.

**Consequence for question five.** The three-scale allocation recorded
there is provisional until the pilot returns.

### 2. Source grounding contradicts the curriculum's defining feature

Question two makes entailment by a retrieved passage the floor, rejecting
any record whose claim exceeds what its source supports.

The curriculum's defining feature is simplified pedagogical content at
early stages. **Simplification produces claims that no source states
verbatim.** As written, the floor rule forbids the product.

This is an incompatibility rather than a tension, and neither record
acknowledges the other.

### RESOLVED 2026-09-23. Labelled simplification with declared scope

**The problem restated more sharply than the finding first put it.** The
incompatibility is not that simplified wording differs from source wording.
Good pedagogy uses **known-false simplifications**, models that are wrong
at a higher level and useful at a lower one, which later stages correct.
That is what teaching a concept in stages and revisiting it at increasing
complexity means. No entailment rule can be satisfied by content whose
purpose is to be superseded.

**Resolution.** Entailment is replaced, for simplified content, by a
**declared fidelity relation that is itself auditable.** Each simplified
record carries.

- A resolvable source claim.
- The kind of simplification applied, such as omission, idealisation,
  superseded model, or analogy.
- The stage range over which it holds.
- A pointer to the later record that supersedes it.

Terminal-stage material drawn from real literature keeps strict
entailment. The weakening applies only where it must, and it is recorded
rather than assumed.

**Why this is an asset rather than a concession.** The corpus becomes one
in which every simplification states its domain of validity and its
correction. That is auditable in a way an unlabelled corpus of true
statements is not, and it is plausibly better training signal for the
project's stated property, since a model trained on explicitly scoped
claims sees claims held with scope rather than absolutely.

**It also supplies the revisit criterion** that question one of the
curriculum specification lists as unspecified. A concept is revisited when
a later record supersedes an earlier one through the recorded pointer,
which is a structural fact rather than a judgment.

**Consequence.** The supersession pointer and the simplification label are
required fields in the corpus record schema. They are not annotations added
later.

### 3. The independent variable is undefined

"Difficulty" appears nine times across tracked documents as a descriptor
and nowhere as a definition. `curriculum/README.md` lists the complexity
metric as unspecified. Question four's pre-registration list fixes metrics,
effect size, seed count, and controls, and **does not include the
curriculum specification or the difficulty metric**.

An experiment whose treatment is undefined cannot be pre-registered.

**A second-order hazard.** If difficulty is assigned by the teacher model,
the teacher's unvalidated judgments silently become the treatment. That is
an uncontrolled confound at the centre of the design, and it is not
recorded anywhere.

### RESOLVED 2026-09-23. Structural difficulty from a concept graph

**Difficulty is derived from structure, not from any model's judgment.**

- Declare a concept set.
- Specify prerequisite relations among concepts.
- Tag each record with the concepts it uses.
- Difficulty is prerequisite depth in the concept graph, combined with
  supersession depth from the finding two resolution.

**The confound is removed rather than measured.** No model assigns
difficulty, so the teacher's unvalidated judgment cannot become the
treatment. The assignment is independently checkable by inspecting the
graph.

**Why this over a reference-model loss.** A reference-model definition is
cheaper and is standard in the literature, which would have helped
comparability. But it makes difficulty a property of the reference model
rather than of the material, and the choice of reference model becomes an
unexamined parameter of the result. For a project whose claim is about
ordering, having the ordering defined by a model outside the experiment is
the wrong kind of dependency.

**Consequence. The concept graph becomes the main new deliverable**, ahead
of corpus generation, because nothing can be staged until it exists. It is
also an auditable artifact in its own right, which suits the project's
provenance goal.

**Pre-registration scope is extended** to include the concept graph, the
difficulty definition, and the curriculum specification, alongside the
metrics, effect size, seed count, and controls already listed.

## Serious

### 4. The budget does not close

Arithmetic against the recorded design, using six times parameters times
tokens and three dollars per accelerator-hour at an assumed 3e14 effective
operations per second.

| Component | Ideal compute |
| --- | --- |
| Ablation, 100M | $33 |
| Ablation, 300M | $300 |
| Ablation, 1B | $3,333 |
| Quantisation pilot | $90 |
| Subtotal | $3,757 |
| With 2.5x overhead | $9,392 |

Excluded from that figure. Corpus generation, the expert audit, kernel
estimation passes, the elenchos suite, storage, and time.

Question one characterised the research scope as five to twenty thousand
dollars. That does not survive, and if finding one forces twenty to thirty
seeds the ablation compute alone multiplies four to sixfold.

**The one-billion arm is 89 percent of ablation cost** and is the obvious
candidate if the design must be trimmed.

### 5. Multiple comparisons are unmanaged

Roughly six secondary measures across three scale points and two
conditions have accumulated. The records declare them secondary and
exploratory once and **specify no correction procedure**. With that many
comparisons, something will reach significance.

**To close.** State a correction procedure, or a pre-declared hierarchy in
which only the primary comparison is inferential and all others are
descriptive.

### 6. Nineteen cited papers, none read

Nineteen arXiv identifiers are cited across tracked records. **All nineteen
resolve**, verified by retrieval, so nothing is fabricated. But every
citation rests on a search-result summary rather than on reading the paper.

For a project whose stated differentiator is source-grounded claims with a
measured error rate, **its own documentation does not meet its own
standard.** This is the finding that would be led with if this project were
auditing someone else.

**To close.** Read the load-bearing citations, or downgrade the claims that
rest on them to explicitly second-hand.

### 7. The elenchos baseline may be a null instrument

Question eight describes measuring the target property on the ablation base
models as a nearly free second finding.

Sycophancy as ordinarily benchmarked requires an assistant persona
responding to user pressure. **A raw pretrained model has no such
persona.** The measurement may return noise, and the record oversells it.

**To close.** Establish what is measurable on a base model, which is
plausibly continuation sensitivity to a confidently asserted false premise,
and specify that instead of the conversational formulation.

## Moderate

### 8. Assertions used as premises without verification

Two claims were asserted from memory and then used as premises in records
that cite other things carefully.

- That consensus collapse is a documented failure mode of multi-agent
  systems, used to justify the verifier-seat positioning.
- A bandwidth figure used to justify choosing a language model over a
  classifier.

Both are plausible. Neither was checked.

### 9. Decision volatility is high and invisible to a new reader

Three decisions reversed within a single session. The framework went
settled, then open, then settled. The Jacobian went from instrumentation to
architecture objective, with a recorded convergence corrected to a
conflict. The low-bit deadline was asserted and then dissolved.

Revision histories record this honestly. **Nothing tells a reader which of
the remaining decisions have been pressure-tested and which are one session
old.**

**To close.** Mark each decision record with a confidence or maturity
indicator.

## Structural

### 10. Specification without implementation

Thirty-three files, nine decision records, no implementation. Several
records specify artifacts whose feasibility is unknown because nothing was
built, including the kernel effective-rank floor, the ordering index
format, and the four-layer verification stack.

The documentation is a maintenance liability that no code has validated.

### 11. Every quantitative claim is cited or estimated

Nothing has been measured on this project. The repository states this in
several places, which is to its credit, but the volume of specification
rests entirely on untested premises.

## What passes

Cross-references resolve. All cited identifiers resolve. `pyproject.toml`
parses. Line wrapping is intact. The term scan over tracked files is clean.

## Disposition

The initial commit proceeds. Committing a documented state is correct and
reversible, and the audit is more useful in history than held out of it.

Findings one, two, and three gate work on the affected components. They do
not gate the commit.
