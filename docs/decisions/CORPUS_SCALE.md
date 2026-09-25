# What level one actually costs

**Measured 2026-09-24**, from five generated books against the recorded
budget. These are projections from a small sample and are marked as such.

## Where it stands

| | |
| --- | --- |
| Books written | **5** |
| Words written | **681**, mean 136, range 106 to 173 |
| Topics scheduled | **83** |
| Level-one terms | **760** |
| Words with a definition | **27** |

## One book per topic is not a corpus

At the observed mean, one book for each of the 83 topics gives **11,304
words**, which is **1.47 percent of the low end** of the recorded budget.

`../spec/CURRICULUM_LEVELS.md` puts level one at 10^6 to 10^7 tokens, so
roughly 770,000 to 7.7 million words at about 1.3 tokens per word for
simple English.

| Budget | Words | At 150/book | At 400/book | At 800/book |
| --- | --- | --- | --- | --- |
| Low, 10^6 tokens | ~770,000 | 5,128 books | 1,923 books | 962 books |
| High, 10^7 tokens | ~7,700,000 | 51,282 books | 19,231 books | 9,615 books |

**Between 12 and 600 books per topic**, depending on where in the budget
and how long a book runs.

## This is the repetition, not a problem with it

The operator recorded early that the corpus needs to be somewhat
repetitive, and that a level-one book is 100 to 800 words. Both hold. What
the arithmetic adds is that **repetition is not a stylistic preference here,
it is the only way the budget is reachable at this book length**.

Many books per topic also gives the spiral its material. The same concepts
recur in different stories, which is what `CURRICULUM_LEVELS.md` describes
and what one book per topic cannot deliver.

## Cost, from the measured throughput

`../../generators/TEACHER.md` records roughly fifty tokens per second warm,
and one million tokens at about five and a half hours single-stream.
Generation produces more than it keeps, between two and four times, once
rejections and reworks are counted.

**So the low budget is on the order of eleven to twenty-two hours of
single-stream wall time**, improving several-fold under concurrency. That
agrees with the earlier estimate of a few hours to a couple of days, which
was made before any book existed.

## The dictionary is the bootstrap, and level one is the hard one

**Operator framing, 2026-09-24.** The dictionary is the applied proof that
the lexicon is closed, and **level one is hardest for the same reason a
self-hosting compiler is**. A compiler written in its own language needs a
seed written in something else. Level two builds on a lexicon that is
already closed. Level one has only the function words under it, which name
nothing, so it has to define itself.

`dictionary_closure` measures it. A word is grounded when every content
word in its definition is in the seed or is itself grounded, iterated to a
fixed point.

| | First measurement | After eight batches |
| --- | --- | --- |
| Defined | 27 of 760 | **49 of 760** |
| **Grounded** | **0** | **1** |
| Blocked, resting on something ungrounded | 27 | 48 |
| Frontier, used and never defined | 38 | **47** |

**The frontier grew while the dictionary grew.** Defining a word introduces
the words its definition used, so the frontier expands before it contracts.
That is the shape of the problem rather than a fault in the approach, and
it is why the generator works the frontier first.

**One word is grounded**, `different`, whose definition reaches only
function words. Everything else rests on something that does not yet
bottom out.

## What this does not establish

The mean book length is from five books, four of them written by the same
prompt shape against adjacent topics. **A different topic may run longer or
shorter and the sample cannot say.**

Nothing here says the budget is right. It is an order-of-magnitude figure
from word counts rather than a measurement, and it is recorded as such
where it is stated.
