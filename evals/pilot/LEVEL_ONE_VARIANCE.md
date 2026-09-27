# Variance and ordering on the level-one corpus

> **STALE, 2026-09-27. Every figure below predates the tree it describes.**
> The corpus is now **400 books and 308,931 tokens**, the vocabulary 2,279
> ids, the head count derived rather than fixed at four, and the held-out
> loss a token-weighted sum over the whole set rather than a mean of
> per-batch means over a systematic slice. **Its variance and correlation
> figures are the ones `evals/PRE_REGISTRATION.md` item 6 depends on**, so
> they need re-measuring before any ablation is run, not merely relabelling.
>
> **Quote nothing here as a current property of this project.** It is kept
> because the reasoning is still worth reading and because deleting a
> measurement corrupts the record of why the next one was taken.
> **The current measurement is at the end of this file.**

**Measured 2026-09-25**, eight paired seeds over 146 books, **35,438
tokens**, 1,382,912 parameters, Metal Performance Shaders. Raw numbers in
`level_1.json`, which has since been overwritten by a larger run.

**A corrected figure.** An earlier version of this file said 44,505
tokens. That was the sum of chunk lengths, and a chunk holds `seq_len + 1`
ids so inputs and targets can be offset, with a padded tail, so it counts
every boundary token twice and every pad once. The corpus was 35,438
tokens and the overstatement was a quarter. `train_level.py` now reports
both numbers under separate names.

## Two harness defects found first, and both were silent

**The chunker discarded three quarters of the corpus.** `chunk` dropped
the tail of every stream, and the streams are books. 35,438 tokens became
68 chunks of 128, which is 8,772 tokens, and every book shorter than 129
tokens contributed nothing at all. The median level-one book is 192
tokens. Chunks now carry a padded tail and the padding id is excluded
from the loss.

**The ordering silently covered thirteen books of a hundred and
forty-six.** A book's taught concepts were taken as the union of its
records' concepts, so a word a book merely defines counted as a concept
the book teaches. That manufactured dependencies between unrelated books
and made the dependency graph cyclic in twenty-four places.
`linear_extension` returns what it could order and says nothing, so the
run trained on nine per cent of the corpus and reported itself as the
level. A book now teaches what its schedule unit teaches, and
`train_level.py` refuses a short ordering instead of training through one.

**One cycle survived and it was real.** `m1.compare` taught
`same_and_different` and `more_and_fewer`, `m1.count` taught
`correspondence`, and the graph puts correspondence between the other
two. Each unit needed the other and no order of the two existed.
`correspondence` moved into `m1.compare`, which puts the chain inside one
unit. Two other resolutions exist and are recorded in the commit.

**Every figure below the first harness measurement is therefore a
measurement of something else**, and the earlier readings of rho 0.9993
and 0.9936 are withdrawn.

## What the corrected run measures

| Quantity | Synthetic stream | Level-one corpus |
| --- | --- | --- |
| Parameters | 818,000 | 1,382,912 |
| Corpus | second-order Markov | 35,438 tokens, 345 chunks |
| Mean held-out loss | 1.895 | 4.460 |
| Unpaired sigma | 0.0750 | 0.0142 |
| Paired sd | 0.0233 | 0.00421 |
| **Correlation rho** | **0.9539** | **0.9574** |
| **Pairing gain** | **20.7x** | **22.8x** |

**The pilot's central finding transfers.** The correlation and the pairing
gain land within a few per cent of the synthetic-stream figures on real
text at a different scale, which is the one thing the pilot was least
confident about. The absolute standard deviations are smaller because the
loss scale differs.

## The ordering effect reverses with training length

**This is the result worth keeping.** Identical corpus, identical arms,
identical seeds, one parameter changed.

| Steps | Mean difference | Paired sd | Seeds where curriculum is worse | Paired t |
| --- | --- | --- | --- | --- |
| 800 | **+0.01244** | 0.00421 | **8 of 8** | **+8.35** |
| 1,600 | **-0.02418** | 0.02157 | **1 of 8** | **-3.17** |

Positive means the curriculum arm has the higher held-out loss. At eight
hundred steps the curriculum ordering is worse in every seed. At sixteen
hundred it is better in seven of eight. **Both would pass a naive paired
test and they disagree.**

So **no ordering effect is claimed in either direction**, and the sign of
the difference is not evidence about ordering. Mean held-out loss also
rose from 4.460 to 4.498 with the longer run, so the second reading sits
past the point where the model stops improving on a corpus this size.

