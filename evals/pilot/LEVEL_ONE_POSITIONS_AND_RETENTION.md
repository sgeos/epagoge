# Rotary positions, whole-book streams, and what the model fails to retain

**Measured 2026-09-26** on the finished level-one corpus, 206,206 tokens,
after the lexicon culls. Held-out is **30 books**, split on book boundaries,
so every figure in the grid below scores the same text and differs only in
how the model saw its training data.

## The grid

Best held-out loss across a step sweep, width 256, four layers.

| Positions | 128-token windows | One sequence per book, 1,088 |
| --- | --- | --- |
| learned table | 3.550, perplexity 34.8 | 3.854, perplexity 47.2 |
| **rotary** | **3.141, perplexity 23.1** | 3.466, perplexity 32.0 |

**Rotary is worth 0.409 nats at 128 and 0.388 at 1,088.** Short windows are
worth 0.304 nats with a learned table and 0.325 with rotary. Each effect is
the same size at either setting of the other, **so they are independent**.

## Two hypotheses, one supported and one refuted

**Supported: rotary positions are a large, cheap win.** 0.4 nats, with
slightly *fewer* parameters, since a table with one row per index is gone.
This is the first architecture change the project has made, and it is the
biggest single improvement it has measured. The BabyLM organisers found
architecture the strongest lever among their submissions and this agrees.

**Refuted: that a book should be one training sequence.** It was worth
testing, the operator's reasoning was sound, and it is wrong at this scale.
A whole-book sequence is worse by about 0.3 nats and takes four times the
tokens to get there.

**Refuted for the second time: my explanation of why.** I proposed the
learned position table was starving, because at 128 tokens each of its rows
is seen by about eleven training sequences and at 1,088 by a fifth of one.
**If that were the cause, rotary would have closed the gap. It did not.**
The gap is 0.304 with a table and 0.325 without one.

**So the cause is something else and this document does not name it.** The
candidates are that 216 sequences give less diverse batches than 1,458, that
fewer gradient updates per token is worse at this data scale, or that the
model simply cannot use long context with 200,000 tokens to learn from.
BabyLM's finding that shorter input sequences succeeded suggests this is
general rather than specific to here.

## What the model fails to retain

`tools/retention.py`, per-token loss on each book under the rotary
checkpoint, averaged over the books whose unit teaches or revisits a
concept. 246 books, 124 concepts, mean loss 2.706. **These are training
books, so this is retention and not generalisation**, which is the same
quantity LFR selects on.

**The worst-retained concepts are the ones this project exists to teach.**

| Loss | Books | Concept |
| --- | --- | --- |
| 4.011 | 1 | `giving_a_reason` |
| 4.011 | 1 | `disagreeing` |
| 4.011 | 1 | `agreeing` |
| 3.687 | 1 | `keeping_your_claim` |
| 3.687 | 1 | `changing_your_mind` |
| 3.445 | 4 | `not_both`, `if_then`, `all_some_none` |
| 3.428 | 1 | `settling_it`, `finding_out` |
| 3.343 | 1 | `right_reason` |

**The best-retained are concrete and physical**: `emptiness` and `presence`
at 2.017, `finished_or_not` 2.058, `goal` 2.177, `who_said_it` 2.194.

**That is the most actionable finding in this document.** The corpus teaches
physical facts well and epistemic relations badly, and the epistemic
relations are the point. `giving_a_reason`, `disagreeing`,
`changing_your_mind` and `keeping_your_claim` are the vocabulary of
falsification, and they are at the bottom of the list.

## The schedule audit is not wrong, it is undiscriminating

**`coverage.py` flags 116 of 124 concepts as taught once and never
revisited. That is 94 percent.** The model's worst quartile is 31 concepts
and all 31 fall inside the 116, which sounds like agreement and is close to
arithmetically unavoidable.

**So the audit identifies almost everything and therefore ranks nothing.**
Its value is as an inventory. The model's measurement says which of the 116
to write for first, which is what the spaced-repetition literature argues
scheduling should be based on.

## Books per concept and retention

**Concepts taught by a single book are retained measurably worse.**

| Books teaching it | Concepts | Mean loss |
| --- | --- | --- |
| 1 | 51 | 3.028 |
| 2 | 2 | 2.542 |
| 3 | 23 | 2.635 |
| 4 | 20 | 2.867 |
| 5 or more | 28 | 2.572 |

Correlation between books per concept and mean loss, **r = -0.362** over
124 concepts.

**Two reasons not to read this as a recipe.** The correlation explains
about a eighth of the variance, and the jump is almost all between one book
and two rather than continuing upward. And it is **confounded**: the
abstract concepts have fewer books partly because they are harder to write
picture books about, so difficulty and book count are entangled and this
measurement cannot separate them.

**What it does support** is the recursive-drafting argument: depth at level
one comes from more books about the same concept, and the concepts with one
book are the ones the model knows least.

## What changed in the tree

`ModelConfig.positions` takes `learned` or `rotary`, rotary is
hand-written because `nn.TransformerEncoderLayer` computes attention
internally, and seven tests cover it including that the model stays causal.
`tools/sample_level.py` defaults to rotary. `tools/retention.py` is new and
reports rather than gates. The checkpoint in `evals/pilot/level_1.pt` is
rotary at 128 tokens and 1,600 steps.

**One figure in this document is not comparable to the others.** The
retraining run reports held-out 3.4426, which is on `sample_level.py`'s own
random fifteen percent of chunks rather than the book-boundary split used
for the grid. Different held-out sets, so the two numbers are not
comparable, which is the rule this project has broken four times and is
restating here.
