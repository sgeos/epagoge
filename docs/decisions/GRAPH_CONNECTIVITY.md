# Graph connectivity, and the metric that was measuring the wrong thing

**Recorded 2026-09-24.** The foundation-feed metric is retired and replaced
by four measures. The design question it was raised to answer is **not
settled here** and is stated at the end.

## What the old metric said

`validate_graph.py` counted prerequisites running outward from three named
domains and reported zero. That zero was carried as a known defect in the
handoff.

**It was measuring domain immaturity and reporting it as disconnection.**
The three domains hold fifteen concepts and **one** prerequisite edge
between all of them. They feed nothing outward because they have almost no
structure inward either. Drawing edges outward from them would be asserting
relations the content does not yet support.

The metric also assumed those three domains were foundations that other
domains rest on. The domain restructure removed that assumption. They are
now peer domains named for activities, each running to level seven, and
each mostly unwritten.

## What replaced it

Four measures, each reporting a defect as a number rather than as silence.

| Measure | Today | What a bad value means |
|---|---|---|
| Isolated concepts | **16 of 78** | The node carries no edge in any layer, so it contributes vocabulary and no structure |
| Cross-domain prerequisites | **0 of 72** | Zero asserts every domain is teachable without any other, which is a strong claim and more likely means the edges are undrawn |
| Specialisation edges | **1** | The layer `anchor_reach` measures is effectively empty, so that metric currently reports nothing about anything |
| Inert formal structures | **2 of 6** | A structure needs two instantiations to yield a transfer edge. One or none is a declaration carrying no load |

## What the measures found

**Sixteen concepts carry no edge of any kind.** Six in
`directed_physical_interactions`, four in `record_keeping`, three in
`agentic_operations`, two in `compressed_communication`, and `quantity` in
`mathematics_and_formal_logic`. The last three are outside the domains the
old metric watched, so they were invisible to it.

**The specialisation layer holds one edge in the whole graph**, `toy` to
`household_object`. `anchor_reach` was built to measure what a concept
gives concrete access to through that layer. It returns zero for
seventy-seven of seventy-eight nodes, which is a property of the layer
rather than of the concepts. **A metric reading zero everywhere is
indistinguishable from one that is not running**, and this is the second
time that failure shape has appeared in this project.

**Two formal structures are inert.** `directed_acyclic_graph` and
`error_detecting_code` are each instantiated once, so neither can produce a
transfer edge. `error_detecting_code` is the structure a
`cybernetic_biological_systems` concept would instantiate, which is an
argument for that domain and not a defect in this one.

## Resolved 2026-09-24. Option one, with a correction the measurement forced

**Twenty-six cross-domain prerequisites are drawn.** The graph previously
held none, which asserted that every domain is teachable without any other.
That assertion was false rather than clean. All sixteen isolated concepts
now carry edges and the count is zero.

**Including the edge the ablation design forbade.** A hazard rate is a
rate, so `hazard_rate` requires `rate_of_change` and the edge is drawn.
Routing it through the formal layer to keep the domains apart would have
recorded something false to protect an experiment.

### The correction the measurement forced

Drawing the edges **broke the premise of the domain pair**, and this was
not anticipated when the option was recommended.

Global prerequisite depth for failure analysis rose from 6 to 9 against
mathematics at 10. The pair was chosen to differ maximally in prerequisite
depth, and a contrast of one is not maximal.

**Global depth stopped describing what it was being used for.** It measures
distance from a root, so once domains are connected it rises for every
domain downstream of a deep one. It had been serving as a proxy for a
domain's internal structure, which it only is while the domains are
disconnected.

**Within-domain depth is the quantity the design actually needs**, and it
is invariant under all twenty-six additions.

| Domain | Internal | Global |
| --- | --- | --- |
| `mathematics_and_formal_logic` | **10** | 10 |
| `failure_analysis` | **6** | 9 |

`validate_graph.py` prints both, because they answer different questions
and the difference is now load-bearing.

### One concept is excluded from the experiment, not from the graph

`hazard_rate` is the **only** failure analysis concept whose prerequisite
closure reaches mathematics, and through it twelve mathematics concepts
entered the failure analysis arm. It is excluded from the ablation corpus
and declared in `../../evals/PRE_REGISTRATION.md` amendment 2.

**The graph records what is true. The pre-registration declares what the
experiment covers.** Excluding a concept from an experiment and saying so
is ordinary. Omitting a true edge from the graph would not be.

With it excluded the arms share three concepts, `change`, `duration`, and
`sequence`. Those are level-one anchors both arms need, and sharing them is
desirable, since the contrast under test is what each arm builds above its
grounding.

### What must be re-checked

Any new cross-domain edge into failure analysis must be tested for whether
its closure reaches mathematics. The check is cheap and its failure is
silent, which is the combination that gets skipped.

### Two proposed edges were wrong, and the corpus is what said so

Thirty edges were drafted. **Two were withdrawn after the corpus validator
rejected them**, which is the level-assignment mechanism doing the job it
exists for.

`falling` was given a prerequisite on `direction`. A child sees falling
well before learning that down is a direction, and the sample corpus
teaches falling at level one and direction at level three. The edge
inverted the actual order.

`emptiness` was given a prerequisite on `presence`, which the corpus also
rejected. **That one was right and the corpus was wrong.** Absence
presupposes something being there. The sample taught `presence` only at
level five, so a level-one record was added and the edge restored. The
distinction matters, since one case was a bad edge and the other was a
thin corpus, and only running the validator told them apart.

### The cascade the edges caused, which is the mechanism working

Drawing true edges made the sample corpus invalid in four ways. It taught
`hazard_rate` without any record teaching a rate, and `person` without any
record teaching that some things are living.

Eight records were added, closing the chain from addition through
subtraction, multiplication, variable, division, and function to
`rate_of_change`, plus records for living things and for presence. Four
vocabulary terms were added and every one is bounded below by where its
concept is taught.

**This is the graph and the corpus constraining each other in both
directions**, which is what they are for. The sample corpus grew from
twenty records to twenty-eight because the graph started asserting more.

## What the specialisation layer still is

**One edge, and unchanged by this work.** `anchor_reach` still returns zero
for seventy-seven of seventy-eight nodes. Left alone deliberately, because
forcing specialisations onto a thin layer would produce the same kind of
assertion the cross-domain absence was. It fills when content exists.
