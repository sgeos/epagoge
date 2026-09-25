# Process

Working practice for this repository.

| Document | What it holds |
| --- | --- |
| `HANDOFF.md` | The resume prompt, with a validity check to run before believing it |
| `PROCESS_STRATEGY.md` | Durable practice. Verification posture, failure classes, autonomy boundaries |
| `CURRENT_BRIEF.md` | The live brief. Deleted when `COMPLETION_CONDITION.md` is met |
| `COMPLETION_CONDITION.md` | The end state the current brief is working toward |

**The split between the last two and `PROCESS_STRATEGY.md` is the point.**
A failure mode recorded in a document marked for deletion is deleted with
it. Anything that outlives the current brief belongs in the strategy.

## Handoff

`HANDOFF.md` is the first thing a resuming session reads. It carries a
validity check that must be run before anything in it is believed, since a
handoff that has gone stale is worse than none.

Validate by ancestry and by content, never by a hash match.

## Current practice

- **Run `tools/check.sh` before any commit.** It gates ruff lint, ruff
  format, pyright in strict mode, the tests, a coverage floor of 95
  percent, graph and corpus validation, and the disclosure scan, and exits
  non-zero on any failure.
- **Tool versions in the gate are pinned.** A gate resolving `@latest` can
  pass today and fail tomorrow for reasons unrelated to the code, which is
  not a property a project about reproducibility should accept in its own
  process. Bump deliberately and record the bump.
- **The disclosure scan holds its pattern outside version control.** A
  tracked list of withheld vocabulary would publish what is being withheld.
  Absent the pattern the scan skips loudly rather than passing silently,
  which is why continuous integration enforces the code gate and not the
  disclosure discipline.
- Static analysis is configured in `pyproject.toml`. Pyright runs in strict
  mode and ruff carries the security ruleset. Zero warnings is the target
  and is currently met.

**Why the gate exists.** The static analysis had been configured since the
initial commit and had never been executed. On first run it reported
eighteen lint errors and eighteen type errors. A standard that is declared
and never checked is not a standard, and the gap was invisible precisely
because nothing ran.
- A decision that constrains later work gets a record in `../decisions/`
  before the work, not after it.
- Unmeasured claims are marked as unmeasured. See `../README.md`.
