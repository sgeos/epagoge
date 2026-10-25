# Brief

Met 2026-10-25. The condition holds on the working tree. This file is
historical evidence. Do not repeat it.

Opened 2026-10-25. The operator directed that the two sandbox fixes found
when Claude Code first resumed this tree be applied. The previous brief and
condition are retained in `evals/review/level_2_scan_10/`.

## Operator direction

Apply the sandbox fixes.

## Findings that define the scope

On 2026-10-25 `tools/check.sh` exited 1 inside the Claude Code sandbox on
`7cd961f` and exited 0 outside it, with 678 tests and no skips. Each cause
was reproduced in isolation.

**`mktemp` without a template ignores `TMPDIR` on this host.** Run with
`TMPDIR` set inside the workspace, it still created its file under
`/var/folders`, which the sandbox denies. An explicit template inside the
workspace succeeded. The gate exports `TMPDIR` for this purpose, so the
calls at its corpus and export steps, and the file list in
`tools/scrub_scan.sh`, defeated that export.

**The sandbox denies writes to `.git/config` and `.git/hooks` at any
depth.** A test that runs `git init` in a temporary directory therefore
failed. A repository whose git directory has another name, selected through
`GIT_DIR` and `GIT_WORK_TREE`, initialised and committed inside the
sandbox.

## Recommended work

Give every `mktemp` call in the gate scripts an explicit template under the
gate's scratch directory or under `TMPDIR`. Point the provenance test at a
git directory that is not named `.git` through the environment, which
`tools/word_provenance.py` inherits. Record Claude Code alongside Codex and
Grok Build in the sandbox notes once the gate has been measured inside its
sandbox.

## Wrong turns to avoid

Do not skip the test inside a sandbox, because the gate refuses skipped
tests and a skip would hide the check. Do not widen the sandbox to make the
gate pass. Do not change what the provenance test asserts.
