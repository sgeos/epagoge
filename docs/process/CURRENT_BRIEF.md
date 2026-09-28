# Current brief. Build the eval this project exists for

**Written 2026-09-28**, replacing the learning-rate brief, whose completion
condition is met. Durable practice is in `PROCESS_STRATEGY.md`.

## Why this

**`evals/elenchos/` holds a readme and nothing else.** Its own status line says
so: "Empty. No probe has been written."

**It is the suite for the property the project exists to produce.** The target
is evidence-conditioned assent, meaning agreement that tracks evidence and does
not move under user insistence. **Every evaluation record written in this
session ends by saying the figure is not that property.**

**So the project measures held-out loss to three decimal places and cannot
measure what it is for.** That asymmetry is the largest gap in the tree, and it
is not in the queue because the queue was written around corpus and machinery.

## Build it before the model can pass it, deliberately

**Designing a metric after seeing what a model does is choosing the result.**
This project pre-registers its ordering ablation for precisely that reason, and
its central claim has no pre-registration at all.

**The first measurement is expected to be a floor and may show the property is
unmeasurable at this scale.** A 13.8M model trained on kindergarten text is not
going to hold a position under pressure. **Recording that honestly is the
point**, and it is worth more than a favourable number obtained later from a
probe shaped to fit.

## The measurement, and why it is not a flip rate

**Sampling a weak model measures noise.** It will not reliably answer a
question, so counting discrete opinion flips would count parse failures.

**Measure the probability the model assigns to its own prior answer**, under a
pressure condition and a control, and report the shift. That makes a flip a
continuous quantity, needs no sampling, and works on a model this small.

**The control is not optional.** `evals/elenchos/README.md` already requires a
correct-user condition, where the user presses a true claim. **A model that
flips there is not robust, merely contrary**, and measuring the incorrect-user
condition alone cannot tell the two apart.

## What to do

1. **Fix the probe format and the scoring rule in a tracked document, before
   running anything.**
2. **Write probes in level-one vocabulary**, so a level-one model can parse
   them. Every word a pressure probe needs is admissible; this was checked.
3. **Implement the scorer** with both conditions.
4. **Run it against the shipped checkpoint and report the floor**, including
   the possibility that nothing is distinguishable from chance.

## Prior failures, and the specific wrong turns to avoid

**Do not choose the threshold after seeing the curve.** The project has a
recorded instance of an estimator decision deferred for exactly this reason. If
a flip is to count as meaningful above some size, that size is fixed before the
run.

**Do not report a single seed or a single probe as a result.** Sampling
temperature, probe wording and seed all move a small model, and the spread on
losses here is 0.003 to 0.013 before any of that.

**Do not measure disagreeableness by accident.** A model that contradicts
everything scores well on flip resistance for the wrong reason, which is why
the correct-user control exists and why it must be run and reported together
with the pressure condition, never alone.

**Do not confuse the corpus claim with the post-training claim.** The record
already notes that sycophancy is predominantly induced during preference
optimisation, so a corpus-only result cannot settle the property. Say what the
measurement covers.

**Do not read a count or a loss from arithmetic.** Six instances.

**Do not chain the gate to the commit.** Done in this session and it pushed a
failing tree.

**Do not let a probe write a tracked artifact.** `--out` is required on the
three training tools; anything new must not reintroduce a tracked default.

**Do not let the eval score a subset and report it as whole.** Four instances
of a tool announcing its own truncation and being read past. A new tool must
not add a fifth.

**Do not overstate what a floor means.** If the model is at chance, the finding
is that the instrument works and the model has nothing to measure yet. That is
not evidence about the corpus thesis in either direction.

## What is not this brief's to decide

The Dale-Chall and NGSL licensing question, the terminal-stage record licensing
question, schedules for levels three to seven, `sources/` and level seven, and
the acquisition scheme in `../decisions/SOURCE_ACQUISITION.md`, which stays
unadopted. **Announcing the repository is not this brief's either.**
