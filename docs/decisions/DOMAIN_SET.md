# The domain set

**Decided 2026-09-24.** Eleven domains, declared in
`curriculum/graph/concepts.json` rather than inferred from which concepts
happen to exist. Seven are populated and four await content.

This supersedes the seven-domain set that preceded it. The earlier names
are kept in `CHANGELOG.md` and in the history below, because several were
withdrawn for reasons that constrain future additions.

## The naming rule, which produced most of the set

**A domain named for an activity excludes whatever does not serve the
activity. A domain named for a bare field admits everything in the field.**

`philosophy_of_science` excludes ethics and metaphysics without anyone
policing it. `civilization_and_society` admits world history, culture, and
kinship, after which the exclusion has to be performed by hand in every
authoring decision. The first name does the work. The second delegates it
to a reviewer who will not always be present.

Specialisation and activity-naming turned out to be the same property
rather than two. An activity has a purpose, so the name carries the
exclusion. A field has an extent, so the name carries everything in it.

Ten of the eleven names are activities or bounded fields under this rule.
Mathematics and formal logic is the deliberate exception, discussed below.

## The set

| Domain | Scope |
|---|---|
| `mathematics_and_formal_logic` | Quantity, structure, and proof, with propositional and predicate logic |
| `failure_analysis` | How systems fail, how a cause is isolated from a correlate, and how failure is anticipated |
| `directed_physical_interactions` | How matter behaves and how it is made to behave differently |
| `compressed_communication` | Conveying a claim when the whole of it cannot be conveyed |
| `record_keeping` | Measurement, reference frames, unit accounting, provenance, accuracy, precision, confidence, and currency |
| `agentic_operations` | Goal-directed execution against the world |
| `accounting` | Tracking and reconciliation of flows |
| `history_and_philosophy_of_science` | How a claim is justified, and how knowledge actually developed |
| `institutional_interfacing` | Adversarial claim evaluation and the institutional context that makes it necessary |
| `cybernetic_biological_systems` | Living systems as control systems |
| `normative_adjudication` | Settling between competing obligations |

`institutional_interfacing` carries its own scope record in
`INSTITUTIONAL_INTERFACING.md`, because its scope is what prevents it
inverting into the failure it teaches readers to detect.

## Four are declared and empty

`history_and_philosophy_of_science`, `institutional_interfacing`,
`cybernetic_biological_systems`, and `normative_adjudication` hold no
concepts. The graph follows content, so concepts arrive when records teach
them. Adding nodes no record teaches would encode guesses where changing
them is most expensive.

**Declaring them anyway is the point of the registry.** A domain set
inferred from node membership cannot distinguish a domain awaiting content
from one nobody decided on, so the gap would be invisible exactly when it
most needs to be visible. `validate_graph.py` reports the count.

## Mathematics and formal logic

**The rename is safe. The addition it implies is not yet made.**

The ordering ablation depends on domain membership, on the depth contrast
of ten against six, and on the absence of any prerequisite between the two
ablation domains. A label change moves none of those, so the partition is
identical and the depth contrast is unchanged at ten against six. No
re-measurement was required for the rename and none was performed.

**Adding formal logic concepts is a pre-registration amendment**, recorded
as such in `../../evals/PRE_REGISTRATION.md`. It is legitimate now because
no data exists, and it would not be legitimate after the first run. The
depth contrast must be measured again when those concepts land rather than
assumed, since logic sits below arithmetic and would probably deepen the
domain.

**Formal logic only.** Informal logic, meaning argument evaluation,
fallacy recognition, and the difference between a valid inference and a
persuasive one, belongs to `institutional_interfacing`, which already
presupposes it. Pulling argumentation into a frozen ablation domain would
put it in the treatment arm of an experiment that is not about
argumentation.

The name also accepts a cost. Mathematics is a domain other published
ordering ablations have used, and a bespoke domain is harder to place
beside them. Naming formal logic explicitly limits that cost, since formal
logic is uncontroversially part of mathematics.

## Boundaries that are not readable from the names

Three pairs sit close enough that the boundary is recorded rather than
inferred.

**`record_keeping` against `accounting` and `compressed_communication`.**
Accounting asks whether the quantities reconcile. Record keeping asks
whether the record is faithful. Compressed communication has a reader.
A record persists with no reader and must survive one arriving late.

**`cybernetic_biological_systems` against `agentic_operations`.** One
keeps the system viable against perturbation, the other accomplishes a
task against the world. Homeostasis maintains and operations change. The
test per concept is whether it concerns keeping the system running or
getting something done. Overlap at self-repair is expected and permitted.

**`institutional_interfacing` against `normative_adjudication`.** The
first contests is-claims through assent, attack, defence, and concession.
The second adjudicates ought-claims. `ClaimClass` already separates
`NORMATIVE` from the rest, so the line exists in code before it exists in
the curriculum.

## Undirected phenomena inside a domain named for direction

Four concepts in `directed_physical_interactions` are phenomena rather
than interactions. Falling, change, presence, and emptiness. Nobody
directs falling.

They belong as **the premises that license an interaction**. Rocks fall
here, therefore build elsewhere. The air here is corrosive, therefore seal
the housing. The span between the two sites is mostly empty, therefore
transport is cheap and slow. The observation-then-consequence move is what
the domain teaches, and the phenomena are its first half.

