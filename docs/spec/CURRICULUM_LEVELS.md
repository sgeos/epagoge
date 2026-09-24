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

## Risk. The early corpus may be too clean

Real text is noisy, contradictory, and varied in register. Purpose-built
text tends to be uniform. A model shaped entirely on tidy material may be
brittle against real input.

Level seven supplies real literature at the end, which mitigates this. But
the early phase is where the kernel is being shaped, so uniformity there is
not obviously harmless.

**No evidence either way.** Recorded as a risk rather than a finding.

## Open questions this scheme raises

Recorded as open questions twenty-one, twenty-two, and twenty-three in
`../decisions/OPEN_QUESTIONS.md`. Reconciliation with the structural
difficulty definition, the status of level one, and the mapping of the
practice spine onto these levels.
