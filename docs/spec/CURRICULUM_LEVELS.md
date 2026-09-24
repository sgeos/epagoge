# Curriculum levels

**Specified 2026-09-23.** Seven levels, labelled by educational stage.

## The levels

| # | Level | Treatment |
| --- | --- | --- |
| 1 | Preschool | Emergent understanding |
| 2 | Elementary | Core knowledge to function, and foundation for later learning |
| 3 | Middle | Broad, simple descriptions of topics and collections of topics |
| 4 | High school | Broad, full treatment of topics |
| 5 | Undergraduate | Deep, full treatment of specialised topics |
| 6 | Graduate | Hyper-specialised treatment of topics |
| 7 | Post-graduate | Real-world problems |

## Rationale for the shape

Narrow, shallow, and concrete at the first level, because capacity to grasp
anything wider does not yet exist. The second level builds on that
foundation with moderate breadth.

**The third level is the inflection point**, where broad breadth and mixed
abstraction both become available.

From there **breadth is progressively traded for depth** through
specialisation, before the final level applies the result to messy
real-world problems.

## The levels bundle four axes

They do not vary along one dimension, and the axes do not move together.

| Level | Breadth | Depth | Abstraction | Groundedness | Genre |
| --- | --- | --- | --- | --- | --- |
| 1 | narrow | shallow | concrete | idealised | exposition |
| 2 | moderate | shallow | concrete | idealised | exposition |
| 3 | broad | shallow | mixed | idealised | exposition |
| 4 | broad | moderate | formal | idealised | exposition |
| 5 | narrow | deep | formal | idealised | exposition and problems |
| 6 | very narrow | very deep | formal | idealised | exposition and problems |
| 7 | broad | deep | formal | **messy** | **problems** |

**Breadth is not monotonic.** It widens to level three, narrows through
specialisation, then widens again at level seven because real problems are
cross-domain. That is an hourglass. **Depth is the only monotonic axis.**

**Consequence for the ablation, recorded as a documented confound.** The
independent variable is order. Because a level bundles four axes, a
positive result establishes that this trajectory beats shuffling without
establishing which dimension did the work. Full decomposition would
multiply the arms beyond budget. **Depth is named as the primary axis** so
that the claim has a stated referent.

**Two properties worth making explicit.** The final level changes genre
from treating topics to posing problems, which matches both the
terminal-stage design and the deployment need. Groundedness is deferred to
the end, mirroring how simplification is handled elsewhere in the design.

## Every topic appears at every level, as enabling material

**Nominal coverage of all topics at all levels.** At low levels this means
covering the enabling primitives rather than the formal discipline.

| Practice domain | Level one form |
| --- | --- |
| Failure analysis | Things break. Living things die. Doing X causes Y |
| Auditing | Check your work. Is that true. Who said so |
| Logic | If then. All, some, none. Two things cannot both be so |
| Philosophy of science | How do you know. Let us find out |
| Modelling | A drawing stands for a thing. A map is not the place |

**This resolves open question twenty-three**, the practice spine's mapping
onto levels. The spine does not enter at a floor level. It appears at every
level in a form appropriate to that level.

## Training to level one is a pipeline validation

Recorded 2026-09-24, because the framing determines how the result is
judged.

**A model trained on level one alone will be poor by construction.** One to
ten million tokens of picture-book content produces something that can say
things break and count to three. Judged as a model, the result would
support a wrong conclusion.

**The deliverable is a working loop**, meaning generate, validate,
tokenise, train, evaluate, with a model as the byproduct that proves the
loop runs. Framed that way it is valuable whatever the model turns out
like, and it de-risks everything downstream for a small fraction of the
eventual cost.

It also makes open question twenty-two answerable almost for free. Train on
level-one axioms, train on an equal budget of non-curriculum simple text,
and compare. That is the axiom-seeding question.

### Tokenisation for level one. Byte-level

