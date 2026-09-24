# Changelog

All notable changes to this project are documented in this file.

The format follows Keep a Changelog, and the project adheres to Semantic
Versioning.

## [Unreleased]

### Added

- Project skeleton, repository initialisation, and directory layout.
- Decision records for language choice, interpreter version, corpus
  tracking, and the open specification questions.

### Added (continued)

- `docs/architecture/TRAINING_SPINE.md` and
  `docs/decisions/PORTABLE_TRAINING_SPINE.md`. The training framework is
  confined to the model definition and step function. Corpus, tokenizer,
  ordering index, checkpoints, metrics, and evaluation are neutral. A
  unified abstraction over PyTorch, JAX, and MLX was considered and
  rejected.
- `docs/decisions/MODEL_ARCHITECTURE_CONSTRAINTS.md`. Hardware portability
  adopted as restraint rather than as a design programme, with
  comparability against published work outranking it.

### Changed, 2026-09-23. Two-spine coverage structure

- Coverage now runs along two orthogonal axes, a subject spine and an
  epistemic-practice spine. The practice spine's members are domains whose
  content is the discipline itself, teaching how a conclusion follows, what
  can be known, where a representation applies, how something is
  established, and how one discovers one was wrong.
- **The practice spine is arguably the actual curriculum**, with subject
  content as the substrate it operates on. It also supplies a principled
  basis for weighting the two axes against each other.
- Three coverage additions, one of which corrected an omission of mine.
  Neither axis's contents are reproduced in tracked documentation.
- **Open question twenty added, gating corpus generation.** Coverage
  breadth now exceeds what the ablation token budget can support at the
  chosen model scales. An ordering ablation is confounded if the corpus is
  too thin for anything to be learned, since a null result would then be
  uninformative. Explicit proportions and a declared ablation subset are
  both required and neither exists. The concept graph and the variance
  pilot are unaffected.

### Added, 2026-09-23. Claim taxonomy and conditional-result records

- `docs/spec/CLAIM_TAXONOMY.md`. Every record is classified into exactly
  one of formal, empirical, attributed position, conditional result,
  normative, or unsupported. Classification precedes verification and
  determines which checks apply.
- The taxonomy is operational, about verification method, and asserts no
  metaphysics. A binary between the measurable-and-falsifiable and
  everything else was considered and withdrawn as too low-fidelity, since
  its residual category would have contained mathematics, definitions, and
  normative claims, and since a purely empirical demarcation criterion
  cannot satisfy itself.
- **Falsificationism is recorded in the specification as an attributed
  position, with Duhem and Quine, Lakatos, Kuhn, and Bayesian
  epistemology attributed alongside it.** It is retained as the worked
  example because it is the operator's own stated position, applied to the
  rule rather than exempted from it.
- **Conditional-result records added as a fourth record type**, carrying
  assumptions, method, and validation status. A simulated result is a
  derivation from assumptions rather than a measurement, and a record of
  the form "the model shows X" without those fields is rejected.
- Coverage extended. A model's domain of validity is the same object as
  the record schema's validity scope, so the domain teaches the project's
  epistemic discipline by example rather than only by assertion.

### Changed, 2026-09-23. Coverage extended, with two schema consequences

Coverage weighting extended. The manifest is not reproduced here.

- **Attributed-position records added as a third record type.** For
  interpretive and contested material the verifiable claim is that a named
  thinker held a position, not that the position is correct. A record
  asserting a contested claim as settled fact is rejected. Without this,
  coverage of interpretive domains would teach the model to assert
  contested claims confidently, which is the failure the project exists to
  prevent.
- **The residual error rate is reported per domain and never aggregated.**
  Verifiability varies enormously across the corpus, and a single number
  would average a machine-verifiable domain against an interpretive one and
  conceal both. This also improves the credential in the collaborative
  positioning record, since a per-domain breakdown is more useful to
  anything selecting on it.
- Coverage that raises the machine-verifiable fraction of the corpus is now
  preferred on verification grounds, independent of subject-matter value.

### Resolved, 2026-09-23. All three blocking audit findings

1. **Power.** The design is paired, sharing initialisation and data within
   a pair so order is the only difference, which was a free correction the
   original specification missed. Seed count and allocation are set by a
   variance pilot at the smallest scale rather than chosen, converting the
   central design parameter from assumption to measurement.
2. **Grounding.** Entailment is retained for terminal-stage literature and
   replaced for simplified content by a declared fidelity relation carrying
   the source claim, the simplification kind, the validity scope, and the
   supersession pointer. Good pedagogy uses known-false models that later
   stages correct, and no entailment rule can cover content whose purpose
   is to be superseded.
3. **Difficulty.** Defined structurally as prerequisite depth in a declared
   concept graph combined with supersession depth. No model assigns it, so
   the teacher cannot confound the treatment. The concept graph becomes the
   main deliverable, ahead of corpus generation.

Consequences. The corpus record schema gains five required fields. The
pre-registration scope gains the concept graph, the difficulty definition,
the curriculum specification, and a multiple-comparison correction
procedure. The three-scale allocation in question five is provisional.

