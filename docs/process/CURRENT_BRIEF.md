# Brief

Opened 2026-10-07 as the second iteration of a self-directed session. The
era-overlap brief and condition are retained in
`evals/review/level_2_food_blockers/` as evidence of the completed scope.

## Present goals

The level-two lexicon remains the active goal. Measured at the start of this
scope, level two admits 1,049 distinct headwords and 8,951 remain to the
approximate target. The era-overlap pool is exhausted. Confirmatory training
remains blocked, and licensing, experimental and later-schedule decisions
remain with the operator.

## What the retained evidence says

Earlier teacher runs retained every rejected definition with the words that
made it fail. Counted across the retained generation reports, 34 of the 43
blocking words are still unadmitted. Sweet blocked 16 definitions, cooking 8,
and fine, ingredients, sour and root 4 each. Sixteen earlier deferrals are
still unadmitted, and all of them are foods or plants. They are honey, yeast,
nut, peach, plum, lemon, onion, carrot, potato, lettuce, pepper, garlic,
cheese, butter, cream and soup.

## Recommended work

**One. Make the blocker count reproducible.** Add a tool that reads the
retained generation reports and ranks still-unadmitted blocking words by the
number of rejected definitions each blocked, naming the words they blocked.
It must say how many reports it read and refuse a malformed report rather
than skip it. Tests cover the ranking, the admission filter and the refusal.

**Two. Admit the blockers that need no reserved decision.** Write grounded
definitions for blockers such as cook, root, vegetable and stem, choosing the
food and plant senses the rejected replies used. Sweet, sour and sugar stay
out because they wait on the operator's ostensive decision.

**Three. Review all sixteen retained deferrals.** Admit each one that can be
defined by distinguishing properties inside the level without sweet or sour.
Defer the rest and name the missing word. The count of deferrals that remain
blocked only by sweet or sour is the measurement the operator needs.

**Four. Record and verify.** Use an agent-authored batch record with every
decision and reason, measure it, preserve earlier evidence, update the
handoff and changelog, pass the full gate and commit locally.

## Rationale

The teacher reaches for these words because ordinary definitions of food need
them. A blocker admitted once unblocks every later definition that needs it,
so this ordering compounds where a frequency pool does not. The retained
rejections are evidence about the corpus rather than about a source, which
`docs/decisions/LEXICON_SOURCING.md` distinguishes.

## Wrong turns to avoid

Do not define a fruit by colour and shape alone when those do not
distinguish it from another admitted fruit. Do not use sweet, sour or a
synonym standing in for them, such as nice-tasting. Do not admit skin or stone
fruit senses implicitly through a definition that relies on them. Those are
recorded unresolved reviews. A definition may say a fruit has a stone inside
only where stone in its admitted sense covers it, and otherwise must avoid it.
Do not reuse a retained teacher reply without marking it as an adaptation.

Carry forward the iteration-one lessons. Generated forms are checked by the
gate, not by eye, so irregular verbs, plurals and doubling go into the
inflection tables. Counts come from tools, never from arithmetic. The gate
runs alone and its exit status is read before any commit. Nothing is pushed
without operator authorization.
