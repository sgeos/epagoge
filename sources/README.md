# sources/

Terminal-stage literature. The unmodified scientific papers that constitute
the final curriculum level, together with whatever source material earlier
stages are derived from.

**Status.** Empty. No source has been acquired.

## Tracked in version control

Not ignored, by operator decision of 2026-09-23. The size and
irreversibility consequences recorded in `corpus/README.md` apply equally
here.

## Unaddressed constraint, stated rather than assumed

Committing scientific literature to a repository raises licensing questions
that have not been examined. Preprint server licences vary per item, and
open access does not uniformly grant redistribution. Publisher-hosted
versions of record are generally more restrictive than preprints. Nothing
here has been checked, and no acquisition policy exists.

This matters more than usual because the directory is tracked, so a
licensing error is committed to history rather than held locally, and
removing it later requires a history rewrite.

The practical mitigation, should it be wanted, is to track identifiers and
retrieval metadata rather than document bodies, and to resolve bodies at
build time into an ignored cache. That inverts the operator's decision for
this directory, so it is offered as an option and not applied.

## Provenance

Every source should carry its identifier, retrieval date, licence as
determined at retrieval, and a content hash. A source whose licence was
never determined should be recorded as undetermined rather than left blank,
because a blank field is indistinguishable from an unexamined one.
