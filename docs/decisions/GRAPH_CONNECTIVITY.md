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

## The open question, which is the operator's

**Do true cross-domain prerequisites get drawn into the ablation domains.**

The graph holds zero cross-domain prerequisites, and both ablation domains
are fully prerequisite-self-contained. That self-containment is what makes
a two-domain ablation corpus a closed set.

**Several real prerequisites appear to run across that boundary.** A stock
and flow is change in a quantity over time, and `change` and `quantity`
live in other domains. A hazard rate is a rate, and `rate_of_change` is in
mathematics while `hazard_rate` is in failure analysis, which is the one
crossing the ablation design forbids outright.

Shared *structure* across that boundary is already handled honestly. The
formal layer carries it, which is why `hazard_rate` and
`exponential_function` yield a transfer edge without a prerequisite between
them. That mechanism is correct for shared structure.

**It is not correct for a genuine prerequisite.** Routing a real ordering
dependency through the formal layer to keep two domains apart would be
recording something false to protect an experimental design, which is the
failure this project exists to oppose, arriving in the project's own data.

### The two ways out

**Draw the edges and redefine the ablation corpus as the two domains plus
their prerequisite closure.** The corpus stays closed, the graph stays
honest, and the closure pulls in the level-one anchors both domains need
anyway. The depth contrast must be measured again, and pre-registration
item four needs a second amendment. Legitimate only while no data exists.

**Keep the two domains self-contained and accept that some true
prerequisites go undrawn.** Cheaper and it protects a fixed design, at the
cost of a graph that records less than is known.

**Neither is chosen.** Nothing has been drawn either way.

## What is not blocked by that question

The sixteen isolated concepts are mostly isolated because their domains are
unwritten rather than because of any policy about the ablation. Writing
those domains is what connects them, and the graph follows content.
