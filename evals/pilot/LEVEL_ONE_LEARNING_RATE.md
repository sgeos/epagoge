# Both defaults were already at their optimum, and nobody had checked

**Measured 2026-09-28** on 523 books and **344,348 training tokens**, at
**3,400 steps**, scoring every held-out batch, **one seed a point**.

**One seed is enough to locate an optimum here and not to rank neighbours.**
The differences between adjacent points run 0.03 to 0.60 against a seed spread
of 0.0125, so the shape of the curve is not noise. **A claim about two points
0.01 apart would need more seeds and none is made.**

## Why this was measured at all

**No tool in this repository exposed the learning rate until this work.**
Every run the project had ever done used the trainer's default of 3e-4,
inherited from torch, across widths 16 to 1,024 and against Muon at its own
reference default of 0.02.

**That made two published conclusions provisional.** Muon's 0.117 nats was a
comparison of configurations rather than of optimisers, and the width ranking
was swept against a rate that maximal update parametrization says should move
with width. **Neither could be settled by argument.**

## AdamW

| Rate | Held out | Train | Gap |
| --- | --- | --- | --- |
| 1e-4 | 3.204 | 2.44 | 0.77 |
| **3e-4, the inherited default** | **3.170** | 2.25 | 0.92 |
| 6e-4 | 3.298 | 2.65 | 0.65 |
| 1e-3 | 3.433 | 2.99 | 0.44 |
| 2e-3 | 3.811 | 3.54 | 0.27 |

**Bracketed on both sides, and the default wins.**

## Muon

| Rate | Held out | Train | Gap |
| --- | --- | --- | --- |
| 0.005 | 3.531 | 0.65 | 2.88 |
| 0.01 | 3.267 | 0.87 | 2.40 |
| **0.02, the reference default** | **3.067** | 1.95 | 1.12 |
| 0.04 | 3.380 | 2.86 | 0.52 |
| 0.08 | 3.869 | 3.62 | 0.25 |

**Bracketed on both sides, and the default wins.**

**Muon's low-rate behaviour is worth recording because it is backwards.** At
0.005 the training loss collapses to 0.65 with a gap of 2.88. **A smaller step
on an orthogonalised update memorises harder**, where a smaller step on AdamW
simply underfits, at 2.44 training loss for 1e-4. The two optimisers fail in
opposite directions and the held-out curve hides that; only the training loss
shows it.

## What this settles

**The caveat on Muon's 0.117 nats is removed, and its resolution is the
opposite of what it implied.** Both optimisers were already at their measured
optimum, so the comparison published on 2026-09-28 was tuned against tuned by
accident rather than default against default. **The figure stands unchanged.**

**It was still right to state the caveat.** Nothing in the tree could have told
a reader that 3e-4 was a good choice rather than an inherited one, and the only
way to find out was to sweep. **A caveat resolved by measurement is worth more
than a caveat that was never raised**, and this one could have gone the other
way.

## What this does not settle

**The width ranking is a separate sweep** and is not answered by the points
above. Every one of them holds width at 512, and the question is whether width
1,024's published disadvantage survives being given its own rate.

**The optimum may move with anything else held fixed here**: duration,
schedule, token replacement, depth and corpus size are all fixed at one value,
and a rate optimal at 3,400 steps need not be optimal at another duration.

**Nothing here is a three-seed result.** The curves locate an optimum. The
figures at the optimum come from `REFERENCE_CONFIGURATION.md`, which is
three seeds.
