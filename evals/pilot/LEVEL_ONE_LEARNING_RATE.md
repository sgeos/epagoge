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

## The width ranking survives per-width tuning

**Every width was given its own sweep and every optimum is bracketed on both
sides.** These are AdamW, one seed, otherwise the reference configuration.

| Width | Params | Rates swept | Optimum | Held out there |
| --- | --- | --- | --- | --- |
| 256 | 3.7M | 3e-4, **6e-4**, 1e-3 | 6e-4 | 3.189 |
| **512** | 13.8M | 1e-4, **3e-4**, 6e-4 | 3e-4 | **3.170** |
| 1,024 | 52.7M | 5e-5, 7e-5, **1e-4**, 1.5e-4, 3e-4 | 1e-4 | 3.220 |

**Width 512 wins at every width's own best rate**, so the ranking the project
published and then marked provisional is sound. **Tuning narrows the
256-against-512 gap from 0.027 to 0.019 and does not flip it**, and width
1,024 is worse by 0.050 even at its optimum.

**The widest model's minimum was at the edge of the first grid it was given**,
at 1e-4 with 1.5e-4 worse, and two further points were run below it before
anything was recorded. **An optimum at the edge of a grid is a boundary, not an
optimum**, and declaring the ranking sound on one would have repeated the
original defect with extra steps.

## The scaling law is confirmed over one doubling and overshot over the next

**Maximal update parametrization says the optimal rate scales as one over the
width.** Measured here:

| Step | Predicted ratio | Measured ratio |
| --- | --- | --- |
| 256 to 512 | 2 | **2**, exactly, 6e-4 to 3e-4 |
| 512 to 1,024 | 2 | **3**, 3e-4 to 1e-4 |

**So the relationship is right in direction and not exact on this tree.** The
optimum falls faster than one over the width at the top end. **This is a
three-point curve at one seed and is not offered as a scaling law**; what it
supports is that the rate must move with width, which is the claim that made
the fixed-rate sweep unsound.

**That is a better reason to keep μP adopted than the one recorded on
2026-09-28**, which reasoned about what a confound could do rather than
showing the relationship holds here.

## What this does not settle

**The optimum may move with anything else held fixed here**: duration,
schedule, token replacement, depth and corpus size are all fixed at one value,
and a rate optimal at 3,400 steps need not be optimal at another duration.

**Nothing here is a three-seed result.** The curves locate an optimum. The
figures at the optimum come from `REFERENCE_CONFIGURATION.md`, which is
three seeds.
