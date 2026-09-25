# Is the level-one model undertrained or out of corpus

**Measured 2026-09-25** over 43,023 corpus tokens, 433 chunks, 54 held
out, vocabulary 2,253. Raw numbers in `level_1_diagnosis.json`.

**The answer is corpus, overwhelmingly.** Training changes are worth
little until the corpus grows by an order of magnitude.

## The sweep

| Width | Steps | Parameters | Train | Held out | Gap |
| --- | --- | --- | --- | --- | --- |
| 128 | 400 | 1,386,496 | 4.792 | 5.146 | 0.353 |
| 128 | 800 | 1,386,496 | 4.084 | **4.884** | 0.800 |
| 128 | 1600 | 1,386,496 | 3.026 | 5.135 | 2.109 |
| 128 | 3200 | 1,386,496 | 1.303 | 6.500 | 5.198 |
| 256 | 400 | 4,345,856 | 3.957 | **4.789** | 0.832 |
| 256 | 800 | 4,345,856 | 2.827 | 5.014 | 2.187 |
| 256 | 1600 | 4,345,856 | 1.075 | 6.037 | 4.962 |
| 256 | 3200 | 4,345,856 | **0.040** | **7.794** | 7.755 |

## What it says

**Held-out loss turns upward almost immediately.** The best figure ever
measured on this corpus is **4.789**, a perplexity of about 120, at width
256 and four hundred steps. Every longer run is worse.

**At 3,200 steps and width 256 the model reaches a training loss of 0.040
and a held-out loss of 7.794.** It has memorised 43,023 tokens essentially
perfectly. ln(2253) is 7.72, so **its held-out predictions are worse than
a uniform distribution over the vocabulary**: it has learned the corpus
and learned nothing transferable.

**The gap is the diagnosis.** A model short of capacity or steps shows a
small gap with both losses high. Every row here shows the gap widening
with training while held-out loss rises. That is the signature of too
little data, not too little training.

**More capacity makes it worse, faster.** Tripling the parameters improves
the best held-out figure by 0.095 and reaches total memorisation in half
the steps.

## What would change it

**Corpus, by one to two orders of magnitude.** At the measured 220 tokens
a book:

| Target | Books | Per unit |
| --- | --- | --- |
| 100,000 tokens | ~456 | ~5 |
| 500,000 tokens | ~2,278 | ~25 |
| 1,000,000 tokens | ~4,556 | ~50 |

The level-one budget in `../../docs/spec/CURRICULUM_LEVELS.md` is 10^6 to
10^7 tokens, and `../../docs/decisions/CORPUS_SCALE.md` asks for twelve to
six hundred books per topic. **The corpus holds two or three per unit**, so
the spec was right and the draft is a twentieth of its low end.

**Training work worth doing, and it is second order.** Early stopping on
held-out loss, since the current default of 800 steps is past the optimum
at width 256 and near it at 128. Dropout and weight decay are both at
their defaults and untuned. Neither turns a perplexity of 120 into a model
anyone would want to talk to.

## What this means for interaction

**A model external parties can satisfactorily interact with is not
reachable at this corpus size**, and no training configuration in this
sweep comes close. The samples in `LEVEL_ONE_SAMPLES.md` are what a
perplexity of 120 looks like: locally plausible, incoherent past a clause.

The path is generation volume, which needs no decision from anyone, and
the tooling for it already exists.
