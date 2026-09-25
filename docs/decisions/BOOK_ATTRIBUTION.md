# What a book says about its own authorship

**Decided 2026-09-25.** Every book carries six metadata fields. Two are
prose for a curator, two are derived from version history, and two are
this decision.

| Field | Value | How it is settled |
| --- | --- | --- |
| `about`, `teaches` | prose | Written by the teacher, in ordinary English |
| `first_published`, `published` | dates | Derived from the commit history of the file |
| `author` | `Epagoge` | This record |
| `licence` | `CC0-1.0` | `LICENSING.md` |

## Why `author` names the project and not a person

**The prose is not written by a person.** Each book's records come from a
local teacher model prompted by this project and accepted by its checks.
Some definitions were authored by hand across many rounds when generation
would not converge. **Which records came by which route is not recoverable
from the history**, because a commit records who committed rather than who
composed, so a per-book split between the two would be invented.

**Naming a person would assert an authorship the project has said may not
exist.** `LICENSING.md` records the reason the corpus is CC0 rather than
permissively licensed: work without human authorship is, on current
guidance in at least one major jurisdiction, not copyrightable at all, so
a synthetic corpus may be something the project does not hold copyright
in. A byline naming an individual would claim exactly the right that
record declines to assert. That would be an unsupported claim in a
repository whose stated purpose is to suppress them.

**The project is therefore the author of record**, which is the ordinary
answer for a corpus and is true without requiring the copyright question
to be settled first.

## What was rejected

**Naming the teacher model.** `qwen3:30b-a3b-instruct-2507-q4_K_M` is
attributed in the README and that is the right place for it. Putting it in
every book would make the field a provenance record, which
`curriculum/provenance.json` already is and does better, and it would go
stale the first time a different teacher writes a book.

**Naming the operator.** Rejected on the grounds above.

**Leaving the field empty.** A curator reading a CC0 corpus needs to know
what they are looking at. `book_head` omits an empty field rather than
writing it blank, so an empty value would be indistinguishable from a book
nobody had got to yet, which is the state all 246 were in until today.

**A per-book value.** Not recoverable, as above, and a value that is
sometimes right is worse than one that is always true.

## Why the dates are derived and not written

**A date a person types is a claim; a date read from the commit that
introduced the file is a fact.** The project's post-facto analysis
requirement is that an artifact can say when it came to exist and have
that checked rather than believed. `tools/stamp_books.py` derives both
dates in one pass over the log and is idempotent, so the answer in the
tree can always be regenerated and compared.

**`--check` reports a `published` date that disagrees with history**, for
any book with no uncommitted modification. A book edited in the working
tree is skipped rather than reported, because the edit is not in history
yet and the date it would produce is the previous commit's.

## The consequence worth knowing

**`published` moves whenever a book is edited and committed**, so a run of
`tools/stamp_books.py` belongs with any change that touches books. The
gate checks that the fields are present and that no committed book
disagrees with its own history, which is what makes the stamp a
measurement rather than a decoration.
