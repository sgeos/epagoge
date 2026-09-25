# Changelog

All notable changes to this project are documented in this file.

The format follows Keep a Changelog, and the project adheres to Semantic
Versioning.

## [Unreleased]

### Added

- Project skeleton, repository initialisation, and directory layout.
- Decision records for language choice, interpreter version, corpus
  tracking, and the open specification questions.

### Added (continued)

- `docs/architecture/TRAINING_SPINE.md` and
  `docs/decisions/PORTABLE_TRAINING_SPINE.md`. The training framework is
  confined to the model definition and step function. Corpus, tokenizer,
  ordering index, checkpoints, metrics, and evaluation are neutral. A
  unified abstraction over PyTorch, JAX, and MLX was considered and
  rejected.
- `docs/decisions/MODEL_ARCHITECTURE_CONSTRAINTS.md`. Hardware portability
  adopted as restraint rather than as a design programme, with
  comparability against published work outranking it.

## 2026-09-24

### Corrected. Simple word, not simple concept, is the level-one test

- The selection rule had been applied to abstractness. **It belongs to the
  word.** A goal is abstract and "goal" is simple, so it is level one. An
  axiom is no more abstract and "axiom" is not simple, so it is not.
- Several concepts had been deferred for being abstract while their words
  were among the simplest available. Small children hold goals, expressed
  concretely, and say so in one syllable.
- **Foundational vocabulary for the axiomatic treatment of a topic belongs
  at level one**, whatever the topic's later complexity, provided the words
  are simple. Recorded in `docs/spec/CURRICULUM_LEVELS.md`.

### Found. Level one must be able to say that an explanation was simplified

- **Every level above level one simplifies**, in five declared kinds. That
  declaration is metadata. **The model needs the language.**
- A model that cannot say "that is the short way to say it, and there is
  more to it" cannot mark its own simplification in what it produces,
  however carefully the corpus marked it in what the model read.
- The language has to be grounded at level one, because a concept cannot be
  used before it is grounded and every level above is doing the
  simplifying.
- `close_enough`, `more_to_learn`, `real_and_pretend` and `story` added to
  compressed communication, joining `leaving_out`. **The vocabulary of
  disclosed approximation sits at the same level as the cup and the
  crayon.**

### Added. Three more simply-named abstract concepts

- `plan` and `mistake` in agentic operations. Deciding before doing, and
  meaning one thing and doing another.
- `rule` in institutional interfacing. What holds today and held before.
- Level one now **68 units, 61 existing concepts and 36 planned**.

### Found. Two domains were missing the thing they are named for

- Every one of the eleven scope notes read against the concepts its domain
  holds, prompted by record keeping having held no record.
- **Compressed communication had no concept of omission.** The domain is
  named for conveying a claim when the whole of it cannot be conveyed, and
  nothing in it named the part that gets dropped. Every concept it held was
  about the conveying.
- **Agentic operations had no goal.** A domain named for goal-directed
  execution, holding a person, an activity, a need, a capability, a method,
  a feeling and a sufficiency, and no target state to execute toward.
- **Why three passes missed it.** Each asked whether a candidate concept
  was already covered. None asked whether a domain's declared scope was.

### Added. Two nodes and ten plans, from the scope review

- `word` and `letter` as nodes, from 文 and 字, attested the way the other
  kanji-derived concepts are. **`name` now specialises `word`** the way
  `metal` specialises `material`. Graph at **109 nodes**, nine
  specialisation edges.
- `leaving_out`, `goal`, `doing_in_order`, `finished_or_not`, `how_sure`,
  `out_of_date`, `same_amount`, `joining_and_separating`, `promise`,
  `fair_and_unfair` and `guess` as plans.
- **Plans rather than nodes**, because they come from my reading of a scope
  note rather than from an external standard, which is weaker evidence.
  Level one now 61 units, 61 existing concepts and 29 planned.
- `letter` as a word was licensed by `variable`, from a level-three algebra
  record. The glyph sense is the level-one one and is what the word names
  first, so it was remapped.

### Recorded. The scope review is not automatable and is not scheduled

- It requires reading prose against identifiers. No check will catch the
  next instance, and the next instance will look exactly like these three
  did, invisible until someone reads a scope note and a concept list side
  by side.

### Corrected. Declined was the wrong bucket for a later-level concept

- The second pass put eight senses into declined because they belong at a
  later level. **Belonging at a later level is a level assignment, not a
  reason to drop a concept.**
- The standing decision is that every topic appears at every level as
  enabling material, so a concept at level three **obliges** a level-one
  concept that enables it. Metal at level one is what makes lead and alloy
  possible at level three.
- **There is also room.** TinyStories ran on roughly fifteen hundred words
  and level one here licenses 508. The constraint that produced the 84
  percent rejection is gone.
- **Three buckets, restated.** Covered by an existing concept, or assigned
  to a level and owing a level-one enabler, or not a concept at all.

### Added. Four concepts the deferral logic had dropped

- `tending` in cybernetic biological systems, from 田. Adding water to a
  plant is a preschool act, and deferring it was simply wrong.
- `measuring` and `written_record` in record keeping, from 正 and from 文,
  字, 名.
- `metal` in physical interactions, from 金, specialising `material` the
  way 銅, 銀 and 鉛 specialise it. **One glyph supplying a category, a
  member, and the relation between them.**

### Found. Record keeping had no measurement and no record

- Its scope names measurement, reference frames, unit accounting,
  provenance, accuracy, precision, confidence and currency. It held five
  concepts, **all of them spatial or temporal**.
- The domain named for keeping records had no concept of a record. Seven
  concepts now. Graph at **107 nodes**, level one at 49 units.

### Added. Six later-level assignments recorded with their enablers

- Not scheduled, because level two currently covers only the two ablation
  domains. Recorded so the assignment survives.
- 正 as precision at level two, enabled by `measuring`. 空 as futility at
  level three, enabled by `activity` and `change`. 名 as reputation at
  level three, enabled by `name`, `opinion` and `being_told`. 文 as culture
  and 円 as harmonious at level four.
- One sense is genuinely not a concept. 赤 as an intensifier modifies and
  names nothing.

### Added. Seven more concepts from a second pass over the eighty kanji

- The first pass treated each character as carrying one sense or two, and
  **kanji polysemy means that undercounted**. Graph at **103 nodes**, level
  one at 45 units and 55 existing concepts.
- `enough` and `can_and_cannot` in agentic operations, from 足 as suffice
  and 力 as ability. **Whether there is enough of something for what it is
  needed for, and whether an action is within what the actor can do, were
  not expressible in the graph at all.** Both are load-bearing for anything
  operating to a resource budget with a fixed set of effectors.
- `way_of_doing` and `feeling` in agentic operations, from 手段 and 気.
  That domain goes from three concepts to seven.
- `raw_and_made` in physical interactions, from 生 as raw.
- `exchange` in accounting, from 貝 as currency and 円 and 金 as money.
- `opinion` in institutional interfacing, from 意見. **This closes a gap in
  the claim taxonomy**, since `ATTRIBUTED_POSITION` had no level-one
  concept behind it.

### Found. 生 is the outlier, and it spans three domains alone

- Eleven senses at least. Living, birth, life, raw, fresh, to grow, to
  sprout, to produce, pure, and the readings inside 学生 and 先生.
- **One glyph supplying concepts to three domains**, being
  `living_and_not_living` in failure analysis, `growing` in cybernetic
  biological systems, and `raw_and_made` in physical interactions.
- 気, 本, 手 and the 上 and 下 pair are the next most loaded.

### Recorded. Thirty senses considered and declined, with reasons

- Kept so a third pass does not re-raise them. Twenty already covered by
  existing concepts, eight belong at a later level as abstract or
  figurative, and 田 as cultivation was declined deliberately because it
  overlaps the planned `mending` and `keeping_going` closely enough that
  adding it now would prejudge their scope.
- **The ablation was measured afterwards and is unchanged.** Arms 30 and
  27, zero mathematics concepts in the failure arm, internal depth 10
  against 6.

### Corrected. 本 does carry a concept relation, and we already model it

- The record called the tree-to-book chain etymology carrying no concept
  relation. **Wrong.** Root is the pivot, root is a concept, and the chain
  through it is semantic. English performs the identical extension, which
  is why `root_cause` is called that.
- **The relation type we lacked turns out to be one we already model.** A
  plant branches, which is where the mathematical object got its name.
  `plant` now instantiates the `tree` formal structure, yielding transfer
  edges to `fault_tree` and `factor_tree` through the structure the
  character encodes. **Transfer edges four to six.**
- So the formal layer carries metaphorical extension and the specialisation
  layer carries kind-of. Two mechanisms for two relations the radical
  system conflates into one glyph.

### Corrected. One of the two stated obstacles was not an obstacle

- Shinjitai and simplified are the same character for this purpose, 気
  standing to 气 as colour stands to color. **No normalisation table is
  needed** and the pairs listed as divergences are not divergences.
- The remaining obstacle is real. The 300-character list could not be
  extracted from any source reached, so the intersection test is one
  successful fetch away from runnable.

### Found. Kanji carry more concepts than Chinese characters, less cleanly

- Kanji were grafted onto an existing language, so a character carries both
  Chinese-derived readings and native words mapped on afterwards. Chinese
  characters map more cleanly, having never been grafted.
