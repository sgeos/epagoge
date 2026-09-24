# AGENTS.md

Guidance for automated agents working in this repository.

The authoritative instructions live in [`CLAUDE.md`](CLAUDE.md). Read that
file first. It is agent-agnostic in content despite its name.

## Summary of the obligations that matter most here

- The curriculum-ordering benefit is a hypothesis under test, never a
  premise. A flat-order control is required before attributing any gain to
  ordering.
- Disagreeableness is not a proxy for correctness. The target property is
  evidence-conditioned assent.
- Teacher-model output is untrusted input. Validate at the generator
  boundary and reject loudly.
- Run-to-run determinism is not available on graphics processing units
  under either candidate framework. The ordering ablation needs multiple
  seeds per condition and a declared effect threshold. A single-run
  comparison establishes nothing.
- The training framework is undecided. Do not assert PyTorch or JAX as
  chosen.
- Unmeasured claims are marked as unmeasured, in the same sentence.
- The specification is incomplete. See
  [`docs/decisions/OPEN_QUESTIONS.md`](docs/decisions/OPEN_QUESTIONS.md)
  before writing pipeline code.
