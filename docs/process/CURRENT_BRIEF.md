# Current brief. Find out whether more corpus still buys anything

**Written 2026-09-27**, replacing the brief that bought pair coverage. Two
rounds of that are done and this asks whether a third is worth running.
Durable practice is in `PROCESS_STRATEGY.md`.

## Why this before more generation

**Two rounds of book writing rested on a claim last measured on an eighth
of this corpus.** `../../evals/pilot/LEVEL_ONE_SCALING.md` says how much
corpus is worth writing, and its largest point is 45,547 training tokens
against roughly 370,000 today. Everything since has assumed the curve
still slopes.

**If it has flattened, generation is the wrong work**, and the project
would be buying tokens rather than capability. `../decisions/
THREE_PROBLEMS.md` says volume is the binding constraint at level one, and
that claim is now old enough to re-check.

**The measurement is controlled and already tooled.** Training on fractions
of the corpus against one fixed held-out set isolates corpus size from
everything else, which is the experiment `COMBINATORIAL_RICHNESS.md`
records as still owed.

## What to do

1. **Measure held-out loss against training corpus size**, over a range
   wide enough to see curvature, with the held-out set identical at every
   point.
2. **Take the best across step counts at each size**, because the optimum
   number of steps moves with corpus size and a fixed step count would
   confound the two.
3. **Say what the slope implies for the next round**, in words a reader can
   act on: keep generating, stop generating, or generate something
   different.

## Prior failures, and the specific wrong turns to avoid

**Do not compare across held-out sets.** A loss that falls while the
held-out set changes has not been shown to fall, and this project has
already withdrawn one finding for exactly that.

**Do not read a fixed step count as the answer.** The old record took the
best across step counts for a stated reason and the reason still holds.

**Do not quote the old curve.** It predates the current corpus, vocabulary,
position scheme, head derivation and evaluation.

**Do not conclude that generation is worthless from a shallow slope.** Pair
coverage and concept coverage are not the same quantity as token count, and
this measures tokens. Say which one the curve is about.

**Do not read a count from arithmetic.** Twice this session I wrote a
number into a record that the gate would have given me correctly.

**Do not overwrite a tracked artifact**, and check CI separately.

## What is not this brief's to decide

Items 5, 7 and 10, the level-two lexicon, schedules for levels three to
seven, `sources/` and level seven, the fourteen sense questions, and the
Rust build output. **Announcing the repository is not this brief's either.**
