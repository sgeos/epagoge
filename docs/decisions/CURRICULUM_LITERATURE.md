# What the literature says about this project's central claim

**Spike run 2026-09-26** on operator instruction, weighted toward the
machinery of training with attention to architecture. **Every paper below
was read rather than recalled**, and where only an abstract was reachable
this says so.

**The short answer is that the literature splits the project's thesis in
two and treats the halves very differently.** The claim that a curated,
simplified corpus buys sample efficiency is well supported. The claim that
**ordering** that corpus by difficulty buys anything is weakly supported at
best and has been directly contradicted three times, once in 1999 in nearly
this setting. What does work at the level of ordering is not content
difficulty but **sequence length** and **model-measured revisiting**.

## The result that most threatens the thesis

**Wu, Dyer and Neyshabur, "When Do Curricula Work?", ICLR 2021.**
Thousands of orderings across curriculum, anti-curriculum, and a
**random-curriculum** control in which the training set grows over time but
its examples are randomly ordered.

**Curriculum helps only under a limited training budget or with noisy data,
and the benefit is entirely attributable to the growing training set size
rather than to the order.** The random-curriculum control captures it.

**This has a direct consequence for pre-registration item 10.** The
project's planned ablation compares a curriculum arm against a flat-order
arm. **Those two arms cannot distinguish ordering from set-size growth.** A
third arm is needed: the training set grows on the same schedule, and the
books entering it are chosen at random. Without it a positive result is
attributable to the schedule and not to the curriculum, and the project
would be publishing the confound this paper named.

**This is the single most actionable finding of the spike.**

## The 1999 result in almost exactly this setting

**Rohde and Plaut, "Language acquisition in the absence of explicit
negative evidence: how important is starting small?", Cognition 1999**,
replying to **Elman, "Learning and development in neural networks: the
importance of starting small", Cognition 1993.**

Elman found a recurrent network could learn an artificial grammar with
embedded clauses only when started on simplified input. Rohde and Plaut
found the opposite on pseudo-natural languages with number agreement,
variable argument structure, embedded clauses and semantic biases:
**networks start small on their own, and delayed introduction of complex
examples is often an impediment.**

**How much this bears on this project is arguable and should be argued
honestly.** What Elman and Rohde and Plaut manipulated was **syntactic**
complexity at fixed vocabulary. This project manipulates **conceptual**
progression under a closed and growing **lexicon**, which is a different
intervention. But the burden of proof runs the project's way: the nearest
prior experiment found the manipulation harmful.

## The closest regime, and its verdict

**Warstadt et al., "Findings of the BabyLM Challenge", arXiv 2504.08165.**
Sample-efficient pretraining on developmentally plausible corpora under 100
million words, which is the regime this project is in.

**"Curriculum learning attempts, which accounted for a large number of
submissions, were largely unsuccessful, though some showed modest
improvements."**

**What did succeed is more interesting than what failed.** Three things:

1. **Architecture.** LTG-BERT, which collects recent transformer
   optimisations, and whose winning submissions "outperformed models
   trained on trillions of words."
2. **Shorter input sequences.**
3. **Distillation from a pretrained teacher.**

**Item 2 is a direct caution to this project's own experiment**, run the
same day, on whether a whole book should be one training sequence.

## The paper the operator found, read carefully

**Yang, Bean, McCraith and Mahdi, arXiv 2408.07888**, human-inspired
learning strategies for fine-tuning on medical question answering.

**It is fine-tuning, not pretraining**: QLoRA, single epoch, 874 questions,
on TinyLlama 1.1B and Llama 2 7B and 13B and Mistral 7B.

**Its spiral arm is named "Interleaved Curriculum", cycling through
difficulty-sorted categories, and it produced the largest single gain in
the paper**: +1.81 percentage points on MedMCQA with model-defined
difficulty. Maximum per-model gain 1.77 points. Averages across models and
datasets, 0.94 and 1.02 points, against baselines from 20.40 to 47.97
percent.

**Three things temper it.** The authors state plainly that the benefits
"do not generalise", with the best strategy differing across all four
models. They report **no confidence intervals**, because their five-sample
design produced dependent observations. And they name the small dataset and
narrow difficulty span as limitations.

**Its most useful finding for this project is about difficulty labels, not
about ordering.** Model-defined difficulty beat human-defined difficulty on
every curriculum arm, moving the spiral arm from +0.16 to +1.81 on one
dataset. **This project's difficulty is entirely human-defined**, by
operator judgement about levels, and that is the label type the paper found
weaker.

## Where ordering demonstrably works: sequence length

**Li, Wang, Zhu et al., "The Stability-Efficiency Dilemma: Investigating
Sequence Length Warmup for Training GPT Models", arXiv 2108.06084.**

**Training instability correlates with extreme gradient variance, and long
sequences early in training are a main source of it.** Starting short and
growing enables **8 times the batch size and 4 times the learning rate**,
and reduces tokens and wall clock by up to **2.2 and 3.7 times**.