- **So the eighteen concepts extracted from the eighty undercount.** A
  second pass found five senses taken too narrowly. 足 as foot and not
  **enough**. 力 as force and not **capability**. 生 as living and not
  **raw**. 気 as air and not **feeling**. 円 as circle and not **money**.
- **Sufficiency and capability matter most and are deployment-shaped.**
  Whether there is enough of something for what it is needed for, and
  whether an action is within what the actor can do, are not expressible in
  the graph as it stands.
- 金 is the compact illustration. One glyph carrying a category, a member
  of that category, and the specialisation relation generating 銅, 銀, 鉛.
- **Recorded, not acted on.** Five concepts is a design pass.

### Corrected. Japan's list is compositional too. The contrast was wrong

- The comparison framed composition as a criterion mainland China states
  and Japan does not. **That distinction matters far less than the shared
  fact underneath it.**
- 木 is the radical in 林 and 森, where the rest of each character is 木
  again. 柏 and 椰 are kinds of tree and carry 木. 日, 水, 火, 口, 手, 目,
  人, 石, 竹, 糸, 貝 and 虫 are high-yield radicals and all are in the
  eighty.
- **Composition is a structural advantage the writing system encodes**, so
  a designer selecting on simplicity and frequency selects on
  compositionality whether they intend to or not. Radicals are by
  construction the simple frequent base forms. Mainland states the
  criterion; Japan's script enforces it.

### Found. The radical relation is three relations, and we model one

- **Aggregation.** 木 to 林 to 森 is one tree, woods, forest. Not kind-of at
  all. Maps onto `grouping`, not specialisation.
- **Specialisation.** 木 plus a phonetic gives 柏, 椰, 松, 梅. This is what
  `specialises` expresses.
- **Etymological derivation.** 本 is a tree marked at its base, giving
  origin then book. Aids memory, carries no concept relation, maps to
  nothing and should not be forced into anything.

### Changed. The specialisation layer is the radical relation, written out

- **English orthography supplies none of this.** Tree, forest, oak and palm
  share nothing on the page. The graph is where we put explicitly what the
  script encodes for free.
- That layer held **one** edge, which makes it the most under-built
  structure in the project rather than a minor gap, and `anchor_reach` was
  measuring an empty layer.
- Six taxonomic edges written. Seven total, and anchor reach is non-zero
  for seven concepts instead of one. **A start, not a fix.** The layer
  needs authoring against content rather than filling to move a metric.

### Added. `revisits` on a schedule unit, and relation coverage from the schedule

- `teaches` is first introduction only, so a schedule could not say a unit
  returns to a concept. **The spiral curriculum requires exactly that.**
- It is also what lets a unit teach a **relation**, since a graph edge is
  taught by material naming both of its ends and the general end was
  introduced elsewhere.
- `covered_relations` reports the pairs a schedule covers, and the corpus
  validator accepts them. **Third time this pattern has appeared.** A
  schedule states intent, records show progress, and a rule written against
  records alone fires on everything not yet written.
- Eleven new tests, 269 total.

### Corrected. Mainland China does name its characters, and the comparison was wrong

- `CHARACTER_STANDARDS.md` said mainland China fixes how many and not
  which. **Wrong, and challenged rather than caught by a check.**
- The 2022 standard carries two appendices. **《识字、写字教学基本字表》 at
  300 characters** and **《义务教育语文课程常用字表》 at 3500** in two
  tables. The 1600 and 800 counts are targets drawn against named lists.
- **The right comparator is Japan's 80 against mainland's 300**, both named
  national first-level lists. The earlier comparison set a per-grade list
  against a two-year-band target, which is not a like comparison.

### Found. The mainland basic table is selected on a generative criterion

- Its 300 are chosen as simple in form, high in frequency, and **mostly
  usable as structural components of other characters**. Learn these and
  the rest decompose. Japan's list is not stated on that basis.
- **We already measure the analogue and have never used it to select.**
  `downstream_reach` counts how many concepts depend on a given one, which
  is what "serves as a structural component" means here. Level one was
  selected on concreteness and prerequisite depth. Downstream reach belongs
  in that selection too, and the metric already exists and is tested.

### Found. Taiwan has no codified first-level list

- 常用國字標準字體表, 1982, fixes **4808** standard forms.
  國小學童常用字詞調查報告書, 2000, reports frequency over elementary
  readers with **5021** characters.
- Standard forms and frequency data, and no base set. **A de facto
  convergence across publishers is plausible and was not verified.**

### Untested, with the obstacle named

- Whether Japan's 80 are mostly present in mainland's 300 was not run. The
  300-character list could not be extracted from any source reached, and a
  raw intersection would undercount because shinjitai and simplified forms
  diverge for several of the 80.
- Whether the 61-character overlap study normalised across simplified and
  traditional is not stated in what was read. If it did not, that figure
  understates agreement.

### Added. Comparative analysis of three character standards

- `docs/decisions/CHARACTER_STANDARDS.md`. Epistemic status marked
  throughout as verified, derived, or inferred.
- **All three separate recognising from producing, by three mechanisms.**
  Japan by a one-year lag over one list, reading the current grade and
  writing the previous one. Mainland China by subset, 1600 against 800.
  Taiwan by near-parity, 670 against 547. No region asks a beginner to
  produce everything it asks them to recognise.
- **Japan's eighty is a writing-system fact, not a pedagogical one.**
  Japanese writes anything unknown in kana permanently, so 80 characters
  plus a syllabary reads fluently. Chinese has no such fallback, since
  zhuyin and pinyin are withdrawn after being taught.
- **So 80 is not a claim that a six-year-old holds eighty concepts.**
  Taiwan at 670 and mainland at roughly 800 a year describe the same child.

### Found. Our vocabulary ceiling is stricter than any of the three

- A record at level L may use no word licensed above L, which is a
  production ceiling applied to every word. All three human curricula admit
  a wider recognition set than production set.
- **Whether it transfers is genuinely open.** Under next-token prediction
  every token is both read and produced, so the human split does not carry
  over mechanically. Recorded as an option, not a recommendation.
- Possibly implicated in the 41 drafts still rejected at the ceiling in the
  last measured run. **Not tested.**

### Found. Forty-eight level-one concepts is probably low

- The two standards that cannot lean on a syllabary put a first-grader
  nearer 600 to 800 characters. Characters are not concepts and the ratio
  is not one to one, but the current figure sits below all three
  comparators rather than between them. Inferred.
- This supports the lexicon expansion from 64 words to 508 rather than
  arguing it went too far.

### Corrected. A national standard encodes more convention than claimed

- `KANJI_CROSS_REFERENCE.md` justified adding concepts ahead of records by
  calling a national curriculum standard "evidence rather than
  speculation". Two further standards were checked and that claim is
  weaker than it was written.
- **Three regions solve the same problem three ways.** Japan fixes which
  characters, per grade, by name. Mainland China fixes how many, per
  two-grade band, not which. Taiwan fixes neither and leaves selection to
  publishers.
- **Mainland and Taiwan first-grade first volumes share 61 characters**,
  20.33 percent of one and 64.89 percent of the other, implying volumes of
  roughly 300 and 94. Two curricula for the same language at the same
  grade agree on a fifth of one list.
- **Character selection is not concept selection**, which is the
  distinction the original record should have drawn. Concept-level
  agreement is very probably much higher and **has not been measured**.
- The eighteen concepts stand, on the weaker claim "attested by one
  standard and plausible under the others". Taiwan at roughly 94 characters
  is the better comparator for any repeat.

### Changed. The lexicon becomes prescriptive. 64 level-one words to 508

- `docs/decisions/LEXICON.md`. 444 terms added, 142 to **586**.
- **No published list was imported.** The New General Service List is
  CC BY-SA and the TinyStories dataset is CDLA-Sharing, both share-alike
  against a corpus intended for CC0. Ogden's 1930 publication is in the
  United States public domain as of 1 January 2026.
- **Licensing was not the decisive argument. The project's own rule was.**
  Every content word must map to a concept, so importing 850 or 2809 words
  forces either hundreds of speculative concepts into the graph or the
  abandonment of the coverage invariant.
- **The standard is adopted as the coverage target and the mappings are
  authored**, which inverts the usage. The standard tests the graph rather
  than supplying the lexicon.
- Ownership resolved by a precedence order over concepts plus an explicit
  **override table of 25 entries** where precedence got it wrong. A table
  rather than a reordering, because reordering to fix one case silently
  moves others.

### Changed. Two vocabulary rules encoded the old descriptive role

- **Coverage retired.** It required every admitted term to appear in a
  record at its level, which could only fire on a mistake while the
  vocabulary was derived from the corpus. A prescriptive lexicon is
  authored ahead of its corpus. `utilisation` reports the number instead,
  never as a violation, because a low figure means a thin corpus or a
  padded lexicon and does not say which.
- **The lower bound now tests against the schedule.** A schedule states
  where a concept is taught. Records only show where it has been taught so
  far, so a prescriptive lexicon measured against records fails for every
  word whose corpus is not yet written.

### Added. Eighteen concepts from a first-grade kanji standard

- `docs/decisions/KANJI_CROSS_REFERENCE.md`. The 80 first-grade kyōiku
  kanji read from the published standard, not recalled.
- **Two empty domains now hold content.** `plant`, `animal` and
  `body_part` are the first concepts in `cybernetic_biological_systems`;
  `someone_in_charge` and `people_together` the first in
  `institutional_interfacing`. Graph at 96 nodes, 38 level-one units.
