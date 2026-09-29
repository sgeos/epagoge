# The reference configuration, and what the frontier is

**Measured 2026-09-28** on 523 books and **344,348 training tokens**, three
seeds a cell, scoring **every held-out batch**.

**If you are looking for what to train with, this is it.**

    PYTHONPATH=src .venv/bin/python tools/sample_level.py --level 1 \
      --steps 3400 --d-model 512 --layers 4 --positions rotary \
      --token-replacement 0.05 --optimiser muon \
      --weights tmp/reference-level-1.pt --out tmp/reference-level-1.json

| Setting | Value | Why |
| --- | --- | --- |
| **optimiser** | **muon** | **0.117 nats over AdamW, the largest single lever measured** |
| positions | rotary | 0.292 nats over a learned table at this window |
| width | 512 | Best of 256, 512 and 1,024 **each at its own tuned rate** |
| layers | 4 | Unswept |
| steps | 3,400 | About 20.2 epochs on this corpus, and twenty is the optimum at every corpus size measured |
| token replacement | 0.05 | 0.15 is indistinguishable from it here |
| schedule | cosine | Warmup-stable-decay is reliably 0.024 worse at a fixed duration |
| weight decay | the default | 0.1 does not move the loss and 0.5 is 0.20 worse |
| tying, derived heads | on, the defaults | |

The example writes new artifacts and refuses existing destinations. It does
not replace the current reference checkpoint. Select a new destination for
each run. Use `--overwrite` only when replacement is intended.

For interrupted-run continuation, add `--training-state` with a separate
path. Keep the planned step count unchanged when resuming with `--resume`.
See `docs/process/HANDOFF.md` for the restart contract.

## The frontier

| Configuration | Held-out, 3 seeds | sd |
| --- | --- | --- |
| Defaults, cosine and AdamW | 3.183 | 0.0125 |
| **Reference** | **3.066** | **0.0032** |

**0.117 nats, and it costs one flag.** A corpus doubling buys about 0.26 and
costs roughly fifteen generation rounds.

**The authoring-host checkpoint reports 3.061** on its own single seed, inside the
three-seed spread. `evals/pilot/level_1.pt` is trained at this configuration
and `tools/talk.py` runs against it.

**The supporting grid is in `LEVEL_ONE_OPTIMISER.md`**, including the
combination that does not add.

## Caveats. Two were raised and resolved, one stands

**~~This is default against default, not tuned against tuned.~~ Resolved
2026-09-28 and the caveat is removed.** Both rates were swept and **both
defaults sit at their measured optimum**, bracketed on either side, so the
comparison was tuned against tuned by accident. The figure stands unchanged.
See `LEVEL_ONE_LEARNING_RATE.md`.

**The caveat is struck through rather than deleted**, because it was correct to
raise and could have gone the other way.

**~~The width row is provisional for the same reason.~~ Resolved 2026-09-28
and the ranking survives.** Each of 256, 512 and 1,024 was swept to a bracketed
optimum and **512 wins at every width's own best rate**, 3.170 against 3.189
and 3.220. Tuning narrows the 256 gap and does not flip it. See
`LEVEL_ONE_LEARNING_RATE.md`.

**Warmup-stable-decay is a capability, not an improvement.** It is adopted
because the stable phase can be extended and the decay applied later, so a run
lengthens without restarting. Choose it when a run needs extending, not to
lower a loss.

## Superseded 2026-09-28, kept for the figures

**The previous reference was measured on 444 books and 322,136 training tokens
at 3,200 steps and reached 3.156**, against defaults at 3.236, a gap of 0.080.
**Those numbers describe a smaller corpus and are not comparable to the ones
above**, which is why the baseline was re-run rather than reused.

| Setting | Value | Why |
| --- | --- | --- |
| positions | rotary | 0.292 nats over a learned table at this window |
| width | 512 | Beats 256 **only when regularised** |
| layers | 4 | Unswept |
| steps | 3,200 | About twenty epochs at that corpus size |
| token replacement | 0.05 | 0.15 is indistinguishable from it here |
| tying, derived heads | on, the defaults | |

### The grid it came from

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

## A truncation that affected every figure two tools produced

**`tools/diagnose_level.py` scored 24 of 48 held-out batches** and announced it
on every run. The same configuration measured **2.908 on 24 batches and 3.156
on 48**.

**Comparisons survive and absolute numbers do not.** Every cell of every sweep
was truncated identically, so a difference measured between cells is sound; the
reference-against-default gap moved only from 0.106 to 0.080. **But any figure
quoted as a loss from that period is about 0.25 nats optimistic**, and that
includes the scaling curve, the capacity table, the regularisation record and
the positions grid.

**Amended 2026-09-28: the defect was the default, and the third tool still had
it.** The fix of 2026-09-27 made two callers pass a large number and left
`TrainConfig.eval_batches` at 24, so `tools/sample_level.py` reported the
shipped checkpoint's loss over **24 of 52 batches, at 2.8771 against a true
3.0614**. The tool announced it and it was read past for the fourth time.
**The default is now every batch** and a caller that wants speed asks for
truncation. Fixing callers one at a time had left the trap armed for the next
one.

## What is not established

**Four layers is unswept.** Every figure here holds depth fixed.

**Muon's momentum and Newton-Schulz step count are unswept**, both at the
reference defaults. Its learning rate is swept and 0.02 is its optimum.

**Whether weight decay helps the matrices is open.** The sweep varied one value
that is coupled to each optimiser's own rate, so it applied about sixty-seven
times the shrinkage to the matrices as to everything else. The two are now
settable independently and a clean test has not been run.

**The implementation deviates from the published optimiser in one stated way**,
using the tensor's own dtype where the reference casts to bfloat16, because the
host is Metal rather than CUDA.

**This is held-out loss on the curriculum tail**, which is not a sample of
typical corpus text and is not the property `../elenchos/` measures.
