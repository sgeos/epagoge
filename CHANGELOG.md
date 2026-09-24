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

## 2026-09-24

### Added. Accounting, and a handoff protocol

- Accounting placed as a measurement discipline rather than applied
  economics. Five concepts and two formal structures. It had to earn its
  place by producing a derived transfer edge and did: balance and
  conservation of number both instantiate conservation.
- `docs/process/HANDOFF.md`, adapted from the protocol in the operator's
  Keleusma project. Validity is checked by ancestry and by content, never
  by a hash match, and the content checks are cheap and independent.
- The handoff separates what a resuming session should do, what the
  operator holds, what stays unstarted and why, and the method rules that
  were expensive to learn. History accumulates below a line and is never
  edited.

### Changed. Communication added, vocabulary fully mapped

- **Communication added as a domain**, closing the gap the curriculum
  coverage test found. Five concepts covering knowing, explanation,
  reporting, and a claim under test.
- **All 131 unmapped words now carry a concept.** Completeness moved from
  8.4 percent to 100. The graph grew from 45 to 71 nodes across four
  domains, and every record now lists the concepts its words touch, which
  is what produces the cross-domain links.
- **The mathematics against failure-analysis depth contrast survives** at 10
  against 6, which the ablation design depends on.
- **A third correction to the vocabulary design, and the validator found
  this one too.** Term levels were derived from the concept. That is wrong,
  because a concept can be taught before its name is introduced. The
  level-one causation record never uses the word "cause", and children grasp
  causation long before they say it. Deriving equality admitted thirty-three
  words at levels where nothing used them.
- A term's level is now **authored**, with the graph supplying a lower bound
  only: a word may not precede the concept it names. Placement above that
  bound is a scheduling decision, which is what the kanji schedule is.
- History and accounting recorded as further additions, with accounting
  earning its place chiefly through a transfer edge, since mass and energy
  balance in a closed loop is accounting and double-entry bookkeeping is
  conservation expressed as a procedure.
- **Drafting a sensible curriculum remains open and non-trivial.** The
  schedule now has somewhere to live, and nothing has scheduled it.

### Changed. The unmapped tier is a measure, not a category

- **A correction to a correction.** General vocabulary was introduced as a
  permanent third category on the model of Basic English. That was wrong. A
  content word names something, so a word mapping to nothing means the
  mapping was not identified or a concept is missing from the graph.
- The tier is a holding pen for unfinished work and its size measures graph
  incompleteness. `completeness` reports the fraction of content words
  carrying a concept. **It currently stands at 8.4 percent**, with 131 words
  awaiting a concept against 12 that have one.
- **`vocabulary_limited` added as a simplification kind.** Distinct from a
  superseded model, which is wrong. A vocabulary-limited record is not
  wrong; it is as accurate as the admitted words allow. Recording which is
  which lets a reader tell a simplification from an error. The fidelity loss
  is accepted rather than apologised for, provided it is labelled and its
  correction named.
- **A coverage test method recorded.** A manifest derived from a deployment
  profile can be checked against a real curriculum in the domain, and gaps
  appear as subjects with no home. Applied once, it found that communication
  coverage was absent while the stated deployment rationale depends on
  reporting over a constrained channel, which was an inconsistency rather
  than merely an omission.

### Added. Relation coverage, and two corrections

- **A specialisation asserted in the graph must be taught in the corpus.**
  Enforced by a new rule. A graph that says a teddy bear is a toy, with no
  record teaching it, asserts a link the model never reads.
- **The asymmetry is the part that must be taught.** A teddy bear is a toy
  and a toy is not necessarily a teddy bear, which is the same structure as
  a square being a rectangle while a rectangle need not be a square. An edge
  records the direction. Only content can teach that the converse fails.
- **Correction. Transfer does occur at level one.** An earlier note held
  that no level-one transfer edges was right, since transfer requires
  abstraction. Teddy-bear-is-a-toy and square-is-a-rectangle instantiate the
  same formal structure, proper class inclusion, which is a cross-domain
  transfer edge between an everyday concept and a mathematical one. The
  existing machinery derives it without modification, and this is how
  children acquire classification.
- **Correction. The teddy bear was not a useless anchor.** It scored zero
  only because its edges were not drawn. Teddy bear to toy to proxy model to
  representation to simulation gives it four, and enters the modelling
  spine. The general lesson is uncomfortable: a low anchor-reach score may
  mean a concept is not worth teaching or may mean the graph is incomplete,
  and the metric cannot tell them apart.