- **`shape` went to physical interactions, not mathematics.** A circle is
  geometry and mathematics is frozen by the ablation, so at level one shape
  is a perceptible property rather than a formal object.
- **This bends the rule that the graph follows content**, and the
  justification is that a national curriculum standard is evidence rather
  than speculation, which is the same class as the primitive register. All
  eighteen are scheduled at level one in the same change.
- **The ablation was measured afterwards, not assumed.** Arms unchanged,
  zero mathematics concepts in the failure arm, internal depth still 10
  against 6.

### Measured. Acceptance more than doubled on the same fourteen concepts

| | Before | After |
| --- | --- | --- |
| Accepted | 16 | **36** |
| Rejected at the ceiling | 84 | 41 |

- **A third defect found by reading.** Three drafts were accepted while
  neither capitalised nor terminated, among them "breath lasted long".
  Every word was admissible and the length rule was satisfied, so nothing
  else would have caught them. A sentence-shape check was added.
- **Near-duplicates remain.** Three of the direction drafts were "She
  moves forward", "It goes forward" and "It moves forward". Exact-match
  deduplication does not reach them.

### Added. The generator runs end to end, and its output is not yet usable

- `src/epagoge/prompt.py`, `generators/generate.py`,
  `vocabulary.unlicensed`. Twenty-seven new tests, 257 total.
- **First measured run. 16 accepted of 100 asked for**, 84 rejected at the
  vocabulary ceiling across fourteen level-one concepts.

### Fixed. A word list in a prompt is a suggestion until it is checked

- A first run without validation produced **zero of twelve** admissible
  records, with 29 percent of tokens outside the level-one list.
- Re-asking with the specific offending words named took that to **ten of
  ten**. A generic repeat of the constraint produces a generic repeat of
  the violation.

### Found. The vocabulary is descriptive and is being used prescriptively

- `curriculum/vocabulary.json` was derived to describe the words the sample
  corpus happens to use. At level one that is 156 function words and **64
  content words**, and it was never authored as a lexicon a level-one
  corpus must be writable in.
- Thirty concepts cannot be taught distinctly in 64 content words. The
  measured symptom is the teacher returning the same sentence for different
  concepts because the vocabulary leaves it nowhere else to go.
- **This is the 84 percent.** It is a design decision for the operator, not
  a generator defect.

### Found. Exclusions are correct and semantic drift persists anyway

- `duration` correctly excludes `sequence` and the teacher still returned a
  sequence sentence for it. **Vocabulary is now mechanically enforced.
  Semantics is not.**
- That makes the unimplemented verification layer load-bearing rather than
  optional, on evidence rather than on assumption.

### Fixed. Two defects found by reading the output rather than the metrics

- **A one-word fragment passed every check.** The ceiling asks whether
  every word is admissible, which a fragment satisfies trivially. The line
  splitter had stripped any leading run of digits, dots and dashes, eating
  the first word of a line beginning with a number word. Minimum length
  added and the splitter now only strips an actual list marker.
- **The same sentence was written for two concepts.** "The cup is empty"
  arrived for both `household_object` and `emptiness`, attributing one
  piece of teaching to two ideas. Deduplicated across a run.

### Added. The curriculum schedule, level one complete and level two partial

- `src/epagoge/schedule.py`, `curriculum/schedule/level_01.json`,
  `curriculum/schedule/level_02.json`, `tools/validate_schedule.py`,
  `docs/spec/CURRICULUM_SCHEDULE.md`. Twenty-five new tests, 230 total,
  the module at 100 percent coverage. The gate is now ten checks.
- **The schedule is where a concept gets its level.** The assignment was
  previously implicit in whichever records happened to be written, so an
  ordering mistake could only be found after generating the record that
  contained it. The same prerequisite rule the corpus validator applies to
  records is now applied to the plan.
- **Level one covers all eleven domains.** Twenty-six units, 30 existing
  concepts and 18 planned, budget 10^6 to 10^7 tokens.
- **Level two covers only the two ablation domains**, nine units and 11
  concepts. Partial by design, since the experiment needs those two at
  depth and nothing else at level two is on the critical path. `covers`
  makes the gap declared rather than an oversight.

### Added. Teaches against introduces, so a plan can precede its graph

- A unit names concepts that already exist under `teaches` and concepts it
  will create under `introduces`. The validator checks the first exist and
  the second do not.
- **This is what lets a schedule plan ahead without breaking the rule that
  the graph follows content.** A planned concept is visible as a plan and
  becomes a node only when a record teaches it. Without the split the
  choice is between a graph full of concepts no record teaches and a
  schedule that cannot mention anything new.
- The four empty domains have level-one content planned this way, eighteen
  concepts in total, none of them yet in the graph.

### Changed. Budget shares are derived rather than authored

- Computed from scheduled concept count, so there is no share field to
  drift out of agreement with the units it describes.
- **Level one allocates by what must be grounded, not by subject
  weighting**, because what has to be grounded is a different question from
  what the corpus emphasises. Subject weighting arrives at level three and
  will need its own decision there.

### Added. Twenty-six cross-domain prerequisites, and what drawing them cost

- The graph previously held none, which asserted that every domain is
  teachable without any other. That was false rather than clean. Isolated
  concepts fell from sixteen to **zero**.
- **Including the edge the ablation design forbade.** A hazard rate is a
  rate, so `hazard_rate` requires `rate_of_change`. Routing it through the
  formal layer to keep the domains apart would have recorded something
  false to protect an experiment.

### Fixed. Global depth was the wrong measure, and the edges proved it

- Drawing the edges took failure analysis from depth 6 to **9** against
  mathematics at 10, collapsing the contrast the domain pair was chosen
  for. This was not anticipated when the option was recommended.
- **Global depth measures distance from a root**, so once domains are
  connected it rises for every domain downstream of a deep one. It had been
  serving as a proxy for internal structure, which it only is while the
  domains are disconnected.
- `within_domain_depth` added. Invariant under all twenty-six additions,
  and the contrast it reports is **10 against 6**. `validate_graph.py`
  prints both, because the difference is now load-bearing.

### Changed. One concept excluded from the experiment, not from the graph

- `hazard_rate` is the only failure analysis concept whose closure reaches
  mathematics, and through it twelve mathematics concepts entered the
  failure analysis arm. Excluded from the ablation corpus in
  pre-registration amendment 2.
- **The graph records what is true. The pre-registration declares what the
  experiment covers.** Excluding a concept from an experiment and saying so
  is ordinary. Omitting a true edge would not be.
- Arms are 30 and 27 concepts, sharing only `change`, `duration`, and
  `sequence`, which are level-one anchors both need.

### Fixed. Two proposed edges were wrong and the corpus is what said so

- Thirty edges were drafted and two withdrawn after the corpus validator
  rejected them. `falling` does not require `direction`, since a child sees
  falling before learning that down is a direction.
- **`emptiness` requiring `presence` was right and the corpus was wrong.**
  The sample taught presence only at level five. A level-one record was
  added and the edge restored. Only running the validator distinguished a
  bad edge from a thin corpus.

### Changed. The sample corpus grew because the graph asserts more

- Twenty records to **twenty-eight**. Eight added, closing the chain from
  addition through subtraction, multiplication, variable, division, and
  function to `rate_of_change`, plus records for living things and for
  presence.
- Four vocabulary terms added, 138 to **142**, each bounded below by where
  its concept is taught. Four new tests, 210 total.

### Changed. The foundation-feed metric is retired, and four replace it

- **It was measuring domain immaturity and reporting it as
  disconnection.** The three domains it watched hold fifteen concepts and
  one prerequisite edge between all of them. They feed nothing outward
  because they have almost no structure inward. It also assumed those three
  were foundations, which the domain restructure removed.
- It missed three isolated concepts outside the domains it watched.
- Replaced by isolated concepts, cross-domain prerequisites, specialisation
  edges, and inert formal structures. Seven new tests, 206 total.
  `docs/decisions/GRAPH_CONNECTIVITY.md` carries the diagnosis.

### Found. Three defects the old metric could not see

- **Sixteen of seventy-eight concepts carry no edge of any kind.** Six in
  `directed_physical_interactions`, four in `record_keeping`, three in
  `agentic_operations`, two in `compressed_communication`, and `quantity`
  in `mathematics_and_formal_logic`.
- **The specialisation layer holds one edge in the whole graph.**
  `anchor_reach` was built to measure that layer and returns zero for
  seventy-seven of seventy-eight nodes, which is a property of the layer
  rather than of the concepts. A metric reading zero everywhere is
  indistinguishable from one that is not running, which is the second
  appearance of that failure shape in this project.
- **Two of six formal structures are inert**, instantiated once each, so
  neither can yield a transfer edge. `error_detecting_code` is the one a
  `cybernetic_biological_systems` concept would instantiate.

### Open. Whether true prerequisites cross into the ablation domains

- Both ablation domains are fully prerequisite-self-contained, which is
  what makes a two-domain ablation corpus a closed set.
- Several real prerequisites appear to cross that boundary. A hazard rate
  is a rate, and `rate_of_change` is in mathematics while `hazard_rate` is
  in failure analysis, which is the crossing the design forbids outright.
- Shared structure across that boundary is already handled honestly by the
  formal layer. **Routing a genuine ordering dependency through it to keep
  two domains apart would record something false to protect an
  experimental design.** Two ways out are recorded and neither is chosen.

### Changed. Seven domains became eleven, and domains are now declared

