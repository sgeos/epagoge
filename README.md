# Epagoge

A graded synthetic corpus and curriculum for training a
falsification-oriented foundation model.

**Status.** Under implementation. The concept graph and the corpus record
schema are specified, implemented, tested, and gated. No corpus has been
generated and no model has been trained.

All nineteen pre-planning questions are resolved, fifteen answered and four
deferred to the gated follow-on. See
`docs/decisions/OPEN_QUESTIONS.md`.

**The deliverable** is the corpus, the curriculum specification, and a
pre-registered ordering ablation at three scale points from random
initialisation. A deployable model is a follow-on gated on that result.

**Next artifact** is the pre-registration document, which must fix the
metrics, the meaningful effect size, the seed count, and the corpus
error-rate ceiling before any run.

## Why evidence-conditioned assent is an engineering requirement

Deferring to a confident but mistaken claim is a failure of calibration
rather than a courtesy. Where the cost of acting on a wrong conclusion is
high, calibrated disagreement is a requirement and not a preference, which
is what `evals/elenchos/` measures.

The rationale beyond that is recorded under the discipline `CLAUDE.md`
points to, and is deliberately not restated here.

## Intent

The project builds a synthetic pretraining corpus that is generated and
curated rather than scraped, organised as a difficulty-graded curriculum.
Early stages present simplified concepts. Later stages revisit the same
concepts at increasing complexity. The terminal stage is unmodified
scientific literature. The organising spine of the curriculum is the
scientific method.

The resulting model is intended to condition its assent on evidence rather
than on user insistence.

## Names

**epagoge**, the repository and the corpus project. Greek, the rearing and
education of a person into a full member of the polis, covering both the
staged instruction of a child and the formation of the resulting
character.

**sporos**, the model. Greek, seed or sowing.

**elenchos**, the anti-sycophancy evaluation suite. Greek, the Socratic
cross-examination.

## Layout

```
epagoge/
├── src/epagoge/     Importable library shared by all stages
├── curriculum/      Stage specifications, authoritative
├── generators/      Corpus synthesis pipeline
├── evals/           Evaluation suites
│   └── elenchos/    Anti-sycophancy and calibration probes
├── corpus/          Generated corpus data, tracked in version control
├── sources/         Terminal-stage literature, tracked in version control
├── docs/            Architecture, decisions, process, specification
├── tools/           Auxiliary scripts
├── secret/          Environment-specific secrets, never tracked
└── tmp/             Transient scratch files
```

## Licensing

Software under `src/`, `tests/`, and `tools/` is 0BSD. The corpus,
curriculum, concept graph, specifications, and documentation are CC0 1.0.
Third-party material under `sources/` retains its own terms and is not
covered by either. See `LICENSE` and `docs/decisions/LICENSING.md`.

## Toolchain

Python is the primary implementation language and that decision is
settled. Rust is reserved for corpus-processing passes that profiling shows
to be bottlenecks, and none has been written.

The training framework is not settled. PyTorch and JAX both remain
candidates, and the choice is blocked on the hardware path. See
`docs/decisions/LANGUAGE_CHOICE.md` for the comparison, the verified
evidence, and the decision rule.

The interpreter is resolved at `>=3.12`, with Python 3.14 verified as
usable. See `docs/decisions/PYTHON_VERSION.md`.

## Running anything

The package must be installed into the environment before a tool will
import it. **Every tool in `tools/` was unrunnable as its own docstring
described it** until 2026-09-25, because they were developed with
`PYTHONPATH=src` exported in the shell and nothing said so.

    uv venv
    uv pip install -e ".[train]"

The `train` extra pulls PyTorch and is needed only by the tools that
train or sample. Without it the rest still run and the gate still passes,
because its tests skip when the extra is absent.

    ./tools/check.sh
    .venv/bin/python tools/talk.py --level 1 --prompt "the cup is"

## Verification posture

The central claim of this project, that difficulty-graded ordering improves
pretraining, is itself the hypothesis under test. It is not an assumption
the project is entitled to make. A flat-order control is required before any
observed gain can be attributed to ordering rather than to data quality.

Because bitwise determinism is unavailable on graphics processing units
under either candidate framework, that control must also run across
multiple seeds with reported variance. A difference smaller than
seed-to-seed variance carries no information, and the published ordering
literature reports small effects, so this is the expected case rather than
the unlikely one.

See `docs/decisions/OPEN_QUESTIONS.md` and `evals/README.md`.
