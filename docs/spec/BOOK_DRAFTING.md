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

Write both as though for a parent who has read nothing else. Name the
concepts plainly, including any the book teaches by showing rather than
stating. Say what a reader is assumed to know already.

`tools/validate_books.py --describe` reports every book missing either.

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
- `about` and `teaches` filled in.
- `./tools/check.sh` exits 0.
