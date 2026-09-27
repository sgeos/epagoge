# Is the corpus the limit, or was the model the wrong size?

> **STALE, 2026-09-27. Every figure below predates the tree it describes.**
> The corpus is now **400 books and 308,931 tokens**, the vocabulary 2,279
> ids, the head count derived rather than fixed at four, and the held-out
> loss a token-weighted sum over the whole set rather than a mean of
> per-batch means over a systematic slice. **The width ranking specifically
> is superseded**, since every wide point ran at four heads regardless of
> width. See the re-measurement at the end of this file.
>
> **Quote nothing here as a current property of this project.** It is kept
> because the reasoning is still worth reading and because deleting a
> measurement corrupts the record of why the next one was taken.

**Measured 2026-09-25 on one frozen corpus**: 70,205 words, 82,038 tokens,
756 chunks of which 94 held out, vocabulary 2,259. Every figure below comes
from that corpus. **It is not the corpus the earlier diagnosis used**,
which held 43,023 tokens, so nothing here should be compared against that
file's numbers except where this document does so explicitly and says it is
doing so.

## Why it was asked

The project records that the model is limited by its corpus rather than by
training, and that claim sets every priority beneath it. It rested on a
width sweep of **two points**, 1.39M and 4.35M parameters, both far into
the regime where a model memorises its data.

**A two-point sweep inside the memorisation regime cannot separate "the
corpus is too small" from "the model is too big for this corpus."** The
hypothesis under test was the second: that a smaller model would generalise
better on the same tokens, and that part of the recorded corpus limit was
really a capacity choice.

**The hypothesis is refuted.** It is recorded here rather than deleted,
because a project about falsification that quietly drops its own refuted
guesses is not doing the thing it claims.

## The capacity curve, twenty-six runs

Best held-out loss at each width, with the step count that produced it.

| Width | Parameters | Best held out | At steps | Perplexity |
| --- | --- | --- | --- | --- |
| 16 | 87,488 | 5.509 | 1600 | 247 |
| 32 | 199,552 | 5.252 | 1600 | 191 |
| 64 | 497,408 | 4.920 | 1600 | 137 |
| 128 | 1,388,032 | 4.628 | 1600 | 102 |
| 256 | 4,348,928 | 4.604 | 800 | 100 |
| 512 | 14,989,312 | 4.542 | 400 | 94 |
| 1024 | 55,144,448 | **4.525** | 400 | **92** |

Improvement per width doubling:

| Step | Held out | Parameters |
| --- | --- | --- |
| 16 to 32 | +0.257 | x2.3 |
| 32 to 64 | +0.332 | x2.5 |
| 64 to 128 | +0.292 | x2.8 |
| **128 to 256** | **+0.024** | x3.1 |
| 256 to 512 | +0.062 | x3.5 |
| 512 to 1024 | +0.017 | x3.7 |

## What it says

**The curve saturates at about width 128.** Below it, each doubling buys
roughly 0.29 nats. Above it, going from 128 to 1024 buys **0.103 nats for
forty times the parameters**. That is the signature of a data-limited
regime, which is what the project claimed.

**Smaller is decisively worse.** Width 16 reaches 5.509 against 4.525 at
width 1024. There is no small-model regime in which this corpus supports
better generalisation, so the hypothesis fails in the direction it
proposed.

**Bigger is barely better**, which is why it also fails in the other
direction. Nothing about model size is the lever here.

**The claim now rests on a saturation curve over a 630-fold range of
parameters** rather than on two adjacent points. It is better supported
than it was this morning, by an experiment designed to break it.

## One correction the sweep forces

**The best configuration was not the one in use.** The project's best
recorded figure was 4.789 at width 256, and nothing above 256 had ever been
run. On this corpus the best is **4.525 at width 1024 and 400 steps**.
`LEVEL_ONE_DIAGNOSIS.md` is amended accordingly.

**The optimal step count falls as width rises**: 1600 at widths 16 to 128,
800 at 256, 400 at 512 and 1024. A larger model reaches its best earlier
and then overfits harder. Width 1024's turn was not bracketed, since 400
steps was still improving and 800 was not run; it does not matter, because
the marginal gain there is 0.017 nats.

## Decomposing today's improvement

From 4.789 this morning to 4.525 now, a total of 0.264 nats and perplexity
120 to 92.

| Source | Change | Share |
| --- | --- | --- |
| Corpus, 43,023 to 82,038 tokens, at fixed width 256 | +0.185 | 70 percent |
| Capacity, width 256 to 1024, at fixed corpus | +0.079 | 30 percent |

**Corpus did most of it**, consistent with the project's position.

## The finding that was not being looked for

**The corpus scaling rate measured on real added material is 0.199 nats per
doubling, against the 0.29 the project has recorded.**

