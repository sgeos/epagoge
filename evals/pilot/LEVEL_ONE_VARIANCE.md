# Variance and ordering on the level-one corpus

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
