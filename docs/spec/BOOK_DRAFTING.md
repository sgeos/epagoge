# Drafting a book, by level

**Specification. Recorded 2026-09-25.**

This corpus is CC0 and is meant to be used. A parent choosing books for a
child, or anyone curating a training corpus, will read these files without
having read anything else in the repository. **A book has to be usable on
its own**, and that is what this specification is for.

Figures and their sources are in `../decisions/READING_LEVEL_RESEARCH.md`.
Level definitions are in `../decisions/LEVEL_CALIBRATION.md`.

## What a book is, at each level

| Level | Reader is entering | Artifact | Spreads | Words a spread | Words a book |
| --- | --- | --- | --- | --- | --- |
| 1 | kindergarten | picture book | 16 | 50 ± 30 | 320 to 1,280 |
| 2 | grade 4 | textbook module | 64 | 250 ± 50 | 12,800 to 19,200 |
| 3 | grade 8 | textbook module | 112 | 500 ± 100 | 44,800 to 67,200 |
| 4 | grade 12 | textbook module | 160 | 500 ± 100 | 64,000 to 96,000 |
| 5 to 7 | university and beyond | paper | — | — | not a book count |

**The spread count is exact and the word count is a band.** Page counts are
multiples of sixteen because a book binds in signatures of sixteen pages,
so a book off the count cannot be physically published without someone
padding or cutting it. Word counts vary with what a spread has to say.

**Above level four the unit stops being a book.** A paper is eight to
twenty pages and a monograph is bound to no standard length.

## The shape of a book

**Say what it is about, define the words, then use them.**

1. **One subject spread.** What the book is about. It carries
   `defines.kind` of `topic`.
2. **One spread per word defined**, each carrying `defines.kind` of `word`.
   At level one a book defines at most eight, because more crowds out the
   story the shape exists to produce.
3. **The rest is the body.** At level one that is a story: one thing
   happening, each spread following from the last, not a list of facts. At
   level two and above it is connected exposition.

**A definition never follows the material that uses it.** The gate refuses
that, because a definition at the back is a glossary and the book stops
teaching its own vocabulary.

## Vocabulary

**Every content word must be admissible at the book's level.** The lexicon
is `../../curriculum/vocabulary.json` and the ceiling is checked exactly,
not by stripping suffixes.

Three responses to a word the level does not carry, in order of
preference:

1. **Rephrase**, where the level can say it another way.
2. **Substitute**, where a level-appropriate phrase exists. The
   `substitutions` map records these, and a generator is shown them.
3. **Admit the word**, where a reader at that level would know it. This
   requires a definition that reduces to the seed, which the closure check
   enforces, and admitting a verb admits every inflection and a noun its
   plural.

**The lexicon grows with the corpus and that is intended.** A word the
writer reached for is evidence about the lexicon, not an error in the
writing.

## The two fields written for a person

**`about` and `teaches` are the one place the level ceiling does not
apply.** They are prose for a curator and are not text a model trains on.

- **`about`** — what the book is about, in ordinary English. Enough that
  someone choosing books can tell whether they want this one.
- **`teaches`** — what a reader should come away with. What the book is
  *for*, which sixteen spreads in eight hundred words often cannot say for
  themselves.

**Write them as back-cover copy.** The title goes on the front, `about`
and `teaches` go on the back, and between them they are what a parent
picking the book off a shelf has to go on. That fixes the register and
the length: a short paragraph each, accurate, and readable by someone who
has never heard of this project.

Name the concepts plainly, including any the book teaches by showing
rather than stating. Say what a reader is assumed to know already.

`tools/validate_books.py --describe` reports every book missing either.

## The fields a book carries besides its text

| Field | What it is |
| --- | --- |
| `author` | Who wrote it: a person, or the teacher model and its operator |
| `licence` | SPDX identifier. **Recorded per book, never assumed** |
| `first_published` | ISO date this book first existed in any version |
| `published` | ISO date of this version |
| `about` | Back-cover copy: what it is about |
| `teaches` | Back-cover copy: what a reader comes away with |

**The licence is per book because this tree can hold books it did not
write.** The corpus is CC0 and `exclude/` exists so contributions can
arrive, so a book that names no licence is one nobody can safely reuse,
which defeats publishing it.

**Two dates because a book is edited.** A curator comparing two copies
needs to know which is later; a reader citing one needs to know when the
text they read was fixed. One date cannot answer both.

## Holding a book out of a run

Each level directory has an `exclude/` subdirectory. **A book moved there
is not trained on**: the loader reads the level directory and does not
descend, so an excluded book is invisible to every generator, validator
and training run.

**Its contents are gitignored and the directory is kept by its
`.gitkeep`.** So the convention travels with the repository and what is
parked travels with the machine. A submission dropped in does not become
a commit by accident, and a local exclusion stays local.

**That means moving a tracked book here removes it from the repository.**
Keeping the file and keeping it in git are different things, and the
commit that moves one should say which was meant. `git add -f` tracks a
book there deliberately.

It exists for two cases. A book may be sound and still wrong for a
particular corpus, off-register or redundant with a better one, and
deleting it destroys the work and the reason. And the corpus is CC0 and
meant to be used, so outside submissions are expected: a submitted book
can land there, be read, and move up into the level once it passes.
**Nothing is trained on because it arrived.**

**A book that is wrong should be fixed or deleted rather than parked**,
and the commit that moves one should say why, because neither the
directory nor the file can.

## What a book must not do

- **Address the reader as a teacher.** State what is so.
- **Assert more than it shows.** A claim carries a claim class and the
  corpus rules govern what each may assert.
- **Use a word outside its level**, including in a definition.
- **Repeat a record from another book.** A record belongs to one book.

## What a draft owes before it is committed

- Sixteen, sixty-four, one hundred and twelve, or one hundred and sixty
  spreads exactly, by level.
- Every word admissible at the level, checked by exact tokenisation.
- A subject definition, or the book is withheld.
- `author`, `licence`, both dates, `about` and `teaches` filled in.
- `./tools/check.sh` exits 0.
