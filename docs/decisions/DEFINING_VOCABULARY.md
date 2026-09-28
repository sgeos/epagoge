# The missing step, and the prompt that grew with the lexicon

**Built 2026-09-28.** The lexicon pipeline had a hole in the middle, and
closing it exposed a scaling problem in how the teacher is asked anything.

## The hole

**`tools/admit.py` refuses a word without a definition**, correctly, because a
word admitted without a grounded one takes the dictionary out of self-hosting.
**`generators/generate_dictionary.py` writes definitions for words that are
already admitted.** Nothing took a candidate and produced the definition that
would let it in.

**So the only route was writing them by hand**, which is what the 47-word batch
of 2026-09-27 did. **Nine thousand words at a hundred a session is ninety
sessions**, and that is not a plan.

`generators/define_candidates.py` is the missing step. It takes candidate words
with their concepts, has the teacher draft definitions, drops any that reach
outside the level, and writes exactly what the admission tool consumes.
**Nothing is admitted by it.** It writes the input that `admit.py` judges, and
`admit.py` re-checks every survivor against the whole dictionary's closure.

## The prompt listed the whole lexicon, so it grew with the work

**At 934 admissible words the definition prompt reached 3,494 tokens against a
budget of 3,328**, and `generate.ask` refused rather than let the server
truncate silently, which is the behaviour that check exists for.

**The shape is the problem, not the budget.** The prompt names every admissible
word, so **at the ten-thousand-word target the list alone is roughly fifteen
thousand tokens.** No context this machine can hold would be enough, and the
failure arrives exactly as the work succeeds.

### Raising the context was tried and reverted the same hour

| | Before | At 6,144 |
| --- | --- | --- |
| Model resident | 18 GB | 19 GB |
| Free memory | 0.9 GB | **0.1 GB** |
| Swap used | | **14.9 GB of 16.4 GB** |

**`NUM_CTX`'s own docstring warned that the cost is quadratic in the wrong
direction on a machine this size, and it was right.** Swap exhaustion is the
condition this host has crashed under. Reverted to 4,096, with the measurement
recorded beside the constant rather than in a commit message nobody reads.

## Narrow the ask, not the acceptance

**The teacher is given a defining vocabulary of 700 words**: the seed, the
function words, the ostensive set, and the most-used content words by corpus
frequency. **A definition is accepted if it stays inside the level**, which is
the real constraint and is wider than what was asked for.

**Asking for less than is allowed costs nothing.** Measured on the same 30
candidates, the acceptance rate is **67 percent either way**, at 4,096 context
with 700 words and at 6,144 with the full lexicon. **A definition written in
common words is better grounded anyway**, which is the property the whole
self-hosting requirement exists for.

**This scales because the defining vocabulary does not grow with the lexicon.**
It is a fixed budget of the most useful words, so the prompt stays the same
size whether the lexicon holds one thousand words or ten.

## What the first run measured

**30 candidates offered, 20 defined, 67 percent.** All 20 admitted, each
carrying the source that proposed it. **Level two is still self-hosting at 917
of 917 words needing a definition.**

**954 words admissible at level two, so 9,046 remain.**

**Ten failed on vocabulary the teacher wanted and could not have**: `honey`,
`fruit`, `flour`, `clothing`, `beans`, `petals`, `yeast`, `nut`, `roasted`,
`rows`. **Those are candidates, not errors.** A word the teacher reaches for to
define another word is evidence about what the lexicon is missing, and it is
the cheapest signal this pipeline produces.

## What it does not do, and one of these is not fixable here

**Archaism is invisible to it.** The candidates come from a frequency scan over
public-domain sources, which are public domain because they are old. Neither
the counter nor the teacher can see that a word was ordinary in 1880 and wrong
for a child now. **Judgement at drafting is the only place this is caught**,
which `LEXICON_SOURCING.md` said before this tool existed.

**Concept assignment is still per word.** The batch above was themed so that
the concept was obvious, which is the easy case. A general batch needs a
judgement per candidate and nothing here supplies it.

**One batch is one sample.** 67 percent on themed concrete nouns is not the
rate on abstract words, and it should not be quoted as the pipeline's rate.

## A correction, kept because the way it happened is the lesson

**A rule was added requiring definitions to lead with the word**, on the
evidence that the dictionary reads "Winter is the cold part of the year". The
rule rejected every definition in the next run.

**The dictionary's dominant form is the gloss**: 551 of 795 level-one entries
do not lead with the word, against 244 that do.

**The evidence had been gathered with a pattern that could only return the
leading form.** A grep for entries beginning with a capitalised word followed
by "is" returned eight examples, all of that shape by construction, and the
conclusion was drawn from them. **A filtered view is not a sample of the
population**, and the filter had built the very pattern it appeared to reveal.
The rule and its check were reverted.
