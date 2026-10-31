# Level-one and level-two vocabulary on file

**Command.** python3 -I tmp/dromon-trial-6/readiness_l12.py "$PWD"

**Fact.** The level-one seed book blob is d32c51b14357971b24738b643e0e4c1210e910d4. The level-two seed book blob is b291839d07dabd48dc6866f777284aebc2015490. The script found 26 scheduled level-two units without a book.

**Fact.** Each concept count is shown as L1/L2/combined. It counts dictionary headwords whose record files that concept. A headword count measures vocabulary on file, not whether a module can be written.

| Unit | Concepts and counts (L1/L2/combined) | Zero concepts (combined) | Combined sum |
|---|---|---|---:|
| ac2.balance | balance=0/1/1; reconciliation=0/1/1; same_amount=1/2/3; exchange=8/35/43 | 0 | 48 |
| ac2.flow | stock_and_flow=0/7/7; using_up=3/18/21 | 0 | 28 |
| a2.plan | doing_in_order=2/3/5; feeling=17/45/62; goal=3/9/12; need=2/11/13; person=17/31/48; plan=2/3/5; way_of_doing=5/17/22 | 0 | 167 |
| a2.mistake | activity=7/33/40; can_and_cannot=5/6/11; enough=5/4/9; finished_or_not=1/2/3; mistake=2/1/3; only_what_was_asked=2/0/2; self_and_other=7/2/9 | 0 | 77 |
| c2.explain | explanation=0/3/3; discourse_marker=3/5/8; giving_a_reason=1/3/4; knowing=7/21/28; real_and_pretend=4/14/18; sentence=4/0/4; word=3/3/6 | 0 | 71 |
| c2.claim | claim_under_test=0/2/2; leaving_out=2/2/4; letter=0/0/0; name=2/1/3; saying_what_you_saw=2/8/10; standing_for=10/7/17; story=2/5/7 | 1 | 43 |
| c2.report | reporting=0/16/16; asking=1/5/6; close_enough=0/11/11; more_to_learn=2/2/4; saying_what_you_did=2/0/2; writing=2/13/15 | 0 | 54 |
| b2.keeping_going | body_part=18/21/39; growing=1/3/4; keeping_going=1/5/6; needing_supply=2/10/12; plant=10/60/70 | 0 | 131 |
| b2.mending | animal=8/45/53; being_hurt=2/13/15; mending=3/3/6; tending=1/15/16 | 0 | 90 |
| p2.force | emptiness=6/4/10; falling=7/1/8; force=9/36/45; household_object=36/82/118; inside_and_outside=4/16/20; joining_and_separating=6/24/30; liquid=14/52/66; moving_and_still=20/66/86; opening_and_shutting=4/1/5; raw_and_made=5/43/48; sound=15/13/28 | 0 | 464 |
| p2.matter | air=3/16/19; change=2/44/46; heat=5/16/21; material=20/79/99; metal=9/5/14; physical_property=35/92/127; presence=4/2/6; shape=12/47/59; touching=7/6/13; toy=8/12/20; weather=13/64/77 | 0 | 501 |
| f2.failing | failing=0/2/2; cause_and_effect=1/13/14; component_and_system=2/40/42; things_break=5/12/17; wearing_out=3/2/5 | 0 | 80 |
| f2.accident | accident=0/3/3; causal_chain=1/3/4; danger=5/33/38; living_and_not_living=5/17/22 | 0 | 67 |
| f2.checking | being_told=7/1/8; checking=3/9/12; dying=2/3/5 | 0 | 25 |
| h2.findout | finding_out=2/39/41; guess=2/6/8; not_always_known=1/3/4; settling_it=4/2/6 | 0 | 59 |
| h2.wrong | being_wrong=2/0/2; changing_your_mind=1/0/1; resting_on_a_guess=1/0/1; taking_on_faith=3/3/6 | 0 | 10 |
| i2.reason | agreeing=1/0/1; disagreeing=2/3/5; giving_a_reason=1/3/4; keeping_your_claim=0/0/0; opinion=2/0/2 | 1 | 12 |
| i2.rule | family=10/6/16; judged_by_another=2/1/3; people_together=6/25/31; rule=2/10/12; someone_in_charge=4/11/15 | 0 | 77 |
| m2.number | natural_number=0/13/13; place_value=0/3/3; grouping=0/17/17; same_and_different=2/29/31 | 0 | 64 |
| m2.addsub | addition=0/4/4; subtraction=0/3/3; correspondence=3/1/4; counting=2/5/7; more_and_fewer=7/18/25 | 0 | 43 |
| m2.howmuch | quantity=0/72/72; measuring=9/37/46; number_word_order=10/2/12; same_amount=1/2/3 | 0 | 133 |
| m2.logic | all_some_none=2/17/19; conservation_of_number=1/2/3; if_then=0/1/1; not_both=1/1/2 | 0 | 25 |
| n2.should | good_and_bad=9/48/57; keep_trying_or_stop=1/3/4; right_reason=0/0/0; should_and_should_not=1/8/9; two_shoulds_at_once=0/0/0 | 2 | 70 |
| n2.fair | allowed_or_not=1/6/7; choosing=2/9/11; fair_and_unfair=4/0/4; promise=1/2/3 | 0 | 25 |
| r2.measure | cycle=7/27/34; how_sure=3/17/20; measuring=9/37/46; sequence=4/22/26; spatial_position=18/138/156; unit=1/18/19 | 0 | 301 |
| r2.record | direction=5/43/48; duration=13/51/64; out_of_date=0/1/1; who_said_it=0/1/1; written_record=5/18/23 | 0 | 137 |

## Top five under the combined-count rule

**Rule.** Sort by fewest concepts with zero combined headwords, then highest minimum combined count among a unit's concepts, then highest sum of combined counts, then unit identifier in ascending order. The script prints the ranking as well as the table.

| Rank | Unit | Empty concepts | Minimum combined count | Combined sum |
|---:|---|---:|---:|---:|
| 1 | r2.measure | 0 | 19 | 301 |
| 2 | ac2.flow | 0 | 7 | 28 |
| 3 | p2.matter | 0 | 6 | 501 |
| 4 | b2.mending | 0 | 6 | 90 |
| 5 | p2.force | 0 | 5 | 464 |

**Fact.** The fourth-trial level-two ranking was r2.measure, ac2.flow, a2.plan, b2.keeping_going, b2.mending. Under combined counts the order is r2.measure, ac2.flow, p2.matter, b2.mending, p2.force. The first two stay in place. p2.matter and p2.force enter the top five; a2.plan and b2.keeping_going leave; b2.mending moves from fifth to fourth.

**Fact.** The fourth-trial delta names thirteen concepts with no level-two headword. Current level-one headwords are present for agreeing (1), being_wrong (2), changing_your_mind (1), fair_and_unfair (4), only_what_was_asked (2), opinion (2), resting_on_a_guess (1), saying_what_you_did (2), and sentence (4). No level-one headwords are present for keeping_your_claim (0), letter (0), right_reason (0), and two_shoulds_at_once (0). The script derives this list from the cited delta file and prints each current level-one count.

**Fact.** Concepts empty at both levels for these missing-book units are: keeping_your_claim, letter, right_reason, two_shoulds_at_once

**Inference.** Adding level-one headwords removes many previously zero concepts and changes which units sort highest under the same rule. This is a change in vocabulary counts, not evidence that the reordered units are more writable or better curriculum choices.
