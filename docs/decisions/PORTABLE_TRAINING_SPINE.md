# Portable training spine

**Decided 2026-09-23.** The training framework is confined to the model
definition and the step function. Every artifact on either side of it is
framework-neutral. One trainer is written, not three.

The full contract is in `../architecture/TRAINING_SPINE.md`.

## Why this decision and not the framework decision

The framework choice remains open and blocked on the hardware path. This
decision makes that acceptable rather than urgent. A wrong framework choice
is expensive only when the framework has leaked everywhere, so bounding the
blast radius is worth more than choosing correctly in advance.

## What was rejected

A unified abstraction over PyTorch, JAX, and MLX. Keras 3 does not cover
MLX, and Hugging Face Transformers chose per-model duplication over
abstraction and then deprecated the duplicates. Evidence and reasoning in
the architecture document.

## What this constrains, before those things exist

- The corpus format must be framework-neutral.
- Order must be a separate emitted artifact, not a data loader behaviour.
- Checkpoints must be safetensors.
- The evaluation harness must not import a training framework.

Recording this now is the point. Each constraint is free while nothing is
implemented and expensive afterwards.

## Reversal condition

None expected. If a single framework becomes certain and permanent, the
spine costs a little indirection and retains its other benefits, namely a
reproducible ordering artifact and portable checkpoints. The decision is
therefore close to risk-free, which is the reason to take it before the
framework question is settled rather than after.