- **The naming rule.** A domain named for an activity excludes what does
  not serve it. A domain named for a bare field admits everything in the
  field. Specialisation and activity-naming are the same property rather
  than two, because an activity has a purpose and a field has an extent.
- Renamed. `mathematics` to `mathematics_and_formal_logic`,
  `physical_world` to `directed_physical_interactions`, `space_and_time` to
  `record_keeping`, `agency` to `agentic_operations`, and `communication`
  to `compressed_communication`. `failure_analysis` and `accounting` keep
  their names, which already passed the rule.
- Added, declared and empty. `history_and_philosophy_of_science`,
  `institutional_interfacing`, `cybernetic_biological_systems`, and
  `normative_adjudication`. The graph follows content.
- `docs/decisions/DOMAIN_SET.md` records all eleven with scope notes, the
  three boundaries that are not readable from the names, and thirteen
  withdrawn candidate names with the reason each failed.

### Added. A domain registry, so an empty domain is visible

- `Domain` in `concept_graph.py`, a `domains` list in `concepts.json`, and
  an `undeclared-domain` violation. Seven new tests, 199 total.
- **Why declare rather than infer.** A set inferred from node membership
  cannot distinguish a domain awaiting content from one nobody chose, so
  the gap is invisible exactly when it most needs to be visible.
- An empty domain is reported and not rejected, because emptiness is the
  expected state between deciding on a domain and writing records for it.
  `validate_graph.py` marks each one and prints the count.

### Changed. Pre-registration amended, and a cost accepted

- Item four amended rather than edited, because it is fixed. Legitimate at
  this date **only because no run has happened and no data exists**, and
  not legitimate after the first run.
- The rename alone changes nothing the design rests on. Membership is
  identical and the depth contrast is unchanged at ten against six. Checked
  rather than assumed. The graph holds zero cross-domain prerequisites of
  any kind, so both ablation domains are fully self-contained.
- Admitting formal logic concepts will change membership, and the depth
  contrast must be measured again at that point. Informal logic is excluded
  and belongs to `institutional_interfacing`.
- Accepted cost. Mathematics is a domain other published ordering ablations
  have used, and a bespoke domain is harder to place beside them.

### Fixed. Two gaps in the disclosure gate, found by running it

- **The scan never reads untracked files.** It iterates `git ls-files`, so
  a new document passes by not being scanned, and the output is
  indistinguishable from a real pass. Working rule is to stage first and
  gate second.
- **The scan never reads commit messages or history**, which is what a push
  publishes. Both were scanned by hand over all commit messages and all 197
  blobs in history against the 27 scrub terms. Both clean.

### Security. Finding A accepted rather than softened

- The option for tighter cover is declined. A second conjunction now exists
  in the eleven domain names, derived from pedagogy by an independent route
  and arriving at the same family.
- The threat model is unintentionally timed disclosure rather than
  disclosure. Reading between the lines is acceptable, lay readers should
  see nothing, and the posture is non-advertisement rather than
  concealment.
- **Scoped to a quiet public repository.** Discovery probability scales
  with attention rather than content, so any deliberate promotion re-opens
  the decision without a file changing.

### Added. Institutional interfacing recorded as a domain, with a bounded scope

- `docs/decisions/INSTITUTIONAL_INTERFACING.md`. A domain teaching
  adversarial claim evaluation and the institutional context that makes it
  necessary. Zero concepts in the graph, because the graph follows content.
- **Four moves, not two.** Attack and defend alone produce a model biased
  toward contradiction, which `CLAUDE.md` records as a failure rather than
  the target and which the elenchos control is built to detect. Assent and
  concede are named alongside them. Concede is the load-bearing move.
- **Two constraints that prevent the domain inverting.** The trigger for
  attack is absence of support and never competition. Every attack
  exemplar requires a matched non-attack exemplar of the same surface
  form, so that the feature the data varies on is support rather than
  aggression.
- **Recognition of instrumental justification is taught, performance is
  not.** The teacher prompt carries the exclusion explicitly, consistent
  with the recorded finding that this teacher conflates adjacent concepts
  otherwise.

### Changed. A naming pattern, and two corrections

- **Domains named for an activity exclude what does not serve it. Domains
  named for a bare field admit everything in the field.** This is why the
  earlier "Operations" suffix instinct was right about the pattern and
  wrong about its three targets, none of which is an activity.
- `civilization_and_society` was proposed, accepted, and then withdrawn in
  favour of `institutional_interfacing` under that test. The general name
  would have required exclusion to be performed by hand in every authoring
  decision.
- **Correction.** An assessment that level one could not carry this domain
  was wrong. It confused the institutional practice with the linguistic
  form. "That is right because" and "that is not true because" carry all
  four moves, depend on `discourse_marker` in `communication`, and yield
  the kind of cross-domain prerequisite the foundation domains lack.

### Open

- A claim explicitly declared to rest on faith has no home in the
  taxonomy. `unsupported` is a rejection class, always rejected, and
  whether `attributed_position` covers a first person declaration is
  undocumented. Adding a class is not obviously safe, since the label is
  also a route past the validator for a claim that simply lacks support.


### Changed. Domain naming assessed, and a correction

- An "Operations" suffix was proposed for the three foundations. **Rejected
  for all three**, because none of them is an activity. They are subject
  areas, and the test a domain name must pass is reading as a module at
  level one *and* at level seven. "Spatiotemporal" fails the low end.
- **But Operations is a genuinely missing domain**, not a relabelling.
  Procedure, process, sequencing of work, control of execution.
  Closed-loop manufacturing is operations and nothing covered it.
- **Civilization and society added to the manifest**, distinct from agency.
  Agency is one actor with goals; society is many actors with institutions,
  norms, and testimony. The primitive register already carries its seeds.
- Both go in the manifest and neither into the graph, because the graph
  should follow content rather than precede it.
- **A correction.** "No cross-domain prerequisites" was reported twice as a
  good property. It was partly hiding disconnection. Zero prerequisites run
  from any foundation outward, and only one foundation concept is depended
  on at all, so the foundations carry vocabulary and contribute no
  structure. The property that matters is narrower: no prerequisite between
  the two ablation domains. Foundations feeding both is desirable.
  `validate_graph.py` now reports the feed count.

### Changed. The everyday domain split into three

- `everyday` was a grab-bag. Split into `physical_world`, `space_and_time`,
  and `agency`, aligned with clusters the primitive register already has.
  The register is the level-one foundation, so the domains should not cut
  across it.
- **The split earns more than tidiness.** A single foundation hides which
  foundation each domain rests on. Measured immediately, failure analysis
  rests on the physical world about two and a half times as heavily as
  mathematics does, while mathematics leans further on space and time. One
  bucket would have reported one undifferentiated number.
- A mis-mapping surfaced. "Therefore" sat under `manner`, which is an
  inference marker, so it became `discourse_marker` and moved to
  communication.
- Independence survives. No cross-domain prerequisites, depth contrast
  unchanged at 10 against 6.

### Added. Accounting, and a handoff protocol

- Accounting placed as a measurement discipline rather than applied
  economics. Five concepts and two formal structures. It had to earn its
  place by producing a derived transfer edge and did: balance and
  conservation of number both instantiate conservation.
- `docs/process/HANDOFF.md`, adapted from the protocol in the operator's
  Keleusma project. Validity is checked by ancestry and by content, never
  by a hash match, and the content checks are cheap and independent.
- The handoff separates what a resuming session should do, what the
  operator holds, what stays unstarted and why, and the method rules that
  were expensive to learn. History accumulates below a line and is never
  edited.

### Changed. Communication added, vocabulary fully mapped

- **Communication added as a domain**, closing the gap the curriculum
  coverage test found. Five concepts covering knowing, explanation,
  reporting, and a claim under test.
- **All 131 unmapped words now carry a concept.** Completeness moved from
  8.4 percent to 100. The graph grew from 45 to 71 nodes across four
  domains, and every record now lists the concepts its words touch, which
  is what produces the cross-domain links.
- **The mathematics against failure-analysis depth contrast survives** at 10
  against 6, which the ablation design depends on.
- **A third correction to the vocabulary design, and the validator found
  this one too.** Term levels were derived from the concept. That is wrong,
  because a concept can be taught before its name is introduced. The
  level-one causation record never uses the word "cause", and children grasp
  causation long before they say it. Deriving equality admitted thirty-three
  words at levels where nothing used them.
- A term's level is now **authored**, with the graph supplying a lower bound
  only: a word may not precede the concept it names. Placement above that
  bound is a scheduling decision, which is what the kanji schedule is.
- History and accounting recorded as further additions, with accounting
  earning its place chiefly through a transfer edge, since mass and energy
  balance in a closed loop is accounting and double-entry bookkeeping is
  conservation expressed as a procedure.
- **Drafting a sensible curriculum remains open and non-trivial.** The
  schedule now has somewhere to live, and nothing has scheduled it.

### Changed. The unmapped tier is a measure, not a category

- **A correction to a correction.** General vocabulary was introduced as a
  permanent third category on the model of Basic English. That was wrong. A
  content word names something, so a word mapping to nothing means the
  mapping was not identified or a concept is missing from the graph.
- The tier is a holding pen for unfinished work and its size measures graph
  incompleteness. `completeness` reports the fraction of content words
  carrying a concept. **It currently stands at 8.4 percent**, with 131 words
  awaiting a concept against 12 that have one.
