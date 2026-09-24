# corpus/

Generated corpus data, partitioned by curriculum stage.

**Status.** Empty. No record has been generated.

## Tracked in version control

This directory is deliberately not ignored, by operator decision of
2026-09-23. Every generated record is therefore reviewable and
attributable through history, which is the stated benefit.

Two consequences follow and are recorded so they are not rediscovered by
surprise.

**Size.** The host volume had 57 GiB free of 926 GiB at project creation.
Using the common approximation of roughly four bytes per token for English
text, a corpus of ten billion tokens occupies on the order of 40 GB as
plain text before any tokenized representation. A corpus at pretraining
scale will not fit. This is an estimate, not a measurement.

**Irreversibility.** Git Large File Storage is installed on this machine
but is not configured for this repository. Large files therefore enter the
object store directly, and removing them later requires a history rewrite.
Configuring Large File Storage is easiest before the first large commit and
progressively harder afterward.

## Format

Undecided. Newline-delimited JSON is the natural authoring format because
it is diffable and greppable, which is what tracking the corpus is for.
Parquet is the natural format for a compiled corpus handed to a data
loader. These are not mutually exclusive, and the pair has not yet been
specified.

## Record provenance

Every record should carry the generator, the teacher model and version, the
curriculum stage, the source it was derived from where one exists, and the
validation verdict that admitted it. A record without provenance cannot be
audited, and an unauditable corpus defeats the purpose of tracking it.
