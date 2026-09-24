#!/usr/bin/env bash
# Disclosure scan over tracked files.
#
# The pattern lives outside version control, because a tracked list of banned
# terms would itself publish what is being withheld. This script is tracked so
# it cannot drift from the code; the pattern it reads is not.
#
# Absent the pattern file the scan skips loudly rather than silently passing.
# A check that quietly does nothing is worse than no check, which this project
# has now learned twice.
set -uo pipefail
cd "$(dirname "$0")/.." || exit 2

PATTERN_FILE="secret/scrub_terms.txt"

if [ ! -f "$PATTERN_FILE" ]; then
  echo "SKIPPED: $PATTERN_FILE absent. Disclosure scan did not run."
  echo "  This is expected in a clone without the private pattern."
  exit 0
fi

# Word-anchored alternation. An unanchored pattern matched 'ore' inside
# 'before' on 2026-09-23 and returned a hundred lines of noise that would
# have looked identical whether or not a leak existed.
terms=$(grep -vE '^\s*(#|$)' "$PATTERN_FILE" | paste -sd'|' -)
if [ -z "$terms" ]; then
  echo "SKIPPED: $PATTERN_FILE holds no terms."
  exit 0
fi

hits=$(git ls-files -z \
  | xargs -0 grep -IniE "\\b(${terms})\\b" 2>/dev/null \
  | grep -v '^secret/' || true)

if [ -n "$hits" ]; then
  echo "DISCLOSURE SCAN FAILED. Tracked files contain withheld vocabulary:"
  echo "$hits"
  exit 1
fi

count=$(grep -vcE '^\s*(#|$)' "$PATTERN_FILE")
echo "disclosure scan: clean ($count terms checked over $(git ls-files | wc -l | tr -d ' ') tracked files)"
exit 0
