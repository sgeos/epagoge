# What each level is calibrated to

**Recorded 2026-09-25.** Operator direction, replacing the looser reading
in `BOOK_FORMATS.md`. A level is named by **the grade a reader is ready to
enter** once that level is complete, which is sharper than naming a band.

## The ladder

| Level | Ready to enter | Material |
| --- | --- | --- |
| 1 | Kindergarten | Picture books |
| 2 | Fifth grade | Books and textbooks |
| 3 | Eighth grade | Books, textbooks, references |
| 4 | Twelfth grade | Books, textbooks, references |
| 5 | University senior year | Books, textbooks, academic papers |
| 6 | Graduate through all-but-dissertation | Books, textbooks, academic papers |
| 7 | Post-graduate in practice | Books, textbooks, academic papers |

**This corrects the earlier reading.** `BOOK_FORMATS.md` took level two as
early elementary, roughly grades one and two, from the level-two
vocabulary already in the tree. The operator's mapping puts it five school
years later, at the end of fourth grade, which makes the sixty-four page
figure recorded there **too short by a wide margin**.

### The first step is the longest

Level one to level two spans five school years. Every later step spans
three or four. **Level one is also the smallest budget**, so the corpus
grows least exactly where the reader grows most, and the level-two lexicon
has to carry that jump.

Whether that is a defect in the ladder or a fact about how reading
develops is not settled here. It is the first thing to revisit if level
two proves unreachable from level one.

## Three axes, and what is measured

### Word count

Token budgets are already recorded in `../spec/CURRICULUM_LEVELS.md` and
are not changed. The page counts below follow from binding, since a book
is bound in signatures of sixteen pages.

| Level | Tokens | Pages | Signatures |
| --- | --- | --- | --- |
| 1 | 10^6 to 10^7 | **32** | 2 |
| 2 | 10^7 to 10^8 | **160** | 10 |
| 3 | 10^8 | **224** | 14 |
| 4 | 10^8 to 10^9 | **320** | 20 |
| 5 to 7 | 10^9 and up | **not a book count** | — |

**Above level four the unit stops being a book.** A paper is eight to
twenty pages and a monograph is bound to no standard length, so a spread
count measures nothing. The format standard applies to levels one through
four and the artifact at levels five through seven is the paper.

### Lexicon

**Measured**: level one admits **738** words, level two **772**.

**Proposed, and not measured**: the controlled lexicon roughly doubles per
level to level four, then opens.

| Level | Controlled lexicon |
| --- | --- |
| 1 | 738, measured |
| 2 | about 2,000 |
| 3 | about 4,000 |
| 4 | about 8,000 |
| 5 and up | **open** |

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

**Measured**: level one teaches 70 concepts at a maximum prerequisite
depth of **5**; level two adds 10 at depth **6**. The graph holds 117
nodes at a maximum depth of **10**.

Depth in the graph is the candidate metric and **it is not yet calibrated
against anything**. A level's complexity ceiling should be the deepest
prerequisite chain it teaches, but no target per level has been set, and
the graph is too small above level two for a target to mean anything yet.

## What this does not settle

**The level-two page count changes from 64 to 160 and nothing has been
built to it.** Level two holds a dictionary and no books.

**The 43 level-one units that only introduce a concept are unaffected.**
They remain blocked on authoring 51 graph concepts.
