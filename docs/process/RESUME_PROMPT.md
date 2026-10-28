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

The latest delivered scope is the Dromon trial brief of 2026-10-28, which
added a level-two lexicon batch and reviewed the level-two corpus. Its brief
and completion condition are marked met and are evidence, not instructions.
The reviewer's ten proposed definition changes were applied on the
operator's direction. The previous brief is
preserved in `evals/review/level_2_agency_02/`. The 2026-10-28 resume state
in the handoff is the authority for the revision, for publication, for the
Dromon trial, for the expected measurement-check failure, and for the
teacher. Earlier resume states are historical for the revision and for
publication. Ask before committing or pushing anything. Determine actual
publication from git and the remote rather than assuming that a stamp
proves it.

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
