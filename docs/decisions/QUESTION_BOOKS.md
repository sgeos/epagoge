# Every unit asks and answers, and the band that was flagging them

**Completed 2026-09-27.** 42 of 96 level-one schedule units carried a
question-and-answer book. **All 96 do now, every one at its full sixteen
spreads.**

## Why the form exists, which was measured rather than assumed

**On 2026-09-25 the corpus held one question mark in 4,419 records, no
question with an answer after it, and the model met "what is the cup ?" by
carrying on rather than answering.** A model reproduces the forms it was
shown, so a corpus that only ever states produces a model that only ever
continues.

## What the batch moved

| Quantity | Before | Now |
| --- | --- | --- |
| Units with a question book | 42 of 96 | **96 of 96** |
| Question books short of sixteen spreads | 8 of 51 | **0 of 96** |
| Books | 469 | 523 |
| Records | 8,267 | 9,131 |
| Words | 315,444 | 330,710 |
| Question marks | 646 | **1,381** |
| Training tokens | 378,156 | 395,715 |
| One question mark per | 49 sentences | **24.7 sentences** |

**The density figures come from the tokeniser**, which is the instrument the
earlier figures came from, so the comparison is between like measurements.
Across three refreshes it has gone one per 103, one per 49, one per 24.7.

**Level-one closure is unchanged at 812 of 812 words needing a definition**,
100 percent, self-hosting. **No word was admitted to make generation
succeed.**

## The band was flagging fifty books against a figure for a different form

**Measured over 44 complete question books.**

| Form | Words a spread | Standard deviation | Relative variation | Band fit |
| --- | --- | --- | --- | --- |
| Narrative, sixteen records | 42.5 | 12.0 | 0.28 | 383 of 425 inside |
| Question, sixteen records | 29.0 | 15.1 | 0.52 | no comparable band fits |

**No band of comparable tightness fits the question form.** The best tried
holds 39 of 44 only by spanning 240 to 880 words, a range of nearly four to
one, which reports nothing. **So the figure is absent rather than invented**,
which is the reasoning `typical_words` already applies to levels five and
above, where its own docstring says reporting the level-one band would be a
made-up number presented as a standard.

**Removing a form from the unsettled set requires a measurement, not a
preference**, and the code says so.

## The check that was missing was firmer than the one that was firing

**A book is bound in signatures of sixteen pages**, so a level-one book short
of sixteen spreads cannot be published without someone padding or cutting it.
**Eight question books sat between eight and fifteen records and nothing said
so**, while fifty were flagged on a word count measured against the wrong
form's band.

**The word band is a judgement and the spread count is arithmetic over the
binding.** The firmer of the two was the one absent. It is reported now, and
the batch brought every question book to sixteen.

**Forty-four books remain outside the word band and none is a question
book.** They are narrative cross-concept variants running 200 to 270 words
against a 320 floor, they predate this work, and the module's posture is that
a book about one narrow thing is allowed to be short. **Untouched and named
rather than left to be rediscovered.**

## Sixteen spreads each, and zero new concept pairs

**Every question book carries sixteen exchanges**, one to a spread, because a
spread is a page turn and the turn is where the answer lands.

**That matters to pair coverage, which counts only books with exactly sixteen
records.** Before this batch, eight question books were below that and were
invisible to the measure. All 96 now qualify.

**And it changed the figure by nothing. Measured: 312 of 8,128 either way.**
Excluding every question book gives the same 312, so **the question books
contribute zero pairs the corpus did not already have.**

**That follows from what the form is** and is worth stating rather than
discovering later. A question book teaches its own unit's concepts, the same
ones its narrative sibling teaches, so every pair it realises was realised
already. **The form buys the corpus the ability to show a question being
answered. It buys no combinatorial richness at all**, and a later reading of
the pair figure should not expect this batch to appear in it.

## The prompt had no substitution block, and that is the third time

**`LEXICON.md` records the finding: naming a banned word is not supplying the
replacement.** The dictionary prompt acts on it. `retitle_books.py` relearned
it four refusals later. **`question_book` never had it at all.**

**Measured on the first full run**, of 86 tallied refusals, **61 were words
with neither an admission nor a substitution**: `important` 21, `okay` 15,
`act` 13, `complete` 6, `unsure` 6. Five substitutions are now recorded,
each replacement checked admissible: "means a lot", "all right", "do",
"done", "not sure". **No word was admitted.**

**The block is now one shared function** rather than a third copy, so a prompt
that wants it reaches for it instead of reimplementing it.

### The evidence that it helped, stated as weakly as it deserves

**`b1.tending` failed three times with "no subject definition survived"**,
meaning every candidate for its opening definition spread was refused. **It
succeeded on the first attempt after the prompt carried substitutions, and its
refusals fell from 67 lines to 2.**

**That is one unit and not a controlled result.** The generator samples the
teacher, so a fourth retry might have succeeded without the change. The
before-and-after is suggestive and is not offered as more than that.

## A title defect whose mechanism is general and whose instance is single

**`bk.b1.tending.q1` was titled "Add water and the plant keeps living", and
`add` is admitted at level two.** The title is not written by the teacher. It
is the first sentence of the schedule unit's own prose, **which is authored for
the schedule and constrained by nothing.**

**Measured: 1 of 96 unit form sentences leaves level one.** So the instance is
single and the mechanism is real. The book was retitled with every word
checked against the lexicon.

**The mechanism is not fixed here.** A check on authored schedule prose is a
larger change than this work covers, and naming it is better than widening
scope quietly.

## What this does not settle

**Question-book density is not a controlled quantity.** Its relative variation
is about twice the narrative form's, and until that narrows there is no band to
set. Whether it should narrow is a question about the form, not about the
measurement.

**The 44 out-of-band narrative books are unexamined.** They are a larger share
than expected and nothing here looked at whether they are short by design.

**Exchange quality is unmeasured.** Every book has sixteen spreads and nothing
here asks whether the answers answer well. `../../evals/elenchos/` is where
that would be measured and it was not run.
