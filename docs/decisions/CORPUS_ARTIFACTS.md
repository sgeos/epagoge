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

## Each level carries a dictionary, and it is derived

**Operator decision, 2026-09-24.** A level's corpus includes a dictionary
of its own vocabulary.

**It is derived, not authored.** Every word definition already exists
inside the book that introduced it, carried on the record as
`defines: {kind: word}`. The dictionary collects them, so there is no
second place to keep in agreement with the first.

**It is the last document of the level, and it is a consolidation.** Every
word in it was already defined in context by the book that introduced it.
Seven hundred definitions at the front, with no story around them, is
exactly the lifeless-assertion failure the books exist to fix.

**It makes the closure gap visible as a number.** `build_corpus.py` reports
the fraction of the level's terms that carry a definition. At the first
build that is **27 of 760**.

## Both questions now answered, and one created

**ANSWERED 2026-09-24. The derived stream is ignored**, for the same reason
a build directory is. `CORPUS_TRACKING.md` carries the amendment. The
directory stays in the tree by a `.gitkeep`, and `sources/` remains tracked
because acquired literature cannot be rebuilt.

**ANSWERED 2026-09-24. The ablation orders books.** Pre-registration
amendment 3 carries it, along with the risk it creates. The orderable set
is smaller by orders of magnitude than the record-level set the seed count
was estimated against, and whether the arms stay distinguishable at that
granularity has not been measured.
