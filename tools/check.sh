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
# pilot.py needs the optional train extra; exclude it from the floor so the
# gate runs without a 600 MB dependency. Its tests skip gracefully.
COVERAGE_OMIT="src/epagoge/pilot.py"

fail=0
run() {
  printf '\n=== %s ===\n' "$1"; shift
  if "$@"; then :; else fail=1; printf '^^^ FAILED\n'; fi
}

run "ruff (lint)"        uvx "$RUFF" check .
run "ruff (format)"      uvx "$RUFF" format --check .
run "pyright (strict)"   uvx "$PYRIGHT"
run "tests"              env PYTHONPATH=src python3 -m unittest discover -s tests
run "coverage"           env PYTHONPATH=src uvx --with coverage coverage run --source=src --omit="$COVERAGE_OMIT" -m unittest discover -s tests
run "coverage floor"     env PYTHONPATH=src uvx --with coverage coverage report --show-missing --omit="$COVERAGE_OMIT" --fail-under="$COVERAGE_FLOOR"
rm -f .coverage
# The corpus rules run over every record together. A book validated alone
# reports every prerequisite the rest of the corpus teaches, so the files are
# concatenated rather than checked one at a time.
CORPUS="$(mktemp)"
env PYTHONPATH=src python3 - <<'INLINE' > "$CORPUS"
import json, pathlib, sys
sys.path.insert(0, "src")
from epagoge.book import load_book_dir
sys.stdout.write(pathlib.Path("curriculum/graph/sample_corpus.jsonl").read_text())
for _, records in [load_book_dir(pathlib.Path("curriculum/books/level_1"))]:
    for record in records:
        print(json.dumps(record))
INLINE
run "seed graph"         env PYTHONPATH=src python3 tools/validate_graph.py curriculum/graph/concepts.json
run "corpus"             env PYTHONPATH=src python3 tools/validate_corpus.py curriculum/graph/concepts.json "$CORPUS" curriculum/primitives.json curriculum/vocabulary.json
run "schedule"           env PYTHONPATH=src python3 tools/validate_schedule.py curriculum/graph/concepts.json curriculum/primitives.json curriculum/schedule/level_01.json curriculum/schedule/level_02.json
run "books"              env PYTHONPATH=src python3 tools/validate_books.py curriculum/graph/concepts.json curriculum/vocabulary.json curriculum/schedule curriculum/books/level_1
run "disclosure scan"    ./tools/scrub_scan.sh
rm -f "$CORPUS"

printf '\n'
if [ "$fail" -eq 0 ]; then echo "ALL CHECKS PASSED"; else echo "CHECKS FAILED"; fi
exit "$fail"
