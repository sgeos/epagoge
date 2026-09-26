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

> **CORRECTED LATER THE SAME DAY. THERE IS NO SUCH TRIGGER, AND THE ERROR
> WAS MINE.** Every prompt above was sampled at `--seed 1`. At one seed the
> sampling path is largely fixed before the prompt is read, so all six
> outputs began alike for a reason that had nothing to do with question
> marks. Re-run over **eight** question prompts at eight different seeds,
> the same checkpoint begins with `was` **once**, with `.` three times, and
> otherwise with `of`, `whole`, `,` and `is`.
>
> The teacher was then shown this artifact as a measurement and built a
> theory on it, calling it a learned syntactic trigger. **That theory was
> answering a fact that was not true.** The lesson is recorded in
> `../../docs/process/PROCESS_STRATEGY.md`: sampling one seed across
> different prompts measures the seed, not the prompt.

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

## Is a better loss visible in the output? Marginally, and measurably

**Measured 2026-09-25**, comparing two checkpoints under **identical**
sampling settings, seed for seed, on the same 2,259-word vocabulary. The
earlier checkpoint was trained on 55,510 words; the later on 94,797 at the
best configuration then known, width 256 and 800 steps. Held-out loss
4.836 against **4.413**, perplexity 126 against **82**.

Over eight question prompts at eight seeds:

| | Earlier, perplexity 126 | Later, perplexity 82 |
| --- | --- | --- |
| Began with a plausible sentence-initial word | **3 of 8** | **8 of 8** |
| Began with punctuation | 3 | 0 |
| Question marks emitted | 0 | 2 |
| Distinct share over five continuations | 0.225 | 0.242 |

**So the improvement is real and narrow.** The later model always starts a
sentence like a sentence, and it has begun to produce question marks at
all. It does not answer questions, both remain dominated by `cup`, and
neither is coherent past a clause.

**Do not read the distinct share as progress.** 0.225 to 0.242 over 250
tokens is not a difference this measurement can resolve.

> **AMENDED 2026-09-26. IT IS WORSE THAN UNRESOLVABLE. Distinct share at a
> fixed temperature measures how SHARP a model is, not how good it is**, and
> a better-fit model is sharper. Swept over the same eight prompts and
> seeds:
>
> | Model | temp 0.8 | temp 1.0 | temp 1.2 |
> | --- | --- | --- | --- |
> | perplexity 126 | 0.428 | 0.597 | 0.694 |
> | perplexity 41 | 0.331 | 0.491 | 0.616 |
>
> The better model is **less** varied at every temperature, and recovers
> past the worse model's 0.8 figure by 1.2. The same holds for the
> attractor: `cup` occurrences for the better model run 24, 11, then 3 as
> temperature rises. **Neither figure separates a worse model from a
> sharper one**, so neither belongs in a quality comparison. The class is
> recorded in `../../docs/process/PROCESS_STRATEGY.md`.

**What it says about using perplexity as the progress measure.** A drop
from 126 to 82 buys a visible change in one discrete behaviour and no
change in the quality a reader would notice. Perplexity is tracking
something real and is a poor proxy for "worth talking to" at this range.

**It does not establish anything about the ordering hypothesis.** No
level-two model exists and no flat-order control has run. A single
undertrained level-one model cannot speak to it either way.


---

## The finished corpus, measured 2026-09-26

The level-one corpus reached its length standard, 244 of 244 content books
inside the word band, **172,810 words**, from 55,510 the previous morning.
A model retrained at the best configuration then available, width 1024 and
800 steps, reaches held-out **3.713**, a perplexity of **41** against 126
for the checkpoint that started the day.

**What improved, under identical prompts, seeds and temperature.**

| | perplexity 126 | perplexity 41 |
| --- | --- | --- |
| Began with a word rather than punctuation | 4 of 8 | **8 of 8** |
| Question marks emitted | 0 | 1 |

