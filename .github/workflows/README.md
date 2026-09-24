# Continuous integration

`check.yml` runs `tools/check.sh` on push and pull request.

**One check cannot run here.** The disclosure scan reads a pattern held
outside version control, so in a clone without it the scan skips loudly and
returns success. Continuous integration therefore enforces the code gate
and not the disclosure discipline.

That is a real limitation and not an oversight. Publishing the pattern
would publish the list of withheld vocabulary, which is the thing being
withheld. The disclosure scan is enforced locally, by whoever holds the
pattern, before pushing.
