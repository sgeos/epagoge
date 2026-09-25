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

## Second pass, 2026-09-24. Seven more concepts, from polysemy

The first pass treated each character as carrying one sense or two. **Kanji
were grafted onto an existing language**, so a character carries
Chinese-derived readings and native Japanese words mapped on afterwards,
and one character can name several unrelated things. Chinese characters map
more cleanly, having never been grafted. The first pass therefore
undercounted.

### 生 is the outlier

Eleven senses at least. Living, birth, life, raw, fresh, to grow, to
sprout, to produce, pure, and the readings inside 学生 and 先生. It is the
clearest case of one glyph carrying an unrelated set, and it alone supplies
concepts to three different domains, being `living_and_not_living` in
failure analysis, `growing` in cybernetic biological systems, and
`raw_and_made` in physical interactions.

気, 本, 手 and the 上 and 下 pair are the next most loaded.

### Added

| Concept | Domain | From |
| --- | --- | --- |
| `enough` | agentic operations | 足 as suffice, 十 as complete |
| `can_and_cannot` | agentic operations | 力 as ability |
| `way_of_doing` | agentic operations | 手 as means, 手段 |
| `feeling` | agentic operations | 気 as mood and mind |
| `raw_and_made` | physical interactions | 生 as raw |
| `exchange` | accounting | 貝 as currency, 円 and 金 as money |
| `opinion` | institutional interfacing | 見 as view, 意見 |

**Sufficiency and capability are the two that matter most.** Whether there
is enough of something for what it is needed for, and whether an action is
within what the actor can do, were not expressible in the graph at all.
Both are load-bearing for anything operating to a resource budget with a
fixed set of effectors.

**`opinion` closes a gap in the claim taxonomy.** `ATTRIBUTED_POSITION` is
a claim class with no level-one concept behind it until now.

Agentic operations went from three concepts to seven, which is the thinnest
domain in the set becoming merely small.

### Third pass, 2026-09-24. Declined was the wrong bucket

**Method correction.** The second pass sorted senses into covered and
declined, and put eight into declined on the grounds that they belong at a
later level. **Belonging at a later level is not a reason to drop a
concept. It is a level assignment.**

The standing decision in `../spec/CURRICULUM_LEVELS.md` is that every topic
appears at every level as enabling material. A concept assigned to level
three therefore obliges a level-one concept that enables it. Metal at level
one is what makes lead and alloy possible at level three, and dropping
metal because alloy is not level one gets the direction backwards.

**There is also room.** TinyStories ran on roughly fifteen hundred words.
Level one here licenses 508 content words. The constraint that produced the
84 percent rejection is gone and has not been replaced by a tighter one.

**The three buckets, restated.** A sense is covered by an existing concept,
or it is assigned to a level and owes a level-one enabling concept, or it
is not a concept at all.

### Wrongly deferred, now at level one

| Concept | Domain | From | Why level one |
| --- | --- | --- | --- |
| `tending` | cybernetic biological systems | 田 as cultivation | Adding water to a plant is a preschool act |
| `measuring` | record keeping | 正 as exactly | Holding two things together to see which is longer |
| `written_record` | record keeping | 文, 字, 名 | A mark you keep so you know later |
| `metal` | physical interactions | 金 | The category 銅, 銀 and 鉛 are members of |

**Record keeping was the worst of it.** Its scope names measurement,
reference frames, unit accounting, provenance, accuracy, precision,
confidence and currency, and it held five concepts, all of them spatial or
temporal. It had **no measurement concept at all**, and the domain named
for keeping records had no concept of a record. Seven now.

`metal` also carries the specialisation your example describes. It is a
kind of material the way copper, silver and lead are kinds of metal, so the
one glyph supplies the category, a member, and the relation between them.

### Assigned to a later level, with their level-one enabling concept

Not scheduled, because level two currently covers only the two ablation
domains. Recorded so the assignment is not lost.

| Sense | Level | Enabled at level one by |
| --- | --- | --- |
| 足 as addition | 2 | already scheduled at level two |
| 正 as precision | 2 | `measuring` |
| 空 as futility | 3 | `activity` and `change`, doing something and nothing changing |
| 名 as reputation | 3 | `name`, `opinion`, `being_told` |
| 文 as culture | 4 | `people_together` |
| 円 as harmonious | 4 | `physical_property`, smoothness |

### Covered by concepts already present

十 complete by `enough`. 百 and 千 as many by `more_and_fewer`. 上 and 下 as
rank by `someone_in_charge`. 山 as heap by `grouping`. 口 as entrance by
`opening_and_shutting`. 手 as skill by `can_and_cannot`. 見 as visible by
`presence`. 校 as proofread by `checking`. 玉 as egg by `animal`. 白 as
blank by `emptiness` and as confess by `being_told`. 先 as tip and
destination by `direction` and `sequence`. 目 as ordinal by
`number_word_order`. 青 as unripe by the planned `growing`. 本 as true by
the planned `not_both`. 天 as innate by `raw_and_made`.

### Not a concept

赤 as an intensifier, meaning utterly or completely. It modifies and names
nothing.

## Mainland cross-reference, 2026-09-24. Six concepts, one of them predicted

