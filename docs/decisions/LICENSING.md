# Licensing

**Decided 2026-09-24.** Two licences by scope.

| Scope | Licence |
| --- | --- |
| Software, meaning `src/`, `tests/`, `tools/` | 0BSD |
| Corpus, curriculum, graph, specifications, documentation | CC0 1.0 |
| Third-party material under `sources/` | Its own terms. Not ours to grant |

**Supersedes** the MIT declaration in `pyproject.toml`, which was a default
chosen without being surfaced rather than a decision.

## Why the split rather than one licence

**Creative Commons recommends against CC0 for software**, principally
because it does not address patent rights explicitly. Using it for the code
would be using a tool against its own guidance.

**0BSD is the software equivalent of the intent.** It is
public-domain-equivalent, requires no attribution, and imposes no
conditions, which MIT does not quite achieve since MIT requires the notice
to travel with the work.

So the split is not a compromise. Each scope gets the instrument designed
for it.

## Why CC0 suits a synthetic corpus specifically

This is the part worth recording, because it is a reason rather than a
preference.

**The copyright status of machine-generated content is unsettled.** Work
without human authorship is, on current guidance in at least one major
jurisdiction, not copyrightable at all. A synthetic corpus may therefore be
something the project does not hold copyright in, and so cannot license in
the ordinary way.

**CC0 does not depend on the answer.** It is a dedication of whatever
rights exist, with a fallback permissive licence for jurisdictions where
dedication is ineffective. It works whether or not the material turns out
to be copyrightable, which is precisely the property needed when nobody can
say which it is.

A conventional permissive licence would instead assert a right that may not
exist, which is a claim the project cannot support. That would be an
unsupported claim in a repository whose stated purpose is to suppress them.

## The carve-out, which is load-bearing

**`sources/` is not covered and cannot be.** Level-seven material is
third-party literature obtained under terms the project did not set. A
licence file that appeared to cover it would be asserting a grant the
project has no standing to make.

This is recorded in `LICENSING.md` at the top level rather than only
here, because a reader checks the licence before the decision record.

**Amended 2026-09-25.** The carve-out and the scope map used to live in
`LICENSE` itself. Automated licence detection reads that file and matches
it against known licence texts, and a preamble in front of the text
defeats the match, so the repository reported its licence as `Other`.
`LICENSE` and `LICENSE-CC0` now hold bare licence text and `LICENSING.md`
holds the scope. The trade is one more file against a licence a tool can
read.

## Unresolved

**Records derived from third-party literature.** A terminal-stage record
that summarises or restates a copyrighted paper occupies unclear ground. It
is neither purely machine-generated nor a reproduction. Whether such
records can be CC0 is not settled here, and a conservative reading is that
some cannot.

**To close.** Decide whether terminal-stage records carry a distinct
licensing status, and if so mark it in the record schema rather than
leaving it to a reader's inference. Recorded as open question twenty-five.

## An alignment worth noting

The collaborative-positioning decision wants this model class recruited
into multi-agent groups. Zero-friction licensing serves that directly.
Neither 0BSD nor CC0 imposes an attribution obligation that would travel
into anything incorporating the corpus or the tooling, so adoption carries
no compliance cost.

That is a convenience rather than a justification. The licences were chosen
on their merits.
