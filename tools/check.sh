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
# **Reported, never gated.** Every unused word is a judgement: a module
# should use it, a module should be drafted for it, or admitting it was a
# mistake. A gate cannot make that call and should not pretend to.
# **Regenerated, then compared.** A provenance record that drifts from the
# lexicon is worse than none, because it reads as evidence. The check is
# that the file on disk is what the history produces.
run "provenance"         env PYTHONPATH=src python3 tools/word_provenance.py --check

run "unused words"       env PYTHONPATH=src python3 tools/unused_words.py --level 1 --top 0

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
# **--spreads is on.** It was wired and not run for as long as the corpus
# had short books, which is a shape of failure this project has recorded
# three times. Every level-one book reached sixteen spreads on 2026-09-25.
run "books"              env PYTHONPATH=src python3 tools/validate_books.py curriculum/graph/concepts.json curriculum/vocabulary.json curriculum/schedule curriculum/books/level_1 --spreads 16
run "closure"            env PYTHONPATH=src python3 tools/validate_closure.py curriculum/vocabulary.json curriculum/books/level_1 1
run "closure L2"         env PYTHONPATH=src python3 tools/validate_closure.py curriculum/vocabulary.json curriculum/books/level_2 2

run "thesaurus"          env PYTHONPATH=src python3 tools/validate_thesaurus.py curriculum/thesaurus.json curriculum/vocabulary.json 1
run "thesaurus L2"       env PYTHONPATH=src python3 tools/validate_thesaurus.py curriculum/thesaurus.json curriculum/vocabulary.json 2

# **Reported, never gated, and that is stated rather than silent.** Levels
# three to seven have no schedule, so every concept reserved for them reads
# as never taught and gating would refuse the tree for unstarted work. The
# --strict flag exists so it can be turned on in one move.
run "coverage"           env PYTHONPATH=src python3 tools/coverage.py curriculum/graph/concepts.json curriculum/schedule

# A dictionary in authoring order is a list. Checked rather than trusted,
# because the ordering is a property of files a generator rewrites.
run "dictionary order"   env PYTHONPATH=src python3 tools/sort_dictionary.py --check curriculum/books/level_1 curriculum/books/level_2

# **Presence, and agreement with history.** A book's two dates are derived
# from the commit log, so a committed book whose `published` field
# disagrees with its own history is reporting something that was true once.
# A book modified in the working tree is skipped, because its edit is not in
# history yet.
run "book metadata"      env PYTHONPATH=src python3 tools/stamp_books.py --level 1 --check

# **Reported, never gated, and the reference is not in the repository.**
# WordNet records what English does; this project decides what a level
# admits, so a mismatch is a question. Every irregular form this project got
# wrong by hand was in these files.
run "inflections"        env PYTHONPATH=src python3 tools/check_inflections.py --level 1 --show 25

# A document that names a file which no longer exists reads as evidence and
# is not. Adapted from the keleusma repository's markdown link check, against
# what this project's documents actually do, which is cite backticked paths.
run "references"         env PYTHONPATH=src python3 tools/check_references.py

run "disclosure scan"    ./tools/scrub_scan.sh
rm -f "$CORPUS"

printf '\n'
if [ "$fail" -eq 0 ]; then echo "ALL CHECKS PASSED"; else echo "CHECKS FAILED"; fi
exit "$fail"
