# The thesis, stated plainly

**Recorded 2026-09-25, operator statement.** It has been implicit in every
decision here and was never written down in one place.

## The claim

**Garbage in produces garbage out.** The internet is a poor-quality
corpus. A curated synthetic corpus for levels one to six, followed by a
curated real-world corpus at level seven, is expected to produce a
superior model.

**This project explicitly rejects volume as the universal answer.** It
operates on the belief that an uncurated corpus produces models with
undesirable properties, and that those properties are a consequence of
what the model was shown rather than of how much it was shown.

## What the claim is not

**It is not the curriculum-ordering hypothesis.** That difficulty-graded
ordering improves pretraining is a separate claim, it is the one the
ablation tests, and `../../CLAUDE.md` forbids stating it as established.
Curation and ordering are different variables and the project holds both.

**It is not a claim that volume is irrelevant.** Measured 2026-09-25, the
level-one model is limited by corpus size and not by training: at four and
a half million parameters it memorises 43,000 tokens perfectly and
predicts held-out text worse than chance. **A curated corpus still has to
be large enough**, and saying so is not conceding the point, because the
claim is about what fills the volume rather than about the volume.

The distinction is worth holding carefully, because it is easy to report
"the corpus is too small" in a way that reads as the opposite thesis. The
honest form is that **a curated corpus of 45,000 words is too small, and
the answer is more curated corpus, not more corpus**.

## What follows for the design

**Every record is written, checked and admitted rather than collected.**
The vocabulary ceiling, the closure requirement and the claim classes all
exist because the alternative is absorbing whatever a generator produced.

**Teacher output is untrusted input**, which is already a standing rule.
It crosses a trust boundary at the generator and is validated against a
schema before it enters the corpus.

**Level seven is where the claim is actually tested.** Levels one to six
are synthetic and controlled by construction. Level seven is real
material, and curating it rather than scraping it is the point at which
the thesis costs something.

## Training is cumulative, not per level

**Level N training starts from the level N minus one model.** Each level
is a continuation rather than a fresh run, so a level-two model inherits
what level one learned about the words the two levels share.

That is why the level-one model matters out of proportion to its size.
**It is not a demonstration, it is the initialisation**, and everything
above it starts from whatever it learned. A level-one model that is
incoherent hands its incoherence to level two.

`epagoge.pilot.warm_start` implements it. The vocabulary grows between
levels, so the embedding and the output head grow with it and rows are
matched by the word they stand for: a word in both lexicons keeps its
learned vector, a word new at the level keeps its fresh initialisation,
and a word that has left is dropped. Every other parameter is copied
outright, and a checkpoint of a different width is refused rather than
reshaped.

**This has not been exercised**, because level two has one module and no
trained model. The mechanism exists and is tested; the run has not
happened.

## What would falsify the thesis

Stated so that it is not unfalsifiable.

A model trained on this curated corpus, compared against one trained on an
uncurated corpus of the same size and the same architecture, showing no
advantage on the properties the project cares about. **That comparison has
not been designed**, and it is a different experiment from the ordering
ablation in `../../evals/PRE_REGISTRATION.md`, which holds the corpus
fixed and varies only the order.
