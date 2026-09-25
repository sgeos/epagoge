# Pre-registration

**Status: INCOMPLETE. Opened 2026-09-23.**

**This document must be complete and committed before the first ablation
run.** Several decisions across the repository defer to it. Its purpose is
to fix every choice that could otherwise be adjusted after results are
seen, which is the only thing separating a falsifiable experiment from a
narratable one.

Items are marked **FIXED** where decided, or **PENDING** with the
dependency that unblocks them. A pending item is not a gap in the design.
It is a value that must be measured rather than chosen, and choosing it now
would be the error this document exists to prevent.

## 1. Hypothesis

**FIXED.** Difficulty-graded curriculum ordering improves pretraining
relative to an ordering that respects the same constraints but discards the
curriculum trajectory.

**Stated referent.** The seven levels bundle breadth, depth, abstraction,
and groundedness. Depth is named the primary axis so the claim has a
referent. The bundling is a documented confound, not a decomposed one.

## 2. Primary endpoint

**FIXED 2026-09-24. Final held-out loss.**

The pilot measured its behaviour and found no reason to substitute
something else. Paired, its standard deviation is 0.0233 against a mean of
1.895, which is about 1.2 percent.

**Nondeterminism floor.** Identical inputs run twice differed by 0.00075 on
Metal Performance Shaders. That bounds the smallest resolvable effect on
that hardware regardless of seed count, and must be re-measured on whatever
accelerator the ablation uses.

## 3. Conditions

**FIXED, with a third arm added 2026-09-24.**

| Condition | Ordering |
| --- | --- |
| Treatment | The curriculum trajectory across seven levels |
| Control | A random topological ordering, fresh per seed |
| **Null arm** | **Two random topological orderings against each other** |

**Why the null arm exists.** The variance pilot found a systematic
difference between two orderings that should be equivalent, seven of eight
pairs in one direction, and a diagnostic showed the sign followed the
ordering rather than the execution position. Marginal at roughly p = 0.04
and unexplained.

That is the exact shape of a false positive. The null arm measures the
pipeline's baseline spurious difference, and **the curriculum effect must
exceed the null arm rather than merely exceeding zero.**

The control respects prerequisites while discarding the trajectory, so the
comparison is the curriculum against an arbitrary valid ordering rather
than against an invalid one. A free shuffle was rejected as close to a
tautology.

**Pairing.** Treatment and control share an initialisation and share the
data within a pair. Order is the only difference.

## 4. Domains

**FIXED.** Mathematics and failure analysis, each at full depth across all
seven levels.

**Amendment, 2026-09-24.** The mathematics domain is renamed
`mathematics_and_formal_logic` and will admit formal logic concepts.

Recorded as an amendment rather than as an edit because item four is fixed.
It is legitimate at this date for one reason only, which is that **no run
has happened and no data exists**. The same change after the first run
would not be legitimate and must not be made.

The rename alone changes nothing the design depends on. Domain membership
is identical, the depth contrast is unchanged at ten against six, and the
two ablation domains remain free of any prerequisite between them. This was
checked rather than assumed, and the graph currently holds zero
cross-domain prerequisites of any kind.

**Admitting formal logic concepts will change membership**, and the depth
contrast must be measured again at that point rather than carried forward.
Logic sits below arithmetic and would probably deepen the domain, which
would widen the contrast rather than narrow it. Probably is not a
measurement.

**Informal logic is excluded** and belongs to `institutional_interfacing`.
Argument evaluation and fallacy recognition are not mathematics, and
pulling them into the treatment arm would put argumentation inside an
experiment that is not about argumentation.

**A cost is accepted.** Mathematics is a domain other published ordering
ablations have used and a bespoke domain is harder to place beside them.
Naming formal logic explicitly limits the cost without removing it.

**Amendment 2, 2026-09-24. The corpus, the excluded concept, and the
difficulty measure.**

Cross-domain prerequisites were drawn into the graph for the first time.
Twenty-six of them. The graph previously held none, which asserted that
every domain is teachable without any other, and that assertion was false
rather than clean. Recorded in `../docs/decisions/GRAPH_CONNECTIVITY.md`.

**This broke a premise of item four and the measurement is why we know.**
Global prerequisite depth for failure analysis rose from 6 to 9 against
mathematics at 10, collapsing the contrast the domain pair was chosen for.
The cause was traced to exactly one edge.

**Structural difficulty is now measured as within-domain depth.** Global
depth measures distance from a root, so it rises for every domain sitting
downstream of a deep one. Once domains are connected it describes where a
domain sits rather than how it is built. Internal depth is invariant under
the twenty-seven additions and preserves the contrast the design rests on.

| Domain | Internal depth | Global depth |
| --- | --- | --- |
| `mathematics_and_formal_logic` | **10** | 10 |
| `failure_analysis` | **6** | 9 |

**The corpus is each domain plus its prerequisite closure**, so that each
arm is a closed set rather than a domain with dangling prerequisites.

**One concept is excluded from the failure analysis arm. `hazard_rate`.**

