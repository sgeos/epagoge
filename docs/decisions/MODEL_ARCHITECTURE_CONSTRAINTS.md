# Model architecture constraints

**Provisional, 2026-09-23.** Adopt hardware-portability constraints as a
discipline of restraint. Do not adopt them as a design programme, and do
not let them justify departure from a standard reference architecture.

One premise is challenged below and one question is open.

## The question that prompted this

Whether to build the model from the ground up so that it is structurally
optimised for the portable cross-section of Tensor Processing Unit and
embedded accelerator functionality.

## Premise challenged

The two are not the same kind of constraint, and conflating them hides a
real decision.

A Tensor Processing Unit is a **training and inference** accelerator. Its
constraints are static shapes, an absence of data-dependent control flow,
large dense matrix multiplications, native bfloat16, and dimension
alignment.

Most embedded accelerators are **inference-only** deployment targets,
typically quantised to eight or four bit integers, with narrow operator
coverage and no training support at all. The Apple Neural Engine is
inference-only and reached through CoreML. The category is also extremely
heterogeneous across vendors, so "the NPU cross-section" is not a single
well-defined target.

Designing for the intersection therefore means two separate activities, one
governing how the model trains and one governing how it deploys. They
should be decided separately because they have different evidence and
different costs.

## The reframing that makes the answer cheap

**The standard architecture already is the portable cross-section.** A
conventional dense decoder-only transformer is what Tensor Processing Unit
compilers and embedded accelerator toolchains are best optimised for,
precisely because it is what everyone runs. Vendors optimise the common
case.

Portability is therefore obtained by restraint rather than by design
effort. The instruction is to decline to innovate on architecture, not to
innovate toward portability. This costs close to nothing, which is why it
is worth adopting.

## Constraints adopted

Cheap, and beneficial on graphics processing units as well.

- Static shapes throughout. Fixed sequence length, padded batches, no
  ragged inputs.
- No data-dependent control flow in the step function.
- Dense matrix multiplications carrying the bulk of the arithmetic.
- Model dimension, head count, and vocabulary size aligned to multiples of
  128. This follows widely published alignment guidance rather than a
  measurement taken here.
- Standard components only. Conventional attention, root mean square or
  layer normalisation, a standard gated activation, rotary position
  embedding.
- No exotic operators. No custom kernels, no complex-valued or transform-
  based mixing, no irregular gathers in the hot path.
- Dense rather than mixture-of-experts. Mixture routing is data-dependent,
  is hostile to embedded accelerator toolchains, and complicates the
  ablation.

## Constraint that outranks the others

**Jacobian-space must stay adequately unconstrained.** See
`JACOBIAN_SPACE.md`. Several constraints in this record reduce the width of
the reachable function space, and ternary quantisation and small parameter
count do so severely. Any constraint here that pushes the tangent-kernel
effective rank below the declared floor is rejected regardless of what it
buys on portability or fault tolerance.

**Fault tolerance is not obtained by flattening the model.** It is obtained
in hardware, through error-correcting codes on weight memory, scrubbing
against a protected copy, and triplication of the small high-precision
core. Training toward flatness would purchase bit-flip tolerance with the
capacity the model exists to have, and flatness is not in any case a
reliable good.

## The cost that must not be paid

**Comparability.** The project's claim concerns curriculum ordering. If the
architecture is also non-standard, an observed effect cannot be attributed
to ordering rather than to the architecture, and the result cannot be
compared against published ordering work. For a project whose purpose is
falsifiable attribution, that is a severe cost.

This is the binding constraint. Where portability and a standard reference
architecture conflict, the standard architecture wins, and the portability
constraint is recorded as unmet rather than allowed to deviate the model.

## Sequencing objection

The project has not tested its central hypothesis. The first milestone is a
small ordering ablation, to which architecture portability contributes
nothing. Adopting the constraints above costs nothing because they are
restraint. Spending design effort on portability before the hypothesis is
tested would be optimising the wrong thing.

## The deployment target, answered 2026-09-23

The target is a **constrained embedded accelerator** as described in the
operational profile. This answers the question
this record previously left open, and changes the second activity rather
than removing it.

### The base model is unaffected

The fault environment constrains deployment, not training. The trained
artifact and the deployed artifact are different objects. The base model
stays standard, which preserves the comparability requirement above
intact.

### Size dominates architecture

The deployment compute and memory budget is orders of magnitude below
contemporary commercial parts. Whatever runs on such a device is a small
distilled student. This is a distillation problem, and no architectural
choice in the base model substitutes for it.

### Numeric format, verified 2026-09-23

Integer and fixed-point bit flips produce errors that are additive and
linear in bit position. Floating-point bit flips produce errors that are
multiplicative and exponential in the exponent bits, where a single
high-order exponent flip can turn a weight of 0.0001 into roughly ten to
the thirty-eighth. Error scaling is double-exponential in exponent width
against exponential in integer width, giving a strict resilience hierarchy
in which lower-precision integer formats are more robust. One reported
result narrowing the exponent to a four-bit-exponent custom format
achieved roughly a 5.8-fold robustness gain over FP16 or BF16 for a 0.23
percent accuracy cost.

