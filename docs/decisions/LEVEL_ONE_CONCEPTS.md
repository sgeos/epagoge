# Authoring the fifty-one level-one concepts the schedule only planned

**Recorded 2026-09-25.** The level-one schedule named ninety-two units.
Forty-nine could have a book and forty-three could not, because those
forty-three carried only `introduces`, which names a concept the graph
does not hold. A unit whose concept is absent has no prerequisites, no
domain and no words, so the generator skipped it and the corpus stopped at
half a level through no fault of generation.

This records the fifty-one concepts authored to close that, and the three
things that had to be true before a book could be written for any of them.

## The gap was never throughput

**Reporting it as "48 of 92 books" implied a generation shortfall.** It was
a graph question. Generation was never asked for the missing forty-three
and would have refused if it had been, since `words_for` returns nothing
for a concept no word names.

## What a unit needs before it can be authored

Three conditions, and all three are enforced.

1. **A node in the graph**, carrying a domain. `validate_schedule` refuses
   a unit that teaches a concept the graph lacks, and refuses one whose
   concept belongs to a different domain than the unit's plan.
2. **Prerequisites scheduled at this level or earlier.** Every prerequisite
   chosen here is drawn from the seventy level-one concepts the graph
   already held, or from the fifty-one authored alongside it.
3. **At least one word.** `_check_lexicalisation` refuses a scheduled
   concept that no word names, so the lexicon work is not optional
   decoration on the graph work.

## Domain assignment follows the schedule, not taste

Each concept's domain is the domain of the unit that teaches it, because
`validate_schedule` requires exactly that. The distribution is therefore
given rather than chosen.

| Domain | New concepts |
| --- | --- |
| normative_adjudication | 8 |
| compressed_communication | 7 |
| history_and_philosophy_of_science | 7 |
| institutional_interfacing | 7 |
| agentic_operations | 6 |
| cybernetic_biological_systems | 5 |
| record_keeping | 4 |
| accounting | 3 |
| mathematics_and_formal_logic | 3 |
| directed_physical_interactions | 1 |

**`history_and_philosophy_of_science` held no concept at all before this**
and the graph reported it as awaiting content for as long as the domain has
existed. No declared domain is empty now.

## Where the words came from, and why most were not new

Fifty-one concepts needed words and only twenty-nine words were admitted.
The rest were already in the lexicon under a broader concept, because the
specific concept did not exist when they were filed.

- **Sixty-six senses were re-filed.** `fair` and `unfair` sat under
  `good_and_bad` and belong under `fair_and_unfair`. `agree` and `disagree`
  sat under `checking`. `story` and `tale` sat under `writing`.
- **Twenty senses were added to words that are genuinely polysemous.**
  `old` already meant not young and now also means out of date. `mind`
  already meant tending and now also means the thing you change. `hard`
  already meant not soft and now also describes a choice. The lexicon has
  been sense-keyed since the `set` and `swallow` decision, so this needed
  no new mechanism.
- **Twenty-nine words were admitted**, each with a definition that
  reduces to the seed. Nine concepts would otherwise have had a word that
  named them only loosely, and two, `mistake` and `judged_by_another`,
  would have had none.

**A re-filed sense carries its thesaurus entry with it.** Moving the
sense and leaving the entry would have dropped the relations on sixty-six
words, since `sync_thesaurus` removes an entry whose sense no longer
exists. All 194 antonyms and 132 synonyms survived the move, and that was
checked rather than assumed.

## What this does not settle

**No book has been written for any of the forty-three.** The units are
authorable and forty-six of ninety-two still have no book. Enabling the
work is not doing the work, and reporting it as though it were is the
error this record exists to avoid repeating.

**Prerequisite choices are judgements and are not measured.** That
`being_wrong` rests on `guess`, `checking` and `mistake` is defensible and
is not derived from anything. The graph now reports a maximum level-one
prerequisite depth of eight, against five before, and no target exists to
say whether eight is right.
