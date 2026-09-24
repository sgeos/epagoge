# Variance pilot

Run 2026-09-24. Results in this directory.

    .venv/bin/python tools/run_pilot.py --pairs 8 --steps 2000 --tokens 4700000

## What it measured

| | Multi-epoch | **Single-epoch** |
| --- | --- | --- |
| Train chunks | 1,405 | 33,046 |
| Epochs over 2,000 steps | ~23 | ~0.97 |
| Seed sd, unpaired sigma | 0.1051 | **0.0750** |
| Paired sd | 0.0188 | **0.0233** |
| Correlation rho | 0.9874 | **0.9539** |
| Pairing gain | 62.5x | **20.7x** |

**The single-epoch column is the one to use.** The multi-epoch run was the
first attempt and is retained because the difference between the two is the
finding.

## The first run was wrong, and the way it was wrong is instructive

The initial pilot trained roughly twenty-three epochs. Real pretraining is
single-epoch or close to it. **Ordering effects necessarily wash out when a
model sees all its data twenty-three times**, which inflated the paired
correlation from 0.954 to 0.987 and the apparent pairing gain from 21 to 62.

Reporting the first number would have understated the required seed count
by a factor of three.

## Seeds required, single-epoch

Effects are relative to the mean held-out loss of 1.895.

| Target effect | Paired | Unpaired | **Plan with** |
| --- | --- | --- | --- |
| 2.0% | 3 | 62 | 5 |
| 1.0% | 12 | 246 | 19 |
| 0.5% | 48 | 984 | 73 |
| 0.2% | 297 | 6,147 | 456 |

"Plan with" is the 90th bootstrap percentile, which carries the pilot's own
uncertainty about sigma. A point estimate from eight pairs understates sigma
about half the time, and planning from it underpowers the study about half
the time.

**The pairing decision is emphatically vindicated.** Twelve paired seeds
beat two hundred and forty-six unpaired ones. The original design of five
unpaired seeds was not merely underpowered, it was off by two orders of
magnitude in cost-efficiency.

## An unexplained systematic difference, and the control it requires

Across eight pairs, seven differences were positive, mean +0.0164. Both
orderings are random shuffles, so under the null the mean should be zero.

A diagnostic ran the two orderings in swapped execution order. The sign
followed the **ordering identity, not the execution position**. Across nine
observations, eight were positive, which a sign test puts near p = 0.04.

**Marginal, unexplained, and not affecting this pilot's deliverable**, since
sigma and rho are computed from the spread of differences and a constant
offset does not change a standard deviation.

**But it is exactly the shape of a false positive.** A systematic
difference between two orderings that should be equivalent, appearing in a
setup where no effect exists, is what the ablation would misattribute to the
curriculum.

**Required control, recorded as a design change.** The ablation carries a
**null arm**, comparing two random topological orderings against each other.
It should show no effect. Whatever it does show is the pipeline's baseline
spurious difference, and the curriculum effect must exceed it rather than
merely exceeding zero.

## Nondeterminism floor

Identical inputs run twice differed by 0.00075. Metal Performance Shaders
reductions are not deterministic, so paired runs are not perfectly paired.
That floor is small against the paired standard deviation of 0.0233 but it
is not zero, and it sets a limit on how small an effect this hardware can
resolve regardless of seed count.

## What does not transfer

Stated plainly, because these numbers will be quoted.

- **818,000 parameters**, not 100 million to 1 billion.
- **A synthetic second-order Markov stream**, not natural language and not
  the curriculum corpus.
- **Partial convergence.** Held-out loss 1.895 against a source entropy of
  1.099.
- **Metal Performance Shaders**, not the accelerator the ablation will use.

The correlation is the number most likely to move. It should be re-measured
at target scale on the real corpus before the seed count is fixed. What does
transfer is the method, the harness, and the finding that pairing is worth
one to two orders of magnitude.
