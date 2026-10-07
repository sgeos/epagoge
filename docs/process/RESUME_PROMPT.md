Resume continuity in this existing working directory.

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

The latest scope is the era-overlap lexical batch described in the handoff
and in CURRENT_BRIEF.md. Its work was committed locally and was not pushed,
because publication was not authorized for that scope. Do not push without
asking. Determine actual publication from git and the remote rather than
assuming that a stamp proves it.

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
