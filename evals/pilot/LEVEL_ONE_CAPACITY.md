# Is the corpus the limit, or was the model the wrong size?

**Measured 2026-09-25 on one frozen corpus**: 70,205 words, 82,038 tokens,
756 chunks of which 94 held out, vocabulary 2,259. Every figure below comes
from that corpus. **It is not the corpus the earlier diagnosis used**,
which held 43,023 tokens, so nothing here should be compared against that
file's numbers except where this document does so explicitly and says it is
doing so.

## Why it was asked

The project records that the model is limited by its corpus rather than by
training, and that claim sets every priority beneath it. It rested on a
width sweep of **two points**, 1.39M and 4.35M parameters, both far into
the regime where a model memorises its data.

**A two-point sweep inside the memorisation regime cannot separate "the
corpus is too small" from "the model is too big for this corpus."** The
hypothesis under test was the second: that a smaller model would generalise
better on the same tokens, and that part of the recorded corpus limit was
really a capacity choice.

**The hypothesis is refuted.** It is recorded here rather than deleted,
because a project about falsification that quietly drops its own refuted
guesses is not doing the thing it claims.

## The capacity curve, twenty-six runs

Best held-out loss at each width, with the step count that produced it.

| Width | Parameters | Best held out | At steps | Perplexity |
| --- | --- | --- | --- | --- |
| 16 | 87,488 | 5.509 | 1600 | 247 |
| 32 | 199,552 | 5.252 | 1600 | 191 |
| 64 | 497,408 | 4.920 | 1600 | 137 |
| 128 | 1,388,032 | 4.628 | 1600 | 102 |
| 256 | 4,348,928 | 4.604 | 800 | 100 |
| 512 | 14,989,312 | 4.542 | 400 | 94 |
| 1024 | 55,144,448 | **4.525** | 400 | **92** |

Improvement per width doubling:

| Step | Held out | Parameters |
| --- | --- | --- |
| 16 to 32 | +0.257 | x2.3 |
| 32 to 64 | +0.332 | x2.5 |
| 64 to 128 | +0.292 | x2.8 |
| **128 to 256** | **+0.024** | x3.1 |
| 256 to 512 | +0.062 | x3.5 |
| 512 to 1024 | +0.017 | x3.7 |

## What it says

**The curve saturates at about width 128.** Below it, each doubling buys
roughly 0.29 nats. Above it, going from 128 to 1024 buys **0.103 nats for
forty times the parameters**. That is the signature of a data-limited
regime, which is what the project claimed.

**Smaller is decisively worse.** Width 16 reaches 5.509 against 4.525 at
width 1024. There is no small-model regime in which this corpus supports
better generalisation, so the hypothesis fails in the direction it
proposed.

**Bigger is barely better**, which is why it also fails in the other
direction. Nothing about model size is the lever here.

**The claim now rests on a saturation curve over a 630-fold range of
parameters** rather than on two adjacent points. It is better supported
than it was this morning, by an experiment designed to break it.

## One correction the sweep forces

**The best configuration was not the one in use.** The project's best
recorded figure was 4.789 at width 256, and nothing above 256 had ever been
run. On this corpus the best is **4.525 at width 1024 and 400 steps**.
`LEVEL_ONE_DIAGNOSIS.md` is amended accordingly.

**The optimal step count falls as width rises**: 1600 at widths 16 to 128,
800 at 256, 400 at 512 and 1024. A larger model reaches its best earlier
and then overfits harder. Width 1024's turn was not bracketed, since 400
steps was still improving and 800 was not run; it does not matter, because
the marginal gain there is 0.017 nats.

## Decomposing today's improvement

From 4.789 this morning to 4.525 now, a total of 0.264 nats and perplexity
120 to 92.

| Source | Change | Share |
| --- | --- | --- |
| Corpus, 43,023 to 82,038 tokens, at fixed width 256 | +0.185 | 70 percent |
| Capacity, width 256 to 1024, at fixed corpus | +0.079 | 30 percent |

**Corpus did most of it**, consistent with the project's position.

## The finding that was not being looked for

**The corpus scaling rate measured on real added material is 0.199 nats per
doubling, against the 0.29 the project has recorded.**

The recorded rate came from subsampling one corpus into fractions. This
figure comes from the corpus actually growing, 43,023 to 82,038 tokens,
which is 0.931 doublings for 0.185 nats at fixed width.

**If it holds, it matters.** At 0.29, a million tokens predicts perplexity
35. At 0.199 it predicts 49.

**A likely explanation, untested.** The growth came from
`generators/fill_spreads.py`, which lengthens the spreads a book already
has. It therefore adds more material about the same ninety-five units from
the same teacher, where subsampling removes and restores genuinely
different content. The project's own brief warned that more books about the
same units raise the token count without raising diversity; the same
argument applies to filling them and was not made.

**This is suggestive and not measured.** The two rates come from sweeps
with different held-out sets, and a controlled test would subsample the
current corpus into fractions the way the original did. Until that is run,
neither rate should be quoted as the project's scaling law.

## Files

`level_1_capacity.json` holds widths 16 to 256 at 200 to 1600 steps.
`level_1_capacity_wide.json` holds 256 and 512 at 400 to 1600.
`level_1_capacity_wider.json` holds 512 and 1024 at 100 to 400. All three
report the same 82,038 corpus tokens and 94 held-out chunks, which is what
makes the twenty-six points comparable.
