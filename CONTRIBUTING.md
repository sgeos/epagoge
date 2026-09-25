# Contributing

Contributions are welcome. Books, lexicon entries, tooling, evaluations,
and corrections are all in scope.

**Everything here is dedicated to the public domain.** By contributing you
agree that your contribution is released under the licence covering the
part of the tree it lands in, per `LICENSING.md`. Corpus and documentation
are CC0 1.0 Universal; software is 0BSD. Do not contribute material you
did not write or that carries terms of its own. That includes text
produced by a model whose terms of use restrict the output.

## Getting the checks running

    git clone https://github.com/sgeos/epagoge
    cd epagoge
    uv venv
    uv pip install -e ".[train]"
    ./tools/check.sh

The `train` extra pulls PyTorch, which is large and is needed only by the
tools that train or sample a model. Without it the rest still run and the
gate still passes, because the tests that need it skip.

**`./tools/check.sh` is the gate and it must be green before a commit.**
Twenty checks covering lint, formatting, strict type checking, tests, a
coverage floor, the concept graph, the corpus, lexicon closure, document
references, and the disclosure scan. Run it, read its exit code, and stop
if it is not zero.

**One check cannot run in a clone.** The disclosure scan reads a pattern
that is deliberately not in version control. In your clone it announces
that it is skipping and returns success. That is expected and it is why
continuous integration is not a strict superset of the local gate here.

## What makes a corpus contribution acceptable

A book is a Markdown file with JSON front matter under
`curriculum/books/level_<N>/`. `docs/spec/BOOK_DRAFTING.md` is the
authority on shape and `docs/spec/RECORD_SCHEMA.md` on records.

Four properties are checked mechanically and a contribution that lacks
them will be caught by the gate rather than by a reviewer.

**Every word must already be admitted at that level.** The corpus is
written to a closed vocabulary. A word that is not in
`curriculum/vocabulary.json` at or below the book's level is rejected, and
the check matches surface forms exactly rather than stripping suffixes.
`walked` is not licensed by `walk`.

**Every word the book defines must reduce to the seed.** The lexicon is
self-hosting. A definition may only use words that are themselves defined
or are among the words that need no definition. A definition that closes a
cycle is rejected.

**A book fits its signature.** Sixteen spreads at level one, and the word
band for the level is in `docs/spec/BOOK_DRAFTING.md`.

**Front matter is complete.** Use `epagoge.book.book_head` rather than
writing the block by hand. Nine places once built it by hand and every one
of them silently erased fields added later.

**Do not weaken a check to make a contribution pass.** If a check is
wrong, say so in the issue or the commit message and fix the check
deliberately. The checks are the only thing standing between this corpus
and the problem it exists to avoid.

## Holding a book out of a training run

`curriculum/books/level_<N>/exclude/` is a parking place. Its contents are
ignored, so a book dropped there is out of the corpus without being
deleted, and a submission dropped there does not become a commit by
accident.

**Moving a tracked book there removes it from the repository.** Keeping
the file and keeping it in version control are different things, and a
commit that does this should say which was meant.

## Commits

Write the subject in the imperative and say what the commit does, not what
area it touches. There is no scope prefix.

    Make a checkpoint carry its vocabulary, and a book carry its licence
    Check that a level uses its own lexicon, and find level one using a third less

Where a commit both changes something and establishes a fact, the subject
may say both. That is the house style and it is visible in the log.

**Corrections are kept in place.** A wrong claim in a pushed commit is
corrected by the next commit, not amended away. The record of having been
wrong is part of what the project is for.

If you used a model, add the `Co-Authored-By` trailer.

## Claims and evidence

This project is about the difference between a claim and a measurement, so
it holds its own documentation to that standard.

**Never state a curriculum benefit as established.** That difficulty
graded ordering improves pretraining is the hypothesis under test. Any
claim of improvement needs a flat-order control.

**A number in a document is measured or it is absent.** Where a claim has
not been measured on the tree, the same sentence must say so.

**A tool that returns less than it was asked for must say so.** Silent
partial coverage is this project's characteristic failure, and it has
produced a book ordering covering thirteen of a hundred and forty-six and
a chunker that kept a quarter of the corpus. Both passed.

## Filing an issue

`.github/ISSUE_TEMPLATE/` holds the templates. A corpus submission and a
request to admit a word are different things and have different forms,
because admitting a word changes what every later book may say.
