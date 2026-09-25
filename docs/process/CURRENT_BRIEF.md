# Current brief. Level one end to end, then level two

**Rewritten 2026-09-25** after the operator expanded the goal set to seven
items. **Revised the same day**, after the twelve short books reached the
spread standard and the fifty-one missing graph concepts were authored.
Delete when `COMPLETION_CONDITION.md` is met.

## The seven, with what each actually depends on

| # | Goal | State | Real blocker |
| --- | --- | --- | --- |
| 1 | Dictionary coverage and closure | **Done. 732 of 732, closure 100%** | — |
| 2 | Thesaurus, synonyms and antonyms | **Done. 194 antonyms, 132 synonyms over 849 entries** | — |
| 3 | Missing words added to both | **Done, and now continuous.** `tools/admit.py` pulls words the corpus asks for | — |
| 4 | Full level-one corpus draft | **46 of 92 units have a book; every book is at 16 spreads** | Generation. Nothing else |
| 5 | Train a level-one model | `epagoge.pilot` has the model, loop, device and paired orderings; torch 2.14 and MPS verified | **Item 4.** The corpus is about 2,200 words and cannot train anything |
| 6 | Level-two dictionary and thesaurus | **Done. 766 of 766, closure 100%** | — |
| 7 | Level-two ablation | Pre-registration has pending items | Items 4 and 5 |

## The sequencing claim, and it is the load-bearing one

**Item 4 is the gate on everything downstream.** The corpus is 2,200
words. Nothing trains on that and no ordering is detectable in it.

One book per schedule unit is roughly 92 books and 40,000 words. That is
both what "full draft" reasonably means and **the minimum orderable set an
ablation can use**, since the ablation orders books and five is not a set.

**It is not the token budget.** `CORPUS_SCALE.md` wants 12 to 600 books
per topic, so 1,923 at the low end. A draft is one per unit. Say which is
meant whenever reporting, because conflating them overstates the project.

## What done means for 5 and 7

**A run that completes and reports honestly.** The corpus will be far
below the scale at which an ordering effect could be detected, and the
published literature already reports such effects as weak and
inconsistent at full scale. **Expect a null. Record it as a null.** A
result that is not there must not be manufactured, and the pre-registered
threshold is what decides, not the sign of the difference.

## How a book round goes now

Generate, then triage the quarantine rather than discard it. Each rejected
line names the words that blocked it. **A word the teacher reached for is
evidence, not an error.** Suitable words go through `tools/admit.py`,
which derives the plural or the inflections, writes the definition through
the closure check, and syncs the thesaurus, all or nothing. Unsuitable
words are rephrased instead.

**The suitability judgement is mine each round and deliberately not
automated.** That is the same triage the operator gave for the lexicon,
and putting a model in charge of it would grow the lexicon by whatever the
model finds convenient.

## The spread standard changes what a draft means

**Sixteen spreads exactly, being thirty-two pages, being one signature.**
A book that misses it cannot be physically published without someone else
padding or cutting it, so the count is exact and not a floor.

The corpus goal is therefore **92 books at 16 spreads**, not 92 books.
Existing books hold six to fifteen spreads and are topped up by
`generators/extend_books.py` rather than regenerated, because a short book
is unfinished and its existing lines are already true and admissible.

**The gate passes `--spreads 16` as of 2026-09-25.** Every level-one book
is at the standard, and a new short book now fails the gate rather than
being noticed later. It was wired and unrun for two sessions, which is the
failure this project has recorded three times.

## Every one of the 92 units can now have a book

**Closed 2026-09-25.** The 43 units that carried only `introduces` now
teach a concept the graph holds. Fifty-one concepts were authored with
prerequisite edges and domain assignments, the schedule moved them from
`introduces` to `teaches`, and each has at least one word, which is what
`words_for` needs before the generator will attempt a book at all.

