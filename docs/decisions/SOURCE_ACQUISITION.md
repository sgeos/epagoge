# How terminal-stage sources would be acquired, drafted before they are

**Drafted 2026-09-27 on operator direction.** **This is a speculative
scheme, not an adopted one.** The standing position is deferral. No source
has been acquired, `sources/` is empty, and the tracking direction of
2026-09-23 remains in force. What this record buys is that the scheme exists
before the first acquisition rather than after it.

## Why draft it now when the decision is deferred

**The cost of choosing is not symmetric in time.** While `sources/` is empty,
adopting a metadata-only scheme is an edit to a readme and one ignore rule.
After bodies have been committed, adopting it requires rewriting the history
of a public repository, and the branch ruleset binds the owner, so the
rewrite is a settings change followed by a force push.

**History here has already been rewritten twice**, on 2026-09-25, and every
commit hash in the repository changed both times. The project knows the cost
of that operation from measurement rather than from estimation.

**So the speculative draft is the cheap half of the decision** and the
adoption is the part that waits.

## The scheme, if it is adopted

**Track the manifest. Do not track the bodies.**

A tracked manifest names each source. Bodies are resolved at retrieval time
into an ignored cache under `sources/`, the way the derived stream under
`corpus/` is rebuilt rather than carried.

### What a manifest entry would carry

| Field | Why it is there |
| --- | --- |
| Identifier | A resolvable name, such as a digital object identifier or an archive identifier |
| Retrieval date | The licence at retrieval is the licence that applied, and licences change |
| Licence as determined at retrieval | Determined, not inferred from the host |
| Redistribution | One of permitted, not permitted, or undetermined |
| Content hash | So a re-resolved body can be checked against the one that was read |

**`undetermined` is a value and not a blank.** A blank field cannot be
distinguished from an unexamined one, which is the defect this project has
recorded in other shapes. A source whose licence was never determined is
recorded as undetermined and is not read until it is determined.

**Redistribution is recorded separately from the licence** because the two
questions differ. Open access does not uniformly grant redistribution, and a
publisher-hosted version of record is generally more restrictive than a
preprint of the same work.

## The precedent, which is this scheme already working

**The research literature vendored during the spikes of 2026-09-27 is
exactly this pattern.** Papers sit in ignored `tmp/references/papers/` and
the tracked record is `REFERENCE_SOURCES.md`, which carries the links and the
retrieval date. Independent work can pull the same references. Nothing
third-party entered history.

That was adopted for a different reason, namely keeping a scratch directory
out of the repository, and it demonstrates the mechanism rather than the
policy.

## What this record does not decide

**It does not invert the 2026-09-23 direction.** `sources/` stays tracked.
Adopting this scheme would change that, and the change is not made here.

**It adds no machinery.** There is no manifest file, no schema in
`docs/spec/`, and no validator, because there is nothing to validate and a
validator for an empty directory is scaffolding rather than verification.

**It does not settle the licensing status of derived records.** Whether a
terminal-stage record that restates a copyrighted paper can carry CC0 is
recorded as open question twenty-five in `OPEN_QUESTIONS.md` and is
untouched here. That question survives either scheme, because it is about
what the project writes rather than about what it stores.

**It does not name an acquisition policy.** Which sources, from where, and
under what selection rule are all open.

## What would trigger the decision

**The first acquisition.** Adoption is cheap until a body is committed and
expensive afterward, so the decision belongs immediately before the first
retrieval and not after it.

**One mechanical step is taken now rather than then.** `sources/bodies/` is
ignored, so a body placed there cannot be committed by accident before the
decision is taken. That is a guard rather than an adoption, and the
directory does not exist.
