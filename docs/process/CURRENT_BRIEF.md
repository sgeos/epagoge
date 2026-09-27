# Current brief. Price the decisions the operator holds

**Written 2026-09-27**, replacing the brief that said to pay the measurement
debt. That debt is paid and its brief is superseded rather than deleted.

**This brief is about a narrower thing: making an operator decision
cheaper to take, without taking it.** Durable practice is in
`PROCESS_STRATEGY.md`.

## Why this and not something else

**Everything left at level one is blocked on a person, and one of those
blocks can be made easier from here.** `evals/PRE_REGISTRATION.md` item 6
fixes the seed count for the ablation. It says the number cannot be fixed
because the paired standard deviation moved by a factor of five between 800
and 1,600 steps, and because item 10, the endpoint, is unchosen.

**Item 10 is the operator's and must stay so.** The handoff records why it
is load-bearing: at 800 steps the curriculum arm was worse in eight seeds of
eight, and at 1,600 it was better in seven of eight. **The endpoint picks
the sign of the headline result**, so an agent choosing it would be choosing
the answer.

**But nothing stops the cost of each choice being measured.** How many
paired seeds a 1 percent effect needs at 800 steps, and how many at 1,600,
is arithmetic once sigma and rho are known at each. That converts item 10
from a decision with unknown consequences into a decision with a price list.

**The numbers it currently rests on describe an eighth of this corpus.**
Item 6's figures were taken over 44,505 tokens. The corpus is 308,931 now,
the architecture has rotary positions, tied embeddings and derived heads,
and the evaluation is a token-weighted sum rather than a mean of per-batch
means over a systematic slice.

## What to do

1. **Measure variance, paired standard deviation and correlation on the
   current corpus, at more than one endpoint**, with enough seeds that the
   estimate means something.
2. **Report required seeds per endpoint per target effect**, so the cost of
   each endpoint choice is visible side by side.
3. **Update item 6 and `evals/pilot/LEVEL_ONE_VARIANCE.md`** with current
   figures, and say plainly what remains provisional and why.
4. **Say whether the pairing design still pays**, which is the one claim in
   item 6 that could fail on a real corpus at this size.

## Prior failures, and the specific wrong turns to avoid

**Do not report an ordering verdict.** The arms are measured here only to
get a paired difference for variance estimation. **Whether curriculum beats
topological is exactly what item 10 controls the sign of**, and reporting it
from a chosen endpoint would be choosing the endpoint. Report spread,
correlation and seed counts; do not report which arm won.

**Do not present item 6 as closed.** Two reasons outlive this work. The
endpoint is unchosen, and `TRAINING_TECHNIQUES.md` adopts an optimiser and
schedule that are not implemented, so sigma and rho will move again when
they are.

**Do not quote the old pairing gain as if it still held.** 22.8x was
measured over 146 books and 44,505 tokens.

**Do not use fewer seeds than the estimator needs**, and report how many
observations each estimate rests on.

**Do not overwrite a tracked artifact.** `tools/train_level.py` writes
`evals/pilot/level_1.json` by default and that file is tracked. Pass
`--out`.

**Do not read a count from arithmetic.** Read it from the tool.

**Check CI separately.** Red while the local gate was green three times.

## What is not this brief's to decide

Items 5, 7 and 10 of the pre-registration, the level-two lexicon, schedules
for levels three to seven, `sources/` and level seven, the fourteen sense
questions, and the Rust build output. **Announcing the repository is not
this brief's either.**
