# Muon is worth more than everything else found so far, and the schedule spoils it

**Measured 2026-09-28** on 523 books and **344,348 training tokens**, three
seeds a cell, **scoring every held-out batch**, at **3,400 steps**.

**The duration is the corpus-scaled one.** The twenty-epoch rule put 3,200
steps at 322,136 tokens, and this corpus has 344,348, so 3,400 steps is
about 20.2 epochs. **Comparing against the recorded 3.156 would have measured
the corpus refresh as well as the change**, so the baseline was re-run.

## The four cells

| Arm | Held out, 3 seeds | sd | Train | Gap | Against baseline |
| --- | --- | --- | --- | --- | --- |
| Baseline, cosine and AdamW | 3.183 | 0.0125 | 2.25 | 0.92 | |
| Warmup-stable-decay | 3.206 | 0.0081 | 2.14 | 1.06 | **+0.024, worse** |
| **Muon** | **3.066** | **0.0032** | 1.95 | 1.12 | **−0.117** |
| Muon and warmup-stable-decay | 3.146 | 0.0095 | 2.48 | 0.67 | −0.037 |

**Muon is worth 0.117 nats, which is more than the entire reference
configuration was.** That configuration bought 0.080 over the defaults, and a
corpus doubling buys about 0.26 and costs roughly fifteen generation rounds.
**This costs one flag.**

**It also has the tightest seed spread of the four**, at 0.0032 against the
baseline's 0.0125, so the effect is not a lucky seed.

## They do not add. They interact, and the sign flips

**Additively the combination should reach about 3.090.** Muon takes 0.117 off
and the schedule adds 0.024 back. **It reaches 3.146**, which is 0.056 worse
than additive and **0.080 worse than Muon alone.**

**The train loss says what happened, and it moves the wrong way.** Each
intervention alone *lowers* training loss against the baseline's 2.25, to 2.14
and 1.95. Together it *rises* to 2.48, and the gap collapses from 1.12 to
0.67. **The combination underfits**, where each part alone fit harder.

**The reading is that both enlarge the effective step and together they
overshoot.** Warmup-stable-decay holds the peak rate for ninety percent of the
run instead of decaying through it, and Muon's orthogonalised update has a
larger natural scale than AdamW's. That is an explanation offered after the
fact and **it is not measured**; what is measured is that the two do not add
and that the combination fits less well rather than more.

**This is the third time two improvements have failed to stack here.** Weight
decay and token replacement did not, being two treatments for the same slack.
The project's rule that a combined result must be measured rather than summed
is now carrying three instances.

## What warmup-stable-decay being worse does and does not mean

**It does not refute the adoption.** `../../docs/decisions/TRAINING_TECHNIQUES.md`
adopts it because the stable phase can be extended and the decay applied
later, so a run lengthens without restarting, which a cosine schedule cannot
do because its every rate depends on the total step count. **That property is
asserted by a test and is unaffected by this measurement.**

**What it refutes is a claim nobody made**, that the shape reaches a better
loss at a fixed duration. **At a fixed duration it reaches a slightly worse
one, reliably**: the baseline's worst seed is 3.195 and the schedule's best is
3.197, so the ranges do not overlap.

**So the schedule is a capability rather than an improvement**, and it should
be chosen when a run needs extending rather than to lower a loss.

## The caveat on Muon's figure, which is the same one as the width ranking

**This is default against default, not tuned against tuned.** Muon runs at the
reference default of 0.02 and AdamW at this project's default of 3e-4. **The
two rates are not comparable quantities**, neither was tuned, and **no tool in
this repository exposes the AdamW learning rate**, so the baseline could not
have been tuned even had that been wanted.

**Part of Muon's gain may be that its default suits this setup better.** That
is not a reason to discount the result, which is large and consistent across
seeds, but it is a reason not to call it a comparison of optimisers. **It is a
comparison of two configurations, one of which nobody could adjust.**

**This is the confound recorded the same day against the width ranking** in
`../../docs/decisions/TRAINING_TECHNIQUES.md`. The learning rate becoming
reachable is what would settle both.

## What is not established

**Weight decay under Muon is unmeasured at the time of writing.** The recorded
rule is that weight decay helps where the train-to-held-out gap exceeds about
one nat, which is why the reference configuration leaves it at the default
with a gap of 0.76. **Muon's gap is 1.12 and the schedule's is 1.06, both
above that line**, so the rule predicts it should now help. That prediction
was made from a rule written before these runs and is being tested.

**Muon's own hyperparameters are unswept.** Its rate, its momentum and the
Newton-Schulz step count are all the reference defaults.

**Depth is unswept**, as everywhere else here. Four layers throughout.

**This is held-out loss on the curriculum tail**, which is not a sample of
typical corpus text and is not the property `../elenchos/` measures.

**The implementation is transcribed and deviates in one stated way.** It runs
in the tensor's own dtype where the reference casts to bfloat16, because the
host is Metal rather than CUDA. It is therefore not numerically identical to
the published optimiser.
