#!/usr/bin/env bash
# Every check the project claims to meet, in one command.
#
# Run before any commit that touches code or documentation.
#
# Two pieces of history are the reason this exists in this shape. The static
# analysis configured in pyproject.toml had never been executed and failed
# thirty-six ways on first run. Separately, the disclosure discipline was
# enforced by nothing, and the ad-hoc scans used to check it were twice found
# to be broken in ways that returned noise rather than findings.
#
# TOOL VERSIONS ARE PINNED. A gate that resolves @latest can pass today and
# fail tomorrow for reasons unrelated to the code, which is not a property a
# project about reproducibility should accept in its own process. Bump these
# deliberately, and record the bump.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 2

RUFF="ruff@0.16.8"
PYRIGHT="pyright@1.1.414"
COVERAGE_FLOOR=95

fail=0
run() {
  printf '\n=== %s ===\n' "$1"; shift
  if "$@"; then :; else fail=1; printf '^^^ FAILED\n'; fi
}

run "ruff (lint)"        uvx "$RUFF" check .
run "ruff (format)"      uvx "$RUFF" format --check .
run "pyright (strict)"   uvx "$PYRIGHT"
run "tests"              env PYTHONPATH=src python3 -m unittest discover -s tests
run "coverage"           env PYTHONPATH=src uvx --with coverage coverage run --source=src -m unittest discover -s tests
run "coverage floor"     env PYTHONPATH=src uvx --with coverage coverage report --show-missing --fail-under="$COVERAGE_FLOOR"
rm -f .coverage
run "seed graph"         env PYTHONPATH=src python3 tools/validate_graph.py curriculum/graph/seed.json
run "sample corpus"      env PYTHONPATH=src python3 tools/validate_corpus.py curriculum/graph/seed.json curriculum/graph/sample_corpus.jsonl
run "disclosure scan"    ./tools/scrub_scan.sh

printf '\n'
if [ "$fail" -eq 0 ]; then echo "ALL CHECKS PASSED"; else echo "CHECKS FAILED"; fi
exit "$fail"
