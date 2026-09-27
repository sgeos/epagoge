# The reference configuration, and what the frontier is

**Measured 2026-09-27** on 444 books and 322,136 training tokens, three
seeds a cell, scoring **every held-out batch**.

**If you are looking for what to train with, this is it.**

    PYTHONPATH=src .venv/bin/python tools/sample_level.py --level 1 \
      --steps 3200 --d-model 512 --layers 4 --positions rotary \
      --token-replacement 0.05

| Setting | Value | Why |
| --- | --- | --- |
| positions | rotary | 0.292 nats over a learned table at this window |
| width | 512 | Beats 256 **only when regularised** |
| layers | 4 | Unswept |
| steps | 3,200 | About twenty epochs, which is the optimum at every corpus size |
| token replacement | 0.05 | 0.15 is indistinguishable from it here |
| steps | 3,200 | About twenty epochs, the optimum at every corpus size |
| tying, derived heads | on, the defaults | |

## The frontier

| Configuration | Held-out, 3 seeds | sd |
| --- | --- | --- |
| Defaults, width 256 | 3.236 | 0.003 |
| **Reference** | **3.156** | 0.018 |

**0.080 nats, which is about a third of a corpus doubling.** A doubling is
worth 0.26 and costs roughly fifteen generation rounds;t his costs one flag.

## The grid it came from

Held-out loss, one seed a cell, **scored on 24 of 48 held-out batches**, so
these are comparable to each other and about 0.25 nats below the true
values.

| Width | Steps | tr 0.00 | tr 0.05 | tr 0.15 |
| --- | --- | --- | --- | --- |
| 256 | 1,600 | 3.229 | 3.243 | 3.314 |
| 256 | 3,200 | 3.014 | **2.984** | 3.043 |
| 512 | 1,600 | 3.067 | 3.074 | 3.141 |
| 512 | 3,200 | 3.028 | **2.910** | 2.927 |

**Capacity pays only if it is regularised.** Unregularised, width 512 is
slightly worse than 256, at 3.028 against 3.014. Regularised at 0.05, it is
clearly better, 2.910 against 2.984. **That interaction is the reason a
sweep over width alone had made 1,024 look bad and 512 look marginal.**

**Token replacement at 0.05 and 0.15 are not distinguishable at this
cell**, at 2.908 and 2.915 over three seeds with a spread of 0.013, so the
choice of 0.05 is arbitrary between them and the record says so rather than
implying a tuned optimum.

## A truncation that affects every figure this tool has produced

**`tools/diagnose_level.py` scored 24 of 48 held-out batches** and
announced it on every run. The same configuration measures **2.908 on 24
batches and 3.156 on 48**.

**Comparisons survive and absolute numbers do not.** Every cell of every
sweep was truncated identically, so a difference measured between cells is
sound; the reference-against-default gap moves only from 0.106 to 0.080.
**But any figure quoted as a loss is about 0.25 nats optimistic**, and
that includes the scaling curve, the capacity table, the regularisation
record and the positions grid, all measured the same day.

**The tool now takes the whole set.** `train_level.py` gained the same
option earlier and this is the second instrument to need it.

## What is not established

**Four layers is unswept.** Every figure here holds depth fixed.

**Weight decay was not re-swept in combination.** It was measured to help
only where the training-to-held-out gap exceeds about one nat, and the
reference configuration's gap is 0.76, so it is left at the default on that
reasoning rather than on a measurement of the combination.

**This is held-out loss on the curriculum tail**, which is not a sample of
typical corpus text and is not the property `../elenchos/` measures.
