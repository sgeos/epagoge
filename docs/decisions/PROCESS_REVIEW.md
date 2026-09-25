# Process review against the reference repository

**Decided 2026-09-25.** The operator's `keleusma` repository was this
project's reference when it was set up. It has moved a long way since, and
it was reviewed on the operator's instruction to find practice worth
pulling across. This record says what was taken, what was adapted, what
was rejected, and on what grounds.

**The durable outcome is `../process/PROCESS_STRATEGY.md`**, which did not
exist here. What follows is the reasoning for the shape of it.

## The finding that mattered most

**The reference repository documents a continuous-integration concurrency
defect that this project had introduced the same day.** Grouping runs by
`github.ref` with `cancel-in-progress` is correct for a pull request and
wrong for a workflow that also triggers on push, because a second push to
the default branch then cancels the first commit's run and leaves that
commit with no verdict of its own. The resume protocol here requires
checking continuous integration rather than assuming it, and a cancelled
run is not a green one. Fixed by keying a branch run on its own run
identifier, which cannot collide.

A review of a more mature sibling repository found a live defect that no
check here would have caught, roughly forty minutes after it was
committed. That is the argument for doing this periodically rather than
once.

## Taken, adapted to what this project does

**A reference check in the gate.** The reference repository gates on
markdown links resolving. This project writes four markdown links and 429
backticked paths, so a link checker would have gated one percent of the
references and reported success over the rest, which is the
silent-partial-coverage shape recorded throughout this project's history.
`tools/check_references.py` checks what the documents actually do.

Its resolution order is deliberately forgiving. A bare basename resolves
against any tracked file, because prose that says `validate_graph.py`
where the file is `tools/validate_graph.py` is followed without
difficulty. What the check is for is a file renamed or deleted while a
document still names it.

**`CHANGELOG.md` is exempt**, which is a decision and not an oversight. A
changelog entry naming a file deleted afterwards is historical rather than
wrong, and editing it to satisfy a checker would falsify the record.

**No by-name exception list.** A path the repository has decided not to
track is asked about with `git check-ignore` rather than listed here. The
reference repository records five separate failures from by-name
enumerations, and an exception list in a checker would be a sixth waiting.

**The public-facing files a published repository is expected to carry**:
`CONTRIBUTING.md`, `CITATION.cff`, `llms.txt`, a pull-request template,
and issue templates. The templates are specific to this project rather
than generic. A corpus submission and a request to admit a word are
separate forms, because admitting a word changes what every later book may
say.

**The distinction between durable practice and the current brief.** The
reference repository keeps them apart. Here the failure modes were
accumulating in `CURRENT_BRIEF.md`, which says on its own first line that
it is deleted when its completion condition is met. A list of failure
modes filed in a document marked for deletion is a list that will be
deleted.

## Taken as a principle rather than a mechanism

**Bounded currency over bounded size.** The reference repository split one
communication channel in two when it reached 362 KB, then watched the
replacement accrete back to the same shape, because sessions prepend
rather than rewrite. The property worth defending is that a reader can
tell what is true now, which is what `HANDOFF.md`'s validity check exists
for.

**A guard that has not been shown able to fail is not a guard.** Already
practised here and now written down. The reference check was shown failing
against an invented path before it was wired into the gate.

**Prefer a pattern to an enumeration.** Already satisfied in `.gitignore`,
where `curriculum/books/level_*/exclude/*` covers a level that does not
exist yet.

## Rejected, with grounds

**The release-branch model.** A version branch, feature branches,
sub-feature branches, and no-fast-forward merges serve a published crate
with releases and more than one concurrent agent. This project has one
operator, commits directly to `main`, and has no releases. The rule kept
is narrower: cut a branch when a change might turn the gate or continuous
integration red, which is what the workflow refresh did.

**Tiered verification.** The reference repository's gate takes about two
and a half hours, which makes the choice of what to run a real cost and
three tiers a real saving. This gate takes about nine seconds. Building a
fast path here would create the opportunity to skip the slow one and buy
nothing.

**Three communication channels.** A task log, a forward prompt, and a
reverse prompt serve a project with sprints and milestones.

**A pre-push hook.** It would duplicate a nine-second gate.

**Conventional commit scopes.** The house style is an imperative subject
saying what the commit does, with no prefix, and 153 commits are
consistent in it. Adopting scopes would make the log inconsistent to buy
machine-readability nothing here consumes.

## One place where the advice inverts

The reference repository's rule is that continuous integration must be a
**strict superset** of the local gate, verified step by step, which is
what makes it safe to be the authority.

**That containment cannot hold here.** The disclosure scan reads a pattern
this repository does not contain, so on a runner it announces a skip
and returns success. Publishing the pattern would publish the list of withheld
vocabulary, which is the thing being withheld.

**So the local gate is load-bearing and cannot be trimmed**, and
continuous integration is a check rather than the authority. Recorded
because the reference repository's reasoning is sound and adopting its
conclusion here would be wrong.
