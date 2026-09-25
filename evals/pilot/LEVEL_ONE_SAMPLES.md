# What a level-one model actually produces

**Measured 2026-09-25.** One model, 1,386,496 parameters, 800 steps on the
level-one corpus, sampled at temperature 1.0 from the book marker. Raw
output in `level_1_samples.json`, weights in `level_1.pt`, which is not
tracked.

## Until today, nothing had been sampled

Every training run before this one returned a single float and discarded
the model. Sixteen models a run, several runs, **no token was ever
generated**. "The corpus-to-model loop is closed" meant corpus to number.

That is defensible for the ablation, which compares two orderings by
held-out loss and has no use for a checkpoint. It is not defensible as the
only thing the project can do, because **held-out loss cannot distinguish
a model that learned the language from one that learned which words are
common.**

## The first metric I wrote was vacuous

It reported the share of sampled word tokens admissible at level one. That
share was **100.0%**, and it would have been 100.0% for an untrained model,
because the tokeniser is built from the level's lexicon and every token the
model can emit is admissible by construction.

**A metric that agrees with you whatever happens is not a measurement.**
It is recorded here because it took a run to notice, and because the
number looked like a result.

## What is reported instead

| Quantity | Value |
| --- | --- |
| Held-out loss | 4.91, against ln(2253) = 7.72 for uniform |
| Sampled word tokens | 315 |
| Distinct share | **51.7%** |
| Sentences of three words or more | **87.1%** |

**Distinct share falls when the model loops**, and these samples loop hard
on "the cup", which is the most common noun in the corpus. **Sentence
share applies the corpus's own shape rule to the model's output**, so the
model and the teacher are judged by one standard.

Neither number has a target. They are descriptive, and at this corpus size
the samples are expected to be poor.

## What the output looks like

> the floor . the butterfly open and reached still close enough said an .
> a window hard of left cup , how ball was cool it again it

**Locally plausible and globally incoherent**, which is what 1.4 million
parameters on forty thousand tokens should produce. Articles and stops
land in roughly the right places, two-word and three-word collocations are
often real, and nothing survives a clause boundary.

**It is worth knowing that it is this bad.** Loss alone would not have
said so, and a reader told only that a model had been trained would
imagine something else.

## What this does not measure

Grammaticality, truth, and whether the corpus taught any concept. No
automated check for any of those exists. The samples are also a single
seed at a single temperature, so they show what the model does and not the
range of what it does.