- **`vocabulary_limited` added as a simplification kind.** Distinct from a
  superseded model, which is wrong. A vocabulary-limited record is not
  wrong; it is as accurate as the admitted words allow. Recording which is
  which lets a reader tell a simplification from an error. The fidelity loss
  is accepted rather than apologised for, provided it is labelled and its
  correction named.
- **A coverage test method recorded.** A manifest derived from a deployment
  profile can be checked against a real curriculum in the domain, and gaps
  appear as subjects with no home. Applied once, it found that communication
  coverage was absent while the stated deployment rationale depends on
  reporting over a constrained channel, which was an inconsistency rather
  than merely an omission.

### Added. Relation coverage, and two corrections

- **A specialisation asserted in the graph must be taught in the corpus.**
  Enforced by a new rule. A graph that says a teddy bear is a toy, with no
  record teaching it, asserts a link the model never reads.
- **The asymmetry is the part that must be taught.** A teddy bear is a toy
  and a toy is not necessarily a teddy bear, which is the same structure as
  a square being a rectangle while a rectangle need not be a square. An edge
  records the direction. Only content can teach that the converse fails.
- **Correction. Transfer does occur at level one.** An earlier note held
  that no level-one transfer edges was right, since transfer requires
  abstraction. Teddy-bear-is-a-toy and square-is-a-rectangle instantiate the
  same formal structure, proper class inclusion, which is a cross-domain
  transfer edge between an everyday concept and a mathematical one. The
  existing machinery derives it without modification, and this is how
  children acquire classification.
- **Correction. The teddy bear was not a useless anchor.** It scored zero
  only because its edges were not drawn. Teddy bear to toy to proxy model to
  representation to simulation gives it four, and enters the modelling
  spine. The general lesson is uncomfortable: a low anchor-reach score may
  mean a concept is not worth teaching or may mean the graph is incomplete,
  and the metric cannot tell them apart.

### Added. Enabling concepts, and the metric that measures them

- `docs/spec/ENABLING_CONCEPTS.md`, a `specialises` edge type, and two
  reach metrics.
- **Level placement is a scheduling problem, not only a dependency one.**
  Japanese education assigns kanji to grades, and some appear where they do
  because they must be introduced somewhere and that level had room.
  Prerequisites say what cannot come before what. They do not say where
  anything should go among the orderings that satisfy them. Capacity per
  level and completion by the end are both unmodelled and are recorded as
  the shape the assignment should take.
- **A concept with no use at a low level can be an enabling concept for a
  high one.** A crayon is paraffin wax, paraffin wax is a lightweight
  hydrocarbon, and paraffin hybrids have flown. Verified: Stanford and
  Lockheed Martin in 2003 to 4,600 metres, a Stanford student vehicle to
  2,871 metres in 2004, with regression rates three to four times HTPB.
- **The divergence from human pedagogy this exposes.** A human curriculum
  introduces crayons because children use crayons. A model has no life, so a
  concrete concept earns level one only as the cheapest anchor for a chain
  that matters later. Selecting by what a child finds familiar would fill
  level one with objects that anchor nothing.
- **A correction made while building.** The first metric counted what
  depends on a concept, which is the wrong direction for an anchor. An
  anchor is a leaf, so a crayon scored zero alongside a teddy bear.
  `anchor_reach` follows specialisation forward to the abstractions a
  concept instantiates and counts what rests on those. In the worked example
  a crayon anchors six concepts and a teddy bear none.
- A `specialises` edge is distinct from the two already present. A crayon
  does not require paraffin wax and shares no formal structure with it. It
  is one.

### Added. Per-level vocabulary, with a correction to my own design

- `docs/spec/VOCABULARY.md`, `src/epagoge/vocabulary.py`, and
  `curriculum/vocabulary.json`. Levels one to six are bounded; level seven
  is unrestricted.
- **Two rules.** A record uses no word admitted above its level. And every
  word admitted at a level appears in at least one record at that level,
  so admitting a word is a commitment to teach it rather than an
  aspiration.
- **The strongest reason for this is not simplicity.** It makes level
  assignment mechanically checkable, which was the design's weakest point.
  A level was authored with only prerequisite coverage constraining it, so
  a disagreement about whether a record sat at level three or four had
  nothing to appeal to.
- **A correction.** I claimed the vocabulary could be derived wholly from
  the concept graph. That was wrong, and the validator is what showed it.
  Most content words name no concept, and forcing a licence on them
  assigned twenty-four words to levels where they never appeared. General
  vocabulary is authored in tiers as Basic English and the Dolch lists are.
  Derivation applies to the technical terms, where drift would do damage.
- A word qualifies as a derived term only if it is actually used at its
  concept's level. A word that merely resembles a concept name is ordinary
  vocabulary.
- **The limit, stated so it is not over-relied on.** The check is lexical.
  It would not have caught this morning's wear-versus-break error, since
  "broken" is unambiguously level-one vocabulary. Vocabulary constrains how
  simply a thing is said and says nothing about whether it is right.
- Prior art recorded. TinyStories constrained generation to a roughly
  fifteen-hundred-word lexicon and produced coherent English from
  three-million-parameter models.

### Added. Teacher model pulled, and a generator requirement it revealed

- `qwen3:30b-a3b-instruct-2507-q4_K_M` pulled and verified. Apache 2.0
  confirmed from the shipped licence, 18 GB on disk, 21 GB resident,
  entirely on GPU, roughly fifty tokens per second warm.
- Text-only rather than vision, since corpus generation uses no vision.
  Instruct rather than thinking, since reasoning traces are wasted tokens.
- Generation budget revised down. One million tokens is about five and a
  half hours single-stream rather than eight, so level one is a few hours
  to a day rather than up to eighty hours.
- **The first two prompts established a generator requirement.** Asked to
  teach that repeated use wears things out, the model returned two
  sentences in three about things breaking and chains snapping, which is
  sudden failure and a concept the graph deliberately separates from wear.
  Adding one negative constraint produced three correct sentences in three.
- **A generation prompt must therefore carry the concept, its grounding
  primitive and observation, and its nearest graph neighbours as explicit
  exclusions.** The graph already holds the neighbours, so the exclusions
  are derived rather than authored. Without this the generator produces
  fluent text that blurs exactly the distinctions the curriculum exists to
  draw, while passing schema validation and reading well.

### Added. Level-one graph coverage, and the review tool

- Concept graph expanded from 33 to 45 nodes with a level-one layer in both
  domains. `seed.json` renamed to `concepts.json`, since it is no longer a
  seed.
- **The prerequisite-depth contrast sharpened** from 7 against 5 to 10
  against 6, and the two domains are **independent subgraphs with no
  cross-domain prerequisites**, so the contrast the ablation rests on is not
  muddied by shared ancestry.
- `src/epagoge/review.py` and `tools/review.py`. **This is the sampled
  expert audit, not only a reading aid.** Its output is the measured
  residual error rate the quality claim rests on.
- Three verdicts rather than two. A flag is counted separately and never
  folded silently into accept or reject.
- **Rates are per domain and carry Wilson score intervals.** Three
  rejections in thirty records is ten percent with an interval from 3.5 to
  25.6 percent, so quoting the point estimate would present as a
  measurement something the audit did not establish. Even zero rejections
  in thirty bounds the rate below about eleven percent, not below zero.
- Where a record cites a primitive, the grounding observation is displayed
  inline, so a claim can be checked against what grounds it without leaving
  the screen.
- Six hand-written level-one records added, teaching the concepts the
  expanded graph requires. The corpus validator found each gap in turn.

### Added. Primitive register, which unblocks level one

- **A problem raised in discussion and never written down until now.**
  Level one breaks the grounding rule. Every record needs a resolvable
  source, but level one seeds civilisational axioms, and there is no
  citation for "things break" or "living things die". A generator facing
  that has three options and two are bad: fail validation, fabricate a
  citation, or find an honest home for axioms. Level one is therefore the
  hardest case for the verification layer rather than the easiest.
- `docs/decisions/PRIMITIVE_REGISTER.md` and `curriculum/primitives.json`.
  Level-one records ground in a hand-authored register of thirty-four
  axioms, each carrying the observation that grounds it, cited through a
  `primitive:` prefix. **The grounding rule is unchanged**; only the kind of
  source is new.
- **The load-bearing rule is that a generator may write records teaching a
  primitive but may not add to the register.** The register is small and
  everything above it inherits its errors, so it is hand-authored and
  reviewed, which puts human attention at the foundation rather than spread
  thinly across millions of generated records.
- The guard works as intended. A record citing
  `primitive:hard-work-brings-success`, a contested normative claim wearing
  a primitive's clothes, is rejected by name.
- Training to level one recorded as a pipeline validation rather than a
  model deliverable, since a model trained on picture-book content will be
  poor by construction and judging it as a model would support a wrong
  conclusion.
- Byte-level tokenisation chosen for level one. No dependency, no
  tokeniser-training step, and the spine already treats tokenisation as a
  neutral artifact so changing it later is contained.

### Added. Training techniques, teacher runtime, and corpus regeneration

- `docs/decisions/TRAINING_TECHNIQUES.md`. Maximal update parametrization,
  Muon, warmup-stable-decay, and multi-token prediction adopted. FP8 when
  the hardware supports it.
- **Maximal update parametrization is confound removal, not
  optimisation.** Without it the three scale points have different optimal
  hyperparameters, so any scale-dependence in the ordering effect could be
  an artifact of mis-tuning. That lands on the project's own mechanism,
  which holds that regime position depends on width and learning rate.
