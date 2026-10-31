# Brief

Delivered 2026-10-31. The clauses of the condition about the tree held
before the holding commit. Its clauses about the remote can only be
observed after the merge, so this file does not attest them. Determine
them from git and the remote. This file is historical evidence. Do not
repeat it.

Opened 2026-10-31. The operator asked that the project be brought into a
nominal holding state, that all work be committed, pushed and merged, and
that the concerns needing a decision be consolidated with the obvious
choices for each. The seventh trial's brief and condition, met on
2026-10-30, are preserved in `docs/process/trials/dromon_trial_7/`.

## Meaning of a holding state

A holding state is one a later session can resume from without inferring
unfinished work. No implementation scope is open. Every piece of work is in
`main` on the remote, and no branch, pull request, worktree or uncommitted
tracked change is left over. No Dromon line or teacher is running for this
project. The handoff carries a fresh stamp on a verified base and says that
a resuming session waits for the operator's next task.

## Recommended work

**The handoff is restamped** on the commit that took the trial work into
`main`, and the superseded resume states and stale status sections move to
`HANDOFF_HISTORY.md`, so the handoff states the current position first.

**The concerns are consolidated** in `OPEN_DECISIONS.md` under
`docs/process/`. Each names the decision, where it is recorded, what waits
on it, and the obvious choices. The list proposes options and decides
nothing. Choosing among them is reserved to the operator.

**The holding commit lands** through a pull request merged by rebase, after
the gate passes, and continuous integration is checked on the pull request
and on `main`.

## Wrong turns to avoid

Do not start any item of the decision list. Do not load the teacher, fetch
text or start a Dromon line. Do not change the curriculum, the generators
or the tools. Do not dismiss Dependabot alerts by hand. Do not restore the
local Dromon project file without the operator's choice.