### Added. Enabling concepts, and the metric that measures them

- `docs/spec/ENABLING_CONCEPTS.md`, a `specialises` edge type, and two
  reach metrics.
- **Level placement is a scheduling problem, not only a dependency one.**
  Japanese education assigns kanji to grades, and some appear where they do
  because they must be introduced somewhere and that level had room.
  Prerequisites say what cannot come before what. They do not say where
  anything should go among the orderings that satisfy them. Capacity per
  level and completion by the end are both unmodelled and are recorded as
  the shape the assignment should take.
- **A concept with no use at a low level can be an enabling concept for a
  high one.** A crayon is paraffin wax, paraffin wax is a lightweight
  hydrocarbon, and paraffin hybrids have flown. Verified: Stanford and
  Lockheed Martin in 2003 to 4,600 metres, a Stanford student vehicle to
  2,871 metres in 2004, with regression rates three to four times HTPB.
- **The divergence from human pedagogy this exposes.** A human curriculum
  introduces crayons because children use crayons. A model has no life, so a
  concrete concept earns level one only as the cheapest anchor for a chain
  that matters later. Selecting by what a child finds familiar would fill
  level one with objects that anchor nothing.
- **A correction made while building.** The first metric counted what
  depends on a concept, which is the wrong direction for an anchor. An
  anchor is a leaf, so a crayon scored zero alongside a teddy bear.
  `anchor_reach` follows specialisation forward to the abstractions a
  concept instantiates and counts what rests on those. In the worked example
  a crayon anchors six concepts and a teddy bear none.
- A `specialises` edge is distinct from the two already present. A crayon
  does not require paraffin wax and shares no formal structure with it. It
  is one.

### Added. Per-level vocabulary, with a correction to my own design

- `docs/spec/VOCABULARY.md`, `src/epagoge/vocabulary.py`, and
  `curriculum/vocabulary.json`. Levels one to six are bounded; level seven
  is unrestricted.
- **Two rules.** A record uses no word admitted above its level. And every
  word admitted at a level appears in at least one record at that level,
  so admitting a word is a commitment to teach it rather than an
  aspiration.
- **The strongest reason for this is not simplicity.** It makes level
  assignment mechanically checkable, which was the design's weakest point.
  A level was authored with only prerequisite coverage constraining it, so
  a disagreement about whether a record sat at level three or four had
  nothing to appeal to.
- **A correction.** I claimed the vocabulary could be derived wholly from
  the concept graph. That was wrong, and the validator is what showed it.
  Most content words name no concept, and forcing a licence on them
  assigned twenty-four words to levels where they never appeared. General
  vocabulary is authored in tiers as Basic English and the Dolch lists are.
  Derivation applies to the technical terms, where drift would do damage.
- A word qualifies as a derived term only if it is actually used at its
  concept's level. A word that merely resembles a concept name is ordinary
  vocabulary.
- **The limit, stated so it is not over-relied on.** The check is lexical.
  It would not have caught this morning's wear-versus-break error, since
  "broken" is unambiguously level-one vocabulary. Vocabulary constrains how
  simply a thing is said and says nothing about whether it is right.
- Prior art recorded. TinyStories constrained generation to a roughly
  fifteen-hundred-word lexicon and produced coherent English from
  three-million-parameter models.

### Added. Teacher model pulled, and a generator requirement it revealed

- `qwen3:30b-a3b-instruct-2507-q4_K_M` pulled and verified. Apache 2.0
  confirmed from the shipped licence, 18 GB on disk, 21 GB resident,
  entirely on GPU, roughly fifty tokens per second warm.
- Text-only rather than vision, since corpus generation uses no vision.
  Instruct rather than thinking, since reasoning traces are wasted tokens.
- Generation budget revised down. One million tokens is about five and a
  half hours single-stream rather than eight, so level one is a few hours
  to a day rather than up to eighty hours.
- **The first two prompts established a generator requirement.** Asked to
  teach that repeated use wears things out, the model returned two
  sentences in three about things breaking and chains snapping, which is
  sudden failure and a concept the graph deliberately separates from wear.
  Adding one negative constraint produced three correct sentences in three.
- **A generation prompt must therefore carry the concept, its grounding
  primitive and observation, and its nearest graph neighbours as explicit
  exclusions.** The graph already holds the neighbours, so the exclusions
  are derived rather than authored. Without this the generator produces
  fluent text that blurs exactly the distinctions the curriculum exists to
  draw, while passing schema validation and reading well.

