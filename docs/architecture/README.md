# Architecture

How the corpus pipeline is built and why.

## Contents

- `TRAINING_SPINE.md` specifies the framework-neutral artifacts that keep
  the training framework a replaceable component. Decided 2026-09-23.
- `MODEL_ARCHITECTURE.md` specifies two architectures, a fully standard
  ablation model and a deployment model adding bounded attention, and
  records why the major 2026 frontier divergences are rejected here.
  Specified 2026-09-23.

The corpus pipeline is undesigned, because several decisions in
`../decisions/OPEN_QUESTIONS.md` determine what its design would have to
be.
