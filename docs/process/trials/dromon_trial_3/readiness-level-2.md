# Level-two vocabulary on file

**Fact.** I read the level-two dictionary seed book on 2026-10-30 02:45:32 UTC. Its Git blob hash was `556c47c4d2a09500f12ed695c149d31528e03a1b`. The level-one seed book was also read for comparison. The worker had finished admissions; these counts are a snapshot of the current tree.

**Command.** `python -I tmp/dromon-trial-4/readiness.py "$PWD"`. The script at `readiness.py` prints each missing unit's concept counts, zero-count concept count, level-two sum, a deterministic ranking, and scheduled concepts grouped by level-two count. It checks the expected `bk.<unit-id>.md` path. It found 26 units without books.

**Fact.** Each count is the number of dictionary headwords whose record lists that concept. Counts are shown as `L2/L1`. A headword count measures vocabulary on file, not whether a module can be written.

| Unit | Concepts and counts (L2/L1) | Zero L2 concepts | L2 sum |
|---|---|---:|---:|
| ac2.balance | balance=1 L2/0 L1; reconciliation=1 L2/0 L1; same_amount=2 L2/1 L1; exchange=33 L2/8 L1 | 0 | 37 |
| ac2.flow | stock_and_flow=7 L2/0 L1; using_up=11 L2/3 L1 | 0 | 18 |
| a2.plan | doing_in_order=0 L2/2 L1; feeling=43 L2/17 L1; goal=9 L2/3 L1; need=8 L2/2 L1; person=30 L2/17 L1; plan=2 L2/2 L1; way_of_doing=15 L2/5 L1 | 1 | 107 |
| a2.mistake | activity=30 L2/7 L1; can_and_cannot=6 L2/5 L1; enough=0 L2/5 L1; finished_or_not=1 L2/1 L1; mistake=1 L2/2 L1; only_what_was_asked=0 L2/2 L1; self_and_other=2 L2/7 L1 | 2 | 40 |
| c2.explain | explanation=2 L2/0 L1; discourse_marker=5 L2/3 L1; giving_a_reason=2 L2/1 L1; knowing=16 L2/7 L1; real_and_pretend=11 L2/4 L1; sentence=0 L2/4 L1; word=2 L2/3 L1 | 1 | 38 |
| c2.claim | claim_under_test=2 L2/0 L1; leaving_out=2 L2/2 L1; letter=0 L2/0 L1; name=0 L2/2 L1; saying_what_you_saw=7 L2/2 L1; standing_for=5 L2/10 L1; story=5 L2/2 L1 | 2 | 21 |
| c2.report | reporting=14 L2/0 L1; asking=3 L2/1 L1; close_enough=9 L2/0 L1; more_to_learn=2 L2/2 L1; saying_what_you_did=0 L2/2 L1; writing=12 L2/2 L1 | 1 | 40 |
| b2.keeping_going | body_part=15 L2/18 L1; growing=3 L2/1 L1; keeping_going=4 L2/1 L1; needing_supply=7 L2/2 L1; plant=55 L2/10 L1 | 0 | 84 |
| b2.mending | animal=40 L2/8 L1; being_hurt=6 L2/2 L1; mending=2 L2/3 L1; tending=15 L2/1 L1 | 0 | 63 |
| p2.force | emptiness=3 L2/6 L1; falling=1 L2/7 L1; force=34 L2/9 L1; household_object=68 L2/36 L1; inside_and_outside=7 L2/4 L1; joining_and_separating=18 L2/6 L1; liquid=43 L2/14 L1; moving_and_still=58 L2/20 L1; opening_and_shutting=1 L2/4 L1; raw_and_made=35 L2/5 L1; sound=13 L2/15 L1 | 0 | 281 |
| p2.matter | air=16 L2/3 L1; change=31 L2/2 L1; heat=14 L2/5 L1; material=62 L2/20 L1; metal=3 L2/9 L1; physical_property=86 L2/35 L1; presence=0 L2/4 L1; shape=35 L2/12 L1; touching=4 L2/7 L1; toy=11 L2/8 L1; weather=56 L2/13 L1 | 1 | 318 |
| f2.failing | failing=2 L2/0 L1; cause_and_effect=12 L2/1 L1; component_and_system=34 L2/2 L1; things_break=11 L2/5 L1; wearing_out=0 L2/3 L1 | 1 | 59 |
| f2.accident | accident=3 L2/0 L1; causal_chain=3 L2/1 L1; danger=28 L2/5 L1; living_and_not_living=16 L2/5 L1 | 0 | 50 |
| f2.checking | being_told=1 L2/7 L1; checking=6 L2/3 L1; dying=3 L2/2 L1 | 0 | 10 |
| h2.findout | finding_out=30 L2/2 L1; guess=6 L2/2 L1; not_always_known=2 L2/1 L1; settling_it=2 L2/4 L1 | 0 | 40 |
| h2.wrong | being_wrong=0 L2/2 L1; changing_your_mind=0 L2/1 L1; resting_on_a_guess=0 L2/1 L1; taking_on_faith=1 L2/3 L1 | 3 | 1 |
| i2.reason | agreeing=0 L2/1 L1; disagreeing=2 L2/2 L1; giving_a_reason=2 L2/1 L1; keeping_your_claim=0 L2/0 L1; opinion=0 L2/2 L1 | 3 | 4 |
| i2.rule | family=5 L2/10 L1; judged_by_another=0 L2/2 L1; people_together=21 L2/6 L1; rule=8 L2/2 L1; someone_in_charge=10 L2/4 L1 | 1 | 44 |
| m2.number | natural_number=13 L2/0 L1; place_value=3 L2/0 L1; grouping=15 L2/0 L1; same_and_different=24 L2/2 L1 | 0 | 55 |
| m2.addsub | addition=2 L2/0 L1; subtraction=3 L2/0 L1; correspondence=0 L2/3 L1; counting=1 L2/2 L1; more_and_fewer=14 L2/7 L1 | 1 | 20 |
| m2.howmuch | quantity=63 L2/0 L1; measuring=33 L2/9 L1; number_word_order=2 L2/10 L1; same_amount=2 L2/1 L1 | 0 | 100 |
| m2.logic | all_some_none=14 L2/2 L1; conservation_of_number=2 L2/1 L1; if_then=1 L2/0 L1; not_both=1 L2/1 L1 | 0 | 18 |
| n2.should | good_and_bad=32 L2/9 L1; keep_trying_or_stop=0 L2/1 L1; right_reason=0 L2/0 L1; should_and_should_not=7 L2/1 L1; two_shoulds_at_once=0 L2/0 L1 | 3 | 39 |
| n2.fair | allowed_or_not=5 L2/1 L1; choosing=6 L2/2 L1; fair_and_unfair=0 L2/4 L1; promise=2 L2/1 L1 | 1 | 13 |
| r2.measure | cycle=20 L2/7 L1; how_sure=13 L2/3 L1; measuring=33 L2/9 L1; sequence=19 L2/4 L1; spatial_position=119 L2/18 L1; unit=12 L2/1 L1 | 0 | 216 |
| r2.record | direction=36 L2/5 L1; duration=42 L2/13 L1; out_of_date=1 L2/0 L1; who_said_it=1 L2/0 L1; written_record=10 L2/5 L1 | 0 | 90 |