### Added, 2026-09-23. Pre-commit adversarial audit

- `docs/decisions/PRE_COMMIT_AUDIT.md`. Eleven findings, three blocking.
- **Blocking.** The ablation is underpowered, detecting only effects of
  1.77 sigma of seed variance at five seeds per condition, against a
  literature reporting small effects and a criterion that treats an
  inconclusive result as failure.
- **Blocking.** Source grounding as specified forbids pedagogical
  simplification, which is the curriculum's defining feature.
- **Blocking.** Difficulty, the independent variable, is nowhere defined,
  and is absent from the pre-registration scope. If assigned by the teacher
  model it becomes an uncontrolled confound.
- Budget arithmetic recorded. Roughly $9,400 for the ablation and pilot
  alone, excluding corpus generation, audit, instrumentation, and time.
- Recorded that nineteen cited papers were cited from search summaries
  rather than read, which fails the project's own standard.

### Added, 2026-09-23. Collaborative-group positioning

- `docs/decisions/COLLABORATIVE_POSITIONING.md`. The model class is
  positioned as the falsifier and verifier specialist, for recruitment into
  multi-agent groups through capability-advertisement protocols.
- Recorded as repositioning rather than new direction. The properties that
  make the model attractive for recruitment are the ones already decided
  for other reasons, and the mapping is close to one-to-one.
- The audited residual error rate gains a second role as the recruitment
  credential, since an orchestrator can select on a number.
- **Guard.** Never train toward being selected. Current orchestrators
  favour agreeableness, so optimising for selection would destroy the
  property the model exists to have. Positioning may change the capability
  advertisement, the output schema, and the documentation. It may not
  change the loss.
- Input from collaborating agents is untrusted by the same standard already
  applied to teacher-model output.

### Added, 2026-09-23. Jacobian-space as an architecture objective

- `docs/decisions/JACOBIAN_SPACE.md`. Maintaining healthy reasoning
  ability through an adequately unconstrained Jacobian-space is an
  architecture objective, not merely instrumentation.
- Made enforceable through a tangent-kernel effective-rank floor, declared
  in the pre-registration and measured, rather than left as a preference.
- Fault tolerance assigned to hardware, namely error correction on weight
  memory, scrubbing against a protected copy, and triplication of the small
  high-precision core. Not to flattening the model.
- Low-rank parameterisation banned outright in the base model, since it
  constrains the Jacobian to a low-rank subspace by construction.
- Quantisation pilot's primary measurement is effective rank against the
  floor rather than the accuracy gap. Same three runs, better question.
- Generates a testable regime hypothesis. If ordering acts by shaping the
  tangent kernel it can help only in the feature-learning regime, whose
  position depends on width and learning rate, which predicts the effect
  varies across the three chosen scale points and would explain the
  inconsistency of the published literature.
- Instrumentation in the primary arms is measurement only. Regularisation
  would confound the pre-registered ablation and belongs in a separate arm.
- **Correction made while drafting, recorded because the error is
  instructive.** An earlier draft held that Jacobian awareness served both
  the ordering mechanism and weight-perturbation tolerance, and called that
  a convergence. It is a conflict. Fault tolerance wants low sensitivity of
  the function to parameter change. Reasoning wants that sensitivity to
  stay rich. The reasoning side wins, and the literature supports it, since
  flatness is not a reliable good.

### Names fixed, 2026-09-23

- `epagoge` names the repository and the corpus project.
- `sporos` names the model.
- `elenchos` names the anti-sycophancy evaluation suite.

A tracked document may gloss what a name means. It may not state why a name
was chosen.

### Deployment material separated, 2026-09-23

Performed before the initial commit, so no history contains the material.

- Positioning records separated from tracked documentation and given code
  names under the project's naming convention.
- The market assessment moved out of `docs/decisions/` for the same reason.
- Tracked documents state generic engineering constraints only. Omission
  only. No tracked statement was made false.
- Standing rule recorded in `CLAUDE.md`.

### Pre-planning closed, 2026-09-23

All nineteen open questions resolved. Fifteen answered, four deferred to
the gated follow-on, none left open.

Decisions taken in this pass.

1. **Scope.** Research first, product gated. The deliverable is the corpus,
   the curriculum specification, and the ordering ablation. A deployable
   model is a follow-on funded on the ablation result.
2. **Verification.** Layered, with a measured residual error rate from
   sampled expert audit. Source grounding is the floor, executable checks
   where the domain permits, consensus as a filter only.
3. **Application boundary.** Weapons-development material is out of
   scope. Recorded rather than assumed.
4. **Falsification.** Pre-registration, with inconclusiveness as the
   failure condition. A negative result is a deliverable.
5. **Scale.** From random initialisation at three scale points, roughly
   100M, 300M, and 1B parameters, five seeds per condition.
7. **Topic basis.** Coverage derived from the operational
   profile, replacing an earlier framing that rested on an unfalsifiable
   objective.
8. **Sycophancy.** Corpus carries positive examples of evidence-conditioned
   revision plus avoidance of approval-seeking patterns, with an elenchos
   baseline measured on the ablation models.