**Consequence.** Integer or fixed-point is the correct deployment format,
for structural reasons rather than empirical ones. This is a quantisation
decision taken at deployment, not an architectural one.

### Training numerics, decided 2026-09-23

**Training is in floating point. Deployment is in integer arithmetic.
These are different formats for different reasons and the division is not
a compromise.**

Q-format is specifically unsuited to training, and its defining property
is the reason. Verified 2026-09-23, the fixed point format, with its
unique shared fixed exponent, is ill-suited to deep learning, because the
dynamic range of such formats is not sufficient to represent error
gradients during backpropagation. Activations, weights, and gradients
occupy very different ranges, and gradient ranges shrink as training
proceeds. Forward tensors want high resolution and narrow range while
backward gradients want wide range, and a single binary point cannot serve
both, nor serve early and late training at once.

The practical deployment format is therefore **dynamic fixed point**, also
called block floating point, meaning integer mantissas with several
scaling factors per tensor or per channel rather than one global binary
point. What is commonly called int8 quantisation is this, not Q-format.

### Fault profile, and why block floating point is the right answer twice

Combining the two findings above yields a better fault profile than either
extreme.

Block floating point concentrates all floating-point exponent into a small
number of scale factors. The bulk of the parameters become integers, whose
corruption is additive and linear. The scale factors are catastrophic if
corrupted, but they are few enough to protect heavily through
triplication, error correction, and scrubbing against a protected golden
copy.

This is strictly better than pure floating point, which is fragile
everywhere, and strictly better than pure Q-format, which is robust but
untrainable. **The principle is to concentrate the fragility where it can
be afforded protection.**

### Quantisation path

| Approach | Operates on | Deferrable |
| --- | --- | --- |
| Post-training quantisation | Pretrained model | Yes, indefinitely |
| Quantisation-aware fine-tuning | Pretrained model | Yes, indefinitely |
| Native low-bit training | From scratch | **No. Decide before pretraining** |

Quantisation-aware training simulates quantisation in the forward pass
with a straight-through estimator and computes in floating point
underneath. It is not fixed-point training and does not change this
record's division.

Native low-bit training is the sole exception and carries a deadline. See
open question fifteen.

### Constraints that gain a second justification

Three constraints adopted above for portability are now also fault-
behaviour constraints, and the fault argument is the stronger one.

- **No data-dependent control flow.** A corrupted value in a pure dataflow
  graph perturbs a number. A corrupted value reaching a branch changes
  which computation happens. Control-flow corruption is qualitatively
  worse than value corruption, being the difference between a degraded
  output and an arbitrary one.
- **Dense rather than mixture-of-experts.** This is now the strongest
  argument against routing. A corrupted activation reaching a router
  selects a wrong expert, which is control-flow corruption by another
  name.
- **Static shapes.** A fixed memory map is a precondition for periodic
  scrubbing against a protected golden copy, and for bounding the fault
  surface by static analysis rather than by testing.

### One new architectural lever, adopted

Design the base model to quantise cleanly to integer. Prefer components
that do not produce large activation outliers, since outliers force a wide
dynamic range and push deployment back toward floating point, which is the
format most to be avoided here. This costs nothing at training time and is
decided now or paid for later.

### The weakness, stated

The target does not exist, so its operator coverage and instruction set are
guesses. The mitigation is to constrain to the intersection of what any
plausible such device would support, and that intersection is a dense
transformer with integer arithmetic and static shapes. The uncertainty
about the target therefore costs nothing, because the safe assumption and
the portable assumption coincide.

Ground-up design work aimed at the hypothetical part is still not
warranted. The constraints above are restraint and are free. Design effort
is not, and the project's central hypothesis remains untested.

### Tension recorded

A foundation model aimed at scientific reasoning and a fault-tolerant
inference part sit at opposite ends of the compute spectrum by many orders
of magnitude. Train-large and deploy-small is the normal resolution, but
the project has no distillation track in scope, and the capability retained
after distillation to that size is an open empirical question rather than
an assumption. Recorded as open question thirteen.

## Sources consulted 2026-09-23

- Evaluating Single Event Upsets in Deep Neural Networks for Semantic
  Segmentation, https://arxiv.org/pdf/2412.03630
- Verification of Bit-Flip Attacks against Quantized Neural Networks,
  https://arxiv.org/pdf/2502.16286
- From Arithmetic to Logic, resilience under parameter bit-flips,
  https://arxiv.org/pdf/2603.22770
- Flexpoint, an adaptive numerical format for efficient training,
  https://arxiv.org/pdf/1711.02213
- Is Integer Arithmetic Enough for Deep Learning Training,
  https://arxiv.org/pdf/2207.08822
- 1.58-bit large language model overview,
  https://en.wikipedia.org/wiki/1.58-bit_large_language_model
- Training low-bit ternary models with Axolotl,
  https://huggingface.co/blog/axolotl-ai-co/finetuning-ternary-llms-tii-axolotl
