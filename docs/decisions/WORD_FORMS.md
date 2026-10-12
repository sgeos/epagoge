# Alternates for every class of word

**Recorded 2026-10-10.** Operator direction. A headword is admitted with
its alternates, and a class that lacks an alternate says so. The spelling
rules remain the default. A registration replaces one slot when the rule
is wrong.

## Nouns and number

A count noun has a singular citation form and a plural. The plural is
derived, or it is registered when the spelling rule is wrong.

Three other number patterns are already English and must not be given a
manufactured extra form.

| Pattern | Ordinary name | Flag | What is recorded |
| --- | --- | --- | --- |
| Singular citation form, no plural | Mass noun, also called an uncountable noun | `mass` on `noun` | No plural. Added 2026-09-26. `while` on duration uses the same flag because its plural is archaic |
| Plural citation form, no singular | Plural-only noun. The grammatical name is pluralia tantum | `plural-only` on `noun` | The headword is the plural. There is no singular, and there is no further plural |
| One spelling for both numbers | Invariable noun | None | The plural table maps the word to itself. `sheep` is the example |

`mass` and `plural-only` together are refused. Each requires `noun`.

## Verbs

A verb owes the third person, the past, the past participle and the
present participle. A registered slot replaces that one derived form. The
other slots stay derived. This is how an irregular past is recorded
without editing the spelling table for a single word.

## Adjectives and adverbs

An adjective already owed a comparative and a superlative, or it was
marked `periphrastic` when it compares with more and most.

An adverb was not a class. It is one now. It has the same three
possibilities as an adjective.

| Possibility | Flag | Example |
| --- | --- | --- |
| A suffix | the class alone | `soon`, `sooner`, `soonest` |
| More and most | `periphrastic` | `quickly` |
| No compared form | `ungraded` | a sense that does not compare |

`periphrastic` and `ungraded` qualify an adjective or an adverb, and they
contradict each other. Most adverbs in `-ly` are periphrastic. `well`
compares as `better` and `best`, and `badly` compares as `worse` and
`worst`. Those compared forms are already headwords, so the adverb does
not take the surface over.

A word already in the lexicon with an empty part of speech is not
backfilled. Its alternates are not checked. A new adverb has to declare
which of the three possibilities it is. `tools/register_forms.py show`
prints the slots, including the note that a class was never declared.

## How a form is registered

`tools/admit.py` accepts an optional `inflection` object and an optional
`forms` list. A string in `inflection` is that slot. Null means the slot
does not exist. `forms` adds any further surface the slots do not name.

`tools/register_forms.py` does not admit a headword. `show` prints the
slots of a word already in the lexicon. `apply` writes `pos` and
`inflection` onto one existing sense, reloads the vocabulary, and restores
the file if the form checks fail.

A registered form must not be listed on a different headword. A form
shared by two senses of the same word remains ordinary.

## Levels above two

`--level` on `tools/admit.py` is 1 to 7. A word may sit above the level
where its concept is taught. It may not sit below that level. Levels three
to seven have no schedule, and the gate still does not require one, for
the reason recorded in `tools/check.sh`. The first definition written at
such a level creates `curriculum/books/level_N/bk.dictionary.seed.md`.
Closure for that level is not claimed until `tools/validate_closure.py` is
run for it.

## Counting forms under one citation

**Recorded 2026-10-10.** The scan counts each spelling separately. Analysis
and scheduling need the other view, and they need it without loosening the
vocabulary check. A group produced here is a proposal. It does not admit
a word.

`epagoge.lexeme` reads a spelling with the same rules `inflection` uses to
write one. Within one class, a noun's plural joins the noun and a verb's
inflections join the verb. An adjective or an adverb joins the compared
forms the class actually has. `mass`, `plural-only`, `periphrastic`,
`ungraded`, and a registered slot are respected, so a mass noun does not
absorb a manufactured plural and a registered plural is not replaced by
the regular one.

`--pos` on `tools/analyse_lexemes.py` keeps the count inside one class.
The citation of an unknown spelling has no class until the caller names
one. `--across-classes` counts every class of the same citation once. A
spelling that fits several classes of that citation is not divided among
them. `--propose-classes` adds a sibling class the spelling rule allows
when the lexicon has already declared a different class of the same
citation. A sibling class is a hypothesis. It is not evidence that the
language has that class.

A spelling the rules send to two citation forms is unresolved and is not
added to either. `axes` stays unresolved between `ax`, `axe`, and `axis`.
`leaves` stays unresolved between `leaf` and `leave`. An admitted headword
keeps its own spelling, so `saw` does not fold into `see` once `saw` is
admitted. Until then the irregular past is the reading that is kept.

Two further limits are stated rather than hidden. A silent-e base and the
truncation that reproduces the same suffix are both kept when neither is
an admitted headword, and the spelling stays unresolved. Comparison that
doubles a final consonant is not proposed for a word the lexicon does not
declare gradable. `cutter` is not treated as the comparative of an
undeclared `cut`. An adverb in `-ly` joins an admitted adjective of that
stem, including the `-ily` spelling of an adjective in `-y`. It does not
join an unknown stem.

`tools/analyse_lexemes.py schedule` lists each admitted citation, the
classes declared for it, and the level of each sense. `--across-classes`
puts those classes on one record. Without it, a verb admitted early and a
noun admitted later stay separate records. `--level` keeps senses admitted
at that level or earlier.
