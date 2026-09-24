# Process

Working practice for this repository.

**Status.** Minimal.

## Current practice

- **Run `tools/check.sh` before any commit that touches code.** It runs
  ruff lint, ruff format, pyright in strict mode, the tests, and seed-graph
  validation, and exits non-zero on any failure.
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