That is an order of magnitude more effect than any content curriculum in
this survey, and it is a curriculum over a property of the data rather than
over its meaning.

**Apple, "Dataset Decomposition: Faster LLM Training with Variable Sequence
Length Curriculum", NeurIPS 2024, arXiv 2405.13226**, extends this to a
variable-length curriculum and reports faster training. Abstract read only.

## Where revisiting demonstrably works: measure it, do not schedule it

**This is the finding that most affects how the project should build its
spiral.**

**"Accelerating Large Language Model Pretraining via LFR Pedagogy: Learn,
Focus, and Review", arXiv 2409.06131.** Llama and GPT models on SlimPajama
and OpenWebText. It **tracks the model's performance across data blocks and
prioritises revisiting the regions it is doing badly on.** Reported: lower
perplexity and higher accuracy using **5 to 19 percent of the training
tokens** of full-dataset baselines, and **3.2 percent** of tokens to match
Pythia models with up to twice the parameters. Abstract read only; the
numbers are large enough to want the full method before believing them.

**"When to Review: Spaced Repetition for Continual Pre-Training of Language
Models", arXiv 2608.17530**, schedules rehearsal with a SuperMemo-2
algorithm and argues that **continual pretraining is a scheduling problem
rather than a mixture problem**: revisit what the model is failing to
retain, not what it has already learned.

**The consequence for this project is sharp.** Its coverage tool reports a
concept "taught once and never revisited" as a gap **against the
schedule**. Both papers say the gap that matters is **against the model**.
A concept the model retains needs no revisiting; one it loses needs it
whether or not the schedule says so. The project has the instrument for
this already, since it can measure per-book held-out loss.

## Where the thesis is well supported

**Corpus quality and simplification, which is the half of the thesis that
is not about ordering.**

**Eldan and Li, "TinyStories"**, showed small models trained on a synthetic
corpus restricted to a young child's vocabulary produce fluent, coherent
English, which models of the same size trained on general web text do not.

**Gunasekar et al., "Textbooks Are All You Need"**, and the phi series
attribute large gains to data quality. **This project's own `CLAUDE.md`
already records that those gains are attributed to quality and not to
ordering**, which the literature continues to support.

**"TinyHelen's First Curriculum", arXiv 2501.00522**, builds a pipeline
that eliminates noise and minimises vocabulary while keeping genre
patterns, producing a 71-million-token leaner pretraining set, and reports
that leaner pretraining improves learning efficiency and that tiny models
trained on it outperform those trained on the originals. **It does not
separate corpus simplification from curriculum ordering**, which is the
confound this project must avoid in its own reporting. Abstract read only.

## What this means for the project, stated as changes

**1. Add a random-curriculum arm to the ablation.** Highest priority. The
present design cannot separate ordering from set-size growth.

**2. Treat the revisit gap as a model measurement.** Report concepts the
model fails to retain, not concepts the schedule mentions once. This is a
change to `tools/coverage.py` and it makes the spiral testable rather than
asserted.

**3. Consider a sequence-length curriculum, which is the one ordering
effect in this survey with a large measured payoff.** It is also nearly
free here, since the corpus is already tokenised per book.

**4. Consider model-defined difficulty.** The operator's level assignments
are human-defined, which is the weaker label type in the one paper that
compared them. A cheap version exists: rank books by the level-one model's
per-book loss and compare that ordering against the curriculum ordering.

**5. Do not claim the quality result as an ordering result.** The
literature supports curated simplified corpora and does not support
difficulty ordering. The project's standing obligation already says this;
the spike confirms it was the right obligation.

**6. Architecture is an underweighted lever.** BabyLM's winners beat models
trained on trillions of words with LTG-BERT. This project uses a plain
transformer encoder and has never varied architecture, only width, depth
and sequence length.

## What the spike did not find

**No work testing a spiral curriculum in pretraining from scratch on a
purpose-written corpus.** The nearest are the fine-tuning result above and
the revisiting papers, which schedule against the model rather than against
a designed curriculum.

**So the project's specific claim is untested rather than refuted**, which
is a better position than it looked at the start of this document, and
worse than it looked before the ablation confound was identified.

## Sources

- https://arxiv.org/abs/2012.03107 When Do Curricula Work?
- https://arxiv.org/abs/2504.08165 Findings of the BabyLM Challenge
- https://arxiv.org/html/2408.07888v1 Human-inspired learning strategies
- https://arxiv.org/abs/2108.06084 Sequence Length Warmup
- https://arxiv.org/pdf/2405.13226 Dataset Decomposition
- https://arxiv.org/pdf/2409.06131 LFR Pedagogy
- https://arxiv.org/abs/2608.17530 When to Review
- https://arxiv.org/abs/2501.00522 TinyHelen
- Rohde and Plaut 1999, Cognition 72(1):67-109. Copy at
  https://ni.cmu.edu/~plaut/papers/pdf/RohdePlaut99Cog.startingSmall.pdf
