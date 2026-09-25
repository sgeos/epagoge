# What each level is calibrated to

**Recorded 2026-09-25.** Operator direction, replacing the looser reading
in `BOOK_FORMATS.md`. A level is named by **the grade a reader is ready to
enter** once that level is complete, which is sharper than naming a band.

## The ladder

| Level | Ready to enter | Material |
| --- | --- | --- |
| 1 | Kindergarten | Picture books |
| 2 | Fourth grade | Books and textbooks |
| 3 | Eighth grade | Books, textbooks, references |
| 4 | Twelfth grade | Books, textbooks, references |
| 5 | University senior year | Books, textbooks, academic papers |
| 6 | Graduate through all-but-dissertation | Books, textbooks, academic papers |
| 7 | Post-graduate in practice | Books, textbooks, academic papers |

**This corrects the earlier reading.** `BOOK_FORMATS.md` took level two as
early elementary, roughly grades one and two, from the level-two
vocabulary already in the tree. The operator's mapping puts it at the end
of third grade, which makes the sixty-four page figure recorded there too
short.

### The spacing, measured

Counting cumulative years of formal education completed at each level's
target, the ladder is even where it can be.

| Level | Target | Years completed | Gap |
| --- | --- | --- | --- |
| 1 | Entering kindergarten | 0 | — |
| 2 | Entering fourth grade | 4 | 4 |
| 3 | Entering eighth grade | 8 | 4 |
| 4 | Entering twelfth grade | 12 | 4 |
| 5 | Entering university senior year | 16 | 4 |
| 6 | All but dissertation | about 20 | about 4 |
| 7 | Post-graduate in practice | about 24 | about 4 |

**Four years at every step.** Kindergarten through twelfth grade is
thirteen years of schooling, so entering twelfth grade is twelve completed
and finishing high school is thirteen. Three university years on top of
that is sixteen, which is why level four to level five is four years and
not three.

**An earlier version of this record said fifteen and was wrong.** The
arithmetic error made the ladder look uneven where it is not.

**Levels six and seven are approximate.** Their boundaries are defined by
candidacy and by practice rather than by enrolment, so the gaps are about
four rather than exactly four. No page count or lexicon target depends on
that stretch, since above level four the unit is a paper.

Level one carries the same four-year step as every other on the smallest
token budget in the scheme, so the corpus grows least where the reader
grows fastest. That is the first thing to revisit if level two proves
unreachable from level one.

## Three axes, and what is measured

### Word count

Token budgets are already recorded in `../spec/CURRICULUM_LEVELS.md` and
are not changed. The page counts below follow from binding, since a book
is bound in signatures of sixteen pages.

| Level | Tokens | Pages | Signatures |
| --- | --- | --- | --- |
| 1 | 10^6 to 10^7 | **32** | 2 |
| 2 | 10^7 to 10^8 | **128** | 8 |
| 3 | 10^8 | **224** | 14 |
| 4 | 10^8 to 10^9 | **320** | 20 |
| 5 to 7 | 10^9 and up | **not a book count** | — |

**The four page counts rise by ninety-six, which is six signatures, at
every step.** That regularity was not designed and is not the reason for
any of them. One hundred and twenty-eight pages is an ordinary length for
an early chapter book at the end of third grade, which is why it was
chosen, and the evenness is a consequence worth noting and not evidence
for anything.

### Words on the page

**Operator figure for level two, 2026-09-25.** About one hundred and
twenty-five words to the page, give or take twenty-five, so a spread
carries two hundred to three hundred and a sixty-four spread book runs
between **12,800 and 19,200 words**.

| Level | Words per spread | Words per book |
| --- | --- | --- | --- |
| 1 | **50 plus or minus 30** | **800**, band 320 to 1,280 |
| 2 | **250 plus or minus 50** | **16,000**, band 12,800 to 19,200 |
| 3 | **500 plus or minus 100** | **56,000**, band 44,800 to 67,200 |
| 4 | **500 plus or minus 100** | **80,000**, band 64,000 to 96,000 |

Words per spread is the only length figure stored. Words per page is half
of it and words per book is the binding times it, so both are arithmetic:
a second table in a second unit for one quantity is a table that drifts.

**The level-one figure supersedes a band of 100 to 800 words a book.**

### Measured against it, the level-one corpus is a fifth of its length

**Measured 2026-09-25**: 227 content books, median **164 words**, which is
**10.2 words a spread against a target of 50**. **Every one of the 227 is
below the band.**

The corpus holds 37,207 words and would hold **181,600 at the standard**,
a factor of 4.9 **without a single new book**. That is the cheapest corpus
growth available and it was invisible until the figure existed: the books
were written to sixteen spreads and nobody had said how long a spread is.