### Added. Level-one graph coverage, and the review tool

- Concept graph expanded from 33 to 45 nodes with a level-one layer in both
  domains. `seed.json` renamed to `concepts.json`, since it is no longer a
  seed.
- **The prerequisite-depth contrast sharpened** from 7 against 5 to 10
  against 6, and the two domains are **independent subgraphs with no
  cross-domain prerequisites**, so the contrast the ablation rests on is not
  muddied by shared ancestry.
- `src/epagoge/review.py` and `tools/review.py`. **This is the sampled
  expert audit, not only a reading aid.** Its output is the measured
  residual error rate the quality claim rests on.
- Three verdicts rather than two. A flag is counted separately and never
  folded silently into accept or reject.
- **Rates are per domain and carry Wilson score intervals.** Three
  rejections in thirty records is ten percent with an interval from 3.5 to
  25.6 percent, so quoting the point estimate would present as a
  measurement something the audit did not establish. Even zero rejections
  in thirty bounds the rate below about eleven percent, not below zero.
- Where a record cites a primitive, the grounding observation is displayed
  inline, so a claim can be checked against what grounds it without leaving
  the screen.
- Six hand-written level-one records added, teaching the concepts the
  expanded graph requires. The corpus validator found each gap in turn.

### Added. Primitive register, which unblocks level one

- **A problem raised in discussion and never written down until now.**
  Level one breaks the grounding rule. Every record needs a resolvable
  source, but level one seeds civilisational axioms, and there is no
  citation for "things break" or "living things die". A generator facing
  that has three options and two are bad: fail validation, fabricate a
  citation, or find an honest home for axioms. Level one is therefore the
  hardest case for the verification layer rather than the easiest.
- `docs/decisions/PRIMITIVE_REGISTER.md` and `curriculum/primitives.json`.
  Level-one records ground in a hand-authored register of thirty-four
  axioms, each carrying the observation that grounds it, cited through a
  `primitive:` prefix. **The grounding rule is unchanged**; only the kind of
  source is new.
- **The load-bearing rule is that a generator may write records teaching a
  primitive but may not add to the register.** The register is small and
  everything above it inherits its errors, so it is hand-authored and
  reviewed, which puts human attention at the foundation rather than spread
  thinly across millions of generated records.
- The guard works as intended. A record citing
  `primitive:hard-work-brings-success`, a contested normative claim wearing
  a primitive's clothes, is rejected by name.
- Training to level one recorded as a pipeline validation rather than a
  model deliverable, since a model trained on picture-book content will be
  poor by construction and judging it as a model would support a wrong
  conclusion.
- Byte-level tokenisation chosen for level one. No dependency, no
  tokeniser-training step, and the spine already treats tokenisation as a
  neutral artifact so changing it later is contained.

### Added. Training techniques, teacher runtime, and corpus regeneration

- `docs/decisions/TRAINING_TECHNIQUES.md`. Maximal update parametrization,
  Muon, warmup-stable-decay, and multi-token prediction adopted. FP8 when
  the hardware supports it.
- **Maximal update parametrization is confound removal, not
  optimisation.** Without it the three scale points have different optimal
  hyperparameters, so any scale-dependence in the ordering effect could be
  an artifact of mis-tuning. That lands on the project's own mechanism,
  which holds that regime position depends on width and learning rate.
- Multi-head latent attention flagged rather than adopted. It is a low-rank
  projection, which the Jacobian-space objective bans in the base model, so
  it must be measured against the effective-rank floor rather than taken on
  its efficiency merits.
- **The pilot's variance numbers do not carry over.** Changing optimiser
  and schedule changes the dynamics, so sigma and rho must be re-measured.
- **The teacher runs locally, and the reason is disclosure rather than
  licensing or cost.** Generation prompts encode the coverage manifest, so
  any hosted interface transmits the withheld artifact. A weight licence
  also does not govern a hosted endpoint, which carries its own terms.
  Hosted generation would have cost between fifty cents and five dollars
  for the whole of level one, so price was never the constraint.
- `docs/decisions/CORPUS_REGENERATION.md`. **The corpus is frozen during
  the research phase**, because regeneration by a model trained on it would
  make the corpus dependent on the treatment and the ablation circular.
