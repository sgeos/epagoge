# Concept graph

**Specified 2026-09-23.** The graph that constrains curriculum ordering and
supplies structural difficulty.

Implementation in `../../src/epagoge/concept_graph.py`.

## What it is for

Three jobs, all of which must be machine-checkable.

1. **Constrain ordering.** Prerequisites give a partial order. No record may
   depend on a concept introduced later. Many total orders satisfy it, and
   the seven levels choose one. See `CURRICULUM_LEVELS.md`.
2. **Supply structural difficulty.** Prerequisite depth is a property of the
   graph, derived from no model, which is what removes the teacher-model
   confound recorded in `../decisions/PRE_COMMIT_AUDIT.md` finding three.
3. **Express transfer.** Inter-topic connection routes through a formal
   layer rather than being asserted directly.

## Node kinds

**Domain concept.** Belongs to exactly one domain. Carries prerequisites.

**Formal structure.** A mathematical or logical object that domain concepts
instantiate. Belongs to no domain, which is the point, since a structure
confined to one domain cannot carry transfer.

## Edge kinds

| Edge | From | To | Meaning |
| --- | --- | --- | --- |
| `prerequisite` | any node | any node | The source cannot be understood before the target |
| `instantiates` | domain concept | formal structure | The concept is an instance of the structure |

**Transfer edges are derived, never authored.** Two domain concepts in
*different* domains are connected by transfer exactly when they instantiate
a common formal structure. Same-domain sharing is not transfer, it is
ordinary structure within a subject.

This is what makes transfer checkable. Whether a concept instantiates a
structure is verifiable. A claimed resemblance is not.

## Invariants

Enforced by `validate`, which returns every violation rather than raising
on the first, so a graph can be audited in one pass.

1. Every edge endpoint resolves to a declared node.
2. The prerequisite graph is acyclic.
3. No self-loop on any edge.
4. `instantiates` runs from a domain concept to a formal structure, never
   in reverse and never between two nodes of the same kind.
5. A domain concept declares a domain. A formal structure declares none.
6. A formal structure has no prerequisite on a domain concept. The formal
   layer does not depend on the domains that instantiate it.

## Prerequisite depth is the longest path

Depth is the **longest** path from a root, not the shortest.

A concept is reachable only once every prerequisite is satisfied, so its
earliest admissible position is governed by its deepest dependency. Using
the shortest path would place concepts earlier than their own requirements
allow.

## Orderings

**Canonical order.** Deterministic topological sort, breaking ties by node
identifier. Reproducible across runs and machines, which the ablation
requires.

**Random linear extension.** The experimental control, per
`../decisions/OPEN_QUESTIONS.md` item twenty-one. Randomised Kahn's
algorithm, drawing uniformly from the available frontier at each step.

**Documented limitation.** This does **not** sample uniformly from the set
of linear extensions. Counting linear extensions of a partial order is
#P-complete, and frontier-uniform selection biases toward orderings that
keep the frontier wide. Uniformity over extensions is not required for the
control, whose purpose is to discard the curriculum trajectory while
respecting the constraints, but the bias is recorded rather than left for
someone to discover. If uniformity is ever required, it needs Markov chain
methods and a separate decision.

## Storage format

JSON, one node or edge per line when formatted, so that diffs are
reviewable. The corpus-tracking decision makes reviewability the reason the
data is in version control at all.

## What this does not contain

**Supersession** is a record-level relation, not a concept-level one. A
later record supersedes an earlier treatment of the same concept. It lives
in the record schema, not here.

**Levels** are not stored on concepts. A concept's admissible levels follow
from its prerequisite depth and from the trajectory chosen. Storing a level
would duplicate derived information and permit it to drift.
