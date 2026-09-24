# The training spine

The architecture that keeps the training framework a replaceable component
rather than a commitment.

**Status.** Specified 2026-09-23. Nothing is implemented.

## Problem

The framework choice is open and the hardware path is unknown. Development
begins on an Apple M1 Max and may migrate. A wrong framework choice is
expensive only if the framework has leaked into every component, so the
design goal is to bound the cost of being wrong rather than to be right in
advance.

## Rejected approach

A single model definition and training loop abstracted over PyTorch, JAX,
and MLX.

This is buildable. The evidence on cost is discouraging. Keras 3, the
mature attempt, supports JAX, TensorFlow, PyTorch, and OpenVINO for
inference, and does not support MLX, verified 2026-09-23. More
informatively, Hugging Face Transformers carried PyTorch, TensorFlow, and
Flax implementations by per-model duplication rather than abstraction, then
progressively deprecated the non-PyTorch variants. A far better-resourced
team found the cost not worth paying.

The divergences are structural rather than incidental. JAX is functional
with immutable arrays, explicit pseudorandom number generator keys, and
parameters passed as trees. PyTorch is stateful with mutable tensors,
global generator state, and parameters owned by modules. MLX is a hybrid,
holding parameters like PyTorch while differentiating functionally like
JAX. Compilation constraints differ, since `jax.jit` forbids
data-dependent control flow that `torch.compile` merely breaks the graph
on. Sharding diverges most, across GSPMD annotations, Fully Sharded Data
Parallel with DTensor, and MLX's thinner distributed story.

An abstraction spanning that is not thin, and a thick abstraction becomes a
third suspect when a loss curve looks wrong.

## Adopted approach

Confine the framework to the model definition and the step function. Make
everything on either side of it framework-neutral.

```
  corpus (parquet/jsonl)
        |
  tokenizer (rust, neutral)  -->  token ids
        |
  ORDERING INDEX (neutral, versioned)     <-- the independent variable
        |
  +-----------------------------+
  |  TRAINER  (framework-bound) |   <- the only replaceable part
  +-----------------------------+
        |
  checkpoints (safetensors)  +  metrics (jsonl)
        |
  evaluation harness (neutral, reads checkpoints)
```

### The ordering index

The most important element for this project specifically.

Data order is the independent variable of the central experiment. It must
therefore not be delegated to any framework's data loader. Order is emitted
ahead of training as an explicit versioned artifact, a deterministic
sequence of document identifiers and positions, produced by a neutral
generator. Every trainer consumes that index rather than deciding order
itself.

Two consequences follow. The independent variable becomes identical across
frameworks by construction. And order becomes exactly reproducible even
where the arithmetic is not, which recovers a substantial part of the
reproducibility that is otherwise unavailable on graphics processing units.
See `../decisions/LANGUAGE_CHOICE.md`.

### Neutral artifacts

| Artifact | Format | Rationale |
| --- | --- | --- |
| Corpus | Parquet or newline-delimited JSON | Language and framework neutral, diffable in the JSON case |
| Tokenizer | Hugging Face tokenizers | Rust implementation, emits plain integer identifiers, no framework sees text |
| Ordering index | Versioned neutral file | The independent variable, see above |
| Checkpoints | Safetensors | Verified 2026-09-23 as used by PyTorch natively, by MLX, and by JAX through Flax and safejax |
| Metrics | Newline-delimited JSON | Step, loss, learning rate, tokens consumed |
| Configuration | Single neutral file | No framework-specific keys |

Checkpoint portability means a model may be trained under one framework and
evaluated under another. Verify reduced-precision dtype round-tripping
rather than assuming it, since that is where formats usually disagree.

## Duplication as a verification asset

Under this arrangement a second trainer is thin, independent, and shares
its inputs and outputs exactly with the first. Independent implementations
agreeing on a loss curve is then evidence that the trainer is not the
confound, which is worth something real in a project whose central claim
rests on an ablation.

**Agreement cannot be bitwise.** Different kernels, reduction orders, and
default precisions guarantee divergence at the last digits. Cross-
validation means curves within a declared tolerance. The tolerance is
declared in advance, not eyeballed after the fact.

## Where this stops working

Distributed training at scale. Fully Sharded Data Parallel, GSPMD, and
MLX's distributed support are not interchangeable, and a multi-node trainer
is no longer thin. This is acceptable because by that point the framework
will have been chosen, and the spine will have made choosing it cheap.

## Build order

1. The neutral spine, now, while nothing exists to be rewritten.
2. One trainer, PyTorch, since it is the only one of the three that both
   works locally on the host machine and carries the reference
   implementations.
3. A second trainer only if wanted. MLX is the more interesting candidate,
   since it buys fast local iteration on hardware already owned, whereas
   JAX would buy a processor-only local path. JAX becomes compelling if
   Tensor Processing Units become available.