9. **Interoperability.** A structured output schema, not a model. Removes
   an artifact and dissolves the original concern.
10. **Framework.** PyTorch, now that the hardware path is small rented
    NVIDIA runs.
17. **Use case.** An agentic model with sensor and instrument inputs access,
    reasoning autonomously and reporting over a [redacted constraint].
19. **Galactica.** Answered by the measured error rate in decision two.

Deferred to the follow-on. Distillation, native low-bit training, bounded
attention and context length, and agentic reliability at deployment scale.

### Added (current)

- the market assessment. Feasibility and market
  distinctness assessed at the close of pre-planning.
- Deployment use case recorded as answered. An agentic model with vision
  and instrument data access, reasoning autonomously and reporting over a
  [redacted constraint].
- Open question nineteen added. An explicit answer is required for why this
  does not repeat Galactica, which failed on this project's exact claimed
  differentiator.
- Open question eighteen added. Agentic reliability is scale-dependent
  while the deployment envelope wants a small model.
- Corrected the deployment hardware assumption. Flight-validated edge AI
  silicon at sixty trillion operations per second in eight watts exists,
  so earlier size-severity arguments are weaker than recorded.

### Added (latest)

- `docs/architecture/MODEL_ARCHITECTURE.md`. The ablation model is fully
  standard for comparability. The deployment model adds bounded attention,
  which converts key-value cache from growing with sequence length into a
  statically bounded quantity.
- Mixture of experts closed rather than merely rejected. Its bargain
  spends memory to buy compute, which inverts this project's binding
  constraint, and this is independent of the existing control-flow
  objection.
- State space and linear attention hybrids rejected on a
  fault-environment-specific ground. Recurrent state is a cumulative persistent
  fault surface where key-value cache corruption is bounded in blast
  radius.
- Open question sixteen added. The window size and the number of
  full-attention layers cannot be chosen until the deployment task's
  context requirement is known, which inherits from question one.

### Changed (current)

- Pilot in open question fifteen revised from two arms to three. Floating
  point, four-bit, and ternary. The k-bit inference scaling law work places
  the optimum at four bits with a sharp decline below three, so the
  two-arm design would have tested only the endpoints and missed the
  frontier.
- Design rule added. Prefer width with grouped-query attention over depth
  when scaling to compensate for low-bit degradation, because cache grows
  with depth and cache is the workspace the low-bit weights were meant to
  free.
- Recorded that BitNet already keeps embeddings, normalisation, the output
  head, and activations above ternary, so selective precision is part of
  the approach rather than an additional lever.

### Changed (latest)

- Ablation model and deployment model separated as distinct artifacts. The
  ablation subject is standard and floating point for comparability. The
  deployment artifact is free to be ternary.
- **Correction.** The deadline recorded against open question fifteen was
  an artifact of assuming a single model would serve both purposes. That
  assumption was not stated by the operator. Decoupling dissolves the
  deadline. The erroneous entry is retained in place so the error stays
  visible.
- Ternary evidence review recorded, with the qualification that most
  negative evidence concerns post-training quantization rather than native
  low-bit training and therefore does not refute the proposal.
- A pilot specified to replace the decision. Train the same small
  architecture twice at target scale, floating point and ternary, and
  measure the gap with reasoning separated from fluency.

### Changed (most recent)

- Training and deployment numerics divided explicitly. Training is
  floating point. Deployment is integer arithmetic in block floating
  point form. Q-format is recorded as unsuited to training because its
  single shared exponent cannot span gradient dynamic range.
- Keleusma recorded as a separate effort with plausible future
  convergence, which the deployment track may not assume.
- Open question fifteen added. Native low-bit training is the only
  quantisation decision that cannot be deferred past pretraining.

### Changed (continued)

- `docs/decisions/MODEL_ARCHITECTURE_CONSTRAINTS.md` extended with the
  fault-tolerant deployment target. Verified that integer and
  fixed-point bit-flip errors are additive and linear in bit position
  while floating-point errors are multiplicative and exponential in the
  exponent, which makes integer quantisation a structural requirement for
  that target rather than a preference. Open questions thirteen and
  fourteen added for the distillation track and for the relationship to
  existing statically bounded execution work.

### Changed

- `docs/decisions/LANGUAGE_CHOICE.md` split into two decisions. Python
  remains settled. The training framework is demoted from settled to open,
  because the original PyTorch assertion was not the product of a
  comparison. A decision rule keyed to the hardware path replaces it.
- `docs/decisions/PYTHON_VERSION.md` resolved by measurement against the
  Python Package Index. Torch 2.14.0 and jaxlib 0.11.2 both publish cp314
  wheels, so Python 3.14 is not a blocker and the first-dependency block is
  lifted.

### Notes

- No corpus data exists. No curriculum stage has been specified. No model
  has been trained.
- Verified 2026-09-23 against upstream documentation. Levanter's bitwise
  determinism guarantee is scoped to Tensor Processing Units and does not
  extend to graphics processing units. PyTorch does not guarantee complete
  reproducibility across releases, commits, or platforms. The ordering
  ablation consequently requires multiple seeds per condition, recorded as
  open question eleven.
