# Corpus tracking

**Decided 2026-09-23 by the operator.** `corpus/` and `sources/` are
tracked in version control rather than ignored.

## The decision

The initial recommendation was to ignore both directories and resolve them
to external storage, on size grounds. The operator directed otherwise. The
decision stands, and the objection is recorded here rather than dropped so
that a later reader can tell the difference between a risk that was weighed
and one that was never seen.

## Benefit

Every generated record and every acquired source is reviewable and
attributable through history. For a project whose stated purpose is the
suppression of unsupported assertion, an auditable corpus is a substantive
benefit rather than a convenience, and it is not available under the
ignored arrangement.

## Accepted risks

**Size.** Measured at project creation, the host volume had 57 GiB free of
926 GiB, at 94 percent capacity. The estimate, not a measurement, is that
a corpus of ten billion tokens occupies on the order of 40 GB as plain
text at roughly four bytes per token. A corpus at pretraining scale will
not fit on this volume.

**Irreversibility.** Git Large File Storage is installed on this machine
but is **not** configured for this repository. Large files therefore enter
the object store directly. Removing them later requires a history rewrite,
which is disruptive for any clone. Configuring Large File Storage is
easiest before the first large commit and progressively harder afterward.
It was not configured unilaterally because it changes how files are stored
and is not cleanly reversible either.

**Licensing exposure in `sources/`.** Committing scientific literature
raises redistribution questions that have not been examined. Because the
directory is tracked, a licensing error enters history rather than staying
local. See `sources/README.md`.

## AMENDED 2026-09-24. The derived stream is ignored

**`corpus/` is now ignored for the same reason a build directory is.**

The original direction is not reversed. It was taken when `corpus/` was
going to hold the authored records, and the benefit it bought was that
every generated record is reviewable and attributable through history.
**That benefit is unchanged. It is now bought by the books.**

`curriculum/books/level_N/*.md` holds the authored prose and its
annotation, and is tracked. A stream under `corpus/` is rebuilt from those
books by `../../tools/build_corpus.py` under a chosen ordering. Tracking a
file that can be regenerated adds bytes without adding auditability, and
the same ordering argument means there is not one stream but one per
ordering.

`sources/` remains tracked. Terminal-stage literature is acquired rather
than derived and cannot be rebuilt.

**This removes most of the size exposure recorded above**, since the
derived stream is the large artifact and the books are the small one. The
Large File Storage question narrows to `sources/` alone.

The directory is kept in the tree by a `.gitkeep`.

## Open follow-up

Whether to configure Git Large File Storage, and whether `sources/` should
track document bodies or only identifiers and retrieval metadata. Both
remain unanswered.