Measured rather than asserted: **0 of 92 units are blocked**, 46 have a
book and 46 do not. `docs/decisions/LEVEL_ONE_CONCEPTS.md` records the
design. **Unblocking is not authoring**, and the remaining 46 books are
ordinary generation work.

## Wrong turns, every one already made once

- **The gate must gate.** A commit ran after `GATE=1` was printed in the
  same invocation. Reading the exit code is not enough if the commit runs
  regardless. Run the gate, stop, then commit.
- **Do not run large generation passes for definitions.** Acceptance fell
  22.6, 16.4, then 6.0 percent. Authoring yields about a hundred a round
  against twenty-nine for a forty-batch pass.
- **Read closure, not acceptance.** Two interventions raised acceptance
  and moved closure not at all.
- **Do not grow the ostensive seed to make closure easy.** 33 to 37 once,
  held at 37 for four rounds. A large enough seed closes any lexicon.
- **Do not assume a word is core.** `done`, `taken`, `doing` were each
  assumed and each wrong.
- **A heuristic needs two pieces of evidence.** One inflection read `a`,
  `i` and `it` as verbs and wrote six nonsense words into core.
- **A guard over records must test `defines.kind`.** Omitting it dropped
  four domain and topic definitions.
- **No magic numbers in tests.** An assertion of more than 800 thesaurus
  entries went stale the moment inflections were merged. Tie to the
  lexicon.
- **Check a tool's remove path, not only its add path.** `sync_thesaurus`
  keyed both on the level it was given, so syncing at level one deleted
  every level-two entry, and `admit.py` calls it after every admission.
  Two tools this session had a remove path the add path concealed.
- **Do not describe a property the tree does not have yet.** Said twice:
  once of incremental writes, once of an assumption I had not recorded.
  Both were caught by checking rather than by remembering.
- **The local gate is not the gate.** CI was red for an entire session
  because pyright resolves optional dependencies from a virtual
  environment that exists locally and not on a runner.
- **The disclosure scan checks vocabulary, not description.** A section
  identified the deployment domain using entirely ordinary words. There is
  no automated answer to that class.
- **Never `git checkout` to undo without checking what else is
  uncommitted.** It cost two authored waves.
- **A long generation run must write as it goes.** Books were written only
  at the end, so one teacher timeout killed a ten-book chunk and lost
  every one of them. Chunking gave checkpointing between chunks and none
  within one.
- **A timeout is not a failure worth raising on.** Over ninety books it is
  an ordinary event. Return empty and let the caller treat it as an
  unusable answer. A non-zero exit still raises, because that is
  misconfiguration rather than slowness.
- **A tool that writes two artifacts must write both or neither.**
  `admit.py` wrote the lexicon, then found a definition bad, and left
  words admitted with nothing defining them, which is the state the
  closure gate exists to forbid.
- **The corpus validator is more permissive than the lexicon.** It accepts
  a word by stripping suffixes, so `clouds` passes on the strength of
  `cloud`. Exact tokenisation is the stricter check and it found twelve
  plurals nothing else had, and later `stared` and `warmed` in two books
  that had already passed.
- **Subtracting an existing form is wrong if the form sits at a higher
  level.** `admit.py` dropped `depends` from `depend` because a level-six
  term already spelled it, and admitted a level-one verb missing a form it
  needs at level one. Deduplicate against what is admissible here.
- **A form may not collide with another term's headword.** `depends` and
  `reporting` were headwords at level six, which is what an inflected form
  filed as a base word looks like. Folding each into its base verb was the
  fix; adding the form to the base as well was not.
- **The teacher reaching for a word is evidence.** Two books could not be
  finished by generation after six attempts each, and the rejects were a
  coherent treasure-hunt vocabulary. Six spreads were authored by hand
  instead, which the operator's rule already permits: edit the story, do
  not reject it.

## Watch these two numbers

**The ostensive seed size**, and **books against schedule units**. The
first guards the self-hosting claim. The second is the honest measure of
how much corpus exists.
