# The project is three problems, not one

**Recorded 2026-09-25, operator framing.** The curriculum runs from level
one to level seven and it is tempting to treat that as one problem at
seven sizes. It is not. **It is three problems with different shapes,
different failure modes and different definitions of done**, and work that
solves one does not transfer to the others.

Stating this changes what to build next, so it is recorded before the
work rather than after it.

## Level one is a bootstrapping problem

**The goal is a constrained model MVP**: prove that a corpus written in a
closed vocabulary, from nothing, can train a model at all.

The hard part was never volume. It was that **a self-hosting lexicon has
no starting point**: every definition needs words, and those words need
definitions. A dictionary restricted to function words accepted nothing in
twenty-four attempts. It was broken by admitting thirty-seven ostensive
words, which are learned by being shown rather than defined, and
hand-authoring a kernel from them.

**Done means the loop closes and the model is worth talking to.** Closure
is reached: 845 words, every one reducing to a seed of 257. The model
trains, can be sampled and is poor, and the measurement says the corpus is
the limit rather than the training. So what remains at level one is volume
and length, which is ordinary work.

**What does not transfer.** Nothing about bootstrapping applies above
level one, because level two starts with level one's lexicon rather than
with nothing. The ostensive seed is a level-one artifact and stays one.

## Levels two to six are a scheduling problem

**Every concept and every word has to be slotted into a level and
revisited across levels at increasing complexity.** That is an allocation
problem over a partial order, not a writing problem.

It has constraints the bootstrap did not:

- **A concept cannot be taught before its prerequisites**, and the graph
  says which those are.
- **A concept should appear at more than one level**, at increasing depth.
  The curriculum's claim is iteration on the same ideas, so a concept
  taught once and never revisited is a gap.
- **Vocabulary grows on a schedule**, from 845 at level one to about
  10,000 at level two, and each word has a level at which it is first
  admissible.
- **Every domain must be covered at every level**, and seven of eleven
  domains already have no concept left to teach at level two, so their
  modules revisit rather than teach.

**Done means the schedule is complete and consistent, and the corpus
fills it.** Neither half exists past level two: `curriculum/schedule/`
holds two files and levels three to seven have none.

**The failure mode is silent partial coverage**, which is what this
project keeps producing: a book ordering that covered thirteen of a
hundred and forty-six, a chunker that kept a quarter of the corpus. A
schedule that covers most concepts and does not say which it missed is the
same shape of failure at the curriculum level.

**What is missing for it.** A schedule for levels three to seven. A way to
express that a concept is revisited at named levels rather than merely
somewhere. Vocabulary targets per level, which are now researched and
recorded in `READING_LEVEL_RESEARCH.md`. And coverage reporting that names
what is uncovered rather than reporting a percentage.

## Level seven is a transition problem

**It is a different problem entirely.** Levels one to six are an idealised
synthetic corpus written to a controlled vocabulary. Level seven is real
material, unmodified, and the model has to work on real problems.

`../spec/CURRICULUM_LEVELS.md` already says the genre changes at level
seven from treating topics to posing problems, and that breadth widens
again because real problems are cross-domain. **The corpus stops being
written and starts being acquired.**

That brings in problems no earlier level has:

- **Distribution shift.** Every level up to six is clean, ordered and
  written to a ceiling. Real literature is none of those, and a model
  trained only on the idealised corpus meets that as a new language.
- **Licensing.** `sources/README.md` records the constraint and it is
  unexamined: preprint licences vary per item, open access does not
  uniformly grant redistribution, and this repository is CC0.
- **Evaluation against real tasks**, which needs a definition of a real
  task. Nothing in `evals/` measures that.

**Done means the model works on problems nobody wrote for it.** That is
not a corpus property and cannot be checked by any gate here.

**`sources/` is empty and no source has been acquired**, so level seven has
not started by any measure.

## What this framing changes

**It says corpus volume is a level-one concern.** Volume is the binding
constraint on the level-one MVP and was measured to be. It is not the
binding constraint at levels two to six, where coverage and consistency
are, and a large corpus with unscheduled concepts would not be progress.

**It says the level-two lexicon gap is a scheduling failure**, not a
writing backlog. 871 words against a target of 10,000 is a schedule that
has not been written, and admitting words one round at a time from what
blocked a generator will not produce ten thousand of them.

**It says level seven should not be planned as level six but larger.**