The recorded rate came from subsampling one corpus into fractions. This
figure comes from the corpus actually growing, 43,023 to 82,038 tokens,
which is 0.931 doublings for 0.185 nats at fixed width.

**If it holds, it matters.** At 0.29, a million tokens predicts perplexity
35. At 0.199 it predicts 49.

**A likely explanation, untested.** The growth came from
`generators/fill_spreads.py`, which lengthens the spreads a book already
has. It therefore adds more material about the same ninety-five units from
the same teacher, where subsampling removes and restores genuinely
different content. The project's own brief warned that more books about the
same units raise the token count without raising diversity; the same
argument applies to filling them and was not made.

**This is suggestive and not measured.** The two rates come from sweeps
with different held-out sets, and a controlled test would subsample the
current corpus into fractions the way the original did.

**THAT TEST WAS RUN THE SAME DAY AND THIS SECTION IS WRONG.** Against one
fixed held-out set, the most recent doubling of the corpus bought **0.316
nats, the largest increment in the series**, so the worry that filling adds
lower-value tokens is not supported. The 0.199 figure was an artifact of
comparing across two held-out sets. See the re-measurement in
`LEVEL_ONE_SCALING.md`, which also finds that the marginal rate rises
rather than holding constant, so no single rate should be quoted.

The section is kept rather than deleted because the reasoning that produced
it was wrong in a way worth being able to find again: **a figure is
comparable only to one measured against the same held-out set.**

## Files

`level_1_capacity.json` holds widths 16 to 256 at 200 to 1600 steps.
`level_1_capacity_wide.json` holds 256 and 512 at 400 to 1600.
`level_1_capacity_wider.json` holds 512 and 1024 at 100 to 400. All three
report the same 82,038 corpus tokens and 94 held-out chunks, which is what
makes the twenty-six points comparable.

---

# Re-measured 2026-09-27, with heads derived

**One of the three measurements `docs/process/HANDOFF.md` recorded as
owed.** Every wide point above ran at four heads regardless of width, so
width 1,024 was measured at head dimension 256 where 64 to 128 is standard.
Heads are now derived at one per 64 channels. Rotary positions, 128-token
windows, 400 books, 308,931 tokens, one seed per cell.

Held-out loss.

| Width | Parameters | 1,600 | 3,200 | 6,400 |
| --- | --- | --- | --- | --- |
| 128 | 1.08M | 3.539 | | |
| 256 | 3.74M | 3.235 | **3.037** | |
| 512 | 13.8M | **3.076** | 3.071 | 4.130 |
| 1,024 | 52.7M | 3.205 | 3.116 | 3.677 |

## What changed

**The old ranking is wrong and 1,024 is not the best width.** The earlier
sweep made width 1,024 the winner at 3.713. With heads derived it is worse
than both 512 and 256 at every duration measured.

**It is not undertraining, which was the obvious explanation and was
tested.** At 1,600 steps width 1,024 had a worse training loss than width
512, which is the signature of a model that has not converged rather than
one that has overfitted. Running it to 3,200 does not rescue it: 3.116
against 3.071 at width 512 and 3.037 at width 256.

**Best held-out loss anywhere in this table is 3.037, at width 256 and
3,200 steps**, which is a quarter the parameters of the width the old sweep
preferred.

## The collapse at 6,400 steps, which is the sharpest thing here

**Every width falls apart.** Width 512 goes to a training loss of 0.501
against held-out 4.130, a gap of 3.629. The model has memorised 308,931
tokens and stopped predicting anything else.

**That is the one place regularisation earns its keep**, and it earns a
great deal:

| Token replacement | Train | Held | Gap |
| --- | --- | --- | --- |
| 0.00 | 0.501 | **4.130** | 3.629 |
| 0.05 | 0.896 | 3.226 | 2.330 |
| 0.15 | 1.469 | **2.913** | 1.444 |

**1.217 nats**, and it converts the worst result in the table into the best
result at that width.

**The optimal rate rises with duration.** At 3,200 steps 0.05 beat 0.15, at
6,400 steps 0.15 beats 0.05 by 0.313. More passes over a fixed corpus need
more corruption, which is what the study this comes from found at 100
epochs.

**It buys duration rather than a better model.** 2.913 at 6,400 steps is
the same held-out loss as 2.912 at 3,200 steps with the lower rate. So
augmentation moves the point at which training stops helping; it has not
been shown here to move the frontier.

## Caveats

**One seed per cell in the capacity table.** The regularisation rows at
6,400 are also one seed. The three-seed work is in
`LEVEL_ONE_REGULARISATION.md` and covers 3,200 steps at width 512 only.

**Width and duration are not separable from this table**, since the wide
cells were not run at every duration. The blanks are missing, not zero.
