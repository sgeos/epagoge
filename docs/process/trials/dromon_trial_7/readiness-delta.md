# Readiness delta from the term list

**Fact.** The current curriculum/vocabulary.json blob is 26fd70343c9a9193e97d22e2fafa176957f04d56.

**Command.** python3 -I docs/process/trials/dromon_trial_6/readiness_terms.py "$PWD"

**Fact.** The script counts distinct words from term entries at levels one and two for each concept taught or revisited by the 26 level-two units without books. A count measures vocabulary on file, not whether a module can be written.

## Current top five

**Rule.** The script ranks by fewest concepts with zero combined words, then highest minimum combined count, then highest combined sum, then unit identifier ascending.

| Rank | Unit | Combined sum |
|---:|---|---:|
| 1 | r2.measure | 357 |
| 2 | p2.matter | 592 |
| 3 | p2.force | 584 |
| 4 | b2.mending | 111 |
| 5 | b2.keeping_going | 169 |

## Units with a changed rank or combined count

**Fact.** Against docs/process/trials/dromon_trial_6/readiness-terms.md, every unit's combined sum changed. Ranks were recalculated with the same rule for the earlier and current counts. Rank 1 is the top.

| Unit | Earlier rank | Current rank | Earlier combined count | Current combined count |
|---|---:|---:|---:|---:|
| a2.mistake | 18 | 19 | 84 | 98 |
| a2.plan | 7 | 9 | 182 | 219 |
| ac2.balance | 25 | 25 | 49 | 57 |
| ac2.flow | 5 | 7 | 28 | 31 |
| b2.keeping_going | 8 | 5 | 142 | 169 |
| b2.mending | 4 | 4 | 100 | 111 |
| c2.claim | 26 | 26 | 49 | 55 |
| c2.explain | 14 | 12 | 73 | 84 |
| c2.report | 20 | 20 | 64 | 67 |
| f2.accident | 13 | 15 | 77 | 83 |
| f2.checking | 6 | 6 | 30 | 35 |
| f2.failing | 19 | 14 | 83 | 94 |
| h2.findout | 9 | 8 | 61 | 64 |
| h2.wrong | 23 | 23 | 12 | 17 |
| i2.reason | 22 | 22 | 18 | 20 |
| i2.rule | 12 | 11 | 83 | 93 |
| m2.addsub | 15 | 16 | 46 | 55 |
| m2.howmuch | 10 | 10 | 143 | 152 |
| m2.logic | 21 | 21 | 26 | 28 |
| m2.number | 11 | 13 | 70 | 73 |
| n2.fair | 16 | 17 | 26 | 30 |
| n2.should | 24 | 24 | 78 | 93 |
| p2.force | 3 | 3 | 513 | 584 |
| p2.matter | 2 | 2 | 543 | 592 |
| r2.measure | 1 | 1 | 325 | 357 |
| r2.record | 17 | 18 | 150 | 169 |

**Inference.** The top five changed only at fifth place, where b2.keeping_going replaces ac2.flow. All units have larger combined counts. These are changes in term-list counts, not evidence of writing readiness.

## Five thinnest scheduled concepts

**Fact.** Sorting concepts by combined distinct-word count and then concept identifier gives these five tied at one word each.

| Concept | Combined count | Word and level |
|---|---:|---|
| balance | 1 | balance, L2 |
| letter | 1 | letter, L1 |
| reconciliation | 1 | reconcile, L2 |
| right_reason | 1 | right, L1 |
| two_shoulds_at_once | 1 | hard, L1 |
