# Current brief. Find out whether the ablation measures ordering

**Written 2026-09-27**, replacing the brief that priced the endpoint
decision. That work is done and its brief is superseded rather than
deleted. Durable practice is in `PROCESS_STRATEGY.md`.

## Why this and nothing else

**The project's central experiment may be measuring the wrong thing, and
one run can tell.** `pilot._batches` takes consecutive positions from an
arm's ordering, so an arm decides both the sequence in which books are
visited and **what each batch contains**.

**Measured over 223 batches**: a curriculum ordering averages 1.20 distinct
subjects per batch against 1.88 for a shuffled one. **The homogeneity
ordering matches the loss ordering exactly**, curriculum most homogeneous
and worst, shuffled least homogeneous and best, at both endpoints.

**Batch homogeneity changes gradient noise for reasons that have nothing to
do with curricula.** So the arm difference is consistent with a curriculum
effect and equally consistent with an optimisation artefact.

**This is the third harness defect of its shape.** The chunker discarded
three quarters of the corpus. `linear_extension` covered thirteen books of
a hundred and forty-six. Both were found after results had been read off
them. `CLAUDE.md` forbids stating a curriculum benefit as established, and
the same discipline forbids stating a curriculum harm.

## What to do

1. **Separate the two mechanisms with a control that keeps one and
   discards the other.** Shuffling books inside blocks of 32 leaves every
   book within 10 percent of its curriculum position while moving batch
   homogeneity 87 percent of the way to the shuffled arm.
2. **Run it against the unshuffled baseline at equal seeds and endpoint**,
   and read which way the curriculum arm moves.
3. **Record the answer whichever way it falls**, and say what it does to
   every ordering result this harness has produced.

## Prior failures, and the specific wrong turns to avoid

**Do not conclude from three points.** Homogeneity and loss agreeing across
three arms is a rank correlation over three items. It motivated this
experiment; it does not settle it.

**Do not report an ordering verdict.** Items 7 and 10 are unchosen. What is
in scope is whether the arms differ *for the reason the experiment
assumes*, not which arm is better.

**Do not let the control change more than intended.** A block shuffle that
moves books far from their curriculum position is not a control, it is a
second shuffled arm. The 10 percent figure is the thing to keep checking.

**Do not assume the instrument is innocent.** The truncated evaluation was
ruled out by measurement last tick, not by argument, and that was right.

**Do not overwrite a tracked artifact.** `train_level.py` writes
`evals/pilot/level_1.json` by default and it is tracked. Pass `--out`.

**Do not read a count from arithmetic.** Read it from the gate.

**Check CI separately.**

## What is not this brief's to decide

Items 5, 7 and 10, the level-two lexicon, schedules for levels three to
seven, `sources/` and level seven, the fourteen sense questions, and the
Rust build output. **Announcing the repository is not this brief's either.**
