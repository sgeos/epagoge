# Brief

Met 2026-10-30. The condition holds on the working tree. This file is
historical evidence. Do not repeat it.

Opened 2026-10-30. The operator directed a sixth multi-agent trial of the
Dromon harness on this project, working on the level-two lexicon and
corpus, with every Dromon line writing another report on its experience of
the harness. The direction does not ask for a commit or a push. The
previous brief and condition, met on 2026-10-30, are retained in
`evals/review/level_2_stripped_forms/`. The work of the fourth and fifth
trials is still uncommitted in the working tree, and this trial builds on
it.

## Operator direction

Spin up another multi-agent trial session on this project. Work on the
level-two lexicon and corpus. Have every Dromon line write another harness
experience report. Every earlier lexicon pool is fully decided, so the
operator was asked which scope the lexicon batch should take, and chose on
2026-10-30 to decide the strings admissible only by suffix stripping, with
no new text. The cost limits are those of the earlier trials, 40 dollars
for the Opus line and 10 dollars for each other line.

## Interpretation and recommended work

**The lexicon batch decides 17 suffix-stripped strings.** The fifth trial's
review found 17 strings frequent in the first agency scan that pass the
pool rule only because the lookup strips a suffix to another headword, and
that no batch lists as a reviewed form. They are buildings, colored,
cooling, cools, experiencing, flooding, graphics, mining, oils, organics,
peoples, powered, sampling, soaps, united, waters and wells. A stripped
form can carry a sense that was never decided, as organics carries a noun
sense beside the adjective organic. For each string the worker line reads
how the first agency sources use it, under `tmp/lexicon-sources/`, and
decides whether it is a form of an admitted headword in the sense that
headword already carries, a new sense or headword to admit, or a string to
defer or exclude. The batch is written in
`evals/review/level_2_stripped_forms/`, with level-three admissions, if any,
in a level-three directory of the same name.

**Second senses need a tool change.** Eight of the strings carry a sense
of a word already admitted in another sense, such as wells, the noun for a
water hole, beside the adverb well. `docs/decisions/LEXICON.md` allows a
word several senses, each with its own concept and level, but
`tools/admit.py` refuses any word already admitted, and
`tools/author_definitions.py` files a new record under the earliest
sense's concept. The operator chose on 2026-10-30 that the worker extend
both tools, with tests, to admit a second sense keyed by word and concept,
and then file the second senses this batch needs. The worker may edit
`tools/` and `tests/` for this.

**The luna line counts readiness from the authoritative vocabulary.** The
readiness reports of the third, fourth and fifth trials counted dictionary
records in the seed books. Level one has a second dictionary book,
`bk.dictionary.1.md`, and the term entries of `curriculum/vocabulary.json`
file words such as letter, right, hold and hard under concepts that those
reports called empty. Counted from the term entries, no concept in the 26
level-two units without a book is empty at levels one and two. Luna counts
from the term entries, ranks the units again, names the thinnest concepts,
and reconciles the result with the fifth trial's seed-book counts. The
report and its script are written under the ignored `tmp/dromon-trial-7/`.

**The reviewer line reviews the batch and the report** and edits nothing
tracked.

**Every line writes a harness experience report** to
`tmp/dromon-trial-7/harness-report-LINE.md`, with LINE its line name. The
reports, the script, the review and the harness reports are copied into
`docs/process/trials/dromon_trial_6/`, so that a later commit can track
them.

## Wrong turns to avoid

Do not load the teacher. Do not reopen a decided word. Do not consult
Dale-Chall or the New General Service List. Do not apply the generator
draft. Lines do not commit or push. The operator's session leaves the work
uncommitted unless the operator asks for a commit.
