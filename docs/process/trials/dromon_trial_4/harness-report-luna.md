# Luna harness experience report

## Changes since the earlier report

**Fact.** The third-trial report described a read-only readiness measurement and a hand-written script. In this fourth trial, the operator pointed me to the tracked readiness script, specified the comparison blob and required delta fields, and assigned a vocabulary sheet plus its generator. I used that script and produced the delta and headword list. The review reports that the vocabulary list contains 299 entries and matches the sheet line for line.

**Fact.** The earlier report's first two suggestions concerned truncated output and a schedule-to-book presence helper. Truncated output happened again when I read the full schedule and book search together. The schedule-to-book helper is less pressing for this task because the tracked readiness script already checks missing-book paths and emits unit counts. The earlier concern about scratch writing creating directories did not recur.

## What worked well

**Fact.** The operator's note gave exact inputs, outputs, limits and deferred work. The review-completion instruction clearly triggered the final report. The tracked readiness script ran successfully under isolated Python and returned the current top five and zero-count concepts.

**Fact.** The vocabulary script extracted metadata from the JSON front matter and definitions from the seed books. Ruff initially found two overlong lines. The project virtual environment's Ruff formatter corrected them, after which both lint and format checks passed. The review independently checked the lists against the seed records and confirmed the entries.

**Inference.** Naming the prior blob and asking for gains, ranking changes and remaining zero-count concepts made the comparison concrete. A tracked script also reduced setup compared with my earlier trial's one-off counter.

## What got in the way

**Fact.** A combined read of the full schedule and dictionary searches was truncated. I narrowed the reads and ran the provided readiness script. The shell did not find Ruff on PATH, so I used the project virtual environment's executable.

**Fact.** The first lint run found formatting violations in my new script. Running the formatter and rerunning both checks resolved them.

## What I could not see or do

**Fact.** This session could not read .dromon/. No task data there was needed. The review notes that the earlier comparison blob is absent from repository history, so the original snapshot cannot be reconstructed from Git.

**Inference.** The known blob hash allowed the report to identify its stated baseline, but not to recover or independently verify that historical content. The reviewer instead compared selected gains against the committed pre-batch seed.

## Ranked harness suggestions

1. **Make truncation visible and local to each command.** Problem: a large combined read was cut off, obscuring whether later schedule units were included. A clear truncation marker would prompt targeted retrieval immediately.
2. **Expose the project tool environment in command guidance.** Problem: Ruff was installed in .venv/bin but absent from PATH. A standard project command or environment activation note would avoid the failed first lookup.
3. **Retain immutable task snapshots used as comparison baselines.** Problem: the specified prior blob was unavailable in Git history. Keeping the exact report or snapshot with the trial would allow independent reconstruction of each delta.

## Earlier suggestions and direction

**Fact.** Truncation remains an issue from the earlier report. Schedule-to-book presence reporting is partly addressed by the tracked readiness script supplied for this task. Scratch directory setup was not an obstacle because the requested trial directory was writable and already available. The earlier suggestion for clearer ordered direction also still applies in general. This note's numbered tasks and named paths made dependencies and the deferred harness report clear.

**Judgement.** The most useful direction named not only the deliverables but also the baseline and fields to compare. The one material evidence gap was the unavailable historical snapshot, which clear instructions could not repair by themselves.
