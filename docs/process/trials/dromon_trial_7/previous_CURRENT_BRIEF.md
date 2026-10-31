# Brief

Met 2026-10-30. The condition holds on the working tree. This file is
historical evidence. Do not repeat it.

Opened 2026-10-30. The operator directed the session to find a high-value
iteration and complete it through the Dromon harness, to update the team
of lines as appropriate, and to have every Dromon line write a report on
its experience of the harness. The direction does not ask for a commit or
a push. The previous brief and condition, met on 2026-10-30, are retained
in `evals/review/level_2_long_tail/`. The work of the fourth, fifth and
sixth trials is still uncommitted in the working tree, and this seventh
trial builds on it.

## Choice of iteration

**The lexicon is the largest measured gap that needs no teacher.** Level
two holds 2,997 distinct headwords against an approximate target of about
ten thousand. Corpus generation needs the teacher, which stays unloaded,
and the generator draft awaits the operator. Every pool drawn at the
threshold of five is decided.

**The pool comes from sources already fetched and already listed.** The
sixteen source texts that earlier batches scanned are all candidates in
`docs/decisions/AGENCY_SOURCES.md` or the McGuffey readers of the first
batch. Scanned together at a threshold of five, they leave 20 undecided
strings. At a threshold of four, `tools/candidate_pool.py` with the private
term list leaves 613. No text is fetched for this trial. Lowering the
threshold is the operator's session's choice under the direction above,
and it reaches the long tail that the scan tool describes as where
judgement is needed.

The scan and pool are kept under the ignored
`tmp/lexicon-sources/longtail/`. The operator's session withdrew 6 strings
before any decision, recorded as a count only, and the remaining 607 are
listed in `tmp/dromon-trial-8/pool.txt`.

## Recommended work

**The worker line runs the batch** in `evals/review/level_2_long_tail/` by
the admission workflow in `docs/process/HANDOFF.md`, with level-three
admissions in `evals/review/level_3_long_tail/`. It reads how the sources
use each string, admits a word only in a sense they use, and records a
string as a reviewed form only where its headword already carries that
sense. A word used mainly in an archaic or dialect sense is deferred.
Admission writes to the dictionary seed books of levels two and three, and
no other book changes. The helper `tmp/dromon-trial-8/keydiff.py` shows how
a generated file differs from the last commit by key.

**The luna line works on the lexicon's next pool and on readiness.** After
the batch, it lists the strings of the threshold-four scan that pass the
pool rule only because the lookup strips a suffix to another headword, and
that no batch lists as a reviewed form, with the headword and the senses
that headword carries. It reruns the sixth trial's readiness script and
reports which units and concepts changed. Its reports are written under
the ignored `tmp/dromon-trial-8/`.

**The reviewer line reviews both** and edits nothing tracked. It moves
from the Haiku model to the Fable model for this trial, because the batch
is far larger than the one the reviewer checked last time and a model
other than the worker's gives a more independent reading. The Sonnet
model was the first choice, and the harness does not offer it.

**Every line writes a harness experience report** to
`tmp/dromon-trial-8/harness-report-LINE.md`, with LINE its line name. The
reports, the review and the harness reports are copied into
`docs/process/trials/dromon_trial_7/`.

## Counting rules

A distinct headword is a distinct word among the term entries at or below
a level. A second sense adds no headword. A form is never counted as a
headword. The batch's before and after counts come from
`tools/measure_lexicon_increment.py`.

## Wrong turns to avoid

Do not load the teacher. Do not fetch text. Do not reopen a decided word.
Do not consult Dale-Chall or the New General Service List. Do not apply
the generator draft. Lines do not commit or push. The operator's session
leaves the work uncommitted unless the operator asks for a commit.
