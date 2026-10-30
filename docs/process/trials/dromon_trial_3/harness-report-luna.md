# Luna harness experience report

## Changes since the earlier report

**Fact.** The second-trial report described two draft rounds on 2026-10-29. In the first, I did not finish the scratch-copy edit or tests. The operator supplied an ordered procedure. In the second, I produced the three-file diff; baseline and revised tests passed, Ruff passed after a formatting correction, and Pyright reported no diagnostics. Rsync returned status 23 because it could not stat the excluded `.dromon` path, while the scratch copy remained usable.

**Fact.** This third trial differs in scope. I was assigned a read-only corpus readiness measurement and reports, with explicit output paths and constraints. I created a small counting script, copied it under the requested ignored directory, and wrote a full unit table. There was no patch or test procedure in my task.

## What worked well

**Fact.** The operator's note gave concrete deliverables, cost and turn limits, prohibited actions, and the concurrent-worker constraint. The brief independently confirmed the task. Mail reading and scratch writing worked. The prior coverage report supplied useful context about the number of missing units.

**Fact.** The schedule contains the concepts and unit identifiers; the seed books store dictionary records whose concepts can be counted. A small script made the measurement repeatable. Checking expected book paths distinguished units without books from those already drafted.

**Inference.** Explicit deliverable paths and scope reduced ambiguity compared with the earlier draft round, where I needed an ordered procedure to complete the scratch-copy workflow.

## What got in the way

**Fact.** Reading the entire schedule together with large book listings produced truncated command output. Targeted searches and a later script avoided relying on the truncated output. The current worker was editing seed books concurrently, so the count is a snapshot and can shift by a few words.

**Fact.** A single terminal read command produced much more output than needed. Separating schema inspection from the actual counting made the data shape clear.

## What I could not see or do

**Fact.** The session instructions denied reads under `.dromon/`. This task did not require those files. The prior report documents the rsync warning caused by that denied path during the earlier scratch-copy round.

**Inference.** No unavailable data blocked this task. The count necessarily measures dictionary concept assignments, not whether the assigned words support a coherent module.

## Ranked harness suggestions

1. **Show truncation clearly for each command.** Problem: the schedule and book listing output was cut off, so I had to inspect files again. A visible truncation marker and per-command output cap would make follow-up predictable.
2. **Offer a schedule-to-book presence report.** Problem: concept coverage and book existence are separate, and checking paths manually is easy to get wrong. A helper listing unit IDs and expected file status would support readiness work.
3. **Expose ignored scratch paths in task setup.** Problem: the earlier patch trial's rsync could not stat the excluded denied directory and returned status 23 despite a usable copy. A standard copy command or exclusion note would prevent interpreting that warning as a failed copy.

## Earlier suggestions and direction

**Fact.** The earlier report suggested clearer truncation, a book measurement helper, and explicit scratch-writer behavior. Truncation and schedule-to-book reporting still apply. Scratch writing succeeded this turn, and I copied the script using a direct command; the earlier concern about scratch-writer directory creation does not apply to this assignment.

**Fact.** The second-trial report said the operator's ordered procedure improved the second draft round. The current note already gave an ordered deliverable list and named the files, which was sufficient for this task. It also specifically required mentioning the seed-book read date and concurrent count drift, making the snapshot's limits auditable.

**Judgement.** The two-round experience suggests that procedural direction is most useful when a task involves several dependent edit and verification steps. A clear deliverable list was enough for this measurement-only task.