A hazard rate is a rate, so it genuinely requires `rate_of_change`. The
edge is drawn in the graph because it is true. But it is the **only**
failure analysis concept whose closure reaches mathematics, and through it
alone twelve mathematics concepts entered the failure analysis arm. Leaving
it in would put a large part of one arm inside the other.

**The distinction this rests on.** The graph records what is true. The
pre-registration declares what the experiment covers. Excluding a concept
from an experiment and declaring the exclusion is ordinary. Omitting a true
edge from the graph to protect the experiment would not be, and was
explicitly rejected.

**Resulting arms.**

| | Concepts | Own | Mathematics inside it |
| --- | --- | --- | --- |
| Mathematics arm | 30 | 26 | n/a |
| Failure analysis arm | 27 | 19 | **0** |

The arms share three concepts, `change`, `duration`, and `sequence`. These
are level-one anchors both arms need, and sharing them is desirable rather
than contamination, since the contrast under test is in what each arm
builds above its grounding.

**Amendment 3, 2026-09-24. The ablation orders books.**

Operator decision. The unit of ordering is the **book**, not the record.

**A book's internal order is never shuffled.** The narrative is the reason a
book exists. Shuffling inside one would destroy the thing the ordering
hypothesis is about while claiming to test it.

**The topological constraint therefore holds between books.** Book B
depends on book A when B teaches a concept whose prerequisite is taught in
A and not in B. `book_prerequisites` derives that relation from the concept
graph, and both arms are linear extensions of it.

| Arm | Ordering |
| --- | --- |
| Treatment | **Derived**, shallowest ready book first, by prerequisite depth |
| Control | A **random linear extension**, fresh per seed |

**The treatment arm is derived and not authored.** Taking it from the file
order gave an alphabetical sequence that broke two book dependencies, which
is not a curriculum in any ordering and would have been the treatment arm of
an experiment about ordering. The build refuses an order that breaks a
dependency.

**The control is a random linear extension and not a random permutation.** A
permutation can put a book teaching counting before the book teaching same
and different, which is not a curriculum under any reading. That control
would be weaker than this design asks for rather than merely different.

### A risk this creates, unmeasured

**The orderable set is much smaller than it was.** With records as the unit
there are very many valid orderings. With books there are far fewer, and
with heavily constrained books fewer still. At five books, three of them
constrained, the control arm has almost no room to vary.

Level one is scheduled at 83 topics, so the full set is larger. **It is
still smaller by orders of magnitude than the record-level set the seed
count was estimated against.** Whether the treatment and control arms
remain distinguishable at that granularity has not been measured, and the
variance pilot did not test it because books did not exist when it ran.

**This is the sharpest open risk to the design** and it follows from a
decision that is otherwise clearly right.

**What must be re-measured if any of this changes.** Any new cross-domain
edge into failure analysis must be checked for whether it reaches
mathematics, and the arms recomputed. The check is cheap and the failure is
silent, which is the combination that gets skipped.

Chosen to differ maximally in prerequisite depth, which is the hypothesised
mechanism. The strongest available outcome is a dissociation, since an
effect in the deep-structure domain with a null in the flat-structure one
would be evidence that prerequisite depth is the mechanism.

## 5. Scale points

**PROVISIONAL** pending the variance pilot.

**Maximal update parametrization is required for these points to be
comparable at all.** Without it each scale has different optimal
hyperparameters, and any scale-dependence in the ordering effect could be an
artifact of mis-tuning rather than a property of scale. See
`../docs/decisions/TRAINING_TECHNIQUES.md`. Roughly 100M, 300M, and 1B
parameters at Chinchilla-style token ratios. Allocation across points is
set by measured variance, and the one-billion arm is the obvious candidate
if the design must be trimmed, since it is the large majority of cost.

## 6. Seed count

**MEASURED 2026-09-24, PROVISIONAL pending re-measurement at target scale.**

The pilot ran at 818,000 parameters on a synthetic stream, single-epoch. See
`pilot/README.md`.

| Quantity | Measured |
| --- | --- |
| Unpaired sigma | 0.0750 |
| Paired sd | 0.0233 |
| Correlation rho | 0.9539 |
| Pairing gain | 20.7x seeds, free |

| Target effect | Paired | Unpaired | Plan with |
| --- | --- | --- | --- |
| 2.0% | 3 | 62 | 5 |
| 1.0% | 12 | 246 | 19 |
| 0.5% | 48 | 984 | 73 |

**Pairing is vindicated beyond what was estimated.** Twelve paired seeds
beat two hundred and forty-six unpaired ones. The original five-seed
unpaired design was off by two orders of magnitude in efficiency, not
merely underpowered.

**The number to fix is pending re-measurement**, because the correlation is
the quantity most likely to move between a synthetic stream at 818,000
parameters and a real corpus at target scale.

**Re-measured on the level-one corpus 2026-09-25, after two harness
defects were found and closed.** Over 44,505 tokens and eight paired
seeds, rho is **0.9574** against the pilot's 0.9539 and the pairing gain
is **22.8x** against 20.7x. **The pilot's central finding transfers to
real text**, which was the thing it was least confident about.