**What did not improve, and what that turned out to mean.** At temperature
0.8 the newer model repeats `cup` more often, 24 occurrences against 10,
and is less varied. Both reverse as temperature rises, so both are
sharpness rather than degradation, and neither is a quality signal. See the
amendment above.

**What the corpus did.** It became less concentrated, not more: `cup` fell
from 1.69 percent of content-book tokens to **1.21**, its lead over the
next content word narrowed from 2.7 times to 1.3, and distinct tokens used
rose from 1,497 to 1,643. The worry that lengthening books would concentrate
the corpus on its existing subjects is not supported.

**What still does not work.** The model does not answer a question. It is
not coherent across sentences. Unprompted it now holds a first-person voice
across a passage and produces whole sentences, which it did not before, but
prompted with a question it returns to declarative continuation.

**The honest summary of the day** is that a threefold corpus and a wider
model took perplexity from 126 to 41 and bought two narrow, checkable
behaviours. Whether that is worth eleven hours is the operator's call, and
the figures are here rather than an opinion about them.

---

## The teacher's rating history

The same teacher model was asked the same question twice, in one
conversation, with its first answer still in context. **Both ratings and
both sets of reasons are recorded**, because the change of mind is worth
more than either verdict.

| Asked | Corpus | Perplexity | Rating |
| --- | --- | --- | --- |
| 2026-09-25 | 55,510 words | 126 | **Extremely disappointing** |
| 2026-09-26 | 172,810 words | 41 | **Slightly disappointing** |

The four options offered were extremely disappointing, slightly
disappointing, slightly impressive, extremely impressive. It was told it
could say the honest answer lay outside them, and did not.

### What it was shown between the two

The capacity sweep, which tested its explanation directly. The corpus
tripling and the concentration figures. The scaling rate measured against
one held-out set. **And the withdrawal of the question-mark trigger it had
built a theory on**, stated as this project's error rather than left in
place.

It was also told plainly what still does not work: no answering, no
coherence across sentences, and more `cup` at a fixed temperature than
before.

### What it said the second time

> "My first answer, extremely disappointing, was too harsh, and I now
> withdraw it."

**What moved it**: the scaling curve holding and the perplexity drop, which
it said "directly contradict my earlier assumption that the corpus was
structurally impoverished."

**What did not**: the persistence of `cup`, which it re-read as "a symptom
of overrepresentation, not a structural flaw."

**Its summary**: "It is not stuck in a trap. It is learning."

### Where the second answer is unsupported, which is the point of recording it

**It withdrew a claim it was shown to be wrong about and immediately made a
new one in the opposite direction.** From "the corpus is not a curriculum
but a trap" to "the data supports the project's core hypothesis: that a
graded, authored corpus can improve pretraining when scaled."

**Nothing measured tests that.** What was measured is that more data lowers
held-out loss, which is true of nearly any corpus. The ordering hypothesis
needs a flat-order control and that ablation has never run. Its further
claim that the corpus improves learning "not just in size, but in quality"
has no comparison corpus behind it at all.

**It also swapped one wrong attribution for another.** It attributed the
remaining incoherence to "the current model's capacity to generalize."
If that means parameters, the capacity sweep it had just been shown says
the opposite: the curve saturates, so the model is data-limited.

**And it asserted learned bias over evidence to the contrary.** It was told
that the `cup` repetition reverses as temperature rises, which points to
sharpness. It concluded learned bias without addressing that.

### What this is worth

**As a rating, little.** A model asked to judge prose it wrote itself,
shown evidence chosen by the asker, moved one step on a four-point scale.

**As a demonstration, more.** Both answers were stated with equal
confidence and both overreached their evidence, in opposite directions,
about fifteen hours apart. **That is the behaviour this project exists to
train against**, produced on demand by the model writing its corpus, and it
is the clearest argument in the repository for why
`docs/spec/CLAIM_TAXONOMY.md` marks the epistemic status of every record
and why `CLAUDE.md` forbids stating a curriculum benefit as established.

The session that produced both is not in version control. The prompts and
the model's answers are quoted above in full where they bear on a claim.
