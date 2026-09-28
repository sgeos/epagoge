# Weight decay at level one, and where it starts to matter

> **Figures below were scored on 24 of 48 held-out batches**, which every
> run announced. Comparisons between cells are sound because the truncation
> is identical; **absolute losses are about 0.25 nats optimistic**. See
> `REFERENCE_CONFIGURATION.md`, measured on the whole set.


**Measured 2026-09-27** on the 400-book corpus, 306,449 training tokens,
rotary positions, tied embeddings, derived head count, sequence length 128.
All figures are held-out loss under the corrected token-weighted evaluation.

**This tests a claim taken from the literature**, recorded in
`../../docs/decisions/TRAINING_ADVANCES.md`, that weight decay in
data-constrained pretraining should be far above the usual default. This
project had never set it, so it was 0.01 by inheritance from torch.

## The answer depends on the endpoint, and the sign flips

**Sweep at weight decay 0.01 against 0.5**, one seed, held-out loss.

| Width | Steps | Gap at 0.01 | Held 0.01 | Held 0.5 | Better |
| --- | --- | --- | --- | --- | --- |
| 256 | 800 | 0.127 | **3.523** | 3.569 | 0.01 |
| 256 | 1,600 | 0.277 | **3.229** | 3.286 | 0.01 |
| 256 | 3,200 | 0.601 | **3.007** | 3.081 | 0.01 |
| 512 | 800 | 0.234 | **3.311** | 3.331 | 0.01 |
| 512 | 1,600 | 0.530 | **3.059** | 3.079 | 0.01 |
| 512 | 3,200 | **1.366** | 3.066 | **3.009** | **0.5** |

**Weight decay loses in five of six cells and wins in the sixth**, and the
sixth is the only one where the model is actually overfitting.

**The clearest single number is not in the table.** At width 512 and weight
decay 0.01, held-out loss goes 3.311, then 3.059, then **3.066**. It stops
improving and turns upward between 1,600 and 3,200 steps. At weight decay
0.5 the same points are 3.331, 3.079, **3.009**, still falling. **The
treatment converted a run that had begun to degrade into one that had
not.**

## The decisive cell, at three paired seeds

Width 512, 3,200 steps, everything else held fixed, seeds differing only in
initialisation and batch order.

| Seed | Held at 0.01 | Held at 0.5 | Difference |
| --- | --- | --- | --- |
| 0 | 3.066 | 3.009 | **-0.057** |
| 1 | 3.045 | 3.002 | **-0.043** |
| 2 | 3.050 | 2.985 | **-0.065** |

**Three of three in the same direction, mean -0.055 nats.** The
training-to-held-out gap falls from about 1.33 to about 0.99 across the
same seeds.

## What this does and does not establish

**It establishes that the literature's claim is conditional, and names the
condition.** Weight decay helps where the gap is large and costs loss where
it is not, which is what a regulariser should do and is not what a
recommendation to raise it by default would predict.

**The decisive cell was chosen after seeing the first sweep.** It was chosen
for a principled reason, being the only cell with heavy overfitting, but it
was chosen post hoc and the three seeds were run only there. **That is a
weaker design than a pre-registered one** and this record says so rather
than presenting six cells and three seeds as one plan.

**Only two values of weight decay were compared.** 0.5 is not shown to be
the best value at that cell, only better than 0.01. The literature's optima
run to 3.2 at much larger scale and nothing here bounds the curve.

**One corpus, one sequence length, one position scheme.** Nothing here says
whether the flip point moves with any of them.

**No variance estimate covers the five losing cells.** They are one seed
each, and the differences there, 0.020 to 0.074, are of the same order as
the paired differences that were significant at the decisive cell. **A
five-of-six count is not five findings.**

## What it changes

**The default stays at 0.01**, because five of six measured cells prefer it
and because the standard training configuration for this project is not the
decisive cell.

**Anything training wider or longer should raise it**, and the tool takes
`--weight-decay` so that is one flag.

**It supplies a rule of thumb this project can use**: raise weight decay
when the training-to-held-out gap passes about one nat. That rule is
induced from six cells and is a hypothesis, not a result.

## Token replacement, which is the larger effect

**Measured 2026-09-27 at the same decisive cell**, width 512, 3,200 steps,
rotary. A fraction of input tokens is replaced by a random one and the
target is left alone, so the model is still asked for the original next
token from a context that is partly wrong.

