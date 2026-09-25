# Current brief. Finish level one's reference material

**Written 2026-09-25 for self-directed work.** Delete when the completion
condition in `COMPLETION_CONDITION.md` is met.

## The goals, and why these two

**One. Define every level-one word that is not in the seed.** 306 of 765
are defined and closure is 100 percent. The remaining 427 are the stated
priority, the applied proof that the lexicon is closed, and they need no
operator input.

**Two. Author synonym sets in the thesaurus.** The operator asked for
them and ranked them below the dictionary. 835 entries carry zero
synonyms. The structure and the check already exist.

**Explicitly not in scope.** The ablation needs a pre-registration that
needs a variance measurement nobody has run. Levels three and up need
profile-derived subject weighting, which the handoff records as a
disclosure decision. Publishing is the operator's. None of these can move
without input, so none belongs in a loop.

## How the work goes

Draft against the available vocabulary, which is the seed plus everything
already grounded. **Validate mechanically before writing anything.** Three
drafts were rejected by the closure check this session and none reached a
file. Patch cycles by grounding one member on the seed and letting the
rest keep referring to it.

## Wrong turns, all of them made once already

- **Do not run large generation passes.** Measured: acceptance fell 22.6,
  16.4, then 6.0 percent. A 480-request pass yielded 29 definitions while
  20 authored ones closed the round. The generator is worth using only on
  concrete nouns.
- **Do not read acceptance as progress.** Read closure. Two interventions
  raised acceptance and moved closure not at all; the one that looked like
  a third failure was the only one that worked.
- **Do not grow the ostensive seed to make closure easy.** It went 33 to
  37 once and has held at 37 for two rounds. **A large enough seed closes
  any lexicon**, so the claim is only as strong as the seed is small. Add
  a word only when it cannot be defined except as not-its-opposite.
- **Do not assume a word is core.** `done`, `taken` and `doing` were each
  assumed and each wrong. Look it up.
- **A heuristic needs two pieces of evidence.** Scanning for verbs on a
  single inflection read `a`, `i` and `it` as verbs and wrote six nonsense
  words into core.
- **A guard over records must test `defines.kind`.** Omitting it dropped
  four domain and topic definitions.
- **Never `git checkout` to undo a mistake without checking what else is
  uncommitted.** Doing so cost two authored waves that had to be redone.
- **Run the gate bare and read its exit code.** Piping it takes the exit
  status of the pipe.
- **Commit only closed states.** The closure check is a gate, so this is
  enforced rather than remembered.

## Watch this number

**The size of the ostensive set**, reported by the closure tool as the
seed. If a round needs several new ostensive words to close, say so
rather than absorbing it.
