# Brief

Met 2026-10-30. The condition holds on the working tree. This file is
historical evidence. Do not repeat it.

Opened 2026-10-29 and restated 2026-10-30. The operator directed a fourth
multi-agent trial of the Dromon harness on this project, working on the
level-two lexicon and corpus, with every Dromon line writing another report
on its experience of the harness. The restated direction of 2026-10-30
does not ask for a commit or a push. The previous
brief and condition, met on 2026-10-29, are retained in
`evals/review/level_2_agency_05/`.

## Operator direction

Spin up another multi-agent trial session on this project. Work on the
level-two lexicon and corpus. Have every Dromon line write another harness
experience report. The scope follows
the operator's choice for the earlier trials, a lexicon batch and corpus
work that needs no teacher, with the same cost limits of 40 dollars for the
Opus line and 10 dollars for each other line.

## Interpretation and recommended work

**The lexicon batch draws on the USGS Water Science School.**
`docs/decisions/AGENCY_SOURCES.md` lists it as a level-two candidate of
employee text. The first agency pass of 2026-10-10 read 19 of its pages.
On 2026-10-30 the operator's session fetched the article pages linked from
its topic pages, and the pages those link to inside the school, into the
ignored `tmp/lexicon-sources/agency5/`, with the URLs read beside the text
and the 19 pages already read left out. It kept 214 pages, about 164,900
words. Only the first tab of each page was kept, and media usage lines,
credit lines, page interface lines and the site footer were removed. A
line already kept from an earlier page was dropped, because the question
and answer pages repeat the same lists of related questions. 34 linked
pages returned not found. The site states that some images are copyrighted, and image
captions were kept as text.

**The worker line runs the batch** in `evals/review/level_2_agency_05/` by
the admission workflow in `docs/process/HANDOFF.md`, with the fourth agency
batch as its model. It stops after drawing the pool, so that the
operator's session can withdraw strings before any decision, and continues
when told. Admission writes to the dictionary seed books of levels two and
three, and no other book changes.

**The luna line works on the corpus without the teacher.** After the batch
is admitted, it reruns the tracked readiness script of the third trial and
reports what changed. It also writes a vocabulary sheet for `r2.measure`,
the unit the readiness report ranked first, listing the admitted headwords
filed under each concept the unit revisits. Both are written under the
ignored `tmp/dromon-trial-5/`.

**The reviewer line reviews the batch, the report and the sheet** and edits
nothing tracked.

**Every line writes a harness experience report** to
`tmp/dromon-trial-5/harness-report-LINE.md`, with LINE its line name.
As in the third trial, the reports, the sheet and the review are copied
into `docs/process/trials/dromon_trial_4/`, so that a later commit can
track them.

**The harness now holds the project's disclosure list.** The local Dromon
project file names the private term list as its disclosure list, which the
lines asked for in the third trial. Dromon matches a term as a substring,
so a refusal can be a false positive.

## Wrong turns to avoid

Do not load the teacher. Do not reopen a decided word. Do not consult
Dale-Chall or the New General Service List. Do not apply the generator
draft. Lines do not commit or push. The operator's session leaves the work
uncommitted unless the operator asks for a commit.