This also sharpens the boundary against
`history_and_philosophy_of_science`, which owns whether the observation is
justified, where this domain owns what to do about it once it is.

## Names considered and withdrawn

Recorded because the reasons constrain future additions rather than
because the history is interesting.

| Withdrawn | Why |
|---|---|
| `everyday` | A grab bag. Split into three foundations, then renamed again here |
| `physical_world`, `space_and_time`, `agency` | Bare subject areas. None named what the model does with the material |
| An `Operations` suffix on those three | Right about the pattern, wrong about the targets. A crayon, a duration, and a need are not activities, so the suffix was cosmetic |
| `civilization_and_society` | Admits world history, culture, and kinship. The exclusion would have been manual and permanent |
| `faithful_simplification` | Simplification is an operation on a model. Idealisation, superseded model, and analogy are modelling moves, so the name would have claimed the territory of modelling and simulation without mentioning it |
| `faithful_compression` | Compression alone is a solo operation with no receiver, and the receiver is the domain |
| `constraint_optimised_communication` | Optimisation names no invariant. Faithfulness is the thing that must not be traded, and a marketing slogan satisfies the name completely |
| `technical_communication` | Narrows by subject matter rather than by honesty, so persuasion passes it |
| `technical_analysis_under_constraints` | Collides with failure analysis, and analysis is work done alone |
| `teleological_normativity` | Names a metaethical position rather than a subject, and asserts as settled what `CLAIM_TAXONOMY.md` requires to be attributed |
| `mandated_obligations` | Picks the authority account of obligation, and excludes obligations that follow from function rather than from instruction |
| `hierarchical_reasoning` | Collides with hierarchical planning and decomposition in machine learning, and carries no normativity |
| `normative_impact` | Points at consequences, which is the consequentialist account asserted as the frame |

**The pattern across the last four.** Every candidate for the normative
domain pre-committed to where obligations come from. Function, authority,
position, or outcome. `normative_adjudication` is neutral on the source,
which matters because the conflict between sources is the domain's
substance. The mandate says one thing, the function implies another, the
chain of authority is unreachable, and something must be decided.

## Scope review, 2026-09-24. Every domain read against its own scope note

Prompted by finding that `record_keeping`, whose scope names measurement
and provenance and currency, held five concepts that were all spatial or
temporal. **That gap survived three passes because each pass asked whether
a candidate concept was already covered, and none asked whether a domain's
declared scope was.**

Each of the eleven scope notes was read against the concepts its domain
holds. Two domains were missing the thing they are named for.

| Domain | Scope element with no level-one concept | Added |
| --- | --- | --- |
| `compressed_communication` | **leaving something out** | `leaving_out`, and `word` and `letter` |
| `agentic_operations` | **a goal**, procedure, completion | `goal`, `doing_in_order`, `finished_or_not` |
| `record_keeping` | confidence, currency | `how_sure`, `out_of_date` |
| `accounting` | conservation, named in the scope | `same_amount` |
| `normative_adjudication` | obligation from one's own word, fairness | `promise`, `fair_and_unfair` |
| `history_and_philosophy_of_science` | a claim held before it is checked | `guess` |
| `directed_physical_interactions` | joining and separating | `joining_and_separating` |
| `cybernetic_biological_systems` | adequate | none |
| `institutional_interfacing` | adequate | none |
| `failure_analysis`, `mathematics_and_formal_logic` | frozen, not reviewed for additions | none |

### The two worth naming

**Compressed communication had no concept of omission.** The domain is
named for conveying a claim when the whole of it cannot be conveyed, and
nothing in it named the part that gets dropped. Every concept it held was
about the conveying.

**Agentic operations had no goal.** A domain named for goal-directed
execution, holding a person, an activity, a need, a capability, a method, a
feeling and a sufficiency, and no target state to execute toward.

Both are the same failure as record keeping having no record.

### What went in as a node and what went in as a plan

`word` and `letter` are nodes, because 文 and 字 attest them the way the
other kanji-derived concepts are attested, and `name` now specialises
`word` the way `metal` specialises `material`.

**Everything else went in as `introduces`.** Those concepts are derived
from my reading of a scope note rather than from an external standard,
which is weaker evidence, and the graph follows content. They become nodes
when records teach them.

### This review is not automatable and is not scheduled

It requires reading prose against identifiers. No check will catch the next
instance of it, and the next instance will look exactly like these three
did, which is to say invisible until someone reads the scope note and the
concept list side by side.

## Known gaps in the set

Stated so they are not discovered later as omissions.

**Five manifest topics remain without a home.** Game theory, economics,
modelling and simulation, and policy and governance. Formal logic is the
fifth and is resolved here. Game theory is mathematics, and mathematics
is frozen, so it cannot go to its natural home before the ablation.

**The set is weighted toward method over subject.** Five domains teach how
to know, check, and convey. Three carry substance and one is mixed. That
is the project's thesis made visible and it is deliberate. It predicts a
model that evaluates claims well and knows comparatively little about the
world.

**Absent entirely.** Arts, literature, languages, and geography. None is
an oversight.