Vocabulary 256, no dependency, no tokeniser-training step, fully
reproducible. Level-one content is simple English and the cost is sequence
length, which does not matter at this scale.

This defers the tokeniser question rather than answering it prematurely,
and `../architecture/TRAINING_SPINE.md` already treats tokenisation as a
neutral artifact, so changing it later is contained.

### Sequence

1. Ground the axioms. Done, see `../decisions/PRIMITIVE_REGISTER.md`.
2. Expand the concept graph to cover level one for both domains.
3. Generate one hundred records, validate them, **and read them.** If they
   are bad, everything downstream is bad, and an hour has been spent rather
   than a million tokens.
4. Scale generation only once a hundred records survive reading.
5. Byte-level tokenise, train, evaluate.

**Throughput, not cost, is the binding constraint.** At roughly thirty-five
tokens per second locally, one million tokens is about eight hours,
improving several-fold with concurrent requests. Level one is a few hours
to a couple of days of wall time.

## Level one seeds civilisational axioms

The first level is not teaching content. It installs **the primitives that
later content presupposes and never states.**

Human learners acquire many of these from embodiment or from being told.
That a street is dangerous is not innate knowledge, it is taught. A model
has no innate anything, so every such primitive must be present in the
corpus or absent from the model.

This is a better specification than "emergent understanding" and it is the
operative definition of level one.

**It sharpens open question twenty-two rather than closing it.** Humans
require explicit instruction on danger. A language model might absorb the
same thing diffusely from any corpus mentioning streets and danger. The
question is whether explicit, early, isolated axiom-seeding beats implicit,
diffuse absorption, which is the curriculum hypothesis restated at the
axiom level.

## The spiral, and the edge type it requires

Material covered at early levels is repeated and iterated upon with greater
complexity later. Early levels bootstrap topic mastery and, intendedly,
inter-topic mastery.

**Vertical repetition is already in the design**, since the supersession
pointer in the record schema is exactly that relation.

**Horizontal connection is not.** Inter-topic mastery is the recognition
that a structure in one domain is the same structure in another, which is
a different relation from supersession. The concept graph therefore
requires **analogy or transfer edges alongside prerequisite edges.**

**It has an instrument already specified.** Transfer between topics is what
cross-domain gradient alignment measures, which is in the Jacobian
instrumentation. Inter-topic mastery is therefore observable in the kernel
rather than only inferable from downstream behaviour.

## Corpus construction

**Levels one to six are entirely synthetic and built to purpose**, the
purpose being the training of this model. Level seven draws on real
literature.

Two consequences.

**Licensing largely dissolves.** Redistribution questions apply only to
level seven. They do not arise for the great majority of records by count.

**The developmental analogy motivates the shape of the ladder without
dictating its content.** Human curricula are shaped by child development,
attention spans, and classroom logistics, none of which apply here. The
question for level one is not what the text equivalent of preschool is. It
is which low-complexity content best initialises this model, and the answer
need not resemble material written for children.

## Token distribution

The corpus is not evenly divided across levels. Early levels are small
because the material at those levels is short. A picture book contains few
words.

| Level | Order of magnitude |
| --- | --- |
| 1 | 10^6 to 10^7 |
| 2 | 10^7 to 10^8 |
| 3 | 10^8 |
| 4 | 10^8 to 10^9 |
| 5 | 10^9 |
| 6 | 10^9 |
| 7 | 10^10 and unbounded |

**Estimates from word counts, not measurements.** Roughly three to four
orders of magnitude from first level to last.

**This partially resolves open question twenty**, along the level axis
only. Levels do not each receive a seventh of the budget. The topic-breadth
half of that question is untouched and still gates corpus generation.

## The hypothesis is a claim about the first one percent of tokens

Everything before level four is a rounding error in the total.

