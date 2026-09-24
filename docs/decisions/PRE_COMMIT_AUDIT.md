# Pre-commit adversarial audit

**Conducted 2026-09-23**, on the design and the tracked documentation,
before the initial commit. Adversarial in intent. Findings are recorded
whether or not they reflect well on the work.

Three findings are blocking, meaning each invalidates part of the design
rather than merely weakening it. Work should not proceed on the affected
components until they are closed.

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

**To close.** A power analysis precedes the pre-registration, with the
assumed effect size stated and justified from the literature rather than
chosen for affordability. Expect the seed count to rise substantially, and
expect that to change the budget and probably the scale points.

### 2. Source grounding contradicts the curriculum's defining feature

Question two makes entailment by a retrieved passage the floor, rejecting
any record whose claim exceeds what its source supports.

The curriculum's defining feature is simplified pedagogical content at
early stages. **Simplification produces claims that no source states
verbatim.** As written, the floor rule forbids the product.

This is an incompatibility rather than a tension, and neither record
acknowledges the other.

**To close.** Decide what grounding means for pedagogical simplification.
One candidate is entailment at the level of the underlying claim, with
simplification permitted and the claim traceable to a source even where the
wording is not. That is weaker and harder to check automatically, and the
weakening must be recorded rather than assumed.

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

**To close.** Define the difficulty metric operationally, validate it
independently of the model that will be trained on it, and add both the
metric and the curriculum specification to the pre-registration scope.

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