**This is what item 10 of `../PRE_REGISTRATION.md` is for.** An estimator
or endpoint chosen after seeing a curve is a choice about the result, and
here the endpoint alone moves the result from a strong effect to a strong
effect of the opposite sign. Fixing the endpoint in advance is not
bureaucracy. It is the difference between a finding and a coin toss.

## What this settles, and what it does not

**Settles**: the harness runs on the whole corpus, both defects above are
closed, and the pilot's pairing result holds on real text.

**Does not settle**: item 6. The seed count depends on a paired standard
deviation that itself moved by a factor of five between the two step
counts, so it cannot be fixed until the endpoint is. Neither run used
maximal update parametrization, Muon or warmup-stable-decay, which
`../../docs/decisions/TRAINING_TECHNIQUES.md` adopts.

**Corpus scale remains short.** 35,438 tokens against a level-one budget
of 10^6 to 10^7 is a factor of **28 to 282**, not the 22 to 220 an earlier
version of this file gave from the inflated count. Eight hundred steps at batch
eight over 345 chunks is about eighteen passes through the corpus, so
repetition still dominates and an ordering signal has eighteen chances to
wash out. The direction of travel is right: the draft was 7,998 tokens
before the two defects were fixed and more books were written.


---

# Re-measured 2026-09-27, and the pairing design has stopped paying

**Eight paired seeds at each of two endpoints**, on the current corpus:
400 books, 360,950 corpus tokens, width 256, four layers, 3,771,648
parameters, rotary positions, batch 16, sequence length 128. **Every
held-out batch is scored**, not the first 24 of 28.

| | 800 steps | 1,600 steps | Synthetic pilot |
| --- | --- | --- | --- |
| Mean loss | 3.5515 | 3.2746 | — |
| Seed sd | **0.006478** | **0.007239** | 0.0750 |
| Paired sd | 0.007356 | 0.010260 | 0.0233 |
| Correlation | **+0.392** | **-0.009** | 0.9539 |
| Pairing gain | **1.55x** | **1.00x** | 20.7x |

**Run-to-run variance has fallen by a factor of about eleven**, from 0.0750
to 0.0065. **The correlation that made pairing worth 22.8x has gone**, to
0.39 at the shorter endpoint and to zero at the longer one.

## Why this is good news even though it destroys the clever part

**The design was clever because the experiment was expensive.** Pairing was
worth two orders of magnitude when a 1 percent effect needed 246 unpaired
seeds. It is worth nothing now because that experiment has become cheap.

Seeds required, at each endpoint:

| Effect | 800 paired | 800 unpaired | 1,600 paired | 1,600 unpaired |
| --- | --- | --- | --- | --- |
| 2.0% | 1 | 1 | 1 | 1 |
| 1.0% | 1 | 1 | 1 | 1 |
| 0.5% | 2 | 3 | 4 | 4 |
| 0.2% | 9 | 14 | 20 | 20 |

**A 1 percent effect now needs one seed either way**, against the
pre-registered twelve paired and two hundred and forty-six unpaired.
Twenty paired seeds resolve 0.0046 nats at 800 steps and 0.0064 at 1,600.

**The cause is almost certainly the corpus.** It was 44,505 tokens when rho
was 0.9574 and it is 360,950 now, so each run sees eight times the data and
converges to a much more consistent place. When the shared component shrinks
toward the floor set by the evaluation itself, the correlation between two
runs that share an initialisation has little left to be a correlation of.

**The truncated evaluation was ruled out as the cause.** At 24 of 28
batches the same measurement gives rho 0.407 and 1.60x at 800 steps against
0.392 and 1.55x over the whole set. The instrument was not doing it.

## What this costs the endpoint decision

**Item 10 is much cheaper to get wrong than it was.** At either endpoint the
ablation is affordable at any effect size down to half a percent, so the
choice no longer trades power against cost. What it still decides is which
question is being asked.

## An observation about the arms, which is not the ablation

**This measurement was set up to estimate spread, and the spread turned out
to be small enough that the arms separate cleanly. That is worth reporting
and it is not a verdict.**

| Arm | 800 steps | 1,600 steps |
| --- | --- | --- |
| curriculum | 3.5947 (sd 0.0046) | 3.3175 (sd 0.0025) |
| topological | 3.5082 (sd 0.0072) | 3.2317 (sd 0.0092) |
| shuffled | 3.4799 (sd 0.0067) | 3.2014 (sd 0.0077) |

**The three arms order the same way at both endpoints**, and the gaps are
ten to thirty times the within-arm spread. **The sign no longer flips
between 800 and 1,600 steps**, which is the property that made item 10
load-bearing when it was recorded.

