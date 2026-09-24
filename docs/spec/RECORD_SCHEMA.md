# Corpus record schema

**Specified 2026-09-23.** The single authoritative definition of a corpus
record. Implementation in `../../src/epagoge/record.py`.

Before this document the fields were described across three prose files. A
generator cannot be written against prose, and the concept graph
demonstrated that specifying and enforcing are different activities with
different failure modes.

## Fields

| Field | Type | Required |
| --- | --- | --- |
| `id` | string | always |
| `level` | integer, 1 to 7 | always |
| `concepts` | list of concept identifiers | always, non-empty |
| `claim_class` | see `CLAIM_TAXONOMY.md` | always |
| `content` | string | always, non-blank |
| `provenance` | object | class-dependent |
| `simplification` | object | only when simplified |

### provenance

| Field | Required for |
| --- | --- |
| `source_claim` | formal, empirical |
| `position_holder` | attributed_position, normative |
| `contested_by` | optional, attributed_position |
| `assumptions` | conditional_result, non-empty |
| `method` | conditional_result |
| `validation_status` | conditional_result, including the absent case |

The on-disk shape is uniform and requirements are conditional on the claim
class. A uniform record with a validator beats five record types with five
parsers.

### simplification

| Field | Meaning |
| --- | --- |
| `kind` | none, omission, idealisation, superseded_model, analogy |
| `validity_scope` | level range over which the record holds |
| `superseded_by` | the record that corrects it |

## Rules enforced

**Per record.**

1. Level within range.
2. At least one concept, every concept resolving in the graph.
3. Content non-blank.
4. Claim class is never `unsupported`. That class exists so the validator
   can name the verdict, not so a record can carry it.
5. Class-specific provenance present.
6. A simplified record declares both a scope and a correction.
7. A simplified record's own level falls inside its declared scope.
8. **Terminal-level records carry no simplification.** Level seven draws on
   real literature and keeps strict entailment.
9. An unsimplified record declares neither scope nor correction.

**Across the corpus.**

10. Identifiers are unique.
11. Supersession resolves to an existing record at a strictly higher level.
12. **Prerequisite coverage.** A concept may not be taught before its
    prerequisites have been.

## Rule 12 is the level-assignment mechanism

Levels are **authored, not derived**. The seven levels choose a trajectory
through the partial order the concept graph supplies, and that choice
carries breadth, abstraction, and groundedness, none of which prerequisite
depth can express. See `../decisions/OPEN_QUESTIONS.md` item twenty-one.

Rule 12 is what keeps an authored level honest. For every concept, the
earliest level at which any record covers it must be no earlier than the
earliest level covering each of its prerequisites.

**Equal levels are permitted.** A prerequisite may be introduced at the
same level as its dependent, because ordering within a level still respects
the partial order. Only a strictly later prerequisite is a violation.

This is the whole of the level-assignment mechanism. There is no scoring
function and no model judgment. An author or generator proposes a level and
the validator rejects it if the graph says it is impossible.

## Storage

Newline-delimited JSON. One record per line, so that a corpus diff is
reviewable, which is the reason the corpus is in version control at all.

## What a rejection means

`validate_corpus` returns every violation and never raises. A corpus is
audited in one pass. Parsing raises, because a malformed file has no
partial reading worth reporting.
