# Readiness delta after agency batch five

**Fact.** I ran python3 -I docs/process/trials/dromon_trial_3/readiness.py "$PWD" on 2026-10-30. The level-two dictionary seed book blob was 99d6bb49533dd3424bfe807e1c2976fd44b0d97d. The comparison snapshot used blob 556c47c4d2a09500f12ed695c149d31528e03a1b.

**Fact.** Every one of the 26 units without books gained at least one concept headword. Concepts with positive gains are listed below. Each value is the increase in level-two headwords since the comparison snapshot. Concepts with zero increase are omitted.

| Unit | Concepts gaining headwords |
|---|---|
| ac2.balance | exchange +2 |
| ac2.flow | using_up +7 |
| a2.plan | doing_in_order +3; feeling +2; need +3; person +1; plan +1; way_of_doing +2 |
| a2.mistake | activity +3; enough +4; finished_or_not +1 |
| c2.explain | explanation +1; giving_a_reason +1; knowing +5; real_and_pretend +2; word +1 |
| c2.claim | name +1; saying_what_you_saw +1; standing_for +1 |
| c2.report | reporting +2; asking +2; close_enough +2; writing +1 |
| b2.keeping_going | body_part +6; keeping_going +1; needing_supply +3; plant +5 |
| b2.mending | animal +5; being_hurt +7; mending +1 |
| p2.force | emptiness +1; force +2; household_object +14; inside_and_outside +9; joining_and_separating +6; liquid +9; moving_and_still +8; raw_and_made +8 |
| p2.matter | change +13; heat +2; material +16; metal +2; physical_property +6; presence +2; shape +12; touching +2; toy +1; weather +8 |
| f2.failing | cause_and_effect +1; component_and_system +6; things_break +1; wearing_out +2 |
| f2.accident | danger +5; living_and_not_living +1 |
| f2.checking | checking +3 |
| h2.findout | finding_out +9; not_always_known +1 |
| h2.wrong | taking_on_faith +2 |
| i2.reason | disagreeing +1; giving_a_reason +1 |
| i2.rule | family +1; judged_by_another +1; people_together +4; rule +2; someone_in_charge +1 |
| m2.number | grouping +2; same_and_different +4 |
| m2.addsub | addition +2; correspondence +1; counting +4; more_and_fewer +4 |
| m2.howmuch | quantity +9; measuring +4 |
| m2.logic | all_some_none +2 |
| n2.should | good_and_bad +16; keep_trying_or_stop +2; should_and_should_not +1 |
| n2.fair | allowed_or_not +1; choosing +3 |
| r2.measure | cycle +7; how_sure +2; measuring +4; sequence +3; spatial_position +19; unit +6 |
| r2.record | direction +7; duration +9; written_record +7 |

**Fact.** The top five changed under the third-trial report's ranking rule. The earlier order was r2.measure, ac2.flow, b2.keeping_going, m2.number, f2.accident. The current order is r2.measure, ac2.flow, a2.plan, b2.keeping_going, b2.mending. The first two positions stayed the same; positions three through five changed.

**Fact.** Concepts scheduled in missing units with no level-two headword are: agreeing, being_wrong, changing_your_mind, fair_and_unfair, keeping_your_claim, letter, only_what_was_asked, opinion, resting_on_a_guess, right_reason, saying_what_you_did, sentence, and two_shoulds_at_once.

**Inference.** All 26 units gained vocabulary somewhere in their scheduled concepts, while some individual concepts in those units had no gain. The ranking change reflects the count rule applied to current coverage. It does not establish which unit is easiest to write.
