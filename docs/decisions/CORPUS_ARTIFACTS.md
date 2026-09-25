# Three artifacts, three readers

**Recorded 2026-09-24.** The corpus is not one thing. It has three readers
with different needs, and trying to serve all three from one file served
none of them well.

| Artifact | Reader | Format | Authored or derived |
| --- | --- | --- | --- |
| `curriculum/books/level_N/*.md` | a person | prose with JSON front matter | **authored** |
| the same files | the validators | the front matter | authored |
| `corpus/*.jsonl` | the trainer | one document per book, text only | **derived** |

## Why the split

**The trainer must not see the annotation.** A training stream containing
`[bk.cup.d01]` markers teaches a model to emit them. The markers exist so
that a reviewer and a validator can attach metadata to a passage, and they
have no business in what the model reads.

**The reviewer must not have to read the annotation.** A level-one book of
173 words occupied 260 lines of JSON before this split. Reading the corpus
is the step the recorded sequence says decides whether generation
continues, and a format that obstructs it obstructs the one check nothing
automates.

**The validator needs neither the prose nor the stream.** It needs the
metadata, which the front matter holds in one place.

## The derived stream is per-ordering, which is the point

`tools/build_corpus.py` takes an ordering. The same books produce a
different stream under a different one, **which is exactly what the
ordering ablation requires**. The treatment and the control are two builds
of one corpus rather than two corpora.

**A book is one document and its internal order is never shuffled.** The
narrative is the reason a book exists. Shuffling inside one would destroy
the thing the ordering hypothesis is about while claiming to test it.

## One question answered, one still open

**ANSWERED 2026-09-24. The derived stream is ignored**, for the same reason
a build directory is. `CORPUS_TRACKING.md` carries the amendment. The
directory stays in the tree by a `.gitkeep`, and `sources/` remains tracked
because acquired literature cannot be rebuilt.

**Does the ablation order books or records?** `evals/PRE_REGISTRATION.md`
speaks of a curriculum trajectory against a random topological ordering,
written before books existed. If the unit is the record, a shuffle breaks
every book apart. If it is the book, the orderable set is much smaller and
the topological constraint applies between books rather than between
concepts. **The pre-registration does not say, and it must before the
ablation runs.**
