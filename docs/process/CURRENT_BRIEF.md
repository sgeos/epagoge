# Current brief. A level-one model worth talking to

**Rewritten 2026-09-25** after operator direction changed the goal: a
level-one model that external parties can satisfactorily interact with,
with poor performance read as a combination of a training problem and a
corpus problem. Delete when `COMPLETION_CONDITION.md` is met.

## Where the seven goals stand

| # | Goal | State |
| --- | --- | --- |
| 1 | Level-one dictionary and closure | **Done.** Closure 100 percent |
| 2 | Thesaurus | **Done** |
| 3 | Missing words | **Done, and continuous** |
| 4 | Level-one corpus draft | **Done.** 92 of 92 units, every book at 16 spreads |
| 5 | Train a level-one model | **Done**, and it can now be talked to |
| 6 | Level-two dictionary and thesaurus | **Done** |
| 7 | Level-two ablation | **Blocked** on corpus scale and on item 10 |

## The goal now, and the measurement that prices it

**A model external parties can satisfactorily interact with.** Three
measurements say what that costs and they agree.

**It is a corpus problem, not a training problem, and that is measured
rather than argued.** Sweeping steps against width separates the two,
because a model short of training shows a small gap between training and
held-out loss while a model short of data shows a widening one. Every row
widened. At width 256 and 3,200 steps the model reaches a training loss
of 0.040 and a held-out loss of 7.794 against ln(2253) = 7.72 for
uniform: it memorises 45,000 tokens perfectly and predicts held-out text
worse than chance.

**The best reachable figure on this corpus is perplexity 133**, at width
256 and four hundred steps. That is what the samples sound like.

**Held-out loss falls linearly in the logarithm of corpus size**, about
0.29 nats a doubling, measured over four fractions. Extrapolated, 10^6
tokens gives perplexity near 35 and 10^7 near 13. See
`../../evals/pilot/LEVEL_ONE_SCALING.md`, including why the
extrapolation is both optimistic and pessimistic.

## What I recommend pursuing, and what I do not

**A. Corpus volume, and nothing else comes close.** `--variants N` writes
an Nth book per unit at about twenty-five books a round. 10^6 tokens is
roughly fifty books a unit against the two or three that exist, so this
is many sessions of work and every round moves the number.

**B. Keep the gate green and closure intact while it grows.** Each round
triages its quarantine: suitable words through `tools/admit.py`,
unsuitable ones into `substitutions`.

**C. Re-measure rather than trust the curve.** The scaling fit is
extrapolated over 2.3 orders of magnitude from 0.9. Re-run
`diagnose_level.py --fractions` when the corpus has doubled, and correct
the record if it bends.

**D. Training work, and it is second order.** Early stopping on held-out
loss, and dropout and weight decay are both at their defaults and
untuned. Worth doing when the corpus is large enough that the tuning
means something. **Not worth doing now**, because none of it turns
perplexity 133 into a model anyone wants to talk to.

**E. Not recommended, and these are the operator's.** The endpoint and
estimator for item 10, which fixes the sign of any ordering result. The
minimum meaningful effect for item 7. Schedules above level two. The
ablation itself, which is not attemptable until those land.

## How a book round goes

Generate a bounded chunk, top it up, then gate.

1. `generators/generate_books.py --limit 25 --variants N`. Runs are
   additive and skip units already holding N books. Each book is written
   as soon as it is built.
2. `generators/extend_books.py` until nothing more can be added. It tops
   up a short book and trims a long one from the end.
3. **Triage the quarantine.** Both generators write one, and the reject
   names the words that blocked it.
4. **A book the teacher cannot finish is finished by hand.** The operator
   rule is to edit the story, not reject it.
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
