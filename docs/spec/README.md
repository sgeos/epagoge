# Specifications

Authoritative specifications for record formats, curriculum stages, and
validation contracts.

## Contents

- `CLAIM_TAXONOMY.md` classifies every record by what it claims and how
  that claim is verified. Specified 2026-09-23.
- `CURRICULUM_LEVELS.md` specifies the seven complexity levels, the four
  axes they bundle, the corpus construction method, and the token
  distribution across them. Specified 2026-09-23.

- `RECORD_SCHEMA.md` is the single authoritative definition of a corpus
  record, with the rules the validator enforces. Specified 2026-09-23.
- `CONCEPT_GRAPH.md` specifies the graph that constrains ordering and
  supplies structural difficulty. Specified 2026-09-23.

**Status.** The specifications an implementation can be written against now
exist. Its required fields are fixed by decisions of
2026-09-23 and listed in `../../curriculum/README.md`. They cover concept
tags, the resolvable source claim, the simplification kind, the validity
scope, and the supersession pointer.

The curriculum stage definitions in `../../curriculum/` are authoritative
for pedagogical content. This directory is authoritative for the formats
and contracts that carry it.
