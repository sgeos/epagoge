# Are kernels intractable? No, and the question was the wrong shape

**Recorded 2026-09-27 after a literature spike, on operator direction.**
`../../evals/PRE_REGISTRATION.md` item 10 says "the exact tangent kernel is
intractable at scale" and defers the estimator. The operator asked whether
that is true, whether it is true only at scale, and noted that techniques
exist. **It is true of the matrix and false of everything this project
wants from it.**

Sources are vendored into ignored `tmp/references/papers/` under
`REFERENCE_SOURCES.md` and listed at the end.

## What is actually intractable

**Constructing the finite-width empirical kernel.** It requires order n
squared evaluations for n states, and existing applications build it and
then take a trace, or compute that trace through n matrix-vector products.
That is what makes published empirical-kernel work "confined to small
datasets and simple architectures".

**For a language model there is a second factor and it is larger.** The
empirical kernel carries the output dimension squared in both time and
memory, and the output dimension is the vocabulary. **At 2,279 tokens that
is a factor of about 5.2 million.**

## What is not intractable

**Every quantity this project wants is a trace, and traces are estimable
without forming the matrix.**

| Quantity | Expression |
| --- | --- |
| Frobenius norm | trace of K times K transpose |
| Alignment between two kernels | trace of the product, over the norms |
| **Effective rank** | **trace of K, squared, over the Frobenius norm squared** |

**Effective rank is the participation ratio**, and it is exactly the
quantity `JACOBIAN_SPACE.md` sets a floor on. It needs two traces and
nothing else.

**Both are estimable matrix-free by Hutch++**, with convergence guarantees.
Reported speedups are 10 to 100 times for a multilayer perceptron and 100
to 10,000 for a recurrent network.

**A one-sided estimator needs only one mode of automatic differentiation**,
forward or reverse, rather than both, and beats Hutch++ in the low-sample
regime when the gap between state count and parameter count is large.

**The vocabulary-squared factor has its own fix.** The pseudo-kernel
approximation removes it and converges to the empirical kernel at the rate
one over the square root of width, with the argument extended to
pretrained finite-width language models.

## What this means here, and it is not a small correction

**This project's models are 3.7 to 13.8 million parameters.** The scale at
which the exact kernel becomes intractable is far above them. **Item 10's
premise is inherited from the literature rather than measured on this
tree**, and it was written when the project planned 100M to 1B scale
points, which item 5 has since abandoned.

**So the estimator question is much easier than item 10 assumed.** What
still has to be fixed in advance, because choosing it after seeing a curve
is choosing the result:

1. **The estimator**: participation ratio from two Hutch++ traces, with the
   one-sided variant as the fallback where only one differentiation mode is
   available.
2. **The probe set**: fixed and identical across conditions, which item 10
   already requires.
3. **The probe-set size and the number of Hutch++ samples**, neither of
   which can be chosen by looking at the answer.

## What this does not settle

**Nothing here has been run.** This is a literature result about what is
computable, not a measurement on this tree, and the project has never
computed an effective rank of anything.

**The floor itself is unset.** `JACOBIAN_SPACE.md` makes effective rank an
architecture objective and names no number. A tractable estimator does not
supply the threshold.

**The speedups cited are for a perceptron and a recurrent network**, not a
transformer, and not at this vocabulary.

## Sources, fetched 2026-09-27

| File | Source |
| --- | --- |
| `ntk_trace_2511.10796.pdf` | `https://arxiv.org/abs/2511.10796` |
| `pntk_2206.12543.pdf` | `https://arxiv.org/abs/2206.12543` |

- Hazelden, *Fast Neural Tangent Kernel Alignment, Norm and Effective Rank
  via Trace Estimation*, 2025. Code at
  `https://github.com/meeree/kpflow/`.
- Mohamadi and others, *A Fast, Well-Founded Approximation to the Empirical
  Neural Tangent Kernel*, 2022.
