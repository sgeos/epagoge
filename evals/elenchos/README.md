# evals/elenchos/

Anti-sycophancy and calibration probes. Named after the Socratic
cross-examination.

**Status.** Empty. No probe has been written.

## What is measured

The target property is evidence-conditioned assent. A model has it when its
agreement tracks the evidence and does not move under user insistence.

This is measurable through opinion-flip-under-pressure tests, in which a
correct answer is challenged without new evidence and the flip rate is
recorded, and through calibration measurement against ground truth.

## What is not measured, and why

Disagreeableness is not a target and is not measured here. A model
dispositionally biased toward contradiction contradicts correct users at
the same rate as incorrect ones, so a high contradiction rate is
indistinguishable from a high error rate. Any metric that rewards
disagreement alone will be satisfied by a model that is simply wrong more
often.

## Required control

A correct-user condition, in which the user asserts a true claim and
presses on it. A model that flips there is not robust. It is merely
contrary. Measuring the incorrect-user condition alone cannot distinguish
the two.

## Open constraint

Sycophancy is predominantly induced during preference optimisation rather
than during pretraining. Corpus design alone is unlikely to be sufficient,
and the property probably has to be carried through post-training as well.
This project's scope does not currently extend that far.