## Five units with the most vocabulary on file under the ranking rule

**Rule.** Sort by ascending number of scheduled concepts with zero level-two headwords, then descending minimum level-two headword count among the unit's concepts, then descending sum of level-two counts, then ascending unit identifier. This orders vocabulary counts only. It does not rank writing readiness.

| Rank | Unit | Zero concepts | Minimum L2 count | L2 sum |
|---:|---|---:|---:|---:|
| 1 | r2.measure | 0 | 12 | 216 |
| 2 | ac2.flow | 0 | 7 | 18 |
| 3 | b2.keeping_going | 0 | 3 | 84 |
| 4 | m2.number | 0 | 3 | 55 |
| 5 | f2.accident | 0 | 3 | 50 |

## Thin scheduled concepts by level-two headword count

**Fact.** The following groups cover concepts scheduled in units without books. Grouping is produced by the same script run.

- **0**: agreeing, being_wrong, changing_your_mind, correspondence, doing_in_order, enough, fair_and_unfair, judged_by_another, keep_trying_or_stop, keeping_your_claim, letter, name, only_what_was_asked, opinion, presence, resting_on_a_guess, right_reason, saying_what_you_did, sentence, two_shoulds_at_once, wearing_out
- **1**: balance, being_told, counting, falling, finished_or_not, if_then, mistake, not_both, opening_and_shutting, out_of_date, reconciliation, taking_on_faith, who_said_it
- **2**: addition, claim_under_test, conservation_of_number, disagreeing, explanation, failing, giving_a_reason, leaving_out, mending, more_to_learn, not_always_known, number_word_order, plan, promise, same_amount, self_and_other, settling_it, word
- **3**: accident, asking, causal_chain, dying, emptiness, growing, metal, place_value, subtraction
- **4**: keeping_going, touching
- **5**: allowed_or_not, discourse_marker, family, standing_for, story
- **6**: being_hurt, can_and_cannot, checking, choosing, guess
- **7**: inside_and_outside, needing_supply, saying_what_you_saw, should_and_should_not, stock_and_flow
- **8**: need, rule
- **9**: close_enough, goal
- **10**: someone_in_charge, written_record
- **11**: real_and_pretend, things_break, toy, using_up
- **12**: cause_and_effect, unit, writing
- **13**: how_sure, natural_number, sound
- **14**: all_some_none, heat, more_and_fewer, reporting
- **15**: body_part, grouping, tending, way_of_doing
- **16**: air, knowing, living_and_not_living
- **18**: joining_and_separating
- **19**: sequence
- **20**: cycle
- **21**: people_together
- **24**: same_and_different
- **28**: danger
- **30**: activity, finding_out, person
- **31**: change
- **32**: good_and_bad
- **33**: exchange, measuring
- **34**: component_and_system, force
- **35**: raw_and_made, shape
- **36**: direction
- **40**: animal
- **42**: duration
- **43**: feeling, liquid
- **55**: plant
- **56**: weather
- **58**: moving_and_still
- **62**: material
- **63**: quantity
- **68**: household_object
- **86**: physical_property
- **119**: spatial_position

**Judgement.** Zero-count concepts are candidates for later lexicon review, not an automatic admission list. A low count alone does not establish that more headwords are needed.
