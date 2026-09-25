# Current brief. Three problems, and only one of them is mine

**Rewritten 2026-09-25** after the operator framed the project as three
problems rather than one. Delete when `COMPLETION_CONDITION.md` is met.

## The framing, and what it does to the work

`../decisions/THREE_PROBLEMS.md` has it in full. In short:

**Level one is a bootstrapping problem** and it is solved in its
essentials. The lexicon closes, every unit has a book, the model trains
and can be talked to. What remains is volume and length, which is
mechanical.

**Levels two to six are a scheduling problem.** Allocation over a partial
order: every concept and word slotted into a level and revisited at
increasing complexity. Measured 2026-09-25: **24 concepts no schedule
teaches, 68 taught once and never revisited**, and schedules for two of
seven levels.

**Level seven is a transition problem** from an idealised synthetic corpus
to real material. `sources/` is empty, its licensing constraint is
recorded and unexamined, and nothing measures performance on a problem
nobody wrote for the model. It has not started.

## What I recommend pursuing

**A. Level-one length.** The corpus is 37,207 words against 181,600 at the
operator's fifty-words-a-spread standard, and every one of 227 content
books is below the band. `fill_spreads.py` lengthens what exists rather
than adding books, which also avoids the repetition that more books about
the same units produces. **A factor of five without a new book.**

**B. The revisit gap, where it is mechanical.** Half the concepts appear
once, which is the curriculum's own claim going unhonoured. Deciding
*which* level a concept should be revisited at is design. Recording that a
level-two module revisits the level-one concepts its own domain already
teaches is not, and it closes a large part of the gap without a judgement
per concept.

**C. `about` and `teaches` for books.** Written in unrestricted English for
a curator, so nothing is rejected on vocabulary and the teacher cannot
fail the way it fails on corpus prose. Zero of 229 books carry them.

**D. Not mine.** Schedules for levels three to seven. Anything under
`sources/`, including the licensing question. The allocation that takes
the level-two lexicon from 871 words to ten thousand, which is a schedule
nobody has written rather than a backlog of admissions. The endpoint and
estimator for pre-registration item 10, which fixes the sign of any
ordering result.

## What the framing corrected in my own priorities

**I had been treating corpus volume as the universal answer.** It is the
binding constraint on the level-one MVP and was measured to be. It is not
binding at levels two to six, where coverage and consistency are, and a
large corpus with unscheduled concepts would not be progress.

**I had been treating the level-two lexicon as a backlog.** Admitting
words a round at a time from whatever blocked a generator will not produce
ten thousand of them.

## How a round goes

1. Generate or fill a bounded chunk. Runs are additive.
2. Bring every book to its exact spread count.
3. Triage the quarantine: suitable words through `tools/admit.py`,
   unsuitable ones into `substitutions`.
4. A book the teacher cannot finish is finished by hand.
5. Gate, read the exit code, stop, then commit.

## Wrong turns, every one already made once

- **The gate must gate.** A commit ran after `GATE=1` was printed in the
  same invocation. Reading the exit code is not the control. Not issuing
  the commit is. Three commits landed on a red gate this way.
- **The local gate is not the gate.** CI was red for an entire session
  because pyright resolves optional dependencies from a virtual
  environment that exists locally and not on a runner. Check CI.
- **Check a tool's remove path apart from its add path.** `sync_thesaurus`
  keyed both on the level it was given, so syncing at level one deleted
  every level-two entry. The dictionary generator replaced instead of
  accumulating. Two tools whose add path concealed a destructive remove.
- **Moving a sense moves its thesaurus entry.** Sixty-six senses were
  re-filed onto newly authored concepts, and `sync_thesaurus` removes an
  entry whose sense no longer exists, so the entries had to be carried
  across in the same step or 194 antonyms and 132 synonyms would have gone.
- **Deduplicate against what is admissible here.** `admit.py` subtracted
  every existing form regardless of level, so `depend` entered level one
  without `depends`, which a level-six term already spelled.
- **An inflected form filed as a headword is a latent collision.**
  `depends` and `reporting` were level-six headwords. Fold such a word
  into its base verb rather than adding the form to the base as well.
- **Nothing compares a derived form against English.** `admit`, `spend`
  and `quit` inflected to `admited`, `spended` and `quited`, the same
  class as the seven nonsense words found earlier. The doubling check
  closes one narrow class of this and the gap is otherwise open.
- **The corpus validator was more permissive than the lexicon, and is not
  any more.** It accepted a word by stripping suffixes, so `ended` passed
  on the strength of `end` and reached a book in a form the lexicon does
  not carry. Eleven real gaps were found that way, every one of them after
  the word was already written: `rains`, `stared`, `warmed`, `clearing`,
  `facing`, `cleared`, `lighting`, `thoughts`, `ended`, `lived` and
  `winding`. `unlicensed` is exact by default as of 2026-09-25 and asks
  the question the tokeniser asks. The permissive reading survives behind
  `exact=False`, for the case it was right for, which is whether a reader
  would know a word rather than whether the corpus may contain it.
- **Where an inflected form is also a word, the word carries it and the
  base stops listing it.** `clear` and `clearing`, `think` and `thought`,
  `live` against `life` and `living`. Otherwise one form belongs to two
  terms and the lexicon refuses the tree.
- **Do not run large generation passes for definitions.** Acceptance fell
  22.6, 16.4, then 6.0 percent. Authoring yields about a hundred a round.
  **Stories are different**: story acceptance runs near fifty percent, so
  generation is the right tool there and authoring is the fallback.
- **Read closure, not acceptance.** Two interventions raised acceptance
  and moved closure not at all.
- **Do not grow the ostensive seed to make closure easy.** Held at 37 for
  many rounds. A large enough seed closes any lexicon.
- **Do not describe a property the tree does not have yet.** Said twice.
  Both were caught by checking rather than by remembering.
- **Unblocking is not authoring.** The fifty-one concepts made forty-three
  units authorable and wrote no books. Reporting enabling work as though
  it were delivery is the error the concept record exists to avoid.
- **No magic numbers in tests.** An assertion of more than 800 thesaurus
  entries went stale the moment inflections were merged.
- **Never `git checkout` to undo without checking what else is
  uncommitted.** It cost two authored waves.

## Watch these three numbers

**The ostensive seed size**, which guards the self-hosting claim.
**Books at the standard against ninety-two**, which is the honest measure
of how much corpus exists. **Whether a reported figure came from the
corpus or from the synthetic stream**, because the pilot numbers are
already being quoted and only one of those two is this project.