**The seed count still cannot be fixed**, because the paired standard
deviation moved by a factor of five between eight hundred and sixteen
hundred steps, and item 10's endpoint is not chosen. Two earlier readings
on this corpus, rho 0.9993 and 0.9936, are withdrawn: they were taken
while the chunker was discarding three quarters of the corpus and the
ordering was covering thirteen books of a hundred and forty-six. See
`pilot/LEVEL_ONE_VARIANCE.md`.

**A second reason to re-measure, added 2026-09-24.** The pilot ran under
AdamW with cosine decay. `../docs/decisions/TRAINING_TECHNIQUES.md` adopts
maximal update parametrization, the Muon optimiser, and a
warmup-stable-decay schedule. Changing the optimiser and schedule changes
the training dynamics, so sigma and rho do not carry over.

## 7. Minimum meaningful effect

**PENDING** the variance pilot. Must be stated in the pilot's measured
units and justified from the literature rather than chosen for
affordability.

## 8. Failure condition

**FIXED.** The project fails if the result is **inconclusive**, meaning the
observed difference falls within seed-to-seed variance.

A negative result is a deliverable. Learning that ordering does not help,
cleanly and with the control to demonstrate it, is a finding.

## 9. Secondary measures, and their status

**FIXED that they are secondary.** They may generate a hypothesis. They may
not rescue an inconclusive primary result.

- Tangent-kernel effective rank
- Relative kernel change from initialisation
- Kernel-target alignment
- Cross-domain gradient alignment
- Weight-perturbation sensitivity
- Anti-sycophancy baseline on the trained base models

**Correction procedure: PENDING.** Only the primary comparison is
inferential. Every secondary measure is descriptive and reported without a
significance claim. This is the default and is recorded here so that it
cannot be revisited after results are seen.

## 10. Estimator choices

**PENDING, and demonstrated to be load-bearing 2026-09-25.** The exact
tangent kernel is intractable at scale. Subsampling scheme, probe-set
size, and estimator must be fixed here before any run, because an
estimator chosen after seeing a curve is a choice about the result.

**The endpoint belongs in this item and it is not a formality.** On the
level-one corpus, holding the corpus, the arms and the seeds fixed and
changing only the step count from eight hundred to sixteen hundred moved
the curriculum arm from worse in eight seeds of eight to better in seven
of eight. Both readings would pass a naive paired test. Whoever picks the
endpoint picks the sign of the result, so it is picked here, in advance,
and in writing.

The probe set is held fixed and identical across conditions.

## 11. Corpus acceptance

**PARTIALLY FIXED.**

- Residual error rate is measured by sampled expert audit and reported
  **per domain**, never aggregated. FIXED.
- The ceiling that admits a corpus to the experiment: **PENDING**. It
  cannot sensibly be chosen before the first audit establishes what rate is
  achievable.
- **A size floor is now known to be necessary and is PENDING.** Measured
  2026-09-25, the completed level-one draft is 7,998 tokens, which is a
  factor of 125 below the low end of its own token budget, and an ordering
  comparison on it is degenerate rather than merely underpowered. Whatever
  the residual error ceiling turns out to be, a corpus below some size
  cannot enter the experiment at all, and that size is not yet fixed.

## 12. Effective-rank floor

**PENDING** the first measurements. The floor is the quantity that decides
whether a deployment constraint is admissible. Choosing a number before any
graph or model exists would be arbitrary; the procedure is fixed now and
the number is fixed once measurable.

## 13. Quirk boundary

**FIXED.** Recorded so that quirk cannot absorb a negative result.

| Quirk, accepted | Failure, not accepted |
| --- | --- |
| Unusual register | Systematic factual error |
| Narrow stylistic range | Degenerate repetition |
| Odd idiom | Mode collapse |
| Gaps in cultural knowledge | Failure to parse real input |

## 14. Reproducibility

**FIXED.**

- Bitwise determinism is unavailable on graphics processing units under
  either candidate framework. The design does not rely on it.
- The ordering is emitted as an explicit versioned artifact before
  training, so order is exactly reproducible even where arithmetic is not.
- Every run records its seed, its ordering artifact hash, its corpus hash,
  and its concept-graph hash.

## What unblocks the pending items

| Item | Unblocked by |
| --- | --- |
| 2 | **Done 2026-09-24** |
| 6 | **Measured 2026-09-24**, provisional pending target scale |
| 7 | The minimum effect, still to be justified from the literature |
| 5 | Allocation, once the seed count is final |
| 9 correction, 10 | Decision, once the endpoint is fixed |
| 11 ceiling | The first corpus audit |
| 12 | The first kernel measurements |

**The variance pilot was the single largest unblocker and has run**, on
2026-09-24 against a synthetic stream. The sentence that stood here said
it depended on nothing and was the largest unblocker; it predated its own
result and is kept in that form nowhere.

**What remains is scale.** Re-measurement on the level-one corpus was
attempted on 2026-09-25 and produced a degenerate result, so the quantity
that has to move next is corpus size rather than seeds, optimiser or
design. See `pilot/LEVEL_ONE_VARIANCE.md`.
