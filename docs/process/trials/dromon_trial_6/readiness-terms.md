# Level-one and level-two term counts for missing units

**Fact.** The vocabulary file blob is e4187a17a4a280d0b1779b10656f3edfa3eeec64.

**Command.** python3 -I tmp/dromon-trial-7/readiness_terms.py "$PWD"

**Fact.** The script found 26 scheduled level-two units without a book. It reads term entries from curriculum/vocabulary.json and includes only levels one and two. Level-three entries and entries at levels four through six are excluded. It counts distinct words for each scheduled concept. If one word has several entries under the same concept and level, it counts once at that level. If it is listed at both levels, it counts once in the combined union. The same word may count under multiple concepts if filed under each concept.

**Fact.** A count measures vocabulary on file, not whether a module can be written. Counts below are L1/L2/combined.

| Unit | Concept counts (L1/L2/combined) | Zero concepts | Combined sum |
|---|---|---:|---:|
| ac2.balance | balance=0/1/1; reconciliation=0/1/1; same_amount=2/2/4; exchange=8/35/43 | 0 | 49 |
| ac2.flow | stock_and_flow=0/7/7; using_up=3/18/21 | 0 | 28 |
| a2.plan | doing_in_order=2/3/5; feeling=21/46/67; goal=3/9/12; need=3/11/14; person=22/31/53; plan=3/3/6; way_of_doing=8/17/25 | 0 | 182 |
| a2.mistake | activity=9/32/41; can_and_cannot=7/6/13; enough=6/4/10; finished_or_not=2/2/4; mistake=2/1/3; only_what_was_asked=2/0/2; self_and_other=9/2/11 | 0 | 84 |
| c2.explain | explanation=0/3/3; discourse_marker=3/5/8; giving_a_reason=2/3/5; knowing=8/21/29; real_and_pretend=4/14/18; sentence=4/0/4; word=3/3/6 | 0 | 73 |
| c2.claim | claim_under_test=0/2/2; leaving_out=3/2/5; letter=1/0/1; name=4/1/5; saying_what_you_saw=2/8/10; standing_for=12/7/19; story=2/5/7 | 0 | 49 |
| c2.report | reporting=0/16/16; asking=4/5/9; close_enough=2/11/13; more_to_learn=3/2/5; saying_what_you_did=2/0/2; writing=6/13/19 | 0 | 64 |
| b2.keeping_going | body_part=24/21/45; growing=2/3/5; keeping_going=2/5/7; needing_supply=3/10/13; plant=12/60/72 | 0 | 142 |
| b2.mending | animal=11/46/57; being_hurt=4/13/17; mending=4/3/7; tending=4/15/19 | 0 | 100 |
| p2.force | emptiness=8/4/12; falling=8/1/9; force=14/36/50; household_object=51/83/134; inside_and_outside=6/16/22; joining_and_separating=7/24/31; liquid=18/54/72; moving_and_still=25/66/91; opening_and_shutting=7/1/8; raw_and_made=9/44/53; sound=18/13/31 | 0 | 513 |
| p2.matter | air=6/16/22; change=5/46/51; heat=9/16/25; material=24/79/103; metal=9/5/14; physical_property=49/92/141; presence=7/2/9; shape=17/47/64; touching=7/6/13; toy=12/12/24; weather=13/64/77 | 0 | 543 |
| f2.failing | failing=0/2/2; cause_and_effect=2/13/15; component_and_system=2/40/42; things_break=7/12/19; wearing_out=3/2/5 | 0 | 83 |
| f2.accident | accident=0/3/3; causal_chain=1/2/3; danger=10/33/43; living_and_not_living=11/17/28 | 0 | 77 |
| f2.checking | being_told=9/1/10; checking=4/10/14; dying=3/3/6 | 0 | 30 |
| h2.findout | finding_out=2/39/41; guess=3/6/9; not_always_known=2/3/5; settling_it=4/2/6 | 0 | 61 |
| h2.wrong | being_wrong=2/0/2; changing_your_mind=2/0/2; resting_on_a_guess=2/0/2; taking_on_faith=3/3/6 | 0 | 12 |
| i2.reason | agreeing=2/0/2; disagreeing=2/3/5; giving_a_reason=2/3/5; keeping_your_claim=2/0/2; opinion=4/0/4 | 0 | 18 |
| i2.rule | family=13/6/19; judged_by_another=2/1/3; people_together=7/25/32; rule=2/10/12; someone_in_charge=5/12/17 | 0 | 83 |
| m2.number | natural_number=0/13/13; place_value=0/4/4; grouping=3/15/18; same_and_different=6/29/35 | 0 | 70 |
| m2.addsub | addition=0/4/4; subtraction=0/3/3; correspondence=5/1/6; counting=3/5/8; more_and_fewer=7/18/25 | 0 | 46 |
| m2.howmuch | quantity=0/73/73; measuring=13/37/50; number_word_order=15/1/16; same_amount=2/2/4 | 0 | 143 |
| m2.logic | all_some_none=3/17/20; conservation_of_number=1/1/2; if_then=1/1/2; not_both=1/1/2 | 0 | 26 |
| n2.should | good_and_bad=13/48/61; keep_trying_or_stop=3/3/6; right_reason=1/0/1; should_and_should_not=1/8/9; two_shoulds_at_once=1/0/1 | 0 | 78 |
| n2.fair | allowed_or_not=1/7/8; choosing=2/9/11; fair_and_unfair=4/0/4; promise=1/2/3 | 0 | 26 |
| r2.measure | cycle=15/27/42; how_sure=3/17/20; measuring=13/37/50; sequence=9/22/31; spatial_position=23/138/161; unit=3/18/21 | 0 | 325 |
| r2.record | direction=10/43/53; duration=17/51/68; out_of_date=1/1/2; who_said_it=2/1/3; written_record=6/18/24 | 0 | 150 |

