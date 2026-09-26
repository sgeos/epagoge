# Current brief. The loop has run out of work that is its own

**Written 2026-09-26**, replacing the brief whose completion condition is
met. **This one recommends stopping rather than continuing**, and says what
each remaining item is waiting on. Durable practice is in
`PROCESS_STRATEGY.md`. The reasoning behind the measurements is in
`../../evals/pilot/`.

## What level one now is

| Property | State |
| --- | --- |
| Lexicon | 845 words at level one, closure 100 percent, seed of 37 |
| Books | 246 over 4,691 records, **172,810 words** |
| Length standard | **244 of 244 content books inside the word band** |
| Metadata | All six fields on all 246 books |
| Best model | Held out **3.713**, perplexity **41**, width 1024 |
| Gate | 21 checks, exits 0, about nine seconds |

The corpus began the previous morning at 55,510 words with 229 of 244
content books below the band and a model at perplexity 120.

## Why there is nothing left for a loop to take

Each remaining item fails one of the two tests in `PROCESS_STRATEGY.md`:
either it needs information only the operator holds, or the project's own
framing says it is not the work to do next.

**The 688 unused surface forms.** Each is a judgement about whether a
module should use it, whether a module should be drafted for it, or whether
admitting it was a mistake. A loop cannot make that call for 688 words and
should not pretend to.

**The ordering ablation.** Blocked on the endpoint and estimator of
pre-registration item 10. **The endpoint fixes the sign of the result**: at
800 steps the curriculum arm was worse in 8 of 8 and at 1,600 better in 7
of 8. Nobody should choose that after seeing the data, which is why it is
the operator's and why it is pre-registration.

**The level-two lexicon, 879 words against a target near 10,000.** An
allocation over a partial order, not a backlog. Admitting words a round at
a time from whatever blocked a generator will not produce ten thousand.

**Schedules for levels three to seven.** None exist.

**`sources/` and level seven.** Empty, and its licensing constraint is
recorded as unexamined.

## The wrong turn that is available and should not be taken

**Writing the level-two corpus now.** It looks like bounded roadmap work:
27 units are scheduled across 11 domains, one book exists at 3 of its 64
spreads, and the tooling would run unattended for about twenty hours.

**The project's own framing forbids it.** `../decisions/THREE_PROBLEMS.md`
says volume is a level-one concern, that at levels two to six coverage and
consistency bind instead, and that **a large corpus with unscheduled
concepts would not be progress**. Writing 432,000 words against an
879-word lexicon would produce level-one prose at level-two length, and
the lexicon allocation would then invalidate it.

So the cheapest-looking work available is the work the project has already
decided against, and a loop optimising for visible output would take it.

## What this session did, for a resuming reader

Eleven hours, and the most useful output was catching its own errors.

**Delivered.** Book metadata on all 246 books, where there had been none.
The word band closed. Three field-enumeration defects fixed, one of which
would have erased metadata from every regenerated book. Two holes closed in
the disclosure scan, one of which had let banned vocabulary reach a public
push. The scaling experiment made reproducible, its tool having never been
committed. The teacher's context declared rather than inherited, which was
a fiftyfold latency regression. A reference check added to the gate.

**Withdrawn, with the reasoning kept in place.** That the model was too big
for the corpus. That filling books added low-value tokens. That a question
mark triggered the token `was`. That distinct-token share measures quality.

**The class they share** is one rule: before reporting a difference, say
what was held fixed and check that it was. Four instances in one day, all
found by doubting a result rather than by any new measurement.
