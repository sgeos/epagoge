# Enabling concepts and level scheduling

**Recorded 2026-09-24.** Two connected observations that change how levels
are assigned.

## The kanji model. Placement is scheduling, not only dependency

Japanese education assigns kanji to grade levels, with roughly two thousand
expected by the end of secondary school. **Some appear where they do because
they need to be introduced somewhere and that level had room**, not because
that is the earliest point at which they are needed.

The schedule solves a distribution problem under two constraints the
concept graph does not express.

**Capacity.** A level can introduce only so much before it stops being that
level.

**Completion.** Everything must be introduced by the end, so a concept
cannot be deferred indefinitely on the grounds that nothing needs it yet.

Prerequisites give a partial order and say what *cannot* come before what.
They do not say where anything *should* go among the many orderings that
satisfy them. **Level assignment is therefore a scheduling problem over the
partial order**, and the seven levels are one schedule among many.

This is not currently implemented. Levels are authored and checked against
prerequisite coverage and the vocabulary ceiling. Capacity and completion
are unmodelled, and are recorded here as the shape the assignment should
eventually take.

## The crayon. Concrete concepts earn their place differently for a model

A crayon is a tool small children use. **A level-one model has no use for
one.** It will never hold a crayon, and nothing at level one requires the
concept.

But a crayon is paraffin wax. Paraffin wax is a lightweight hydrocarbon,
solid at room temperature, and paraffin-based hybrid rocket fuels have
flown. Verified 2026-09-24: Stanford and Lockheed Martin flew paraffin
hybrids in 2003 to 4,600 and 1,670 metres, a Stanford student vehicle
reached 2,871 metres in 2004, and paraffin achieves regression rates three
to four times those of conventional HTPB.

**So a concept with no use at a low level can be an enabling concept for a
high one.**

### The divergence from human pedagogy this exposes

A human curriculum introduces crayons **because children use crayons**. The
concept earns its place by immediate relevance to the learner's life.

A model has no life. A concrete concept earns its place at level one only as
**the cheapest concrete anchor for a chain that matters later.**

This is the built-to-purpose decision reaching further than expected. The
developmental progression gives the shape of the ladder. It does not select
the content, and selecting content by what a human child finds familiar
would fill level one with objects that anchor nothing.

## Two metrics, because one measures the wrong direction

| Metric | Answers | Measures |
| --- | --- | --- |
| `downstream_reach` | What depends on this? | Foundational importance |
| `anchor_reach` | What does this give access to? | Anchor value |

**The first is the wrong measure for an anchor.** An anchor is a leaf.
Nothing depends on a crayon, so its downstream reach is zero, which is also
the teddy bear's. The two are indistinguishable by that measure.

`anchor_reach` follows specialisation edges forward to the abstractions a
concept instantiates, then counts everything resting on those. In the
worked example under `examples/enabling_chain.json`, a crayon anchors six
concepts and a teddy bear anchors none.

**That is the argument for including a concept made countable.** A concrete
concept with no immediate use and no anchor reach has no case at all.

## The edge this required

`specialises`, linking a concrete concept to a more general one. Distinct
from the two edges already present.

| Edge | From | To |
| --- | --- | --- |
| `prerequisite` | any | any. Cannot be understood before |
| `instantiates` | domain concept | formal structure. Shared mathematics |
| `specialises` | domain concept | domain concept. Concrete instance of |

A crayon does not *require* paraffin wax and does not share a formal
structure with it. It **is** one, and that is a third relation.

## The relation is content, not only structure

**A specialisation asserted in the graph must be taught in the corpus.** A
graph that says a teddy bear is a toy, with no record teaching it, asserts a
link the model never reads. The corpus is what the model sees.

Enforced. A record covering both endpoints teaches the relation, and an
untaught specialisation is a violation. Nothing further is required of the
record, because a declaration field would let a record claim to teach a
relation it does not.

### The asymmetry is the part that must be taught

A teddy bear is a toy. **A toy is not necessarily a teddy bear.**

That is the same structure as a square being a rectangle while a rectangle
need not be a square. One-directional implication is a level-one primitive
underpinning all later classification, and **it is invisible in an edge that
merely points.** An edge records the direction. Only content can teach that
the converse fails.

## A correction. Transfer does occur at level one

An earlier note held that no transfer edges at level one was "exactly right
pedagogically, since transfer requires abstraction and level one is
concrete."

**That was wrong.** Teddy-bear-is-a-toy and square-is-a-rectangle
instantiate the same formal structure, proper class inclusion. That is a
cross-domain transfer edge between an everyday concept and a mathematical
one, available at level one, and the existing machinery derives it without
modification.

It is also how children actually acquire classification, which the earlier
note managed to reason past.

## A second correction. The teddy bear was not a useless anchor

The worked example used a teddy bear as the concept with no anchor value,
against a crayon with six.

**It was valueless only because its edges were not drawn.** A teddy bear is
a toy, a toy is a proxy model of something real, and a proxy model leads to
representation and simulation. With those edges the teddy bear anchors four
concepts and enters the modelling spine.

The lesson generalises and is uncomfortable. **A low anchor-reach score may
mean the concept is not worth teaching, or it may mean the graph is
incomplete.** The metric cannot distinguish them, and treating a zero as a
verdict rather than a question would prune concepts for being
under-described.

## What remains unresolved

Capacity per level is unmodelled, so nothing prevents a level from being
overloaded. Completion is unchecked, so a concept needed at level six can be
introduced nowhere and only surface as a prerequisite violation. Both belong
in the scheduling work this document describes and neither exists.

## Sources consulted 2026-09-24

- Scale-up tests of high regression rate paraffin-based hybrid rocket fuels,
  https://web.stanford.edu/~cantwell/Selected_Publications/Liquifying%20hybrid%20fuels,%20hybrid%20rocket%20design,%20small%20thrusters,%20propulsion%20designs%20for%20Mars/Scale-up%20tests%20of%20high%20regression%20rate%20paraffin-based%20hybrid%20rocket%20fuels%20JPP%202004.pdf
