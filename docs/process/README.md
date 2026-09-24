# Process

Working practice for this repository.

**Status.** Minimal.

## Current practice

- Static analysis is configured in `pyproject.toml`. Pyright runs in strict
  mode and ruff carries the security ruleset. Zero warnings is the target.
- A decision that constrains later work gets a record in `../decisions/`
  before the work, not after it.
- Unmeasured claims are marked as unmeasured. See `../README.md`.