- Multi-head latent attention flagged rather than adopted. It is a low-rank
  projection, which the Jacobian-space objective bans in the base model, so
  it must be measured against the effective-rank floor rather than taken on
  its efficiency merits.
- **The pilot's variance numbers do not carry over.** Changing optimiser
  and schedule changes the dynamics, so sigma and rho must be re-measured.
- **The teacher runs locally, and the reason is disclosure rather than
  licensing or cost.** Generation prompts encode the coverage manifest, so
  any hosted interface transmits the withheld artifact. A weight licence
  also does not govern a hosted endpoint, which carries its own terms.
  Hosted generation would have cost between fifty cents and five dollars
  for the whole of level one, so price was never the constraint.
- `docs/decisions/CORPUS_REGENERATION.md`. **The corpus is frozen during
  the research phase**, because regeneration by a model trained on it would
  make the corpus dependent on the treatment and the ablation circular.
- Downward regeneration has a sound form and an unsound one. The student
  here is weaker than the teacher, not stronger, so a student rewriting the
  teacher's work is a novice revising an expert. The sound form separates
  the roles: the student measures which records helped, by attribution, and
  the teacher regenerates. Accumulating rather than replacing, since the
  replace paradigm collapses on even small synthetic contamination.
- Lateral regeneration introduces no new information and narrows coverage.
  A verifier makes it survivable as rejection sampling, but it breaks
  provenance, which is the project's strongest differentiator.

### Added. Variance pilot, run and measured

- `src/epagoge/variance.py` and `src/epagoge/pilot.py`, with
  `tools/run_pilot.py`. The analysis is standard library only and verified
  against closed-form cases and by recovering known parameters from
  synthetic data. Torch is an optional `train` extra, so the core stays
  dependency-free.
- **Measured single-epoch.** Unpaired sigma 0.0750, paired sd 0.0233,
  correlation 0.954, pairing gain 20.7x seeds at no cost. Twelve paired
  seeds beat two hundred and forty-six unpaired ones, so the original
  five-seed unpaired design was off by two orders of magnitude in
  efficiency rather than merely underpowered.
- **The first pilot was wrong in an instructive way.** It trained about
  twenty-three epochs, where ordering effects necessarily wash out, which
  inflated the correlation from 0.954 to 0.987 and would have understated
  the required seed count threefold. Both results are retained, because the
  difference between them is the finding.
- **Two harness defects found by running it.** A vocabulary of 256 gave a
  second-order source 65,536 contexts over 200,000 tokens, so nothing was
  learnable and every ordering produced an identical result. And warmup
  with no decay left the rate at peak forever, making four thousand steps
  converge worse than two thousand.
- **A null arm is added to the ablation.** The pilot found a systematic
  difference between two orderings that should be equivalent, with the sign
  following the ordering rather than the execution position, marginal at
  about p = 0.04 and unexplained. That is the shape of a false positive, so
  the ablation now compares two random topological orderings against each
  other, and the curriculum effect must exceed that null rather than merely
  exceeding zero.
- **Nondeterminism floor measured.** Identical inputs differed by 0.00075
  on Metal Performance Shaders, bounding the smallest resolvable effect on
  that hardware regardless of seed count.
- Pre-registration items two and six move from pending to fixed and
  measured. Six items remain pending.

### Added. Gate completed, and four gaps closed

Found by checking rather than by recalling.

- **The disclosure scan was enforced by nothing.** `tools/scrub_scan.sh`
  now runs in the gate. Its pattern lives in `secret/`,
  because a tracked list of withheld vocabulary would publish the thing
  being withheld, and absent the pattern it skips loudly rather than
  passing silently. It is word-anchored, since an unanchored pattern
  matched `ore` inside `before` on 2026-09-23 and produced noise that
  would have looked identical to a clean result.
- **The gate resolved `@latest` and was therefore not reproducible.** Tool
  versions are pinned. A gate that can fail tomorrow for reasons unrelated
  to the code is not a property this project should accept in its own
  process.
- **No continuous integration existed.** `.github/workflows/check.yml`
  added, with its one limitation documented rather than left implicit.
- **Coverage had never been measured.** It was 94 percent. Nine tests were
  added for the untested paths, raising it to 99, and a floor of 95 is now
  enforced.
- The `normative` claim class was never exercised by the sample corpus.
  Adding a record for it exposed two genuine prerequisite gaps, which the
  corpus validator caught and which were closed by teaching the missing
  concepts rather than by deleting the record that revealed them.
- Status lines in `README.md` and `CLAUDE.md` still said nothing was
  implemented.

### Changed. Licensing decided

- **0BSD for software, CC0 1.0 for corpus and documentation.** Supersedes
  the MIT declaration in `pyproject.toml`, which was an unsurfaced default
  rather than a decision.
- The split is not a compromise. Creative Commons recommends against CC0
  for software because it does not address patent rights, and 0BSD is the
  software equivalent of the same intent without MIT's notice requirement.
- **CC0 suits a synthetic corpus for a specific reason.** The copyright
  status of machine-generated content is unsettled, so the project may hold
  no rights to license conventionally. CC0 dedicates whatever rights exist
  with a fallback permissive licence, and therefore does not depend on the
  answer. A conventional licence would assert a right that may not exist,
  which is an unsupported claim in a repository meant to suppress them.
- **`sources/` is excluded from both**, in `LICENSE` itself and not only in
  the decision record, since a reader checks the licence file. Third-party
  terms are not the project's to grant.
- Open question twenty-five added. A terminal-stage record that restates
  third-party literature is neither purely machine-generated nor a
  reproduction, and whether it can be CC0 is unresolved.

### Added, 2026-09-23. Record schema, level mechanism, pre-registration, teacher decided

**Record schema.** `docs/spec/RECORD_SCHEMA.md` and
`src/epagoge/record.py`. The single authoritative definition, replacing
fields described across three prose documents. Twelve rules enforced, nine
per record and three across the corpus. Thirty-six tests, weighted to
negative cases. A worked sample corpus exercises every claim class and a
simplification chain, and `tools/validate_corpus.py` gates it.

**The level-assignment mechanism existed only as prose and now exists.**
Levels are authored rather than derived, because the seven levels carry
breadth, abstraction, and groundedness that prerequisite depth cannot
express. Rule twelve keeps an authored level honest. For every concept, the
earliest level covering it must be no earlier than the earliest level
covering each prerequisite. Equal levels are permitted, since ordering
within a level still respects the partial order. There is no scoring
function and no model judgment.

**Pre-registration opened** at `evals/PRE_REGISTRATION.md`. Fourteen
sections, ten fixed and eight items pending, each pending item naming what
unblocks it. A pending item is a value to be measured rather than chosen.
The document must be complete before the first ablation run.

**Teacher model decided by verification.** Frontier interfaces are
excluded. Their terms prohibit training competing models, enforcement is
active, and a language model trained on those outputs is not defensibly
non-competing. Generation uses a specifically named MIT or Apache 2.0
checkpoint with the licence recorded at time of use.

### Fixed, 2026-09-23. Static analysis run for the first time

- **The analysis configured since the initial commit had never been
  executed.** On first run ruff reported eighteen errors and pyright in
  strict mode reported eighteen. A declared standard that is never checked
  is not a standard.
- All thirty-six are fixed. Both tools now report clean.
- **One fix was substantive rather than cosmetic.** `from_json` read a file
  from disk, which is external input, and cast rather than validated. It
  now checks every field and raises at the boundary, which is what the
  project's own trust-boundary rule requires. Ten tests were added for
  malformed input, which had none.
- The pseudo-random exemption is documented rather than silently ignored.
  The control must be reproducible from a declared seed, which is precisely
  what a cryptographic generator does not offer.
- `tools/check.sh` added as a gate. It caught a violation of its own on
  first run.

### Added, 2026-09-23. Concept graph. First implementation

- `docs/spec/CONCEPT_GRAPH.md`, `src/epagoge/concept_graph.py`,
  `tests/test_concept_graph.py`, `tools/validate_graph.py`, and a seed
  graph at `curriculum/graph/concepts.json`.
- Standard library only. No dependency is added, so the graph can be
  validated before any environment question is settled.
- Six invariants enforced. Reference resolution, acyclicity, no self-loops,
  instantiation direction and kinds, domain declaration by node kind, and
  layering, meaning the formal layer may not depend on the domains that
  instantiate it.
- **Validation returns every violation rather than raising on the first**,
  so a graph is audited in one pass.
- **Prerequisite depth is the longest path, not the shortest.** A concept is
  reachable only once every prerequisite is satisfied, so its earliest
  admissible position is governed by its deepest dependency.
- **Transfer edges are derived, never authored.** Two domain concepts in
  different domains are connected exactly when they instantiate a common
  formal structure. Same-domain sharing is ordinary structure, not transfer.
- The random linear extension is the experimental control. **Documented
  limitation.** Randomised Kahn does not sample uniformly over linear
  extensions, since counting them is #P-complete and frontier-uniform
  selection biases toward orderings that keep the frontier wide. Uniformity
  is not required for the control, but the bias is recorded rather than
  left to be discovered.
- Twenty-two tests, weighted toward negative cases. Every invariant has a
  test that breaks it, because a validator shown only valid input has not
  been tested.
- Seed graph of 33 nodes across two domains and a formal layer. Validates
  clean. Three transfer edges derived rather than asserted.
