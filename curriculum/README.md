# curriculum/

Authoritative stage specifications. This directory defines what each
curriculum level teaches, at what complexity, and how a record at that
level is recognised as belonging to it.

**Status.** Empty. No stage has been specified.

## What belongs here

A specification per stage, stating the concept coverage, the complexity
band, the admissible record forms, and the acceptance criteria that a
generated record must satisfy to be placed at that stage. Specifications
are documents. Machine-readable manifests derived from them are also
appropriate here.

## What does not belong here

Generated records. Those live in `corpus/`. Code that produces them lives
in `generators/`.

## Topic coverage

Coverage weighting is supplied by the coverage manifest, which is an input
to the generation pipeline.

Coverage weighting decides what is written about. It never licenses a claim
to exceed its evidence.

## Difficulty is structural. Decided 2026-09-23

Difficulty is **prerequisite depth in a declared concept graph, combined
with supersession depth.** No model assigns it.

- Declare a concept set.
- Specify prerequisite relations among concepts.
- Tag each record with the concepts it uses.
- A concept is **revisited** when a later record supersedes an earlier one
  through the supersession pointer in the record schema, which is a
  structural fact rather than a judgment.

**The concept graph is the main deliverable and is ahead of corpus
generation on the critical path.** Nothing can be staged until it exists.

Rationale and the rejected alternatives are in
`../docs/decisions/PRE_COMMIT_AUDIT.md`, finding three.

## Record schema fields this requires

Required, not annotations added later.

| Field | Purpose |
| --- | --- |
| `concepts` | Concept tags, which fix prerequisite depth |
| `source_claim` | Resolvable source for the underlying claim |
| `simplification` | Kind applied: omission, idealisation, superseded model, analogy |
| `validity_scope` | Stage range over which the record holds |
| `superseded_by` | The later record that corrects it |

Terminal-stage material drawn from real literature keeps strict source
entailment and carries no simplification label.

## Open constraint

The number of stages remains unspecified, though it is now derivable from
the depth of the concept graph once that graph exists.
