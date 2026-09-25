# Epagoge

[![check](https://github.com/sgeos/epagoge/actions/workflows/check.yml/badge.svg)](https://github.com/sgeos/epagoge/actions/workflows/check.yml)

A graded synthetic corpus and curriculum for training a
falsification-oriented foundation model.

**Status.** Under implementation. Level one is drafted: 246 books over
95 scheduled units, a self-hosting lexicon of 845 words, and a model
trained on it that can be prompted. Levels two and above are specified
and barely written. The measured limit on model quality is corpus size,
recorded in `evals/pilot/`.

**The corpus is machine-generated.** Every book was written by a local
instance of `qwen3:30b-a3b-instruct-2507-q4_K_M`, Apache 2.0, against a
closed vocabulary, and every line was checked against that vocabulary
before entering the corpus. Rejected lines were rewritten or the words
were admitted deliberately; nothing was absorbed unchecked. Some passages
were written by hand where the model could not meet the constraint, and
the commits say which.

All nineteen pre-planning questions are resolved, fifteen answered and four
deferred to the gated follow-on. See
`docs/decisions/OPEN_QUESTIONS.md`.

**The deliverable** is the corpus, the curriculum specification, and a
pre-registered ordering ablation at three scale points from random
initialisation. A deployable model is a follow-on gated on that result.

**The pre-registration exists** at `evals/PRE_REGISTRATION.md` and has
open items, the sharpest being the training endpoint. Holding everything
else fixed and changing only the step count moved the ordering result
from one sign to the other, so no ordering claim from this repository
means anything until that is fixed in advance.

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

**Software is 0BSD. Everything else is CC0 1.0 Universal.** Software means
`src/`, `tests/`, `tools/`, and `generators/`. Everything else means the
corpus, the curriculum, the concept graph, the specifications, the
evaluations, and the documentation.

Third-party material under `sources/` retains its own terms and is covered
by neither, because those terms are not this project's to grant.

`LICENSE` and `LICENSE-CC0` hold the licence texts. `LICENSING.md` says
which applies where, and `docs/decisions/LICENSING.md` says why the split
exists.

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
