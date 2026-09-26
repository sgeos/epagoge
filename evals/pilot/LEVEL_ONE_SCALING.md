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

---

## RE-MEASURED 2026-09-25, on a corpus more than twice the size

The instruction above was followed. Four fractions of a **98,033-token**
corpus against one fixed held-out set of 110 chunks, width 256 throughout,
best taken across 200, 400 and 800 steps. Raw numbers in
`level_1_scaling_now.json`.

**The tool that produced the original table was never committed.** Every
row of `level_1_scaling.json` carries a `fraction` field and nothing in the
repository could produce one, so the number setting this project's corpus
target could not be reproduced from the tree. `tools/diagnose_level.py`
takes `--fractions` as of today.

| Training tokens | Best held out | Perplexity | At steps |
| --- | --- | --- | --- |
| 10,135 | 5.262 | 193 | 200 |
| 20,925 | 5.056 | 157 | 400 |
| 42,099 | 4.825 | 125 | 400 |
| 85,747 | **4.501** | **90** | 800 |

### The log-linear claim does not survive

**The marginal rate is not constant. It rises.**

| Doubling | Nats bought | Per doubling |
| --- | --- | --- |
| 10,135 to 20,925 | +0.206 | 0.197 |
| 20,925 to 42,099 | +0.231 | 0.229 |
| **42,099 to 85,747** | **+0.324** | **0.316** |

The average over the whole range is **0.247**, against 0.294 measured the
same way on the smaller corpus. But an average is the wrong summary of a
curve whose increments run 0.197, 0.229, 0.316. **"Every doubling buys
about 0.29 nats" is a fit to a relation the data does not show**, and any
extrapolation from a single rate inherits that.

What the extrapolation to 10^6 tokens becomes, depending on which rate is
carried forward:

| Rate carried forward | Predicted perplexity at 10^6 |
| --- | --- |
| 0.247, the average fit | 38 |
| 0.294, the earlier figure | 32 |
| 0.316, the latest marginal | 29 |

**All three land in the same order**, which is the only claim the earlier
table was making, so the conclusion about the level-one budget stands. The
precision does not.

### A correction to a concern raised earlier the same day

An earlier reading compared the best figure on the 43,023-token corpus to
the best on the 82,038-token corpus, inferred a rate of **0.199**, and from
that raised the worry that filling spreads adds lower-value tokens than
writing new material would.

**That comparison was across two different held-out sets and the worry is
not supported.** Measured against one held-out set, the most recent
doubling bought **0.316 nats, the largest increment in the series**. On
present evidence lengthening books is paying at least as well as anything
measured before it. The 0.199 figure should not be quoted.

**Why the cross-set comparison misled.** Each sweep holds out the last
eighth of its own chunk list, so a corpus that has grown holds out
different material. The two numbers were never measuring the same thing,
and the lesson generalises: **a figure is comparable only to one measured
against the same held-out set.**

## What it means for the interaction goal

Operator direction 2026-09-25: a level-one model external parties can
satisfactorily interact with.

**Perplexity 133 is not that**, and the samples in `LEVEL_ONE_SAMPLES.md`
show what it sounds like. **Perplexity 35 might be**, and that is 10^6
tokens, about fifty books a unit, roughly twenty times what exists.

This is generation volume, not a decision. `generate_books.py --variants
N` writes an Nth book per unit and the observed rate is about
twenty-five books a round.
