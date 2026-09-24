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

## Open constraint

The number of stages, the complexity metric that separates them, and the
criterion by which a concept is judged to have been revisited rather than
merely repeated are all unspecified. These are not implementation details.
A pipeline cannot be written without them.
