# Review and audit

`tools/review.py` reads and judges corpus records. It is the **sampled
expert audit** from open question two, not only a reading aid, and its
output is the measured residual error rate the project's quality claim
rests on.

## Use

    PYTHONPATH=src python3 tools/review.py \
        curriculum/graph/concepts.json \
        curriculum/graph/sample_corpus.jsonl \
        --primitives curriculum/primitives.json

| Mode | Purpose |
| --- | --- |
| default | Review interactively, resuming where you stopped |
| `--print` | Format records for reading with no prompts. Pipe to a pager |
| `--report` | Per-domain rates from verdicts already recorded |
| `--sample N --seed S` | A reproducible sample, for auditing rather than reading everything |

Verdicts append to `verdicts.jsonl` with a timestamp and a reviewer, so a
session can stop and resume, and so a disputed rate can be traced to the
judgments that produced it.

## Three verdicts, not two

Accept, reject, and **flag**. A flag is counted separately and never
silently folded into either. A reviewer who is unsure should be able to
record that without the count quietly choosing for them.

## Rates are per domain and never aggregated

Verifiability varies enormously across the corpus. One number would average
a machine-verifiable domain against an interpretive one and conceal both.
See open question two.

## Every rate carries an interval

Reported as a Wilson score interval rather than a point estimate, because
an audit is small and the rate is near zero, which is where the normal
approximation misleads.

The reason this is not optional. **Three rejections in thirty records is a
rate of ten percent with a ninety-five percent interval from 3.5 to 25.6
percent.** Quoting ten percent alone would present as a measurement
something the audit did not establish, which is the failure the project
exists to prevent, occurring in the project's own quality metric.

Even a clean audit says less than it appears to. Zero rejections in thirty
records bounds the true rate below about eleven percent, not below zero.

## What the display gives a reviewer

Each record shows its concepts, claim class, provenance, and any
simplification with the record that corrects it. **Where a record cites a
primitive, the grounding observation is shown inline**, so the claim can be
checked against what grounds it without looking anything up.
