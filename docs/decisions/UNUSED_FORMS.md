# A judgement on every unused surface form

**Decided 2026-09-26**, on operator instruction to make the call per word
rather than leave the count standing. `tools/unused_words.py --level 1
--out <file>` regenerates the list.

**The count was 688 when it was last reported and is 535 now.** The
intervening work used 146 of them, and wholly unused headwords fell from 11
to 4. **So the count was never the defect.** Most of what it measured was a
corpus that had not been written yet.

## The rule per class, which is the judgement for most of them

Every form is one of three things, and the lexicon cannot tell which.

**An inflection of a word the corpus uses: KEEP.** 494 of the 535. Plurals
of concrete nouns, comparatives and superlatives of gradable adjectives,
and the regular verb forms. `cats`, `biggest`, `accepting`. Each is real
English that a writer may reach for, and admitting a word means admitting
its forms. **Nothing is gained by culling a form that would be correct if
written**, and a corpus that has used 1,509 of 2,044 forms after one day of
lengthening is not carrying dead weight so much as unfinished writing.

**A form that is not English: CULL.** Seven, named below. These are
manufactured by a rule applied where it does not hold, and they sit in the
tokeniser where the model can emit them.

**A headword no module uses at all: DRAFT OR DROP.** Four remain: `boss`,
`forbidden`, `hook`, `insect`. Each is a real word with no book reaching
for it. Recorded for the operator rather than decided here, because the
answer is whether the curriculum wants the idea, which is not a fact about
the lexicon.

## The seven culled, one at a time

| Form | Why | Cause |
| --- | --- | --- |
| `farrer` | Not English. `further` is admitted | Regular rule on an irregular word |
| `farrest` | Not English. `furthest` is admitted | The same |
| `thiefs` | Not English. `thieves` was admitted | `thief` missing from the irregulars |
| `fulls` | The noun sense has no plural | No way to mark a mass noun |
| `funs` | `fun` is a mass noun here | The same |
| `magics` | `magic` is a mass noun here | The same |
| `copieds` | Not English, and its base was not a word | A form filed as a headword |

## Two defects in the lexicon's model, which is the real finding

**Judging the forms one at a time found what no other check could**,
because a form nobody writes is invisible to every check that reads the
corpus.

**`thief` was missing from `IRREGULAR_PLURAL`.** The table had `leaf`,
`shelf`, `knife`, `life`, `wife`, `loaf`, `half` and `self` and not this
one, so the lexicon carried both `thiefs` and `thieves`. Added.

**The lexicon could not say that a noun has no plural.** The rule requiring
every noun's plural to be admissible is right for count nouns and
manufactures nonsense for the rest. `pos` now accepts `mass` as a qualifier
on `noun`, the rule skips it, and `fun`, `magic` and the noun sense of
`full` carry it. A `mass` without a `noun` is refused.

## `copied`, which was three mistakes in one entry

The eighth inflected form found filed as a headword, and the first where
the corpus had built on the error.

**It was recorded as a noun on `written_record` with the plural
`copieds`.** It is a past participle, it is not a noun, and `copieds` is
not a word.

**Four books and the seed dictionary defined it**, and they did not agree
with each other. `r1.written.d01` reads *"A copy is a thing made to look
like another thing"*, which defines the noun **`copy`**. `dict.1.copied`
reads *"Copied is when someone has made a thing the same as another
thing"*, which defines the participle.

**So the lexicon was missing a sense and had invented a word to hold it.**
`copy` existed only as a verb on `toy`. It now also exists as a noun on
`written_record`, which is what four books were already teaching, and the
four records point at it. The participle is a form of the verb, so its
dictionary entry is gone the way `copies` and `copying` never had one.

**A sense-keyed lexicon is what made this fixable.** One word, two senses,
two concepts, and no need to invent a headword to carry the second.

## What this does not settle

**Fourteen forms are real English in a sense the base does not carry**, and
they are the operator's: `furs`, `earths`, `faiths`, `whiles`, `lots`,
`manners`, `tens`, `fives`, `fours`, `sixes`, `hundreds`, `thousands`,
`drunk`, `lighted`. Each is a question about whether the lexicon wants a
second sense, not about whether the form is well formed.

**`drunk` and `lighted` are the two worth deciding soon.** `drunk` is the
correct participle of `drink` and collides with an adjective no picture
book wants. `lighted` is correct but archaic beside `lit`, which is **not**
admitted, so culling it would leave `light` with no past form at all.
