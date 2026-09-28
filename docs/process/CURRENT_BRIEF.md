# Current brief. Make the learning rate reachable, then re-decide two claims

**Written 2026-09-28**, replacing the brief that adopted Muon, whose
completion condition is met. Durable practice is in `PROCESS_STRATEGY.md`.

## Why this

**No tool in this repository exposes the learning rate.** Every run it has
ever done used the trainer's default of 3e-4, so that value was inherited and
never chosen. **A parameter no tool can reach has never been held fixed
deliberately, only by default, and a default is not a control.**

**Two published conclusions depend on it and both are currently provisional.**

**Muon's 0.117 nats is a comparison of configurations, not of optimisers.**
Muon runs at its reference default of 0.02 and AdamW at 3e-4. Those are not
comparable quantities and neither was tuned. If AdamW at a better rate closes
most of the gap, the headline shrinks and the record has to say so.

**The width ranking is worse than provisional.** Widths 16 to 1,024 were swept
against one fixed rate, and maximal update parametrization's central claim is
that the optimal rate scales with width. `LEVEL_ONE_CAPACITY.md` published that
width 1,024 is worse and a later re-measurement withdrew the ranking. **Whether
1,024 is genuinely worse or is mis-tuned at a rate chosen for a quarter its
width is not separable from the runs that exist.**

**This brief does not add a finding. It decides whether two existing ones are
real.** That is worth more than a third finding on the same foundation.

## What to do

1. **Expose the learning rate** on the tools that train.
2. **Sweep AdamW's rate** at the reference configuration and find its best.
3. **Sweep Muon's rate** the same way.
4. **Restate the optimiser comparison at each one's best**, over more than one
   seed, and say plainly whether the 0.117 survives.
5. **Measure whether the width ranking survives per-width tuning**, or record
   why it could not be settled and leave it provisional with the reason.

## Prior failures, and the specific wrong turns to avoid

**Do not sweep at a short duration to afford more points.** An intermediate
reading of a decelerating scaling curve was wrong, and the cause was sweeping
only 1,600 and 3,200 steps; adding 400 and 800 removed it. The duration here is
3,400 steps, about 20.2 epochs, and a cheaper run measures a different thing.

**Do not compare a tuned arm against an untuned one and call it a comparison of
methods.** That is the mistake this brief exists to correct, and the correction
is worthless if it introduces the same shape in the other direction.

**Do not report a single seed as a result.** The seed spread here runs 0.003 to
0.013 depending on the arm, and a best-of-many over one seed each is a maximum
of noise as much as of quality.

**Do not assume the best rate transfers across anything.** Width, optimiser,
duration and schedule may each move it. Whatever is held fixed must be stated
and checked.

**Do not read a count or a loss from arithmetic.** Six instances. If a tool
supplies the number, the number comes from the tool.

**Do not chain the gate to the commit.** Done in this session and it pushed a
failing tree to `origin`.

**Do not let a probe write a tracked artifact.** `--out` is required on the
three measurement tools now, so this should be structurally impossible; if a
new tool is added it must not reintroduce a tracked default.

**Check what the evaluation scored.** Four instances of a tool announcing its
own truncation and being read past. The default now scores every held-out
batch, and a figure quoted without that being true is about 0.25 nats
optimistic.

**Do not widen the claim to fit the effort.** If tuning AdamW closes the gap,
the finding is that the gap was tuning, and that is a real and publishable
result rather than a failure of this brief.

## What is not this brief's to decide

The Dale-Chall and NGSL licensing question, the terminal-stage record
licensing question, schedules for levels three to seven, `sources/` and level
seven, and the acquisition scheme in `../decisions/SOURCE_ACQUISITION.md`,
which stays unadopted. **Announcing the repository is not this brief's
either.**
