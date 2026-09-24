#!/usr/bin/env bash
# Every check the project claims to meet, in one command.
#
# Run before any commit that touches code. The static analysis configured in
# pyproject.toml had never been executed before 2026-09-23 and failed
# thirty-six ways on first run, which is the reason this gate exists.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 2

fail=0
run() {
  printf '\n=== %s ===\n' "$1"; shift
  if "$@"; then :; else fail=1; printf '^^^ FAILED\n'; fi
}

run "ruff (lint)"        uvx ruff@latest check .
run "ruff (format)"      uvx ruff@latest format --check .
run "pyright (strict)"   uvx pyright@latest
run "tests"              env PYTHONPATH=src python3 -m unittest discover -s tests
run "seed graph"         env PYTHONPATH=src python3 tools/validate_graph.py curriculum/graph/seed.json

printf '\n'
if [ "$fail" -eq 0 ]; then echo "ALL CHECKS PASSED"; else echo "CHECKS FAILED"; fi
exit "$fail"