- Downward regeneration has a sound form and an unsound one. The student
  here is weaker than the teacher, not stronger, so a student rewriting the
  teacher's work is a novice revising an expert. The sound form separates
  the roles: the student measures which records helped, by attribution, and
  the teacher regenerates. Accumulating rather than replacing, since the
  replace paradigm collapses on even small synthetic contamination.
- Lateral regeneration introduces no new information and narrows coverage.
  A verifier makes it survivable as rejection sampling, but it breaks
  provenance, which is the project's strongest differentiator.

### Added. Variance pilot, run and measured

- `src/epagoge/variance.py` and `src/epagoge/pilot.py`, with
  `tools/run_pilot.py`. The analysis is standard library only and verified
  against closed-form cases and by recovering known parameters from
  synthetic data. Torch is an optional `train` extra, so the core stays
  dependency-free.
- **Measured single-epoch.** Unpaired sigma 0.0750, paired sd 0.0233,
  correlation 0.954, pairing gain 20.7x seeds at no cost. Twelve paired
  seeds beat two hundred and forty-six unpaired ones, so the original
  five-seed unpaired design was off by two orders of magnitude in
  efficiency rather than merely underpowered.
- **The first pilot was wrong in an instructive way.** It trained about
  twenty-three epochs, where ordering effects necessarily wash out, which
  inflated the correlation from 0.954 to 0.987 and would have understated
  the required seed count threefold. Both results are retained, because the
  difference between them is the finding.
- **Two harness defects found by running it.** A vocabulary of 256 gave a
  second-order source 65,536 contexts over 200,000 tokens, so nothing was
  learnable and every ordering produced an identical result. And warmup
  with no decay left the rate at peak forever, making four thousand steps
  converge worse than two thousand.
- **A null arm is added to the ablation.** The pilot found a systematic
  difference between two orderings that should be equivalent, with the sign
  following the ordering rather than the execution position, marginal at
  about p = 0.04 and unexplained. That is the shape of a false positive, so
  the ablation now compares two random topological orderings against each
  other, and the curriculum effect must exceed that null rather than merely
  exceeding zero.
- **Nondeterminism floor measured.** Identical inputs differed by 0.00075
  on Metal Performance Shaders, bounding the smallest resolvable effect on
  that hardware regardless of seed count.
- Pre-registration items two and six move from pending to fixed and
  measured. Six items remain pending.

### Added. Gate completed, and four gaps closed

Found by checking rather than by recalling.

- **The disclosure scan was enforced by nothing.** `tools/scrub_scan.sh`
  now runs in the gate. Its pattern lives in `secret/`,
  because a tracked list of withheld vocabulary would publish the thing
  being withheld, and absent the pattern it skips loudly rather than
  passing silently. It is word-anchored, since an unanchored pattern
  matched `ore` inside `before` on 2026-09-23 and produced noise that
  would have looked identical to a clean result.
- **The gate resolved `@latest` and was therefore not reproducible.** Tool
  versions are pinned. A gate that can fail tomorrow for reasons unrelated
  to the code is not a property this project should accept in its own
  process.
- **No continuous integration existed.** `.github/workflows/check.yml`
  added, with its one limitation documented rather than left implicit.
- **Coverage had never been measured.** It was 94 percent. Nine tests were
  added for the untested paths, raising it to 99, and a floor of 95 is now
  enforced.
- The `normative` claim class was never exercised by the sample corpus.
  Adding a record for it exposed two genuine prerequisite gaps, which the
  corpus validator caught and which were closed by teaching the missing
  concepts rather than by deleting the record that revealed them.
- Status lines in `README.md` and `CLAUDE.md` still said nothing was
  implemented.

### Changed. Licensing decided

- **0BSD for software, CC0 1.0 for corpus and documentation.** Supersedes
  the MIT declaration in `pyproject.toml`, which was an unsurfaced default
  rather than a decision.
- The split is not a compromise. Creative Commons recommends against CC0
  for software because it does not address patent rights, and 0BSD is the
  software equivalent of the same intent without MIT's notice requirement.
- **CC0 suits a synthetic corpus for a specific reason.** The copyright
  status of machine-generated content is unsettled, so the project may hold
  no rights to license conventionally. CC0 dedicates whatever rights exist
  with a fallback permissive licence, and therefore does not depend on the
  answer. A conventional licence would assert a right that may not exist,
  which is an unsupported claim in a repository meant to suppress them.