- **Weak empirical support for the question twenty design.** Mathematics
  reaches prerequisite depth seven in the seed and failure analysis reaches
  five, which is the contrast the ablation assumes. The mathematics
  subgraph also has more nodes, so this is directional rather than
  measured.

### Resolved, 2026-09-23. Four open questions closed

**21. Levels against structural difficulty.** They are not competing
definitions. Prerequisites and supersession are hard checkable constraints
giving a partial order. The seven levels choose one trajectory within the
feasible set. The earlier proposal that prerequisite depth be authoritative
was withdrawn as wrong, since dependency depth cannot express breadth,
abstraction, or groundedness.

**Consequence.** The flat-order control is a **random topological
ordering**, respecting prerequisites while discarding the curriculum
trajectory. A free shuffle would have compared valid ordering against
invalid ordering, which is close to a tautology and is what much of the
published literature does.

**24. Transfer edges route through the formal spine.** An edge exists
between two domain concepts exactly when a formal structure exists that
both instantiate, and that structure is a node in the graph. Checkable,
model-free, and it excludes loose metaphor, which is where false transfer
originates. The graph becomes layered.

**20. The ablation corpus is two domains, not the full manifest.**
Mathematics for deepest prerequisite chains and machine-verifiable content,
plus a near-flat-structure contrast domain. The contrast varies the
hypothesised mechanism rather than merely the tidiness of the subject.

**The strongest available outcome is now a dissociation.** A positive result
in the deep-structure domain paired with a null in the flat-structure one
would be evidence that prerequisite depth is the mechanism, which is a
better finding than an ordering effect alone, and would explain the
inconsistency of prior work, which has not controlled for the prerequisite
depth of its subject matter.

### Changed, 2026-09-23. Enabling material, spiral structure, and quirk

- **Every topic appears at every level, as enabling material.** At low
  levels this is the enabling primitives rather than the formal discipline.
  Failure analysis at the first level is that things break and living
  things die. This answers open question twenty-three and unblocks staging
  of practice-spine content.
- **Level one seeds civilisational axioms**, meaning the primitives later
  content presupposes and never states. A human learner is taught that a
  street is dangerous. A model has no innate anything, so every such
  primitive is in the corpus or absent from the model. This is a better
  specification than emergent understanding.
- Open question twenty-two sharpened rather than closed. Whether explicit,
  early, isolated axiom-seeding beats implicit, diffuse absorption is the
  curriculum hypothesis restated at the axiom level.
- **Open question twenty-four added.** The spiral has a vertical relation,
  already encoded by the supersession pointer, and a horizontal one that
  does not exist in the design. Inter-topic mastery needs analogy or
  transfer edges in the concept graph. Cross-domain gradient alignment
  already instruments it, so it is observable in the kernel.
- **Quirk accepted within a declared boundary.** Unbounded, it would absorb
  any negative result, which is the unfalsifiable move this project exists
  to prevent and is more dangerous from the operator than from the model.
  Unusual register and narrow stylistic range are quirk. Systematic error
  and mode collapse are failures. The boundary goes in the pre-registration.
- **Spin-off artifacts recorded as an option preserved, not a goal
  pursued.** Extraction stays cheap, no corpus decision is driven by human
  readability, and the disclosure implication of publishing curriculum
  material is recorded as requiring a deliberate decision.

### Added, 2026-09-23. Seven curriculum levels

- `docs/spec/CURRICULUM_LEVELS.md`. Seven levels from preschool to
  post-graduate, with the developmental rationale for the shape. Narrow and
  concrete at first because nothing wider can be grasped, an inflection at
  the third level where broad breadth becomes available, then breadth
  progressively traded for depth before messy real problems at the end.
- **The levels bundle four axes**, namely breadth, depth, abstraction, and
  groundedness. Breadth is an hourglass rather than monotonic. Depth is the
  only monotonic axis and is named primary so the ordering claim has a
  stated referent. The confound is documented rather than decomposed, since
  decomposition would multiply the arms beyond budget.
- **Levels one to six are synthetic and built to purpose.** Licensing
  questions therefore apply only to level seven. The developmental analogy
  motivates the shape of the ladder without dictating its content.
- **Token distribution is power-law across three to four orders of
  magnitude**, since early-level material is short. This partially resolves
  open question twenty along the level axis. The topic-breadth half is
  untouched.
- The curriculum hypothesis is consequently a claim about roughly the first
  one percent of tokens, which is consistent with the kernel-shaping
  mechanism rather than in tension with it, since shaping requires the
  correct data first rather than much data.
- Risk recorded. A purely synthetic early corpus may be too clean, and the
  early phase is where the kernel is shaped.
- Open questions twenty-one, twenty-two, and twenty-three added.

### Changed, 2026-09-23. Two-spine coverage structure

- Coverage now runs along two orthogonal axes, a subject spine and an
  epistemic-practice spine. The practice spine's members are domains whose
  content is the discipline itself, teaching how a conclusion follows, what
  can be known, where a representation applies, how something is
  established, and how one discovers one was wrong.
- **The practice spine is arguably the actual curriculum**, with subject
  content as the substrate it operates on. It also supplies a principled
  basis for weighting the two axes against each other.
- Three coverage additions, one of which corrected an omission of mine.
  Neither axis's contents are reproduced in tracked documentation.
- **Open question twenty added, gating corpus generation.** Coverage
  breadth now exceeds what the ablation token budget can support at the
  chosen model scales. An ordering ablation is confounded if the corpus is
  too thin for anything to be learned, since a null result would then be
  uninformative. Explicit proportions and a declared ablation subset are
  both required and neither exists. The concept graph and the variance
  pilot are unaffected.

### Added, 2026-09-23. Claim taxonomy and conditional-result records

- `docs/spec/CLAIM_TAXONOMY.md`. Every record is classified into exactly
  one of formal, empirical, attributed position, conditional result,
  normative, or unsupported. Classification precedes verification and
  determines which checks apply.
- The taxonomy is operational, about verification method, and asserts no
  metaphysics. A binary between the measurable-and-falsifiable and
  everything else was considered and withdrawn as too low-fidelity, since
  its residual category would have contained mathematics, definitions, and
  normative claims, and since a purely empirical demarcation criterion
  cannot satisfy itself.
- **Falsificationism is recorded in the specification as an attributed
  position, with Duhem and Quine, Lakatos, Kuhn, and Bayesian
  epistemology attributed alongside it.** It is retained as the worked
  example because it is the operator's own stated position, applied to the
  rule rather than exempted from it.
- **Conditional-result records added as a fourth record type**, carrying
  assumptions, method, and validation status. A simulated result is a
  derivation from assumptions rather than a measurement, and a record of
  the form "the model shows X" without those fields is rejected.
- Coverage extended. A model's domain of validity is the same object as
  the record schema's validity scope, so the domain teaches the project's
  epistemic discipline by example rather than only by assertion.

### Changed, 2026-09-23. Coverage extended, with two schema consequences

Coverage weighting extended. The manifest is not reproduced here.

- **Attributed-position records added as a third record type.** For
  interpretive and contested material the verifiable claim is that a named
  thinker held a position, not that the position is correct. A record
  asserting a contested claim as settled fact is rejected. Without this,
  coverage of interpretive domains would teach the model to assert
  contested claims confidently, which is the failure the project exists to
  prevent.
- **The residual error rate is reported per domain and never aggregated.**
  Verifiability varies enormously across the corpus, and a single number
  would average a machine-verifiable domain against an interpretive one and
  conceal both. This also improves the credential in the collaborative
  positioning record, since a per-domain breakdown is more useful to
  anything selecting on it.
- Coverage that raises the machine-verifiable fraction of the corpus is now
  preferred on verification grounds, independent of subject-matter value.

### Resolved, 2026-09-23. All three blocking audit findings

1. **Power.** The design is paired, sharing initialisation and data within
   a pair so order is the only difference, which was a free correction the
   original specification missed. Seed count and allocation are set by a
   variance pilot at the smallest scale rather than chosen, converting the
   central design parameter from assumption to measurement.
2. **Grounding.** Entailment is retained for terminal-stage literature and
   replaced for simplified content by a declared fidelity relation carrying
   the source claim, the simplification kind, the validity scope, and the
   supersession pointer. Good pedagogy uses known-false models that later
   stages correct, and no entailment rule can cover content whose purpose
   is to be superseded.
3. **Difficulty.** Defined structurally as prerequisite depth in a declared
   concept graph combined with supersession depth. No model assigns it, so
   the teacher cannot confound the treatment. The concept graph becomes the
   main deliverable, ahead of corpus generation.

Consequences. The corpus record schema gains five required fields. The
pre-registration scope gains the concept graph, the difficulty definition,
the curriculum specification, and a multiple-comparison correction
procedure. The three-scale allocation in question five is provisional.

### Added, 2026-09-23. Pre-commit adversarial audit

- `docs/decisions/PRE_COMMIT_AUDIT.md`. Eleven findings, three blocking.
- **Blocking.** The ablation is underpowered, detecting only effects of
  1.77 sigma of seed variance at five seeds per condition, against a
  literature reporting small effects and a criterion that treats an
  inconclusive result as failure.
- **Blocking.** Source grounding as specified forbids pedagogical
  simplification, which is the curriculum's defining feature.
- **Blocking.** Difficulty, the independent variable, is nowhere defined,
  and is absent from the pre-registration scope. If assigned by the teacher
  model it becomes an uncontrolled confound.
