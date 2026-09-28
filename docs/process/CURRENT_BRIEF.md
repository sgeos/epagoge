# Current brief. Adopt what was decided, and re-measure what moved

**Written 2026-09-28**, replacing the question-book brief, whose completion
condition is met. Durable practice is in `PROCESS_STRATEGY.md`.

## Why this

**`TRAINING_TECHNIQUES.md` adopted four things on 2026-09-24 and none is
implemented.** `train_level.py` says so in a comment. An adoption that never
reaches the code is a decision the tree does not have, and this is the
operator's third priority.

**The frontier is stale by a corpus refresh.** `REFERENCE_CONFIGURATION.md`
measured 3.156 on 444 books and 322,136 training tokens. The corpus now holds
523 books and 395,715 tokens, twenty-three percent more. **The twenty-epoch
rule says the optimal step count scales with corpus size**, so 3,200 steps is
the right duration for a corpus that no longer exists, and every figure
measured at it describes a smaller one.

**So a technique cannot be credited against 3.156.** The baseline has to be
re-measured on the current corpus at the corpus-scaled duration before
anything is compared to it, or an improvement and a corpus refresh will be
indistinguishable.

## The premise problem, which comes first

**Maximal update parametrization's stated justification is gone.** The record
calls it "mandatory, and not for efficiency", because without it "the three
scale points in open question five have different optimal hyperparameters",
and "any observed scale-dependence in the ordering effect could then be an
artifact of mis-tuning rather than a property of scale."

**Item 5 was decided on 2026-09-27 as a single scale point**, with rescaling
as a fallback. **With one scale point there is no cross-scale confound to
remove.**

**This is the shape of the item 10 finding.** An adoption resting on a premise
a later decision removed, where nobody propagated the change. **Decide what
μP is still worth and say so**, rather than implementing against a reason that
has expired or dropping it without looking.

## What to do

1. **Re-measure the baseline on the current corpus** at the duration the
   twenty-epoch rule implies, with more than one seed, scoring every held-out
   batch.
2. **Implement warmup-stable-decay** and measure it against that baseline.
3. **Implement Muon** and measure it against that baseline.
4. **Measure them together**, because two improvements are not two
   improvements until they have been run together.
5. **Record what μP is still for**, with the superseded reason kept in place.

## Prior failures, and the specific wrong turns to avoid

**Do not credit an improvement against the old frontier.** 3.156 is a figure
about a smaller corpus. Anything compared to it measures the corpus refresh as
well as the change.

**Do not assume improvements add.** Weight decay and token replacement were
measured together once and did not stack, being two treatments for the same
slack. A combined result is measured, not summed.

**Do not sweep duration and corpus size independently.** The optimum is about
twenty epochs at every corpus size measured so far, so a step count held fixed
across corpus sizes measures the interaction rather than the corpus.

**Do not report a single seed as a frontier.** A best-of-many over one seed
each is a maximum of noise as much as a maximum of quality, and the
seed-to-seed spread here is around 0.007 to 0.018.

**Check what the evaluation tool scores.** `diagnose_level.py` scored 24 of 48
held-out batches for a day while announcing it on every run, and every
absolute figure from that period is about 0.25 nats optimistic. Read the line.

**Do not pipe a run through a filter and read the exit code.** It reports the
filter's status, and that has cost one wasted training run and hidden one lint
failure.

**Do not chain the gate to the commit.** Done in this session's history and it
pushed a failing tree to `origin`.

**Do not read a count from arithmetic**, and do not compare across anything
held fixed without checking it was actually held fixed. Five instances of the
second in one session, including a loss compared across held-out sets and an
architecture comparison confounded by bias asymmetry.

**Do not overwrite a tracked evaluation artifact with a probe.** The diagnosis
and sample tools take an output path.

**Do not implement an optimiser from memory.** Muon's update is an
orthogonalisation of the momentum matrix and the details matter. If the
implementation cannot be checked against a stated source, say so rather than
presenting it as the published method.

**Do not apply a matrix optimiser to vectors.** Muon is for two-dimensional
parameters. Embeddings, biases, norms and the output head are conventionally
left to the other optimiser, and a run that ignores that is not a test of
Muon.

## What is not this brief's to decide

The Dale-Chall and NGSL licensing question, the terminal-stage record
licensing question, schedules for levels three to seven, `sources/` and level
seven, and the acquisition scheme in `../decisions/SOURCE_ACQUISITION.md`,
which stays unadopted. **Announcing the repository is not this brief's
either.**
