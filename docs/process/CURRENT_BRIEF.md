# Brief

Met 2026-10-28. The condition holds on the working tree. This file is
historical evidence. Do not repeat it.

Opened 2026-10-28. The operator directed a multi-agent trial of the Dromon
harness on this project, working on the level-two lexicon and corpus, with
every Dromon line writing a report on its experience of the harness. The
previous brief and condition, met on 2026-10-25, are retained in
`evals/review/level_2_agency_02/`.

## Operator direction

Spin up a multi-agent trial session on this project. Work on the level-two
lexicon and corpus. Have every Dromon line write a harness experience
report. On 2026-10-28 the operator chose a lexicon batch and a corpus review
that needs no teacher, with an estimated cost limit of 40 dollars for the
Opus line and 10 dollars for each other line.

## Interpretation and recommended work

**The lexicon is the binding constraint on level-two modules**, as
`docs/decisions/LEVEL_CALIBRATION.md` records. The pools already in the
tree are decided or closed, so the batch draws on two candidates from
`docs/decisions/AGENCY_SOURCES.md` that were not fetched before. On
2026-10-28 the operator's session fetched 39 Energy Information
Administration elementary pages and 4 pages of Ben's Guide for ages 4 to 8
into the ignored `tmp/lexicon-sources/agency2/`, with the URLs read beside
each text. Lines crediting images and data, some marked copyrighted, were
removed before any scan, because they are not page prose. The teacher
and game sections of the first site were not fetched.

**The worker line runs the batch** in `evals/review/level_2_agency_02/` by
the admission workflow in `docs/process/HANDOFF.md`. A word is admitted with
one grounded definition, or deferred or excluded with a reason. A prior
decision stays decided. Inflected forms are excluded. No teacher runs.
Admission writes each definition to the dictionary seed book of its level,
so those two books change and no other book does. The worker line found
that the first wording of the condition forbade this, and the operator's
session corrected it on 2026-10-28.

**The reviewer line reviews that batch** and edits nothing tracked.

**The luna line reviews `curriculum/books/level_2/bk.ac2.ledger.md`**
against `docs/spec/BOOK_DRAFTING.md` and the level-two schedule, and writes
its findings to the ignored `tmp/dromon-trial/`. It changes no book, since
replacing spreads needs the teacher.

**Every line writes a harness experience report** to
`tmp/dromon-trial/harness-report-LINE.md`, with LINE its line name.

## Wrong turns to avoid

Do not load the teacher. Free memory was about 0.35 gigabytes on
2026-10-28. Do not reopen a decided word. Do not consult Dale-Chall or the
New General Service List. Lines do not commit or push. The operator's
session does both after the gate passes and the operator approves.
