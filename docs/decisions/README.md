# Decisions

Decision records, and the open questions that block implementation.

## Records

- `LANGUAGE_CHOICE.md` decided. Python primary, Rust deferred to measured
  bottlenecks, PyTorch as the training framework.
- `CORPUS_TRACKING.md` decided. `corpus/` and `sources/` tracked.
- `PYTHON_VERSION.md` decided. Resolved by measurement on 2026-09-23.
  Python 3.14 is usable and the floor stays at 3.12.
- `PORTABLE_TRAINING_SPINE.md` decided. The framework is confined to the
  trainer and every surrounding artifact is neutral. Contract in
  `../architecture/TRAINING_SPINE.md`.
- `MODEL_ARCHITECTURE_CONSTRAINTS.md` provisional. Portability by
  restraint, with comparability outranking it. Integer quantisation and
  the absence of data-dependent control flow are fault-behaviour
  requirements rather than merely portability ones.
- The market assessment and the operational profile are
  internal records under the project's code-name convention.
- `JACOBIAN_SPACE.md` decided. Keeping Jacobian-space adequately
  unconstrained is an architecture objective, made enforceable through a
  tangent-kernel effective-rank floor. Supersedes an earlier version that
  treated it as instrumentation only and recorded a conflict as a
  convergence.
- `COLLABORATIVE_POSITIONING.md` decided. The model class is positioned as
  the falsifier and verifier specialist for recruitment into multi-agent
  groups. Positioning and interface only. Never a training objective.
- `LICENSING.md` decided. 0BSD for software, CC0 for corpus and
  documentation, third-party material under `sources/` excluded from both.
- `TRAINING_TECHNIQUES.md` decided. Maximal update parametrization, Muon,
  warmup-stable-decay, and multi-token prediction adopted. The first is
  confound removal rather than optimisation.
- `CORPUS_REGENERATION.md` decided. Frozen during the research phase,
  because regeneration by a trained model would make the corpus dependent
  on the treatment and the ablation circular.
- `PRE_COMMIT_AUDIT.md` recorded 2026-09-23. Adversarial audit of the
  design and tracked documentation. Three blocking findings, which gate
  work on the affected components but not the commit.
- `OPEN_QUESTIONS.md` **closed for pre-planning 2026-09-23.** Nineteen
  questions, fifteen answered and four deferred to the gated follow-on.
  None open.

## Convention

A decision that constrains later work is recorded before the work. Where a
decision was made against a stated objection, the objection is recorded
alongside it rather than dropped, so that a later reader can tell the
difference between a risk that was weighed and one that was never seen.
