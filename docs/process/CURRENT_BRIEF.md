# Current brief. Pay the measurement debt, and stop adding surface

**Written 2026-09-27**, replacing the brief that recommended stopping. That
one was right at the time and the situation changed: three sessions of
capability landed on top of it, and the corpus, the vocabulary, the
architecture and the training machinery all moved.

**The work now is arithmetic, not invention.** Durable practice is in
`PROCESS_STRATEGY.md`. The reasoning behind each measurement is in
`../../evals/pilot/`.

## Why this and not something else

**Every recorded number describes a tree that no longer exists.** The
corpus went from 246 books to 400, the vocabulary from 2,246 tokens to
2,279, the head count from fixed to derived, the evaluation from a biased
slice averaged wrongly to a token-weighted sum, and every work now carries a
beginning, an end and a title announcement. **None of the figures in
`evals/pilot/` were taken under any of that.**

**No checkpoint on disk loads.** `evals/pilot/level_1.pt` holds a vocabulary
of 2,246 against 2,279 today. It is refused cleanly, which is the machinery
working, and it means `tools/talk.py`, `tools/retention.py` and
`tools/plan_pairs.py` cannot run at all. **The project currently cannot be
talked to.**

**The handoff lists three measurements as owed and says none is optional.**
They have been owed since before this session and this session did not pay
them. Adding a fourth capability instead would be the same choice a fourth
time.

## What to do

1. **Produce a checkpoint that loads.** Train at the current vocabulary and
   architecture and save it where the tools look.
2. **Re-run the position comparison.** 128 against a whole-book window, at
   both schemes, now that both share one `Block` and heads are derived. The
   claim that rotary is worth 0.4 nats is confounded and must not be quoted
   until this is redone.
3. **Re-run the capacity sweep** with derived heads, so the wide points mean
   something. Width 1,024 previously ran at head dimension 256.
4. **Re-run retention**, which is what `COMBINATORIAL_RICHNESS.md` commits
   to: whether the eleven worst-retained epistemic concepts moved after 153
   cross-concept books. If retention does not respond, the combinatorial
   argument is right about the corpus and wrong about the model.
5. **Make every stale eval record say so**, in the record itself, so a
   reader cannot quote a confounded figure by accident.
6. **Re-stamp the handoff** so its validity block matches the tree.

## Prior failures, and the specific wrong turns to avoid

**Do not add a feature.** The temptation this brief exists to resist is that
the next capability is more interesting than the next measurement. Five
landed in one session. The debt is measurement.

**Do not quote a figure taken before the change it spans.** Retention
numbers from 216 books and retention numbers from 400 books are not
comparable, because the book set is the denominator. Say what moved and say
that the set moved with it.

**Do not report one seed as a result.** It was done twice this session and
flagged both times. A paired difference over three seeds is the minimum that
earns the word "result", and even that is weak.

**Do not overwrite a tracked eval artifact with a probe.** It happened twice
this session. `tools/diagnose_level.py` and the sample tools take `--out`.

**Do not claim a count from arithmetic.** A commit message claimed 533 tests
where the tree had 526. Read it from the gate.

**Do not conflate "the corpus grew" with "the model improved."** A loss that
falls while the held-out set changes has not been shown to fall.

**Do not weaken a check to make something pass**, and do not delete a
correction. Corrections stay beside the claim.

**Check CI separately.** Red while the local gate was green three times.

## What is not this brief's to decide

The seven operator-held items in `HANDOFF.md`, unchanged: the endpoint and
estimator, whether the third ablation arm suffices, the level-two lexicon,
schedules for levels three to seven, `sources/` and level seven, the
fourteen sense questions, and the 219 GB of Rust build output.

**Announcing the repository is not this brief's either.** It is public and
discovery is not.
