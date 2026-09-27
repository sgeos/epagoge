# Weight decay at level one, and where it starts to matter

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

## Reproducing

**Pass `--out`.** `tools/diagnose_level.py` writes
`evals/pilot/level_1_diagnosis.json` by default, which is a tracked record,
so a probe silently overwrites it with one cell. That happened while these
figures were being taken and was reverted.

    PYTHONPATH=src .venv/bin/python tools/diagnose_level.py --level 1 \
      --positions rotary --steps 3200 --width 512 --weight-decay 0.5 --seed 0 \
      --out tmp/probe.json

**`level_1_diagnosis.json` is stale and was left alone rather than
replaced.** It records a corpus of 43,023 tokens against 358,099 today, so
it describes a tree that no longer exists, and a single-cell probe is not a
better record than a stale full sweep. Re-running it belongs with the
measurements `../../docs/process/HANDOFF.md` lists as owed.
