# Current brief. Find out what the surviving forty percent is

**Written 2026-09-27**, replacing the brief that asked whether the ablation
measures ordering. It answered: about sixty percent of the arm difference
was batch homogeneity. **This brief is about the rest.** Durable practice is
in `PROCESS_STRATEGY.md`.

## Why this and nothing else

**A residual of about 0.045 nats survived the control**, which is several
times the within-arm spread, so it is not noise. It is either a real
ordering effect, which would be the first evidence this project has for its
own thesis, or it is homogeneity at a grain the control does not reach.

**Those two possibilities call for opposite work** and the project cannot
tell them apart from what has been run. **Distinguishing them is worth more
than anything else available**, because one of them says the experiment has
started working and the other says it still has not.

## The test

**Block size traces a curve with the sequence held fixed.** Running the
curriculum arm at block sizes from 1 to 64 varies batch homogeneity while
keeping every book near its curriculum position, so loss against homogeneity
along that curve is the effect of homogeneity alone.

**The shuffled arm is the test point.** It differs from the curriculum arm
in both homogeneity and sequence. If its loss falls on the curve extrapolated
to its homogeneity, then sequence contributes nothing and the residual is
homogeneity the control did not reach. If it falls below the curve, the gap
is the ordering effect.

## Prior failures, and the specific wrong turns to avoid

**Measure homogeneity from the real chunking.** The first measurement of it
used a proxy for how many chunks a book makes, and the proxy was wrong. The
proportions survived and the absolute numbers did not, and three committed
records carry the wrong ones. **Correct them rather than quietly replace
them.**

**Do not fit a line to a curve.** Loss against homogeneity has no reason to
be linear, and an extrapolation past the measured range is the weakest part
of this design. If the shuffled arm sits outside the range the curriculum
arm covers, say so rather than extrapolating confidently.

**Do not conclude a curriculum effect exists.** A residual consistent with
an ordering effect is not a demonstration of one. `CLAUDE.md` forbids
stating a curriculum benefit as established, and this design cannot
establish it: the endpoint and the minimum effect are unchosen.

**Do not let the control drift into a second shuffled arm.** Block 64 moves
books out of place. Report how far each block size displaces books alongside
its homogeneity.

**Do not overwrite a tracked artifact**, do not read a count from
arithmetic, and check CI separately.

## What is not this brief's to decide

Items 5, 7 and 10, the level-two lexicon, schedules for levels three to
seven, `sources/` and level seven, the fourteen sense questions, and the
Rust build output. **Announcing the repository is not this brief's either.**
