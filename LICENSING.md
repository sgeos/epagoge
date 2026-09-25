# Licensing

**Epagoge is released under two licences, by scope.** `LICENSE` and
`LICENSE-CC0` hold the licence texts and nothing else, so that automated
licence detection reads them correctly. This file says which applies
where. `docs/decisions/LICENSING.md` says why the split exists.

| Scope | Licence | Text |
| --- | --- | --- |
| Software, meaning `src/`, `tests/`, `tools/`, `generators/` | 0BSD | `LICENSE` |
| Corpus, curriculum, concept graph, specifications, documentation, evaluations | CC0 1.0 Universal | `LICENSE-CC0` |
| Third-party material under `sources/` | Its own terms | Not this project's to grant |

**Third-party material is covered by neither.** Anything under `sources/`
is obtained under terms set by whoever published it, and those terms
travel with it. See `sources/README.md`. The licensing of that material
is recorded as unexamined in `docs/decisions/THREE_PROBLEMS.md`, and
nothing has been acquired yet.

**Package metadata declares 0BSD** because a Python package declares one
licence and the package is the software. The corpus ships in the same
tree under CC0, which this file is the authority on.
