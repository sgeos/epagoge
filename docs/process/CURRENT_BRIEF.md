# Current brief. Finish the level-one corpus, then measure the trainer

**Rewritten 2026-09-25**, third revision of the day, after every
level-one book reached the spread standard and the fifty-one missing
graph concepts were authored. Delete when `COMPLETION_CONDITION.md` is
met.

## Where the seven goals stand

| # | Goal | State | Real blocker |
| --- | --- | --- | --- |
| 1 | Dictionary coverage and closure | **Done.** 732 of 732 at level one, 766 of 766 at level two, closure 100 percent | — |
| 2 | Thesaurus, synonyms and antonyms | **Done.** 849 entries, 194 antonyms, 132 synonyms | — |
| 3 | Missing words added to both | **Done, and continuous** through `tools/admit.py` | — |
| 4 | Full level-one corpus draft | **Done. 92 of 92 units, every book at sixteen spreads** | — |
| 5 | Train a level-one model | **Done, and the result is a null that means nothing.** Eight paired seeds on the real corpus | Corpus scale, for a result that means anything |
| 6 | Level-two dictionary and thesaurus | **Done** | — |
| 7 | Level-two ablation | Blocked, and now measurably so | **Corpus scale**, plus decisions not mine |

## What I recommend pursuing, and what I do not

**A. Done.** All ninety-two units have a book at sixteen spreads.

**A2, which replaces it: more books per unit.** Twelve per topic is the
low end of `CORPUS_SCALE.md` and is where an ordering comparison stops
being degenerate. Ordinary generation work at eleven times the volume
already done, needing no decision from anyone.

**B. Closure, coverage and the gate hold the whole way.** The corpus and
the lexicon grow together. A word the teacher reaches for is evidence, and
`tools/admit.py` is the path for the suitable ones.

**C. Re-measure variance on the real corpus.** **The variance pilot has
already run**, on 2026-09-24, and the sentence in
`evals/PRE_REGISTRATION.md` calling it the single largest unblocker that
depends on nothing predates that run. What is outstanding is narrower and
`evals/pilot/README.md` names it: the measured sigma of 0.0750, paired
standard deviation of 0.0233 and correlation of 0.9539 come from **a
synthetic second-order Markov stream at 818,000 parameters**, and the
correlation is the number most likely to move on natural language. Once
item A lands there is a real corpus to re-measure on, and the seed count
in item 6 stays provisional until that happens.

**D. Audit the corpus.** Item 11's acceptance ceiling is pending the first
audit, and an audit needs a corpus. A sampled per-domain error rate is
reportable without any decision the operator has not made, and the ceiling
itself stays open.

**E. Not recommended, and these are the operator's.** The minimum
detectable effect for item 7 needs justifying from the literature. The
endpoint decision for items 9 and 10 follows from it. Schedules for levels
three through seven, and a concept-complexity target per level, are design
work. **The ablation itself is not attemptable** until those land, and
attempting it would produce a number with no threshold to judge it
against.

**A caution on item 6 that item C does not remove.** The pilot ran under
AdamW with cosine decay, and `docs/decisions/TRAINING_TECHNIQUES.md`
adopts maximal update parametrization, Muon and warmup-stable-decay.
Changing the optimiser changes the dynamics, so sigma and rho will not
carry over even after a re-measurement on real text. Implementing those
three is a larger piece of work and is a candidate, not a promise.

## How a book round goes

Generate a bounded chunk, top it up, then gate. Never a whole level in one
pass.

1. `generators/generate_books.py --limit 8`. Runs are additive and skip
   units that already have a book. Each book is written as soon as it is
   built, because holding a run's output to the end once lost ten books to
   one timeout.
2. `generators/extend_books.py` until nothing more can be added. A book
   below sixteen spreads is unfinished, not wrong, and its existing lines
   are already true and admissible.
3. **Triage what is left.** Each rejected line names the words that
   blocked it. Suitable words go through `tools/admit.py`, which derives
   the forms, writes the definition through the closure check and syncs
   the thesaurus, all or nothing. Unsuitable words mean rephrasing.
4. **A book the teacher cannot finish is finished by hand.** Two books
   resisted six attempts each because the teacher had settled into a
   treasure-hunt vocabulary the level does not hold. Six spreads were
   authored directly. The operator's rule is to edit the story, not reject
   it, and that applies to me as much as to the generator.
5. Gate, read the exit code, stop, then commit.

**The gate now enforces `--spreads 16`.** A freshly generated book is
short until it is topped up, so a chunk is not committable until its books
are at the standard. That is the intended shape: the gate refuses an
unfinished corpus.

## The sequencing claim, corrected by measurement

**I claimed one book per unit was the minimum orderable set an ablation
could use. It is not, and now there is a number.** The completed draft is
**7,998 tokens**, which is fifty-three training chunks. At batch eight
that is seven batches, so an 800-step run cycles them about a hundred and
fourteen times and the ordering stops mattering after the first pass.
Measured 2026-09-25: rho 0.9993, paired standard deviation 0.00344, and a
requirement table claiming one seed per arm. All artifact. See
`../../evals/pilot/LEVEL_ONE_VARIANCE.md`.

**The binding constraint is corpus scale.** 7,998 tokens against a
level-one budget of 10^6 to 10^7 is a factor of 125 to 1,250 short.
`CORPUS_SCALE.md` asks for twelve to six hundred books per topic and the
corpus holds one, so the draft is about a twelfth of the low end.

A draft is one book per unit and that target is met. **Say which is meant
whenever reporting**, because conflating a draft with a trainable corpus
overstates the project by a factor of twelve at the very least.

## What done means for 5 and 7

**A run that completes and reports honestly.** The corpus will be far
below the scale at which an ordering effect could be detected, and the
published literature already reports such effects as weak and
inconsistent at full scale. **Expect a null. Record it as a null.** The
pre-registered threshold decides, not the sign of the difference.

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
- **The corpus validator is more permissive than the lexicon**, because it
  accepts a word by stripping suffixes. Exact tokenisation is the stronger
  check and has now found a real missing form six times.
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
