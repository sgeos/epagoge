#!/usr/bin/env bash
# Disclosure scan over every file this repository would publish.
#
# The pattern is read from a file this repository does not contain, because a
# tracked list of banned terms would itself publish what is being withheld.
# This script is tracked so it cannot drift from the code; the pattern it
# reads is not.
#
# Absent the pattern file the scan skips loudly rather than silently passing.
# A check that quietly does nothing is worse than no check, which this project
# has now learned twice.
#
# TWO HOLES WERE FOUND IN THIS SCRIPT ON 2026-09-25, both of the shape this
# project keeps producing: a check reporting success over less than it was
# asked to cover.
#
#   1. IT SCANNED ONLY TRACKED FILES. A new document is untracked until its
#      first commit, so the scan that runs before that commit never sees it.
#      Two documents carrying banned vocabulary were committed and pushed to
#      a public repository that way, with a green gate either side.
#
#   2. IT MATCHED LINE BY LINE. A banned multi-word phrase wrapped across a
#      line break was invisible. Two files had been carrying one for days,
#      one of them since before publication, and the scan reported clean
#      every time.
#
# Both passes below now run, over the same widened file set.
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

# **Tracked AND untracked-but-not-ignored.** Everything a commit could pick
# up. Ignored files are excluded because they are not published; secret/ is
# excluded because it is the pattern's own home.
FILES=$(mktemp)
trap 'rm -f "$FILES"' EXIT
{ git ls-files; git ls-files --others --exclude-standard; } \
  | grep -v '^secret/' | sort -u > "$FILES"

fail=0

# Pass one, line by line, which is the pass that can name a line number.
hits=$(tr '\n' '\0' < "$FILES" | xargs -0 grep -IniE "\\b(${terms})\\b" 2>/dev/null || true)
if [ -n "$hits" ]; then
  echo "DISCLOSURE SCAN FAILED. Files contain withheld vocabulary:"
  echo "$hits"
  fail=1
fi

# Pass two, whitespace collapsed per file, which is the pass that sees a
# phrase broken by a line break. It can only name the file.
wrapped=""
while IFS= read -r file; do
  [ -f "$file" ] || continue
  if tr '\n' ' ' < "$file" 2>/dev/null | tr -s ' ' | grep -qIE "\\b(${terms})\\b"; then
    case "$hits" in
      *"$file"*) ;;
      *) wrapped="${wrapped}  ${file}"$'\n' ;;
    esac
  fi
done < "$FILES"
if [ -n "$wrapped" ]; then
  echo "DISCLOSURE SCAN FAILED. A withheld phrase spans a line break in:"
  printf '%s' "$wrapped"
  fail=1
fi

# Two further rules in the code-name discipline were enforced by nothing
# until a pre-push audit found both violated: a tracked document may not
# cite a file under secret/ by name, and CLAUDE.md is the one exception
# because the rule has to be enforceable somewhere. The euphemism the
# discipline also bans is a term in the pattern file, so that the banned
# phrase is not itself published here.
cited=$(tr '\n' '\0' < "$FILES" \
  | xargs -0 grep -IlnE "secret/[A-Z_]+\\.md" 2>/dev/null \
  | grep -vx 'CLAUDE.md' || true)
if [ -n "$cited" ]; then
  echo "DISCLOSURE SCAN FAILED. These files name a file under secret/:"
  echo "$cited"
  fail=1
fi

if [ "$fail" -ne 0 ]; then
  exit 1
fi

count=$(grep -vcE '^\s*(#|$)' "$PATTERN_FILE")
echo "disclosure scan: clean ($count terms over $(wc -l < "$FILES" | tr -d ' ') files, tracked and untracked, line by line and with whitespace collapsed)"
exit 0