- **`sources/` is excluded from both**, in `LICENSE` itself and not only in
  the decision record, since a reader checks the licence file. Third-party
  terms are not the project's to grant.
- Open question twenty-five added. A terminal-stage record that restates
  third-party literature is neither purely machine-generated nor a
  reproduction, and whether it can be CC0 is unresolved.

### Added, 2026-09-23. Record schema, level mechanism, pre-registration, teacher decided

**Record schema.** `docs/spec/RECORD_SCHEMA.md` and
`src/epagoge/record.py`. The single authoritative definition, replacing
fields described across three prose documents. Twelve rules enforced, nine
per record and three across the corpus. Thirty-six tests, weighted to
negative cases. A worked sample corpus exercises every claim class and a
simplification chain, and `tools/validate_corpus.py` gates it.

**The level-assignment mechanism existed only as prose and now exists.**
Levels are authored rather than derived, because the seven levels carry
breadth, abstraction, and groundedness that prerequisite depth cannot
express. Rule twelve keeps an authored level honest. For every concept, the
earliest level covering it must be no earlier than the earliest level
covering each prerequisite. Equal levels are permitted, since ordering
within a level still respects the partial order. There is no scoring
function and no model judgment.

**Pre-registration opened** at `evals/PRE_REGISTRATION.md`. Fourteen
sections, ten fixed and eight items pending, each pending item naming what
unblocks it. A pending item is a value to be measured rather than chosen.
The document must be complete before the first ablation run.

**Teacher model decided by verification.** Frontier interfaces are
excluded. Their terms prohibit training competing models, enforcement is
active, and a language model trained on those outputs is not defensibly
non-competing. Generation uses a specifically named MIT or Apache 2.0
checkpoint with the licence recorded at time of use.

### Fixed, 2026-09-23. Static analysis run for the first time

- **The analysis configured since the initial commit had never been
  executed.** On first run ruff reported eighteen errors and pyright in
  strict mode reported eighteen. A declared standard that is never checked
  is not a standard.
- All thirty-six are fixed. Both tools now report clean.
- **One fix was substantive rather than cosmetic.** `from_json` read a file
  from disk, which is external input, and cast rather than validated. It
  now checks every field and raises at the boundary, which is what the
  project's own trust-boundary rule requires. Ten tests were added for
  malformed input, which had none.
- The pseudo-random exemption is documented rather than silently ignored.
  The control must be reproducible from a declared seed, which is precisely
  what a cryptographic generator does not offer.
- `tools/check.sh` added as a gate. It caught a violation of its own on
  first run.

### Added, 2026-09-23. Concept graph. First implementation

- `docs/spec/CONCEPT_GRAPH.md`, `src/epagoge/concept_graph.py`,
  `tests/test_concept_graph.py`, `tools/validate_graph.py`, and a seed
  graph at `curriculum/graph/concepts.json`.
- Standard library only. No dependency is added, so the graph can be
  validated before any environment question is settled.
- Six invariants enforced. Reference resolution, acyclicity, no self-loops,
  instantiation direction and kinds, domain declaration by node kind, and
  layering, meaning the formal layer may not depend on the domains that
  instantiate it.
- **Validation returns every violation rather than raising on the first**,
  so a graph is audited in one pass.
- **Prerequisite depth is the longest path, not the shortest.** A concept is
  reachable only once every prerequisite is satisfied, so its earliest
  admissible position is governed by its deepest dependency.
- **Transfer edges are derived, never authored.** Two domain concepts in
  different domains are connected exactly when they instantiate a common
  formal structure. Same-domain sharing is ordinary structure, not transfer.
- The random linear extension is the experimental control. **Documented
  limitation.** Randomised Kahn does not sample uniformly over linear
  extensions, since counting them is #P-complete and frontier-uniform
  selection biases toward orderings that keep the frontier wide. Uniformity
  is not required for the control, but the bias is recorded rather than
  left to be discovered.
- Twenty-two tests, weighted toward negative cases. Every invariant has a
  test that breaks it, because a validator shown only valid input has not
  been tested.
- Seed graph of 33 nodes across two domains and a formal layer. Validates
  clean. Three transfer edges derived rather than asserted.
- **Weak empirical support for the question twenty design.** Mathematics
  reaches prerequisite depth seven in the seed and failure analysis reaches
  five, which is the contrast the ablation assumes. The mathematics
  subgraph also has more nodes, so this is directional rather than
  measured.

### Resolved, 2026-09-23. Four open questions closed

