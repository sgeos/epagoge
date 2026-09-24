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

### Seven levels. Decided 2026-09-23

Complexity levels are specified in `../docs/spec/CURRICULUM_LEVELS.md`.
Levels one to six are synthetic and built to purpose. Level seven draws on
real literature. The token distribution across levels is power-law rather
than uniform.

### Per-level vocabulary. Decided 2026-09-24

Levels one to six are bounded by a vocabulary; level seven is unrestricted.
Two rules, both checked. A record uses no word admitted above its level, and
every word admitted at a level appears somewhere in that level.

Specification in `../docs/spec/VOCABULARY.md`. The catch worth knowing is
that the check is lexical and not conceptual: a record can pass it while
teaching the wrong thing.

### Two spines. Decided 2026-09-23

Coverage runs along two orthogonal axes rather than one.

**A subject spine**, covering what the model reasons about.

**An epistemic-practice spine**, covering how the model reasons, checks,
and revises. Its members are domains whose content is the discipline
itself, teaching how a conclusion follows, what can be known and where the
limits are, where a representation applies, how something is established,
and how one discovers one was wrong.

**The practice spine is arguably the actual curriculum**, with subject
content as the substrate it operates on. Its members are logic, philosophy
of science, modelling and simulation, auditing and verification, and
failure analysis, with mathematics supplying the formal layer through which
transfer edges route.

A record belongs to one spine or both, and the two are proportioned against
each other deliberately rather than by accident of what was easy to
generate.

Subject-spine coverage is not enumerated here.

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

## Claim classification

Independently of its place in the progression, every record is classified
by what it claims and how that claim is verified. See
`../docs/spec/CLAIM_TAXONOMY.md`. The classes are formal, empirical,
attributed position, conditional result, normative, and unsupported, the
last of which is always rejected.

A record carries both a curriculum position and a claim class. They are
independent.

## Attributed-position records. Added 2026-09-23

A third record type, alongside simplified and terminal-stage records.

Some material is **interpretive and contested**, where competing positions
are not resolvable by citation. For such material the verifiable claim is
that a named thinker or school held a position, not that the position is
correct.

| Field | Purpose |
| --- | --- |
| `position_holder` | Whose position this is |
| `position` | What is claimed |
| `contested_by` | Competing positions, where they exist |

A record asserting a contested interpretive claim as settled fact is
rejected. Without this rule, coverage of interpretive domains would teach
the model to assert contested claims confidently, which is the failure this
project exists to prevent.

## Conditional-result records. Added 2026-09-23

A fourth record type, for computed and simulated results.

A simulated result is a derivation from assumptions, not a measurement. Its
bearing on the world depends on validation, and the standard distinction
applies. Verification asks whether the equations were solved correctly.
Validation asks whether the correct equations were solved.

| Field | Purpose |
| --- | --- |
| `assumptions` | What the result is contingent on |
| `method` | The model or computational method used |
| `validation_status` | Whether validated, and against what, including the absent case |

A record of the form "the model shows X" without assumptions and
validation status is rejected. Such phrasing is among the most reliable
sources of claims that sound empirical and are not.

## Open constraint

The number of stages remains unspecified, though it is now derivable from
the depth of the concept graph once that graph exists.
