# Why the model does not answer a question

**Measured 2026-09-25**, prompted with `what is the cup ?`.

> of . the cup . the child is doing . one breeze that is not been and that
> is lift and the light . a small where colour .

**It continued the text. It did not answer.** That is not a failure of
training and it would not be repaired by a larger corpus of the same kind.

## The corpus contains no question being answered

Counted over 4,419 level-one records:

| | |
| --- | --- |
| Records containing a question mark | **1** |
| Records ending in a question, with an answer following | **0** |

The one instance is a rhetorical question inside a single record: *How do
you know? Let us go and find out.*

**A model cannot produce a form the corpus never shows it.** Every record
in this corpus is a declarative statement in a sequence of declarative
statements, so continuing text is the only thing the corpus ever
demonstrates, and continuing text is exactly what the model did.

## What this means for the interaction goal

Operator direction: a level-one model external parties can satisfactorily
interact with.

**`LEVEL_ONE_SCALING.md` prices the coherence half of that** and predicts
perplexity near 35 at a million tokens. **This is the other half, and
scale does not touch it.** A perfectly coherent model trained on this
corpus would still continue a question rather than answer one.

**Interaction is a form, and the corpus teaches no forms.** Whatever a
reader is meant to be able to do with the model has to appear in the
corpus as something being done. If the target is question and answer,
the corpus needs questions being answered.

## What this does not settle

**Whether question-answer pairs belong in this corpus at all.** The
artifact at levels one to four is a book, and a picture book is not a
dialogue. The forms a reader meets in a book are exposition and narrative,
and a corpus of books is a faithful corpus of books.

So the choice is between three things and it is the operator's:

1. **Add the form to the corpus**, as records that ask and answer, which
   makes the books something other than books.
2. **Add it as a separate artifact** alongside the books, trained on
   together, which keeps the books intact.
3. **Accept that the model continues text**, and judge it on that, which
   means interaction is not the level-one goal after all.

**The third is more defensible than it sounds.** Continuing text
coherently in a controlled vocabulary is a real property and the thing
this corpus was built to produce. It is only the word "interact" that
implies otherwise.
