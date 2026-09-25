# What another order of magnitude of corpus would buy

**Measured 2026-09-25.** Four corpus fractions against one held-out set,
three step counts each, width 256, four layers, 4,345,856 parameters. Raw
numbers in `level_1_scaling.json`.

`LEVEL_ONE_DIAGNOSIS.md` established that the corpus is the limit. This
says how much corpus is worth writing.

## Best achievable held-out loss, by corpus size

| Training tokens | Best held out | Perplexity | At steps |
| --- | --- | --- | --- |
| 5,607 | 5.782 | 324 | 200 |
| 11,329 | 5.400 | 221 | 200 |
| 22,773 | 5.120 | 167 | 400 |
| 45,547 | **4.894** | **133** | 400 |

**Best is taken across step counts** because the optimum moves with corpus
size: a twelfth of the corpus overfits by two hundred steps and the whole
corpus wants four hundred. Comparing at one fixed step count would have
measured the schedule rather than the data.

## The fit, and what it extrapolates to

Held-out loss falls almost exactly linearly in the logarithm of corpus
size over the range measured.

    held = 9.382 - 0.422 * ln(tokens)

**Every doubling of the corpus buys about 0.29 nats.**

| Tokens | Books, at 220 a book | Per unit | Predicted perplexity |
| --- | --- | --- | --- |
| 45,547 | 207 | 2 | **133, measured** |
| 100,000 | ~456 | ~5 | ~92 |
| 1,000,000 | ~4,556 | ~50 | ~35 |
| 10,000,000 | ~45,560 | ~500 | ~13 |

The level-one budget is 10^6 to 10^7 tokens, and `CORPUS_SCALE.md` asks
for twelve to six hundred books per topic. **Both land in the range where
this curve predicts a usable model**, which is the first evidence in the
repository that those figures were set at the right order.

## Why the extrapolation is optimistic, and why it is also pessimistic

**Optimistic.** Four points spanning 0.9 orders of magnitude are being
extended over 2.3. A log-linear fit has no floor, and real curves flatten
towards an irreducible loss, so the true figures at 10^6 and 10^7 will be
worse than these.

**Pessimistic.** The model is fixed at 4.3 million parameters throughout.
At 10^6 tokens that is far below the size the data would support, and the
diagnosis already shows capacity helping once data allows it.

The two pull in opposite directions and neither is quantified here.
**Treat the table as an order of magnitude, not a prediction**, and
re-measure the curve rather than trusting it once the corpus has grown.

## What it means for the interaction goal

Operator direction 2026-09-25: a level-one model external parties can
satisfactorily interact with.

**Perplexity 133 is not that**, and the samples in `LEVEL_ONE_SAMPLES.md`
show what it sounds like. **Perplexity 35 might be**, and that is 10^6
tokens, about fifty books a unit, roughly twenty times what exists.

This is generation volume, not a decision. `generate_books.py --variants
N` writes an Nth book per unit and the observed rate is about
twenty-five books a round.
