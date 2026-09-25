# corpus/

**Derived. Do not edit and do not track.** Everything here is rebuilt from
`../curriculum/books/` by `../tools/build_corpus.py`.

The directory is ignored for the same reason a build directory is, and kept
in the tree by a `.gitkeep`. `../docs/decisions/CORPUS_ARTIFACTS.md` has
the reasoning and `../docs/decisions/CORPUS_TRACKING.md` carries the
amendment to the original direction.

**Status.** One stream built, `level_1.jsonl`, five documents and 681
words, from the five books at level one.

## What is here, and what is not

One JSON object per line, one per **book**, carrying the book identifier,
its level, and its text. Nothing else.

**The annotation is deliberately absent.** A stream containing the block
markers that books use would teach a model to emit them. Concepts, claim
classes, provenance and definitions live in the books, where a reviewer and
the validators can reach them and the trainer cannot.

## One stream per ordering

`build_corpus.py` takes an ordering, so the same books yield a different
stream under a different one. **The ablation's treatment and control are
two builds of one corpus rather than two corpora.**

A book is one document and its internal order is never shuffled, because
the narrative is the reason a book exists.

## Provenance is not lost by not tracking this

Every record is reviewable and attributable through the book that holds it,
which is tracked. What is not tracked is a file that can be rebuilt.
