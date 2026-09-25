# Current brief. Level one end to end, then level two

**Rewritten 2026-09-25** after the operator expanded the goal set to seven
items. Delete when `COMPLETION_CONDITION.md` is met.

## The seven, with what each actually depends on

| # | Goal | State | Real blocker |
| --- | --- | --- | --- |
| 1 | Dictionary coverage and closure | **Done. 661 of 661, closure 100%** | — |
| 2 | Thesaurus, synonyms and antonyms | 194 antonyms, 0 synonyms | None. Authoring |
| 3 | Missing words added to both | No method yet | None. Derive from what definitions had to work around |
| 4 | Full level-one corpus draft | **5 content books of 92 units** | None, at draft scale |
| 5 | Train a level-one model | `epagoge.pilot` has the model, loop, device and paired orderings; torch 2.14 and MPS verified | **Item 4.** The corpus is about 2,200 words and cannot train anything |
| 6 | Level-two dictionary and thesaurus | Level two holds 49 terms | Item 1, and a level-two lexicon |
| 7 | Level-two ablation | Pre-registration has pending items | Items 4 and 5 |

## The sequencing claim, and it is the load-bearing one

**Item 4 is the gate on everything downstream.** The corpus is 2,200
words. Nothing trains on that and no ordering is detectable in it.

One book per schedule unit is roughly 92 books and 40,000 words. That is
both what "full draft" reasonably means and **the minimum orderable set an
ablation can use**, since the ablation orders books and five is not a set.

**It is not the token budget.** `CORPUS_SCALE.md` wants 12 to 600 books
per topic, so 1,923 at the low end. A draft is one per unit. Say which is
meant whenever reporting, because conflating them overstates the project.

## What done means for 5 and 7

**A run that completes and reports honestly.** The corpus will be far
below the scale at which an ordering effect could be detected, and the
published literature already reports such effects as weak and
inconsistent at full scale. **Expect a null. Record it as a null.** A
result that is not there must not be manufactured, and the pre-registered
threshold is what decides, not the sign of the difference.

## Wrong turns, every one already made once

- **The gate must gate.** A commit ran after `GATE=1` was printed in the
  same invocation. Reading the exit code is not enough if the commit runs
  regardless. Run the gate, stop, then commit.
- **Do not run large generation passes for definitions.** Acceptance fell
  22.6, 16.4, then 6.0 percent. Authoring yields about a hundred a round
  against twenty-nine for a forty-batch pass.
- **Read closure, not acceptance.** Two interventions raised acceptance
  and moved closure not at all.
- **Do not grow the ostensive seed to make closure easy.** 33 to 37 once,
  held at 37 for four rounds. A large enough seed closes any lexicon.
- **Do not assume a word is core.** `done`, `taken`, `doing` were each
  assumed and each wrong.
- **A heuristic needs two pieces of evidence.** One inflection read `a`,
  `i` and `it` as verbs and wrote six nonsense words into core.
- **A guard over records must test `defines.kind`.** Omitting it dropped
  four domain and topic definitions.
- **No magic numbers in tests.** An assertion of more than 800 thesaurus
  entries went stale the moment inflections were merged. Tie to the
  lexicon.
- **Never `git checkout` to undo without checking what else is
  uncommitted.** It cost two authored waves.

## Watch these two numbers

**The ostensive seed size**, and **books against schedule units**. The
first guards the self-hosting claim. The second is the honest measure of
how much corpus exists.
