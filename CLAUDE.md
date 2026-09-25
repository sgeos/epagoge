# CLAUDE.md

This file provides guidance to Claude Code when working in this repository.

## Project Overview

Epagoge builds a graded synthetic corpus and curriculum for training a
falsification-oriented foundation model. The corpus is generated and
curated rather than scraped. It is ordered as a difficulty-graded
curriculum whose early stages present simplified concepts and whose later
stages revisit those concepts at increasing complexity, terminating in
unmodified scientific literature. The organising spine is the scientific
method.

**Status**: Under implementation. Level one is drafted at 246 books and
a model has been trained on it and can be prompted. Levels two and above
are specified and barely written.

**Read `docs/process/HANDOFF.md` first, and run its validity check before
believing anything in it.**

**Run `tools/check.sh` before any commit.** It gates lint, formatting,
strict type checking, tests, a coverage floor, graph and corpus validation,
and the disclosure scan.

**Engineering classification**: Research project. Claims are provisional
until measured.

## Standing obligations specific to this project

These derive from the project's own subject matter and are not general
style preferences.

1. **Never state a curriculum benefit as established.** That
   difficulty-graded ordering improves large language model pretraining is
   the hypothesis under test, not a premise. Published ordering ablations
   at pretraining scale report weak and inconsistent effects, and the
   documented gains in the textbook-quality-data line of work are
   attributed to data quality rather than to ordering. Any claim of
   improvement requires a flat-order control run.

2. **Do not conflate disagreeableness with correctness.** Sycophancy is a
   failure of calibration under social pressure. Disagreeableness is a
   dispositional bias toward contradiction, and a model trained toward it
   contradicts correct users at the same rate as incorrect ones. The
   target property is evidence-conditioned assent, which is measurable.
   Disagreeableness is not measurable in a way that distinguishes it from
   being wrong more often.

3. **Treat teacher-model output as untrusted input.** Every record
   entering the corpus crosses a trust boundary. Validate against a
   declared schema at the generator boundary. A malformed or unsourced
   record must be rejected loudly rather than absorbed silently, because a
   corpus that absorbs its generator's errors cannot be distinguished
   later from one that did not.

4. **Topic coverage follows the coverage manifest.** Settled 2026-09-23.
   Coverage weighting decides what is written about. It never licenses a
   claim to exceed its evidence, since that would train exactly the
   confident extrapolation this project exists to suppress.

5. **Do not assume run-to-run determinism.** Verified 2026-09-23,
   neither candidate framework offers bitwise determinism on graphics
   processing units. Levanter's guarantee is scoped to Tensor Processing
   Units, and PyTorch states that complete reproducibility is not
   guaranteed across releases, commits, or platforms. The ordering
   ablation therefore requires multiple seeds per condition and a
   meaningful-effect threshold declared in advance. A single-run
   comparison establishes nothing.

6. **Record what is unverified.** Where a claim in documentation has not
   been measured on this tree, say so in the same sentence. Counts,
   benchmark results, and corpus statistics are measured or they are
   absent.

## Names

`epagoge` is the repository and the corpus project. `sporos` is the model.
`elenchos` is the anti-sycophancy evaluation suite.

A tracked document may gloss what a word means. It may not state why a
name was chosen.

## Code-name convention. Read `secret/CODE_NAMES.md` before writing tracked prose

**Hard constraint.** `secret/CODE_NAMES.md` holds the mapping, the
convention, the banned vocabulary, and the term scan to run before any
commit touching documentation. It follows the equivalent discipline in the
operator's Keleusma project, so the two require one habit rather than two.

The short form. State engineering constraints truthfully and stop. Cite a
code name where a source must be named. Do not explain why a topic was
selected, why a constraint exists, or why a name was chosen, where the
reason would identify the domain.

Omission is permitted. Misdirection is not. If a constraint cannot be
stated truthfully without revealing the domain, omit the rationale rather
than inventing one.

## Repository Structure

```
epagoge/
├── CLAUDE.md          # This file
├── AGENTS.md          # Agent-agnostic pointer to this file
├── README.md
├── CONTRIBUTING.md    # What makes a contribution acceptable
├── LICENSING.md       # Which licence applies to which part of the tree
├── CITATION.cff       # Citation metadata
├── llms.txt           # Machine entry point
├── CHANGELOG.md
├── pyproject.toml     # Package metadata, ruff, pyright, pytest config
├── src/epagoge/       # Importable library shared by all stages
├── curriculum/        # Stage specifications, authoritative
├── generators/        # Corpus synthesis pipeline
├── evals/             # Evaluation suites
│   └── elenchos/      # Anti-sycophancy and calibration probes
├── corpus/            # Derived stream, IGNORED and rebuilt from the books
├── sources/           # Terminal-stage literature, TRACKED
├── docs/
│   ├── architecture/  # How the pipeline is built
│   ├── decisions/     # Decision records and open questions
│   ├── process/       # Working practice
│   └── spec/          # Authoritative specifications
├── tools/             # Auxiliary scripts
├── secret/            # Never tracked
└── tmp/               # Transient scratch
```

## Toolchain

Python is primary and settled. Rust is reserved for corpus-processing
passes that profiling shows to be bottlenecks, and none is written.

The training framework is **open**. PyTorch versus JAX is blocked on the
hardware path. Do not assert either as chosen. The decision rule and the
verified evidence are in `docs/decisions/LANGUAGE_CHOICE.md`. In short,
Tensor Processing Unit access favours JAX with Levanter, and NVIDIA-only
or local-only favours PyTorch.

The interpreter is resolved. Verified 2026-09-23, torch 2.14.0 and jaxlib
0.11.2 both publish cp314 wheels, so 3.14 is not a blocker.
`requires-python` stays at `>=3.12` because nothing requires more. See
`docs/decisions/PYTHON_VERSION.md`.

Static analysis is configured in `pyproject.toml`. Pyright runs in strict
mode. This is a deliberate compensation for Python's weaker static
guarantees relative to the rest of this operator's toolchain.

## Host environment as measured at project creation

Apple M1 Max, 32 GB unified memory, no CUDA device. The volume had 57 GiB
free of 926 GiB. This machine cannot pretrain a foundation model. It can
train a small model adequate for curriculum ablation experiments. Any real
run requires rented NVIDIA hardware.

## Corpus tracking

**`sources/` is tracked. `corpus/` is not, as of the amendment of
2026-09-24.** The original decision of 2026-09-23 tracked both, and it was
taken while `corpus/` was going to hold the authored records. It no longer
does: the books under `curriculum/books/` are the authored artifact, and a
stream under `corpus/` is rebuilt from them by `tools/build_corpus.py`
under a chosen ordering. What tracking bought is now bought by the books.
`sources/` stays tracked because terminal-stage literature is acquired
rather than derived and cannot be rebuilt.

**This file said both were tracked until 2026-09-25**, which is the same
class of defect the project records elsewhere: a decision was amended in
`.gitignore` and the amendment did not reach the document an agent reads
first.

Git Large File Storage is installed on this machine but is **not**
configured for this repository. Consequences are recorded in `.gitignore`
and `docs/decisions/CORPUS_TRACKING.md`.