| Rate | Train | Held | Gap |
| --- | --- | --- | --- |
| 0.00 | 1.870 | 3.061 | 1.191 |
| **0.05** | 2.058 | **2.912** | 0.854 |
| 0.15 | 2.304 | 2.930 | 0.626 |

**Three paired seeds at 0.05 against nothing.**

| Seed | Held at 0.00 | Held at 0.05 | Difference |
| --- | --- | --- | --- |
| 0 | 3.061 | 2.912 | **-0.149** |
| 1 | 3.050 | 2.941 | **-0.109** |
| 2 | 3.054 | 2.923 | **-0.131** |

**Three of three, mean -0.130 nats**, which is 2.4 times the weight-decay
effect at the same cell.

**The rate this project wants is lower than the published one.** The study
that motivated this found 15 percent best at 150M parameters on 75M tokens.
Here 5 percent beats 15 percent, by 0.018 at seed 0. That is one seed and
the two are close, so the honest statement is that 5 is at least as good
here and the published optimum did not transfer unchanged.

## At 6,400 steps it stops being an improvement and becomes a rescue

**Measured 2026-09-27**, width 512, where training to 6,400 steps collapses.

| Rate | Train | Held |
| --- | --- | --- |
| 0.00 | 0.501 | **4.130** |
| 0.05 | 0.896 | 3.226 |
| 0.15 | 1.469 | **2.913** |

**1.217 nats.** At this duration the untreated model has memorised the
corpus, and `LEVEL_ONE_CAPACITY.md` has the surrounding table.

**The best rate rises with duration**, from 0.05 at 3,200 steps to 0.15 at
6,400. That is the direction the source study predicts, since it found 15
percent best at 100 epochs.

**It buys duration and not a better model.** 2.913 at 6,400 steps is the
same as 2.912 at 3,200 with the lower rate, so what moves is where training
stops helping.

## The two regularisers do not stack

Weight decay 0.5 with token replacement 0.05, seed 0, same cell: **2.921**,
against 2.912 for token replacement alone and 3.009 for weight decay alone.

**Adding weight decay on top of token replacement changes nothing**, and if
anything is marginally worse. They are two treatments for the same slack
rather than two independent gains, and token replacement dominates. One
seed, so this bounds the combination rather than settling it.

## The learning-rate floor, which is a null here

`min_lr_fraction` is 0.1 and the optimizer benchmark's eighth takeaway says
decaying further than 10 percent of the maximum significantly improves
results. **It does not here.** Width 256, one seed.

| Floor | Held at 1,600 | Held at 3,200 |
| --- | --- | --- |
| **0.1** | **3.235** | **3.037** |
| 0.01 | 3.258 | 3.043 |
| 0.0 | 3.262 | 3.045 |

**The current value is best at both endpoints** and the ordering is
consistent, though the differences run from 0.006 to 0.027 and are one seed
each. **This is an absence of evidence for the finding here, not a
refutation of it.** The benchmark's result is at 124M to 720M parameters
with batch sizes in the hundreds of thousands of tokens.

## What all of this changes

**Token replacement at 0.05 is the one intervention worth using**, and only
where the model overfits. The default stays at 0.0 for the same reason the
weight-decay default stays at 0.01: the standard configuration is not the
decisive cell.

**The rule of thumb is unchanged and now has a better lever.** When the
training-to-held-out gap passes about one nat, reach for
`--token-replacement 0.05` before `--weight-decay`.

## Reproducing

**Pass `--out`.** `tools/diagnose_level.py` writes
`evals/pilot/level_1_diagnosis.json` by default, which is a tracked record,
so a probe silently overwrites it with one cell. That happened while these
figures were being taken and was reverted.

**Amended 2026-09-28: it happened again, and the default is gone.** A
200-step probe overwrote the same file one command after a brief carrying
this warning was written. That is the second occurrence against three
warnings, so `--out` is now required on `diagnose_level.py`,
`sample_level.py` and `train_level.py`, all three of which defaulted to a
tracked path. **A tool cannot know whether a run is a probe or a record**, and
the two had been sharing a default.

    PYTHONPATH=src .venv/bin/python tools/diagnose_level.py --level 1 \
      --positions rotary --steps 3200 --width 512 --weight-decay 0.5 --seed 0 \
      --out tmp/probe.json

**`level_1_diagnosis.json` is stale and was left alone rather than
replaced.** It records a corpus of 43,023 tokens against 358,099 today, so
it describes a tree that no longer exists, and a single-cell probe is not a
better record than a stale full sweep. Re-running it belongs with the
measurements `../../docs/process/HANDOFF.md` lists as owed.