**21. Levels against structural difficulty.** They are not competing
definitions. Prerequisites and supersession are hard checkable constraints
giving a partial order. The seven levels choose one trajectory within the
feasible set. The earlier proposal that prerequisite depth be authoritative
was withdrawn as wrong, since dependency depth cannot express breadth,
abstraction, or groundedness.

**Consequence.** The flat-order control is a **random topological
ordering**, respecting prerequisites while discarding the curriculum
trajectory. A free shuffle would have compared valid ordering against
invalid ordering, which is close to a tautology and is what much of the
published literature does.

**24. Transfer edges route through the formal spine.** An edge exists
between two domain concepts exactly when a formal structure exists that
both instantiate, and that structure is a node in the graph. Checkable,
model-free, and it excludes loose metaphor, which is where false transfer
originates. The graph becomes layered.

**20. The ablation corpus is two domains, not the full manifest.**
Mathematics for deepest prerequisite chains and machine-verifiable content,
plus a near-flat-structure contrast domain. The contrast varies the
hypothesised mechanism rather than merely the tidiness of the subject.

**The strongest available outcome is now a dissociation.** A positive result
in the deep-structure domain paired with a null in the flat-structure one
would be evidence that prerequisite depth is the mechanism, which is a
better finding than an ordering effect alone, and would explain the
inconsistency of prior work, which has not controlled for the prerequisite
depth of its subject matter.

### Changed, 2026-09-23. Enabling material, spiral structure, and quirk

- **Every topic appears at every level, as enabling material.** At low
  levels this is the enabling primitives rather than the formal discipline.
  Failure analysis at the first level is that things break and living
  things die. This answers open question twenty-three and unblocks staging
  of practice-spine content.
- **Level one seeds civilisational axioms**, meaning the primitives later
  content presupposes and never states. A human learner is taught that a
  street is dangerous. A model has no innate anything, so every such
  primitive is in the corpus or absent from the model. This is a better
  specification than emergent understanding.
- Open question twenty-two sharpened rather than closed. Whether explicit,
  early, isolated axiom-seeding beats implicit, diffuse absorption is the
  curriculum hypothesis restated at the axiom level.
- **Open question twenty-four added.** The spiral has a vertical relation,
  already encoded by the supersession pointer, and a horizontal one that
  does not exist in the design. Inter-topic mastery needs analogy or
  transfer edges in the concept graph. Cross-domain gradient alignment
  already instruments it, so it is observable in the kernel.
- **Quirk accepted within a declared boundary.** Unbounded, it would absorb
  any negative result, which is the unfalsifiable move this project exists
  to prevent and is more dangerous from the operator than from the model.
  Unusual register and narrow stylistic range are quirk. Systematic error
  and mode collapse are failures. The boundary goes in the pre-registration.
- **Spin-off artifacts recorded as an option preserved, not a goal
  pursued.** Extraction stays cheap, no corpus decision is driven by human
  readability, and the disclosure implication of publishing curriculum
  material is recorded as requiring a deliberate decision.

### Added, 2026-09-23. Seven curriculum levels

- `docs/spec/CURRICULUM_LEVELS.md`. Seven levels from preschool to
  post-graduate, with the developmental rationale for the shape. Narrow and
  concrete at first because nothing wider can be grasped, an inflection at
  the third level where broad breadth becomes available, then breadth
  progressively traded for depth before messy real problems at the end.
- **The levels bundle four axes**, namely breadth, depth, abstraction, and
  groundedness. Breadth is an hourglass rather than monotonic. Depth is the
  only monotonic axis and is named primary so the ordering claim has a
  stated referent. The confound is documented rather than decomposed, since
  decomposition would multiply the arms beyond budget.
- **Levels one to six are synthetic and built to purpose.** Licensing
  questions therefore apply only to level seven. The developmental analogy
  motivates the shape of the ladder without dictating its content.
- **Token distribution is power-law across three to four orders of
  magnitude**, since early-level material is short. This partially resolves
  open question twenty along the level axis. The topic-breadth half is
  untouched.
- The curriculum hypothesis is consequently a claim about roughly the first
  one percent of tokens, which is consistent with the kernel-shaping
  mechanism rather than in tension with it, since shaping requires the
  correct data first rather than much data.
- Risk recorded. A purely synthetic early corpus may be too clean, and the
  early phase is where the kernel is shaped.
- Open questions twenty-one, twenty-two, and twenty-three added.

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
