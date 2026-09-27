# Current brief. Find the frontier and ship it

**Written 2026-09-27**, replacing the brief that measured corpus scaling.
Durable practice is in `PROCESS_STRATEGY.md`.

## Why this

**Six improvements have been measured and never combined.** Rotary
positions, weight tying, derived head counts, token replacement, weight
decay and the twenty-epoch rule were each measured against a baseline
holding everything else fixed. **No run has used more than one of the
optional ones at a time.**

**So the project does not know its own best result.** The figure it quotes,
3.014, comes from a configuration with token replacement off and weight
decay at the value torch supplies. The checkpoint anyone talks to was
trained the same way.

**That number is the baseline every future claim is measured against.** A
corpus round, an architecture change or an ablation is judged by how far it
moves the frontier, and the frontier is currently unmeasured.

## What to do

1. **Sweep the options that are off by default against the two widths that
   matter**, at step counts around the measured optimum.
2. **Name the best configuration found** and record it where a reader
   looking for "what should I train with" will meet it.
3. **Train the shipped checkpoint at that configuration**, so the model
   people prompt is the best one the project can make rather than the
   default one.
4. **Say what the frontier is**, as one number with its configuration
   attached, so the next claim has something to beat.

## Prior failures, and the specific wrong turns to avoid

**Do not assume improvements add.** Weight decay and token replacement were
measured together once and did not stack, being two treatments for the same
slack. A combined result has to be measured, not summed.

**Do not sweep corpus size and step count independently.** The optimum is
about twenty epochs at every corpus size, so a fixed step count across
sizes measures the interaction. The same may hold across widths and is not
yet checked.

**Do not report a single seed as a frontier.** A best-of-many over one seed
each is a maximum of noise as much as a maximum of quality, and the spread
between seeds here is about 0.007.

**Do not overwrite a tracked evaluation artifact with a probe.** The
diagnosis and sample tools take an output path.

**Do not read a count from arithmetic.** Three times this session a number
went into a record that the gate would have supplied correctly.

**Do not pipe a run through a filter and read the exit code.** It reports
the filter's status, and that has already cost one wasted run and hidden
one lint failure.

## What is not this brief's to decide

Items 5, 7 and 10, the level-two lexicon, schedules for levels three to
seven, `sources/` and level seven, the fourteen sense questions, and the
Rust build output. **Announcing the repository is not this brief's either.**
