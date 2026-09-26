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

---

## The teacher was given the model to interrogate

**Measured 2026-09-25**, after the question-and-answer books were in the
training data. The operator asked for the teacher model to be briefed on
the project, allowed to interact with `sporos`, and then asked to rate it.
The teacher chose its own prompts, twice, the second set after seeing the
first results.

**The corpus at the time of the checkpoint held 233 question marks over
233 of 4,691 records, and 17 of 246 books were question-and-answer books.**
So this is not the earlier finding repeated. The form was present in
training and the model still did not learn it.

### What it produced

Six continuation prompts, every word verified to be inside the model's
vocabulary so that nothing could be blamed on an unreadable prompt:

> the floor . the air . the cup is not the cup is one . the cup is on the
> table . she is not cold . the cup is shows a name each , and it for
> drank to let . the cup is

**All six converged on `the cup is`**, and long spans appeared verbatim
across different prompts, including `a name each , and it for drank to
let`. The prompt barely moved the output.

Six question prompts:

> was is not move brought . that is where . the cup is one . the cup is on
> the table . she is not cold . a sure , not a name each , and each for
> drank to let . the cup is

**Every answer to a question began with `was`.** A question mark appears
to act as a cue for that single token. The model reported the two prompt
words it did not have, `color` and `winter`, rather than guessing.

### The teacher's verdict, and where it does not hold

Asked to rate the model given the project's maturity, it answered
**extremely disappointing**.

**Two of its observations are reproducible and worth keeping**: the
attractor collapse, and the question mark mapping to one token.

**Its causal reasoning does not follow.** It argued that predicting worse
than chance when overtrained "confirms that the corpus is not just small
but structurally impoverished." That is the ordinary signature of
overfitting a small dataset and is a statement about size, not structure.
The two were not separated by anything it saw.

**One of its claims is measurably overstated.** It called `cup` a dominant
subject. Measured over the 244 content books:

| | |
| --- | --- |
| `cup` share of content-book tokens | **1.69 percent** |
| Books containing `cup` | **85 of 244** |
| Next most frequent content word | `still`, 0.62 percent |

So `cup` leads the content words by a factor of 2.7 and appears in about a
third of the books. Disproportionate, not dominant. **That the model
collapses onto the single most frequent content noun is what a model of
4.3M parameters trained on 82,000 tokens would be expected to do.**

**And the teacher wrote this corpus.** A generator asked to judge a model
trained on its own output located the fault in the corpus rather than in
the training setup. That is at least not self-serving, but it is the part
of its answer its evidence least supports.

### What this does and does not establish

**It establishes that 5 percent of records carrying a form is not enough
to teach it.** 233 question marks in 4,691 records did not produce a model
that answers.

**It does not establish anything about the ordering hypothesis.** No
level-two model exists and no flat-order control has run. A single
undertrained level-one model cannot speak to it either way.
