# Artifacts for asking why, afterwards

**Recorded 2026-09-25, operator direction.** The project should carry
artifacts and metadata that serve post-facto analysis. The example given
is the one that bites: **for every word, why it was included and when.**

## What can be answered honestly, and what cannot

**Most of the lexicon predates any field recording why.** 1,068 of 1,069
words were admitted before `source` existed, so their reasons cannot be
retrieved. They can only be reconstructed or invented, and inventing them
would produce exactly the artifact this file exists to prevent: something
that reads as evidence and is not.

**The repository's own history is the honest source.** The commit that
first contains a word says when it arrived and, in its message, what was
being done at the time. `tools/word_provenance.py` walks every revision of
the lexicon and records that, writing `curriculum/provenance.json`.

**The two kinds of answer are labelled differently and that is the point.**

- `recorded at admission` — written when the decision was made.
- `reconstructed from history` — the commit that first held the word,
  which is *what the commit was about* rather than necessarily why that
  particular word was in it.

Today that is 1 against 1,068. The ratio will improve going forward and
will never be repaired backwards.

## The admission criterion, reconstructed

**Operator direction 2026-09-25: make a best effort, and it is acceptable
that it is not clean.** Every word now carries a criterion, recovered from
the commit that introduced it.

| Criterion | Words | What it means |
| --- | --- | --- |
| `prescriptive` | 444 | Authored as a foundational lexicon before any corpus existed |
| `lexicalisation` | 271 | Admitted so a scheduled concept has a word naming it |
| `mapping` | 138 | Given a concept and a level when the vocabulary was mapped |
| `corpus` | 87 | Blocked a book round and triage judged it suitable |
| `teacher` | 64 | The teacher reached for it and was refused |
| `inflection` | 27 | A form of an admitted word, or a correction to one |
| `operator` | 19 | Admitted on direction, as a word the level plainly needs |
| `thesaurus` | 18 | Named as a synonym or antonym of an admitted word |
| `scan` | 1 | Proposed by a frequency scan and admitted on judgement |

**It is right about the pass and cannot be right about every word in a
pass.** The criterion is the reason the commit gives for its batch,
applied to each word in it.

**The largest group is the least precise, and deliberately so.** Declaring
all 444 words of the prescriptive pass admitted on one criterion explains
any single one of them only loosely. Bootstrapping a closed lexicon does
not decompose into per-word reasons: the words were chosen together,
against each other, and against what the dictionary needed in order to
close at all. That is part of why it is a hard problem, and a
reconstruction that claimed more would be a worse record than one that
says this.

## What the reconstruction actually shows

Four commits account for most of the lexicon: 444 words from the
prescriptive authoring pass, 235 added to satisfy the concepts-without-a-
word check, 126 from the vocabulary mapping, 56 from what the teacher
reached for. **That is a fair description of how this lexicon was built**,
and it is more informative than a per-word rationale would have been had
one been invented.

## The record is regenerated and compared, not trusted

**A provenance record that has drifted from the lexicon is worse than
none**, because it reads as evidence while describing something else. The
gate runs `--check`, which rebuilds the mapping from history and fails if
the file on disk names words the lexicon no longer has or misses words it
does.

## Other artifacts the project already keeps for this purpose

Recorded together so that the answer to "what can be analysed afterwards"
is in one place.

- **`evals/pilot/*.json`** — every training run with its seeds, corpus
  size, configuration and per-seed losses.
- **`evals/pilot/LEVEL_ONE_*.md`** — what each measurement does and does
  not settle, including two withdrawn readings and the metric found to be
  vacuous.
- **`docs/decisions/`** — a record before the work it constrains, with
  objections kept alongside decisions rather than dropped.
- **Commit messages** — the only place a judgement call is usually
  written, which is why they carry the reasoning rather than a summary.
- **`substitutions`** — what a level chose not to admit, and what it says
  instead.

## What is still not recoverable

**Why a concept was assigned to the domain it was.** The graph records the
assignment and not the argument, and 51 concepts were authored in one pass
with the reasoning in a single commit message.

**Why a word was given the level it was.** Level assignment is the
scheduling problem's central decision and nothing records the reason for
an individual placement.

Both are worth a field. Neither has one, and adding one now would have the
same 1-against-1,068 problem, so the honest first step is to record it
from here rather than to backfill.