That appears to weaken the curriculum hypothesis and plausibly does the
opposite. If ordering acts by shaping the tangent kernel, per
`../decisions/JACOBIAN_SPACE.md`, the shaping happens early and does not
require much data. It requires the correct data first. A small early phase
with a large effect is what the kernel-shaping mechanism predicts, and the
kernel instrumentation already specified would detect it directly.

The token distribution and the proposed mechanism are therefore consistent,
which is mild evidence for both.

**Optional control, not required.** A third arm using unstructured
low-complexity text in the early position would separate whether the effect
comes from the content of early data or merely from low-complexity data
arriving first. Recorded as an option because arms are expensive.

## Quirk is accepted, within a declared boundary

The model is expected to be quirky, and low-level synthetic iterations
especially so. This is accepted.

**It has positive value.** A model distinctly unlike frontier generalists
is more complementary to them, which serves the positioning in
`../decisions/COLLABORATIVE_POSITIONING.md`. Uniformity would be
anti-differentiating.

**The condition is a declared boundary.** Accepted in advance and
unbounded, quirk absorbs any negative result. The model failed the
evaluation, but it is quirky. That is the unfalsifiable move this project
exists to prevent, and it is more dangerous coming from the operator than
from the model.

| Quirk, accepted | Failure, not accepted |
| --- | --- |
| Unusual register | Systematic factual error |
| Narrow stylistic range | Degenerate repetition |
| Odd idiom | Mode collapse |
| Gaps in cultural knowledge | Failure to parse real input |

The boundary belongs in the pre-registration, fixed before results are
seen, alongside the effect size and the seed count.

## Spin-off artifacts. An option preserved, not a goal pursued

A staged curriculum with labelled simplifications and their corrections is
structurally a textbook series. Extraction for human readers is therefore
feasible, and would supply an external quality signal independent of the
model.

**Two tensions.** It pulls back toward human pedagogy, which the
built-to-purpose decision deliberately freed the corpus from. Content
optimised for human engagement carries narrative padding that is probably
worse training data, and content adequate for training may be unreadably
repetitive.

**It is also a disclosure channel.** Publishing the curriculum exposes
topic weighting to any reader, and which topics receive published material
is itself informative. This interacts with the project's positioning
discipline and must be a deliberate decision rather than a side effect.

**Posture.** Keep records self-contained and well-formed enough that
extraction remains cheap. Let no corpus decision be driven by human
readability. Preserving the option is nearly free. Optimising for it is
not.

## Risk. The early corpus may be too clean

Real text is noisy, contradictory, and varied in register. Purpose-built
text tends to be uniform. A model shaped entirely on tidy material may be
brittle against real input.

Level seven supplies real literature at the end, which mitigates this. But
the early phase is where the kernel is being shaped, so uniformity there is
not obviously harmless.

**No evidence either way.** Recorded as a risk rather than a finding.

## The ablation corpus is a declared subset

The full manifest describes the eventual production corpus. The corpus for
the ordering experiment covers **mathematics and failure analysis at full
depth across all seven levels**, chosen so that the two differ maximally in
prerequisite depth, which is the hypothesised mechanism.

Mathematics has the deepest and cleanest prerequisite chains available and
is machine-verifiable, so corpus quality is not a plausible confound.
Failure analysis is case-based and near-flat in prerequisite structure,
since one investigated failure rarely depends on another.

**Ordering within a domain is constrained, not free.** Prerequisites and
supersession give a partial order. The seven levels choose one trajectory
within the feasible set. The control is a random topological ordering,
which respects prerequisites while discarding the curriculum trajectory, so
the comparison is the curriculum against an arbitrary valid ordering rather
than against an invalid one.

See `../decisions/OPEN_QUESTIONS.md` items twenty and twenty-one.

## Open questions this scheme raises

Recorded as open questions twenty-one, twenty-two, and twenty-three in
`../decisions/OPEN_QUESTIONS.md`. Reconciliation with the structural
difficulty definition, the status of level one, and the mapping of the
practice spine onto these levels.
