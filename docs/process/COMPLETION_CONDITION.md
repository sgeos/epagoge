Ordering is not a completion criterion.

Met on 2026-10-25 and measured on the working tree. This file is
historical evidence. Do not treat it as an open task.

Every `mktemp` call in `tools/check.sh` and `tools/scrub_scan.sh` names an
explicit template inside the gate's scratch directory or inside `TMPDIR`.

`test_admission_is_valid_before_and_after_commit_and_fields_are_checked` in
`tests/test_handoff.py` creates no directory named `.git`, and it makes the
same assertions as before.

`tools/check.sh` exits 0 with no skipped tests both inside the Claude Code
sandbox on the authoring host and outside it, with core coverage at or above
the floor and a clean disclosure scan. Continuous integration is reported
separately for any published revision.

`AGENTS.md` and `docs/process/HANDOFF.md` state the Claude Code sandbox
result as measured, with its date, and no longer describe exporting
`TMPDIR` as sufficient for `mktemp` on this host.

Ordering is not a completion criterion.
