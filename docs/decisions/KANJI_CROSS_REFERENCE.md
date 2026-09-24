# Concepts derived from a first-grade kanji standard

**Decided 2026-09-24.** Eighteen concepts were added to the graph after
cross-referencing the 80 first-grade kyōiku kanji, the characters taught to
every Japanese child in their first school year.

## Why this list

It is an externally attested answer to a question this project otherwise
has to guess at. **Which concepts does a curriculum designer, working
independently and at national scale, judge a six-year-old should hold?**

The characters are also unusually good at exposing concept clusters,
because a single character carries a direct sense and a compound sense that
a designer had to consider together. 日 is the sun and it is Sunday. 木 is a
tree and it is Thursday. The set 日月火水木金土 is simultaneously sun, moon,
fire, water, tree, metal and earth, and the seven days of the week, so it
carries both the substances and the fact that time comes round again.

## What the cross-reference yielded

| Domain | Added |
| --- | --- |
| `directed_physical_interactions` | `inside_and_outside`, `moving_and_still`, `force`, `material`, `liquid`, `air`, `heat`, `sound`, `shape`, `weather` |
| `record_keeping` | `cycle` |
| `cybernetic_biological_systems` | `plant`, `animal`, `body_part` |
| `compressed_communication` | `name`, `writing` |
| `institutional_interfacing` | `someone_in_charge`, `people_together` |

**Two domains that held nothing now hold something.** 犬虫貝 and 木林森花草
gave `animal` and `plant`, and 目耳口手足 gave `body_part`, which is the
first content in `cybernetic_biological_systems`. 王 and 村町 gave
`someone_in_charge` and `people_together`, the first content in
`institutional_interfacing`.

Characters already covered by the graph were left alone. 一 through 千 map
to counting, number word order and place value. 上下左右中 to spatial
position and direction. 大小赤青白 to physical property. 人子女男 to person.
見 to knowing. 正 to a claim under test.

## Where the mapping was not taken at face value

**木林森 is one tree, then woods, then forest.** It is the clearest
statement of grouping in the whole set, and grouping is already a
mathematics concept. The characters were mapped to `plant` rather than used
to duplicate it.

**円 is a circle, which is geometry, which is mathematics.** Mathematics is
frozen by the ablation, so adding a geometric concept there would change
the treatment domain's membership. `shape` went to
`directed_physical_interactions` instead, where at level one it is a
perceptible property of an object rather than a formal object. The geometry
belongs at level three and later.

**空 is both sky and empty.** `emptiness` already existed, so only the
substance sense was new, which became `air`, the thing that fills a cup
called empty.

## The rule this bends, and why

`DOMAIN_SET.md` records that the graph follows content, because concepts no
record teaches encode guesses where changing them is most expensive.
**These eighteen were added before any record teaches them.**

The rule exists to keep speculation out of the graph. These are not
speculation. They are an external, national-scale, long-standing curriculum
standard, which is the same class of evidence as the hand-authored
primitive register, itself placed in the graph before records existed.

All eighteen are scheduled at level one in the same change, so the gap
between a concept existing and a record teaching it is a schedule entry
rather than an open question.

## Verified, and checked afterwards

The 80 characters were read from the published standard rather than
recalled.

**The ablation is untouched and this was measured, not assumed.** No
concept was added to either ablation domain. After the addition, the
failure analysis arm still reaches zero mathematics concepts, the two arms
still share only `change`, `duration` and `sequence`, and internal depth is
still 10 against 6.