- Budget arithmetic recorded. Roughly $9,400 for the ablation and pilot
  alone, excluding corpus generation, audit, instrumentation, and time.
- Recorded that nineteen cited papers were cited from search summaries
  rather than read, which fails the project's own standard.

### Added, 2026-09-23. Collaborative-group positioning

- `docs/decisions/COLLABORATIVE_POSITIONING.md`. The model class is
  positioned as the falsifier and verifier specialist, for recruitment into
  multi-agent groups through capability-advertisement protocols.
- Recorded as repositioning rather than new direction. The properties that
  make the model attractive for recruitment are the ones already decided
  for other reasons, and the mapping is close to one-to-one.
- The audited residual error rate gains a second role as the recruitment
  credential, since an orchestrator can select on a number.
- **Guard.** Never train toward being selected. Current orchestrators
  favour agreeableness, so optimising for selection would destroy the
  property the model exists to have. Positioning may change the capability
  advertisement, the output schema, and the documentation. It may not
  change the loss.
- Input from collaborating agents is untrusted by the same standard already
  applied to teacher-model output.

### Added, 2026-09-23. Jacobian-space as an architecture objective

- `docs/decisions/JACOBIAN_SPACE.md`. Maintaining healthy reasoning
  ability through an adequately unconstrained Jacobian-space is an
  architecture objective, not merely instrumentation.
- Made enforceable through a tangent-kernel effective-rank floor, declared
  in the pre-registration and measured, rather than left as a preference.
- Fault tolerance assigned to hardware, namely error correction on weight
  memory, scrubbing against a protected copy, and triplication of the small
  high-precision core. Not to flattening the model.
- Low-rank parameterisation banned outright in the base model, since it
  constrains the Jacobian to a low-rank subspace by construction.
- Quantisation pilot's primary measurement is effective rank against the
  floor rather than the accuracy gap. Same three runs, better question.
- Generates a testable regime hypothesis. If ordering acts by shaping the
  tangent kernel it can help only in the feature-learning regime, whose
  position depends on width and learning rate, which predicts the effect
  varies across the three chosen scale points and would explain the
  inconsistency of the published literature.
- Instrumentation in the primary arms is measurement only. Regularisation
  would confound the pre-registered ablation and belongs in a separate arm.
- **Correction made while drafting, recorded because the error is
  instructive.** An earlier draft held that Jacobian awareness served both
  the ordering mechanism and weight-perturbation tolerance, and called that
  a convergence. It is a conflict. Fault tolerance wants low sensitivity of
  the function to parameter change. Reasoning wants that sensitivity to
  stay rich. The reasoning side wins, and the literature supports it, since
  flatness is not a reliable good.

### Names fixed, 2026-09-23

- `epagoge` names the repository and the corpus project.
- `sporos` names the model.
- `elenchos` names the anti-sycophancy evaluation suite.

A tracked document may gloss what a name means. It may not state why a name
was chosen.

### Deployment material separated, 2026-09-23

Performed before the initial commit, so no history contains the material.

- Positioning records separated from tracked documentation and given code
  names under the project's naming convention.
- The market assessment moved out of `docs/decisions/` for the same reason.
- Tracked documents state generic engineering constraints only. Omission
  only. No tracked statement was made false.
- Standing rule recorded in `CLAUDE.md`.

### Pre-planning closed, 2026-09-23

All nineteen open questions resolved. Fifteen answered, four deferred to
the gated follow-on, none left open.

Decisions taken in this pass.

1. **Scope.** Research first, product gated. The deliverable is the corpus,
   the curriculum specification, and the ordering ablation. A deployable
   model is a follow-on funded on the ablation result.
2. **Verification.** Layered, with a measured residual error rate from
   sampled expert audit. Source grounding is the floor, executable checks
   where the domain permits, consensus as a filter only.
3. **Application boundary.** Weapons-development material is out of
   scope. Recorded rather than assumed.
4. **Falsification.** Pre-registration, with inconclusiveness as the
   failure condition. A negative result is a deliverable.
5. **Scale.** From random initialisation at three scale points, roughly
   100M, 300M, and 1B parameters, five seeds per condition.
7. **Topic basis.** Coverage derived from the operational
   profile, replacing an earlier framing that rested on an unfalsifiable
   objective.
8. **Sycophancy.** Corpus carries positive examples of evidence-conditioned
   revision plus avoidance of approval-seeking patterns, with an elenchos
   baseline measured on the ablation models.
9. **Interoperability.** A structured output schema, not a model. Removes
   an artifact and dissolves the original concern.
10. **Framework.** PyTorch, now that the hardware path is small rented
    NVIDIA runs.
17. **Use case.** An agentic model with sensor and instrument inputs access,
    reasoning autonomously and reporting over a [redacted constraint].
19. **Galactica.** Answered by the measured error rate in decision two.

Deferred to the follow-on. Distillation, native low-bit training, bounded
attention and context length, and agentic reliability at deployment scale.

### Added (current)

- the market assessment. Feasibility and market
  distinctness assessed at the close of pre-planning.
- Deployment use case recorded as answered. An agentic model with vision
  and instrument data access, reasoning autonomously and reporting over a
  [redacted constraint].
- Open question nineteen added. An explicit answer is required for why this
  does not repeat Galactica, which failed on this project's exact claimed
  differentiator.
- Open question eighteen added. Agentic reliability is scale-dependent
  while the deployment envelope wants a small model.
- Corrected the deployment hardware assumption. Flight-validated edge AI
  silicon at sixty trillion operations per second in eight watts exists,
  so earlier size-severity arguments are weaker than recorded.

### Added (latest)

- `docs/architecture/MODEL_ARCHITECTURE.md`. The ablation model is fully
  standard for comparability. The deployment model adds bounded attention,
  which converts key-value cache from growing with sequence length into a
  statically bounded quantity.
- Mixture of experts closed rather than merely rejected. Its bargain
  spends memory to buy compute, which inverts this project's binding
  constraint, and this is independent of the existing control-flow
  objection.
- State space and linear attention hybrids rejected on a
  fault-environment-specific ground. Recurrent state is a cumulative persistent
  fault surface where key-value cache corruption is bounded in blast
  radius.
- Open question sixteen added. The window size and the number of
  full-attention layers cannot be chosen until the deployment task's
  context requirement is known, which inherits from question one.

### Changed (current)

- Pilot in open question fifteen revised from two arms to three. Floating
  point, four-bit, and ternary. The k-bit inference scaling law work places
  the optimum at four bits with a sharp decline below three, so the
  two-arm design would have tested only the endpoints and missed the
  frontier.
- Design rule added. Prefer width with grouped-query attention over depth
  when scaling to compensate for low-bit degradation, because cache grows
  with depth and cache is the workspace the low-bit weights were meant to
  free.
- Recorded that BitNet already keeps embeddings, normalisation, the output
  head, and activations above ternary, so selective precision is part of
  the approach rather than an additional lever.

### Changed (latest)

- Ablation model and deployment model separated as distinct artifacts. The
  ablation subject is standard and floating point for comparability. The
  deployment artifact is free to be ternary.
- **Correction.** The deadline recorded against open question fifteen was
  an artifact of assuming a single model would serve both purposes. That
  assumption was not stated by the operator. Decoupling dissolves the
  deadline. The erroneous entry is retained in place so the error stays
  visible.
- Ternary evidence review recorded, with the qualification that most
  negative evidence concerns post-training quantization rather than native
  low-bit training and therefore does not refute the proposal.
- A pilot specified to replace the decision. Train the same small
  architecture twice at target scale, floating point and ternary, and
  measure the gap with reasoning separated from fluency.

### Changed (most recent)

- Training and deployment numerics divided explicitly. Training is
  floating point. Deployment is integer arithmetic in block floating
  point form. Q-format is recorded as unsuited to training because its
  single shared exponent cannot span gradient dynamic range.
- Keleusma recorded as a separate effort with plausible future
  convergence, which the deployment track may not assume.
- Open question fifteen added. Native low-bit training is the only
  quantisation decision that cannot be deferred past pretraining.

### Changed (continued)

- `docs/decisions/MODEL_ARCHITECTURE_CONSTRAINTS.md` extended with the
  fault-tolerant deployment target. Verified that integer and
  fixed-point bit-flip errors are additive and linear in bit position
  while floating-point errors are multiplicative and exponential in the
  exponent, which makes integer quantisation a structural requirement for
  that target rather than a preference. Open questions thirteen and
  fourteen added for the distillation track and for the relationship to
  existing statically bounded execution work.

### Changed

- `docs/decisions/LANGUAGE_CHOICE.md` split into two decisions. Python
  remains settled. The training framework is demoted from settled to open,
  because the original PyTorch assertion was not the product of a
  comparison. A decision rule keyed to the hardware path replaces it.
- `docs/decisions/PYTHON_VERSION.md` resolved by measurement against the
  Python Package Index. Torch 2.14.0 and jaxlib 0.11.2 both publish cp314
  wheels, so Python 3.14 is not a blocker and the first-dependency block is
  lifted.

### Notes

- No corpus data exists. No curriculum stage has been specified. No model
  has been trained.
- Verified 2026-09-23 against upstream documentation. Levanter's bitwise
  determinism guarantee is scoped to Tensor Processing Units and does not
  extend to graphics processing units. PyTorch does not guarantee complete
  reproducibility across releases, commits, or platforms. The ordering
  ablation consequently requires multiple seeds per condition, recorded as
  open question eleven.