**Operator figure for levels three and above, 2026-09-25:** five hundred
words to the spread, being two hundred and fifty to the page, which is the
standard English typesetting metric.

Level one was fixed as a word count directly rather than as a density,
because a picture book's page is mostly picture. Levels five and above are
papers rather than books, so a spread count measures nothing there and
`typical_words` reports none.

**The level-two figure is a range that spans fifty per cent**, which is
wide enough that it will not by itself catch a book of the wrong shape. It
is reported and never enforced, like every other length figure here.

**Above level four the unit stops being a book.** A paper is eight to
twenty pages and a monograph is bound to no standard length, so a spread
count measures nothing. The format standard applies to levels one through
four and the artifact at levels five through seven is the paper.

### Lexicon

**Measured 2026-09-25**, after the fifty-one level-one concepts were
authored: level one admits **769** words, level two **803**. The earlier
figures of 738 and 772 predate that work.

**Proposed, and not measured**: the controlled lexicon roughly doubles per
level to level four, then opens.

| Level | Controlled lexicon | Basis |
| --- | --- | --- |
| 1 | 845, measured | what the corpus needed to close |
| 2 | **about 10,000** | operator figure, consistent with Biemiller |
| 3 | **about 25,000** | extrapolated past Biemiller's range |
| 4 | **about 40,000** | the lower adult estimate |
| 5 and up | **open** | real literature consults no word list |

**Researched 2026-09-25**, with sources and caveats in
`READING_LEVEL_RESEARCH.md`. Biemiller and Slonim put an average reader at
about 6,000 root words at the end of grade 2 and 10,000 at the end of
grade 6, so entering fourth grade interpolates to about 7,000 root words.
This project counts forms rather than roots, so the operator's ten
thousand and Biemiller's seven thousand are the same claim in different
units.

**Adult estimates disagree by a factor of twelve**, from 16,785 lemmas to
200,000 words for comparable populations, so rows three and four are the
weakest here and are placed to be argued with.

The earlier proposal of about 2,000 at level two was mine and was not the
operator's. It also roughly doubled per level, which the operator figure
does not: ten thousand is **twelve times** level one, not double.

**The lexicon is prescriptive while the material is authored and becomes
descriptive when the material is real literature.** That is why it opens
rather than continuing to grow: at level seven the corpus terminates in
unmodified scientific literature, which does not consult a word list.

**A caution on the figures.** Published vocabulary-size estimates by age
exist and are contested, and none is cited here because none was checked.
The controlled lexicon is in any case a different quantity from a reader's
receptive vocabulary: level one admits 738 words to a reader who
recognises several thousand, because a defining vocabulary is deliberately
smaller than a reading one.

### Concept complexity

**Measured 2026-09-25**: level one teaches **121** concepts at a maximum
prerequisite depth of **8**; level two adds 10. The graph holds **168**
nodes at a maximum depth of **10**. The earlier reading of 70 concepts at
depth 5 was taken before `LEVEL_ONE_CONCEPTS.md` added fifty-one nodes,
and the depth rose because the new concepts sit on top of the old ones
rather than beside them.

Depth in the graph is the candidate metric and **it is not yet calibrated
against anything**. A level's complexity ceiling should be the deepest
prerequisite chain it teaches, but no target per level has been set, and
the graph is too small above level two for a target to mean anything yet.

## What this does not settle

**The level-two page count changes from 64 to 128 and nothing has been
built to it.** Level two holds a dictionary and a thesaurus and no books.

**Concept complexity per level is still uncalibrated.** Depth is the
candidate metric, level one now measures eight, and no target says whether
eight is right. The number moved because concepts were added, which is
evidence that the metric tracks the graph rather than the level.

## The level-two lexicon is far short of its own target

**Measured 2026-09-25.** Level two admits **871 words against level one's
845**, which is **twenty-six more**. The operator figure is about ten
thousand, so the level-two lexicon is at **nine per cent** of its target
and needs some nine thousand words admitted.

**This is the binding constraint on level-two modules**, in the same way
corpus size is the binding constraint on the level-one model. A module is
sixty-four spreads of connected fourth-grade prose, and a lexicon that is
three per cent larger than a kindergarten one cannot carry it. The teacher
is refused on ordinary fourth-grade words and the module is written in
picture-book vocabulary at seventy times the length.

**Backporting made this worse and was still right.** Moving `ten`,
`group`, `pile`, `set`, `unchanged` and `knock` down to level one was
correct, and each one narrowed the gap between the levels from the other
side.

The work is an admissions pass against level two of the same kind that
built level one, and it is not a decision anyone has to make first.