**This must not be read as the pre-registered result, for three reasons.**
Item 7, the minimum meaningful effect, is unchosen. Item 10, the endpoint
and estimator, is unchosen. And the confound below is large enough to
account for the whole thing.

## The confound, which is the most important thing on this page

**Batches are built from consecutive positions in the ordering.**
`pilot._batches` takes `order[start:start + batch_size]`, so the ordering
decides not only the sequence in which books are visited but **what each
batch is made of**.

**A curriculum ordering therefore produces homogeneous batches** of books
about neighbouring concepts at similar depth, and a shuffled ordering
produces heterogeneous ones. Batch composition affects gradient noise
independently of any curriculum effect, and it is a large effect in ordinary
stochastic gradient descent.

**So the arms differ in two things at once, and the ablation was designed to
vary one.** The observation above is consistent with a curriculum effect and
equally consistent with homogeneous batches training worse, and nothing here
separates them.

**The experiment that separates them** holds batch composition fixed while
varying only visit order, for instance by assigning chunks to batches by a
stride that is the same under every arm and permuting only the order in
which those fixed batches are visited. **It is not run here** and it is not
a small change to the trainer.

**Until it is run, no ordering result from this harness means what it
appears to mean**, including the earlier finding that the sign flipped with
the endpoint.

---

# The confound is real and it is most of the effect

**Measured 2026-09-27**, six seeds a cell, both endpoints, width 256, every
held-out batch scored.

## The control

**Books are shuffled inside consecutive blocks of 32.** That keeps the
curriculum and discards the homogeneity: over 223 batches it moves distinct
subjects per batch from **1.20 to 1.79**, which is 87 percent of the way to
the shuffled arm's 1.88, while leaving **every book within 10 percent of its
curriculum position**.

| Books per block | Subjects per batch | Books within 10% of place |
| --- | --- | --- |
| 1 | 1.20 | 100% |
| 8 | 1.55 | 100% |
| **32** | **1.79** | **100%** |
| 64 | 1.83 | 88% |
| 400 | 2.06 | 22% |

## What it does

Held-out loss, block 1 against block 32.

| Arm | 800 steps | 1,600 steps |
| --- | --- | --- |
| curriculum | 3.5946 → 3.5299, **-0.0647** | 3.3172 → 3.2563, **-0.0609** |
| topological | 3.5091 → 3.5116, +0.0026 | 3.2323 → 3.2320, -0.0003 |
| shuffled | 3.4799 → 3.4856, +0.0057 | 3.2002 → 3.2076, +0.0075 |

**The control moves the curriculum arm and leaves the other two alone.**
That is the placebo check and it passes: topological and shuffled were
already heterogeneous, so destroying homogeneity should do nothing to them,
and it moves them by at most 0.0075 against a curriculum shift of 0.06, an
order of magnitude more. **It replicates at both endpoints.**

## The answer

| | 800 steps | 1,600 steps |
| --- | --- | --- |
| curriculum minus shuffled, uncontrolled | +0.1147 | +0.1170 |
| the same gap, controlled | +0.0443 | +0.0486 |
| **share attributable to ordering** | **39%** | **42%** |

**About sixty percent of the curriculum arm's penalty is batch homogeneity
and not ordering.** The remaining 0.044 to 0.049 nats is still several
times the within-arm spread, so something ordering-related survives, and it
is less than half of what this harness reported.

**Every ordering figure this harness has produced overstates the effect by
about two and a half times**, including the earlier result that the sign
flipped between 800 and 1,600 steps, which was measured on the uncontrolled
arms.

**The control also makes runs more consistent.** Seed standard deviation
falls from 0.0058 to 0.0048 at 800 steps and from 0.0082 to 0.0041 at
1,600, and the correlation that pairing depends on recovers from about zero
to 0.24 and 0.33. **Homogeneous batches were a source of run-to-run noise
as well as of bias.**

## What this does not settle

**It does not say which ordering is better.** Items 7 and 10 are unchosen
and that verdict is not this measurement's to give. What is settled is that
the arms differ substantially for a reason the experiment was not designed
to measure.

**One width, one batch size, one corpus.** The homogeneity a batch has is a
function of how many chunks a book makes and how many chunks a batch holds,
both of which are fixed here.

**Block 32 is not a proof that 100 percent of the sequence is preserved.**
It preserves each book's position to within 10 percent of the corpus, which
is a coarse guarantee. A curriculum effect operating at a finer grain than
32 books would be partly destroyed by this control and would show up here as
homogeneity.
