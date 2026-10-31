Resume continuity in this existing working directory. This prompt is written
for any agent, including Codex, Grok Build and Claude Code.

Read AGENTS.md, CLAUDE.md and docs/process/HANDOFF.md. Run the handoff validity
check and distinguish verified state from stale claims or unavailable host
artifacts. Read the private code-name instructions required by CLAUDE.md
before editing tracked prose. Preserve local work and ignored host artifacts.

Use the latest explicit user task and the current tree to determine what
remains. After compaction, continue unfinished work from the transcript.
In a fresh session, use the handoff task status and inspect subsequent
changes. A completed CURRENT_BRIEF.md and COMPLETION_CONDITION.md are evidence
of delivered work, not instructions to repeat it. Historical handoffs and
recommendations do not authorize new scope. If no unfinished task remains,
report the verified state and readiness for the next task.

The project is in the holding state of 2026-10-31. No implementation
scope is open, and the holding brief and its completion condition are
evidence, not instructions. All work, including that of the fourth to
seventh Dromon trials, is committed and in `main` on the remote. The
concerns awaiting the operator are consolidated in
`docs/process/OPEN_DECISIONS.md`. That list proposes options and decides
nothing, so do not start any item of it without the operator's choice. The
revised generator draft of the second trial follow-up is ignored and
unapplied. The holding section of the handoff is the authority for the
revision, for publication, for the Dromon trials and for the teacher.
Earlier resume states are historical and are kept in
`docs/process/HANDOFF_HISTORY.md`.
Ask before committing or pushing anything. Determine actual publication
from git and the remote rather than assuming that a stamp proves it.

If a subsequent task requests a new recommendation and implementation,
establish a new brief and completion condition for that scope. Preserve the
previous artifacts as historical evidence. The condition must remain under
4000 characters, describe observable tree properties and explicitly state
that ordering is not a completion criterion. It must impose no task-order,
branch or process requirements.

Keep experimental, licensing and later-schedule decisions reserved to the
operator. Confirmatory training remains blocked. Run the full gate before
any commit, inspect its exit status, and check continuous integration
separately for the published revision. Report actual results and limitations.
