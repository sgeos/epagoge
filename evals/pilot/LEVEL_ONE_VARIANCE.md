# Variance on the level-one corpus, and why it does not replace the pilot

**Measured 2026-09-25**, on the completed level-one corpus, eight paired
seeds, 800 steps, 1,371,136 parameters, Metal Performance Shaders.
Raw numbers in `level_1.json`.

## What was measured

| Quantity | Synthetic stream, 2026-09-24 | Level-one corpus, 2026-09-25 |
| --- | --- | --- |
| Parameters | 818,000 | 1,371,136 |
| Corpus | second-order Markov | **7,998 tokens, 62 chunks** |
| Mean held-out loss | 1.895 | **5.847** |
| Unpaired sigma | 0.0750 | **0.0889** |
| Paired sd | 0.0233 | **0.00344** |
| Correlation rho | 0.9539 | **0.9993** |
| Pairing gain | 20.7x | **1,338x** |

Mean difference **-0.00127**, curriculum arm below topological, which is
**within the paired standard deviation and decides nothing**. Five of
eight seeds favour the curriculum arm and three the topological one,
which is what a null looks like.

## The result must not be quoted as an improvement on the pilot

**It is a measurement of a degenerate regime, not a better estimate of the
same quantity.** Three facts together explain the correlation and none of
them is a property the ablation will have at scale.

**The corpus is cycled about 121 times.** 53 training chunks at batch
eight is seven batches, and 800 steps runs through them roughly 114 times
in the same sequence. `train_once` takes `batches[step % len(batches)]`,
so after the first pass the ordering contributes nothing that the
initialisation does not already determine. **An ordering effect is
expected to vanish under repetition, and it did.**

**The model has barely learned.** Held-out loss is 5.85 against ln(2193)
= 7.69 for a uniform distribution over the vocabulary. That is above
chance and far from converged, so the two arms are being compared on a
quantity neither has resolved.

**A paired sd of 0.0034 is not evidence that pairing is powerful here.**
It is evidence that the two arms are nearly the same run. The requirement
table in `level_1.json` consequently reports one paired seed for every
target effect, which is an artifact and **must not be used to plan an
ablation**.

## What this settles, and what it does not

**Settles**: the measurement harness runs end to end on the real corpus,
tokenising per book and permuting a shared chunk set, and reports the same
statistics as the pilot. The corpus-to-model loop is closed on real text.

**Does not settle**: item 6 of `../PRE_REGISTRATION.md`. The seed count
still rests on the synthetic pilot's rho of 0.9539, because that run at
least had a corpus it did not exhaust. Neither run used maximal update
parametrization, Muon or warmup-stable-decay, which
`../../docs/decisions/TRAINING_TECHNIQUES.md` adopts and which change the
dynamics.

## The binding constraint is corpus scale, not seed count

**7,998 tokens against a level-one budget of 10^6 to 10^7 is a factor of
125 to 1,250 short.** `../../docs/decisions/CORPUS_SCALE.md` asks for
twelve to six hundred books per topic; the corpus holds one, so the draft
is about a twelfth of the low end.

A full draft at one book per unit was the right target and it is reached.
**It is not a corpus an ordering ablation can be run on**, and the number
that has to move next is books per topic, not seeds per arm.

**An ablation run on this corpus would produce a null that means nothing**,
which is worse than no run, because a null from an underpowered design
reads the same as a null from a well-powered one unless someone records
the difference. This file is that record.
