# Language and framework choice

This record covers two decisions that were originally conflated. They are
separated here because only the first is settled.

1. **Implementation language. Decided.** Python is primary. Rust is
   deferred to measured bottlenecks.
2. **Training framework. Open.** PyTorch versus JAX is blocked on the
   hardware path. A decision rule is given below.

## Revision history

- 2026-09-23, initial. Recorded Python primary and asserted PyTorch as
  settled on the grounds that the training stage "admits essentially one
  choice."
- 2026-09-23, amended. That assertion was not the product of a comparison
  and is withdrawn. The framework question is demoted to open. The
  comparison is recorded below against verified sources.

## Decision one. Python is primary

**Settled, and unaffected by the framework question.** Both candidate
frameworks are driven from Python, so this decision does not depend on
which is chosen.

**Ecosystem convention dominates.** Reference implementations of
transformer pretraining, distributed training strategies, checkpoint
formats, optimizer variants, and published curriculum ablations exist in
PyTorch or JAX. Implementing the training loop elsewhere would mean
reimplementing sharded data parallelism, mixed precision, activation
checkpointing, and sharded optimizer state, and then being unable to
compare against any published result.

**Corpus generation is input and output bound.** The generation pipeline
waits on model responses, so language choice barely affects throughput and
should match the rest of the stack rather than introduce a boundary.

**The Rust options were considered and rejected.** Burn is a genuine
training framework with autodiff and pluggable backends. Candle is
predominantly inference-oriented. Neither is rejected on language grounds.
Both are rejected because there are no reference pretraining
implementations, no sharded-training story comparable to Fully Sharded Data
Parallel, and no published ablations to compare against, which would leave
this project's results unsituated against anyone else's. This is the same
reasoning that produced the Python decision, applied consistently.

**Why not Rust, given this operator's repository history.** Fifty-four
Rust projects and a Rust language implementation as the most mature work
would make Rust the agreeable recommendation. It is not the correct one,
and the operator's standing directive that ecosystem conventions take
precedence points the same way.

**Costs accepted.** Weaker static guarantees than the rest of this
operator's toolchain, mitigated by pyright in strict mode as a gate, ruff
with the security ruleset, and schema-validated models at every boundary
rather than dictionaries. The last is not stylistic. Teacher-model output
is untrusted external input and the generator boundary is where validation
belongs. A future Rust port would also introduce an interoperability seam
requiring a differential test rather than an assumption, which is a reason
to delay the port rather than to avoid it permanently.

## Decision two. Training framework, OPEN

The field reduces to PyTorch versus JAX. Names that sound like competitors
mostly are not. Megatron-LM, DeepSpeed, NeMo, torchtitan, nanotron,
GPT-NeoX, and llm-foundry are all PyTorch. MaxText and Levanter are JAX.
Keras 3 wraps both and is not used for frontier pretraining. MLX is treated
separately below.

### The argument that appeared to favour JAX, and what verification did to it

The central experiment in this project is an ablation. Curriculum-ordered
training is compared against flat-order training and the difference is
attributed to ordering. That attribution is valid only if the runs differ
in ordering and in nothing else, and the expected effect size is small,
since small and inconsistent is what the published ordering literature
reports. Reproducibility is therefore close to a load-bearing requirement
rather than a nicety.

Levanter, from Stanford's Center for Research on Foundation Models,
appeared to offer that structurally. **Verified 2026-09-23, the guarantee
is narrower than claimed.** Its documentation and repository README state
"On TPU, Levanter is bitwise deterministic, meaning that the same
configuration will always produce the same results, even in the face of
preemption and resumption." No equivalent claim is made for graphics
processing units. Separately, "Training can even be resumed on a different
number of hosts, though this breaks reproducibility for now."

PyTorch states the converse explicitly. "Completely reproducible results
are not guaranteed across PyTorch releases, individual commits, or
different platforms," and "results may not be reproducible between CPU and
GPU executions, even when using identical seeds." Mechanisms exist, namely
`torch.use_deterministic_algorithms`, the cuDNN determinism flags, and
`worker_init_fn` with an explicit generator for data loading, but they are
opt-in, carry a performance cost, and several attention backends have
nondeterministic backward passes by default.

**Net effect.** Neither framework offers bitwise determinism on NVIDIA
hardware. The reproducibility argument does not discriminate between them
on that path. It discriminates only in favour of JAX on Tensor Processing
Units.

### What favours PyTorch

**Local iteration.** PyTorch has a working Metal Performance Shaders
backend on the host M1 Max. JAX does not have a maintained one. The
`jax-metal` plugin is effectively abandoned, with maintainers closing
issues in December 2025 citing no active development. Third-party
successors named `jax-mps`, `applejax`, and `metaljax` exist and are
experimental or beta, pinned to specific `jaxlib` versions. Verified
2026-09-23.

**Ecosystem leverage.** More reference implementations, more evaluation
tooling, tighter integration with Hugging Face Transformers, and more
published work to compare against.

**Debuggability.** Eager execution is easier to inspect than traced and
compiled functional code, and this project will spend considerable time
inspecting.

### A correction to an earlier claim in this project's favour of JAX

An earlier statement held that JAX is second-class on NVIDIA hardware. That
was overstated. Published guidance covers JAX scaling from a single GPU to
multi-node Blackwell clusters, and general support quality is adequate. It
is the determinism guarantee that is Tensor Processing Unit scoped, not
JAX itself.

### MLX

Not viable as primary. The CUDA backend is real and in progress, with
partial operator coverage still being merged as of 2026-09-23, so it does
not yet provide a deploy path off Apple Silicon. Adopting it would also
require maintaining a second model implementation kept numerically
equivalent to the first.

## Decision rule

The choice is decidable once the hardware path in
`OPEN_QUESTIONS.md` items one and five is answered.

| Hardware path | Framework | Reason |
| --- | --- | --- |
| Tensor Processing Unit access | JAX with Levanter | The bitwise determinism guarantee applies, and Marin-8B is evidence the path works at that scale |
| NVIDIA only | PyTorch | The sole differentiating argument for JAX does not apply, and PyTorch wins on ecosystem and local iteration |
| Local prototyping only | PyTorch | JAX has no maintained Metal backend |

## Consequence that outranks the framework choice

Because bitwise determinism is unavailable on graphics processing units
under either framework, the ablation cannot rely on it. The ordering effect
must be demonstrated to exceed seed-to-seed variance, which requires
multiple seeds per condition and reported variance rather than single runs
compared point to point. This requirement is framework-independent and is a
larger threat to the project's central claim than the framework choice is.
Recorded in `evals/README.md`.

## Sources consulted 2026-09-23

- Levanter documentation, https://levanter.readthedocs.io/en/latest/
- Levanter repository README,
  https://github.com/marin-community/levanter
- PyTorch reproducibility notes,
  https://docs.pytorch.org/docs/2.14/notes/randomness.html
- Python Package Index metadata for torch, jax, jaxlib, and mlx
