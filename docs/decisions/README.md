# Decisions

Decision records, and the open questions that block implementation.

## Records

- `LANGUAGE_CHOICE.md` decided. Python primary, Rust deferred to measured
  bottlenecks, PyTorch as the training framework.
- `CORPUS_TRACKING.md` decided, then amended 2026-09-24. `sources/` is
  tracked. `corpus/` is not, since it became a derived stream rebuilt
  from the books rather than the authored artifact.
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
- `PROCESS_REVIEW.md` decided. What was taken from the reference
  repository's process and what was rejected, with grounds. The durable
  outcome is `../process/PROCESS_STRATEGY.md`.
- `BOOK_ATTRIBUTION.md` decided. A book's `author` is the project, its
  `licence` is CC0-1.0, and its two dates are derived from version
  history rather than written. Names what was rejected and why.
- `COMBINATORIAL_RICHNESS.md` decided. Repetition should make new concept
  combinations rather than repeat old ones. The corpus realised 109 of
  7,626 possible pairs and every partner was a unit-mate.
- `CURRICULUM_LITERATURE.md` recorded. A literature spike on curriculum and
  spiral training. The corpus-quality half of the thesis is well supported;
  the ordering half is weakly supported and contradicted three times. Names
  a confound in the planned ablation that would have invalidated it.
- `RECURSIVE_DRAFTING.md` recorded. Level one needs a backport built on
  level-two concepts, so the levels cannot be drafted in order. Corrects
  THREE_PROBLEMS.md on where coverage and consistency bind.
- `REFERENCE_SOURCES.md` decided. WordNet for irregular inflection and
  Moby for synonymy, fetched into ignored `tmp/references/` rather than
  vendored, with links and checksums so independent work can follow.
- `WHOLESOMENESS.md` decided. Wholesome age-appropriateness is an
  acceptance criterion. Not mechanically checkable, so it lives in the
  generation prompt, the lexicon, and review.
- `UNUSED_FORMS.md` decided. A judgement on every unused surface form at
  level one. Seven culled as not English, four headwords left to the
  operator, and two defects found in the lexicon model itself.
- `TRAINING_ADVANCES.md` recorded. A spike on state-of-the-art training and
  architecture. Names this project's regime as data-constrained and
  compute-abundant, which is what makes the literature searchable, and finds
  that the weight-decay recommendation is conditional on overfitting being
  present. Says what does not transfer and why.
- `STRUCTURAL_TOKENS.md` decided. An end-of-text token, packing rather than
  padding, and reserved slots. The measured claim that moves this project is
  that a structural announcement changes what a reader predicts while its
  notation does not, so the marker must exist and its spelling is free.
- `ETIQUETTE.md` recorded. Salutations and valedictions belong in
  `institutional_interfacing` as the register its four moves are performed
  in. Names the bound that keeps it from becoming general social skills, and
  leaves the level and the words to the operator.
- `KERNEL_TRACTABILITY.md` recorded. The tangent kernel matrix is
  intractable and every quantity this project wants from it is a trace, so
  effective rank is estimable matrix-free. Corrects a premise item 10
  inherited from the literature rather than measured.
- `FIELD_ENUMERATION.md` recorded. Four instances of a record built from a
  subset of its own dataclass's fields, three in the book code and one in
  the checkpoint code. Classifies which omissions fail loudly and which
  rebuild a different model in silence.
- `LICENSING.md` decided. 0BSD for software, CC0 for corpus and
  documentation, third-party material under `sources/` excluded from both.
- `TRAINING_TECHNIQUES.md` decided. Maximal update parametrization, Muon,
  warmup-stable-decay, and multi-token prediction adopted. The first is
  confound removal rather than optimisation.
- `CORPUS_REGENERATION.md` decided. Frozen during the research phase,
  because regeneration by a trained model would make the corpus dependent
  on the treatment and the ablation circular.
- `PRIMITIVE_REGISTER.md` decided. Level one grounds in a hand-authored
  register of civilisational axioms rather than in citations. A generator
  may write records that teach them and may not extend the register.
- `PRE_COMMIT_AUDIT.md` recorded 2026-09-23. Adversarial audit of the
  design and tracked documentation. Three blocking findings, which gate
  work on the affected components but not the commit.
- `OPEN_QUESTIONS.md` **closed for pre-planning 2026-09-23.** Nineteen
  questions, fifteen answered and four deferred to the gated follow-on.
  None open.
- `LEVEL_CALIBRATION.md` decided 2026-09-25. Each level is the grade a
  reader is ready to enter, from kindergarten at level one to
  post-graduate practice at level seven. Fixes page counts by binding and
  leaves concept complexity uncalibrated.
- `LEVEL_ONE_CONCEPTS.md` recorded 2026-09-25. The fifty-one level-one
  concepts the schedule planned and the graph lacked, with their domains
  and prerequisites. Unblocks the forty-three units that could not be
  authored, and does not author them.
- `READING_LEVEL_RESEARCH.md` recorded 2026-09-25. Vocabulary size and
  book length by age, with sources. The vocabulary estimates are contested
  by more than an order of magnitude and the file says so.
- `BACKPORT.md` recorded 2026-09-25. Backporting level-two concepts into
  level-one picture books. Three of four blockers were lexicon defects
  rather than conceptual barriers.
- `THREE_PROBLEMS.md` recorded 2026-09-25, operator framing. Level one is
  a bootstrapping problem, levels two to six a scheduling problem, and
  level seven a transition from an idealised synthetic corpus to real
  material. Different shapes, different failure modes, different
  definitions of done.
- `CORPUS_THESIS.md` recorded 2026-09-25, operator statement. Garbage in
  produces garbage out; the project rejects volume as the universal
  answer. Also records that level N training starts from the level N minus
  one model, so the level-one model is an initialisation rather than a
  demonstration.
- `LEXICON_SOURCING.md` recorded 2026-09-25. The pipeline for taking the
  level-two lexicon to about ten thousand words: seed from three lists,
  scan public-domain and CC0 sources, accept the frequent in bulk, inspect
  the per-source long tail. Frequency is per source rather than pooled,
  and provenance is recorded at admission.
- `POST_FACTO_ANALYSIS.md` recorded 2026-09-25. What the project keeps so
  that "why is this word here" can be answered later. Most of the lexicon
  predates any such field, so its provenance is reconstructed from git
  history and labelled as reconstructed rather than invented.

## Convention

A decision that constrains later work is recorded before the work. Where a
decision was made against a stated objection, the objection is recorded
alongside it rather than dropped, so that a later reader can tell the
difference between a risk that was weighed and one that was never seen.
