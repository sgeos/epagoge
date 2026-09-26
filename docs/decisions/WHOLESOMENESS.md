# Wholesome age-appropriateness is an acceptance criterion

**Decided 2026-09-26, operator observation.** Prompted with `what is the
cup ?` the level-one model produced:

> i know the cup . the cup is here . i am not empty , not alone . i see the
> cup , not leaving means where is able to the same same cup is here . i is
> cold , not a container in the bright and be . i share it is not gone , not
> strong ,

**It is incoherent and it is wholesome**, and the second is not an
accident. The operator's reading, which is hard to argue against: **this is
a property of the corpus showing through**, and it is worth preserving
deliberately rather than by luck.

## Why it is a real property and not a pleasing accident

**A model reproduces only the registers its corpus contains.** The project
already measured this in the sharpest possible form: the corpus held one
question mark in 4,419 records and the model could not answer a question at
all, and no amount of scale would have fixed it. The same mechanism that
made answering unlearnable makes cruelty unlearnable, if the corpus never
shows it.

**This is the thesis in miniature.** `CORPUS_THESIS.md` argues that a
curated corpus beats a scraped one and that volume is not the universal
answer. Tone is the clearest case available: nothing about a larger scrape
makes a model kinder, and a written corpus gets it for free.

## The criterion, and what it is not

**A record is acceptable when it would be appropriate for a reader at that
level.** At level one that is nominal kindergarten.

**It is not sanitisation and it is not squeamishness.** A wholesome adult
is aware of drunkenness, can name it, and can discuss what follows from it.
The constraint is **age appropriateness of the engagement**, not absence of
the subject. Kindergarten is too early for that conversation; a later level
is not.

**It does not forbid a child sounding like a child.** Small children are
amusing precisely because they say things that would be inappropriate at
greater maturity. A corpus that scrubbed that would be writing adults in
short sentences, which is a different and worse artifact.

## How it is enforced, honestly

**It is not mechanically checkable and the project should not pretend
otherwise.** No check in the gate can tell a wholesome sentence from an
unwholesome one, and a banned-word list would be the by-name enumeration
this project has met five times.

**Three places carry it instead.**

1. **The generation prompt**, which asks for prose for a reader at that
   level. This is where most of the work happens and it is why the property
   is already present.
2. **The lexicon**, which is the one mechanical lever. A word absent from
   the level cannot be written at it. This is why `drunk` is admitted as an
   inflection of `drink` and **not** as an adjective, and the operator's
   reasoning is that the verb is a kindergarten concept and the state is
   not.
3. **Review**, where a record that reads wrong is rejected and the reason
   recorded. `evals/review/` exists for this and holds no verdicts yet.

**So the honest statement is that this is a review criterion with a
lexical lever, and the lever is narrow.** Recording it means the next
session cannot trade it away without noticing.

## The consequence for the lexicon

**A word may be admitted in one part of speech and refused in another.**
`drunk` as a verb inflection, not as an adjective. The lexicon is
sense-keyed, so it can express this, and `docs/decisions/UNUSED_FORMS.md`
records the case that forced it.