The first-grade first-volume character list of the People's Education Press
unified textbook was obtained and read. Roughly a hundred entries, eleven
of which are pinyin letters rather than characters.

**Evidence class.** This is a textbook implementing the ministry standard,
not the ministry appendix itself, so it is slightly weaker than the
Japanese per-grade table. It is still national in scale and independent of
the Japanese selection, which is what makes a divergence informative.

### The divergence that was predicted

**妈, 爸, 奶, 妹 and 家.** Mother, father, grandmother, younger sister, and
home-or-family. Japanese grade one has 人, 子, 女 and 男 and puts 父, 母,
兄, 弟, 姉 and 妹 later.

`CHARACTER_STANDARDS.md` recorded a hypothesis that if the Chinese first
volume introduced family terms earlier it would point at a concept the
graph lacks, which is **who someone is to someone else**, distinct from
`person` and from `people_together`. It does, and the concept is added as
`family`.

The hypothesis was recorded before the list was obtained. That is the only
prediction in this line of work that has been tested.

### Added

| Concept | Domain | From |
| --- | --- | --- |
| `family` | institutional interfacing | 妈 爸 奶 妹 家 |
| `self_and_other` | agentic operations | 己 自 我 你 |
| `having` | accounting | 有 的 |
| `asking` | compressed communication | 问 |
| `sentence` | compressed communication | 句 |
| `good_and_bad` | normative adjudication | 好 |

**`self_and_other` is the one with the most weight here.** An agent
reasoning about what it can do, what it was told, and what another party
holds, needs the distinction between itself and everything else, and
`person` covered only the other side of it.

**`asking` had its primitive and no concept.** The register carries
others-can-be-asked, and `being_told` covered receiving while nothing
covered requesting.

**`sentence` completes a chain the writing system makes visible.** Letter
to word to sentence is aggregation, the same relation as 木 to 林 to 森,
which the graph does not model as an edge type. Recorded, not fixed.

`normative_adjudication` and `institutional_interfacing` both gain their
first or second node from this pass, leaving one domain empty.

### Confirmations rather than additions

The mainland list independently attests several concepts added here on
other grounds. 尺 as a ruler attests `measuring`. 心 as heart and mind
attests `feeling`. 可 attests `can_and_cannot`. 果 as both fruit and result
attests the `plant` and `cause_and_effect` pair. 词 and 字 attest `word`
and `letter`.

### Taiwan was not usable

Only one lesson's characters were obtained, being 呼, 白, 雲, 前, 游, 噴,
柱, 試, 吸, 氣, 用, 力, 擠, 哇, 又, 第 and 功. Every one of them maps to a
concept already present. **A single lesson is not a sample** and no
conclusion is drawn from it. The Taiwan first-volume list remains
unobtained, and the mainland-against-Taiwan divergence analysis remains
unrun.

## Correction, 2026-09-24. The evidence is weaker than this record claimed

Two further standards were checked after the eighteen concepts were added.

**Three regions solve the same problem three different ways.**

| Region | What the national standard fixes | Grade one |
| --- | --- | --- |
| Japan | **Which characters**, per grade, by name | 80 |
| Mainland China | **How many**, per two-grade band, not which | 1600 recognised across grades one and two |
| Taiwan | **Neither.** Competencies only, publishers choose | 670 in one publisher's grade one |

**The finding that matters.** A published comparison of mainland and
Taiwan first-grade first-volume textbooks reports **61 characters in
common**, being 20.33 percent of the mainland volume and 64.89 percent of
the Taiwan one. Those percentages imply volumes of roughly 300 and 94
characters, which is arithmetic on the published figures rather than a
stated result.

**Two curricula for the same language at the same grade agree on a fifth
of one list.** This record claimed that a national curriculum standard is
"evidence rather than speculation". That claim is weaker than it was
written. A large part of what such a standard encodes is local convention.

**It is not as weak as the number first suggests, and the reason is a
distinction this record should have drawn.** Character selection is not
concept selection. Two curricula can choose different characters that carry
the same concept, and a script where one morpheme is one character makes
selection sensitive to writing-system decisions that have nothing to do
with what a six-year-old should hold. The concept-level agreement is very
probably much higher than twenty percent. **It has not been measured, and
nothing here should be read as though it had.**

**What follows for the eighteen.** They stand. Every one of them is a
concept two of the three regions would recognise, and none rests on a
character choice peculiar to Japanese. But the justification is now
"attested by one national standard and plausible under the others" rather
than "attested, therefore not speculative", and a future addition on the
same basis should carry the weaker claim.

**Taiwan is the better comparator for any repeat**, at roughly 94
characters in the first volume against Japan's 80 for the year. Mainland
grade one at roughly 300, inside a band of 1600, is a different kind of
artifact and yields far less per character.

## Verified, and checked afterwards

The 80 characters were read from the published standard rather than
recalled.

**The ablation is untouched and this was measured, not assumed.** No
concept was added to either ablation domain. After the addition, the
failure analysis arm still reaches zero mathematics concepts, the two arms
still share only `change`, `duration` and `sequence`, and internal depth is
still 10 against 6.