## Top five under the combined-count rule

**Rule.** Sort by fewest concepts with zero combined words, then highest minimum combined count among a unit's concepts, then highest combined sum, then unit identifier in ascending order. The script prints this ranking.

| Rank | Unit | Zero concepts | Minimum combined count | Combined sum |
|---:|---|---:|---:|---:|
| 1 | r2.measure | 0 | 20 | 325 |
| 2 | p2.matter | 0 | 9 | 543 |
| 3 | p2.force | 0 | 8 | 513 |
| 4 | b2.mending | 0 | 7 | 100 |
| 5 | ac2.flow | 0 | 7 | 28 |

## Ten thinnest scheduled concepts

**Fact.** The script sorts the concepts used by the 26 missing-book units by combined distinct word count, then by concept identifier. It prints each word and the level of its term entry.

| Concept | Combined count | Words on file |
|---|---:|---|
| balance | 1 | balance (L2) |
| letter | 1 | letter (L1) |
| reconciliation | 1 | reconcile (L2) |
| right_reason | 1 | right (L1) |
| two_shoulds_at_once | 1 | hard (L1) |
| agreeing | 2 | accept (L1), agree (L1) |
| being_wrong | 2 | false (L1), wrong (L1) |
| changing_your_mind | 2 | admit (L1), mind (L1) |
| claim_under_test | 2 | claim (L2), hypothesis (L2) |
| conservation_of_number | 2 | unchanged (L1), rearrange (L2) |

## Reconciliation with the fifth-trial report

**Fact.** The fifth-trial report called keeping_your_claim, letter, right_reason, and two_shoulds_at_once empty at levels one and two. The authoritative term list has entries for all four. Each is level one and is defined in curriculum/books/level_1/bk.dictionary.1.md.

| Concept | Term entry or entries | Level and defining book |
|---|---|---|
| keeping_your_claim | hold; holds | L1, curriculum/books/level_1/bk.dictionary.1.md |
| letter | letter | L1, curriculum/books/level_1/bk.dictionary.1.md |
| right_reason | right | L1, curriculum/books/level_1/bk.dictionary.1.md |
| two_shoulds_at_once | hard | L1, curriculum/books/level_1/bk.dictionary.1.md |

**Inference.** The fifth-trial script counted dictionary records in the level-one and level-two seed books. It did not include the separate level-one book bk.dictionary.1.md, where these four concepts' words are defined. More generally, vocabulary.json records word, concept, and level directly, while a seed-book count depends on which dictionary files it reads and how their records file words. Only the term entry word field contributes here. The forms field does not add counts. A word with its own term entry, such as hold and holds, counts as a distinct word even when one may be an inflection of the other. Repeated entries for the same word under the same concept count once; a word filed under several concepts counts once for each concept.

**Fact.** The reviewer found that folding the flagged inflected words into their base words changes no top-five position. The review identifies holds as a clear inflection; its other flags need manual checking.

**Judgement.** The report limits the measure to levels one and two because it assesses vocabulary available to a level-two unit. Its counts measure vocabulary recorded in files and do not assess coverage quality or writing readiness.
