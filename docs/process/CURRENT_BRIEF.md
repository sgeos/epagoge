# Brief

Closed 2026-10-23. The seven-source condition was met, and the later agency
pass is recorded in `HANDOFF.md`. This file is historical evidence. Do not
repeat it.

Opened 2026-10-09. The operator directed that the remaining level-two
candidates be admitted. The lexicon is far under its approximate target of
about ten thousand words, and capacity is not a reason to hold a candidate
back. The previous brief and condition are retained in
`evals/review/level_2_one_source/`.

## Operator direction

Admit the level-two candidates from the reference-source scan. Do not wait
for a further word-by-word decision.

## Interpretation and recommended work

**The candidate set is the frequent group already scanned.** On 2026-09-27
`tools/scan_lexicon.py` counted seven public-domain and CC0 sources, each
source separately, at a threshold of five. Measured on 2026-10-09, after
removing words already admissible, words already decided, strings shorter
than three letters, and words capitalised in at least half of their
occurrences, **1,300** candidates remained. The two-source pool is empty.
The long tail below the threshold is not part of this brief. Dale-Chall and
the New General Service List stay unused. That licensing question is still
the operator's.

**A candidate is admitted only with a grounded definition.** `tools/admit.py`
refuses a word that would take the dictionary out of self-hosting, and this
brief does not override that. A word that cannot yet be defined inside the
level is deferred with a reason and can be admitted in a later batch, once
the words its definition needs are in. An inflected form of a headword is
excluded, as in the earlier batches. A prior decision stays decided.

**The teacher is not required for this path.** On 2026-10-09 about 175
megabytes of pages were free and swap held 10,956 of 12,288 megabytes. The
teacher needs about eighteen gigabytes resident, so it was not loaded.
Definitions are agent-authored and pass the same admission and closure
checks as teacher output. Semantic review is agent review.

**The first batch is 24 words** from the McGuffey portion of that pool,
recorded in `evals/review/level_2_one_source/`. A second batch, recorded in
`evals/review/level_2_scan_02/`, admits 432 and excludes 7. A third batch,
recorded in `evals/review/level_2_scan_03/`, admits 71 and excludes 3.
Later batches through `level_2_scan_10/` continue the same work.
`level_2_scan_07/` admits 72 and excludes 191. `level_2_scan_08/` admits
72. `level_2_scan_09/` admits 72. `level_2_scan_10/` admits 72 and defers
thee, thy, thine and unto, because function-word definitions are not
decided in this brief. Measured after that batch, distinct headwords
through level two are 2,159. A fresh selection from the same scan prints
an empty pool. The approximate target is not met. That gap is 7,841, and
it is not a claim that more words are frequent in the scanned sources.

## Wrong turns to avoid

Do not admit a word without a definition. Do not reopen a word that already
has a review decision. Do not consult Dale-Chall or the New General Service
List. Do not treat the long tail as if this brief had included it. Do not
load the teacher while free memory cannot hold it. Counts come from the
measurement tool.
