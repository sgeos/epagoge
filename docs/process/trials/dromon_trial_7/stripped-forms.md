# Threshold-four stripped-form candidates

**Fact.** The vocabulary file blob was 26fd70343c9a9193e97d22e2fafa176957f04d56. I ran python3 -I tmp/dromon-trial-8/stripped_forms.py "$PWD". It found 160 frequent strings meeting the stated filters.

**Method.** The script imports Vocabulary.lookup from src/epagoge/vocabulary.py, the same lookup called by tools/candidate_pool.py. The scan's frequent keys are the input strings. A candidate is kept only when lookup resolves it at level two or below, the string is not a term word or a listed form, and no review record lists it as reviewed_forms or has decision exclude. A listed form means the exact word field or an exact value in a term's explicit forms field, as returned by Term.surface_forms. Derived suffix forms are not treated as listed forms unless explicitly recorded. Occurrences use the shared vocabulary tokenise function and the scan's alphabetic-token rule. The vector gives counts in the source order below, including zeroes.

**Fact.** Each resolved headword's concepts and levels are listed for all senses attached to that headword. The frequency vector positions map to these source texts.

- S01 src_bens_guide_4_8.txt
- S02 src_bens_guide_4_8_rest.txt
- S03 src_eia_kids.txt
- S04 src_mcguffey_1.txt
- S05 src_mcguffey_2.txt
- S06 src_mcguffey_3.txt
- S07 src_mcguffey_4.txt
- S08 src_nasa_kids_earth.txt
- S09 src_nasa_spaceplace.txt
- S10 src_nasa_starchild_l1.txt
- S11 src_noaa_jetstream.txt
- S12 src_noaa_ocean.txt
- S13 src_spaceplace_rest.txt
- S14 src_starchild_l1_full.txt
- S15 src_usgs_water.txt
- S16 src_usgs_wss_rest.txt

| String | Resolves to | Headword concepts and levels | Total occurrences | Counts S01 to S16 |
|---|---|---|---:|---|
| united | unit | unit@L1 | 718 | 6, 2, 166, 0, 0, 1, 3, 1, 1, 1, 190, 4, 16, 11, 55, 261 |
| basics | basic | physical_property@L2 | 303 | 0, 0, 259, 0, 0, 0, 0, 0, 0, 0, 0, 13, 0, 0, 4, 27 |
| buildings | build | activity@L1 | 229 | 0, 0, 140, 0, 0, 1, 1, 1, 0, 0, 47, 1, 1, 0, 6, 31 |
| graphics | graphic | writing@L2 | 165 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 4, 0, 0, 153, 1, 2 |
| flooding | flood | weather@L2 | 162 | 0, 0, 0, 0, 1, 0, 1, 2, 0, 0, 62, 8, 1, 0, 5, 82 |
| based | base | spatial_position@L2 | 144 | 0, 0, 19, 0, 0, 0, 0, 2, 5, 1, 51, 19, 9, 3, 6, 29 |
| tornadoes | tornado | weather@L2 | 109 | 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 107, 0, 1, 0, 0, 0 |
| woods | wood | plant@L1 | 91 | 0, 0, 42, 15, 9, 12, 11, 0, 0, 0, 0, 0, 0, 0, 0, 2 |
| causing | cause | cause_and_effect@L1 | 78 | 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 36, 1, 6, 1, 3, 28 |
| accounted | account | reporting@L2 | 71 | 0, 0, 56, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15 |
| james | jam | moving_and_still@L2 | 71 | 0, 0, 0, 14, 9, 27, 7, 0, 0, 0, 0, 0, 13, 0, 0, 1 |
| forecasting | forecast | guess@L2 | 69 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 62, 1, 1, 0, 0, 5 |
| resulting | result | cause_and_effect@L2 | 66 | 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 30, 0, 0, 0, 0, 31 |
| circulations | circulation | cycle@L2 | 62 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 62, 0, 0, 0, 0, 0 |
| orbiting | orbit | cycle@L2 | 60 | 0, 0, 0, 0, 0, 0, 0, 4, 3, 0, 13, 0, 34, 6, 0, 0 |
| warnings | warn | danger@L2 | 51 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 49, 0, 2, 0, 0, 0 |
| longwaves | longwave | physical_property@L2 | 50 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 50, 0, 0, 0, 0, 0 |
| fronts | front | spatial_position@L1 | 47 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 46, 1, 0, 0, 0, 0 |
| shortwaves | shortwave | physical_property@L2 | 47 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 47, 0, 0, 0, 0, 0 |
| powered | power | force@L2 | 46 | 0, 0, 7, 0, 0, 0, 0, 29, 0, 0, 1, 0, 7, 0, 0, 2 |
| soils | soil | material@L2 | 45 | 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 1, 0, 0, 0, 0, 42 |
| metals | metal | metal@L1 | 44 | 0, 0, 13, 0, 0, 0, 0, 0, 0, 0, 1, 0, 4, 0, 2, 24 |
| towards | toward | direction@L1 | 44 | 0, 0, 0, 0, 0, 2, 6, 0, 0, 0, 7, 1, 2, 0, 0, 26 |
| mines | mine | having@L1 | 40 | 0, 0, 32, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8 |
| echoes | echo | sound@L2 | 39 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 37, 0, 0, 0, 0, 2 |
| seconds | second | number_word_order@L1 | 38 | 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 17, 3, 5, 1, 2, 6 |
| wastes | waste | using_up@L2 | 36 | 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 31 |
| bearing | bear | toy@L1 | 35 | 0, 0, 3, 0, 0, 2, 3, 0, 0, 0, 0, 0, 0, 0, 4, 23 |
| solids | solid | material@L1 | 34 | 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 4, 25 |
| salts | salt | material@L2 | 33 | 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 4, 0, 0, 0, 2, 26 |
| processing | process | way_of_doing@L2 | 31 | 0, 0, 25, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 5 |
| tracking | track | spatial_position@L2 | 31 | 0, 0, 5, 0, 0, 0, 0, 3, 1, 0, 19, 0, 0, 0, 0, 3 |
| rating | rat | animal@L2 | 30 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 1, 0, 0, 0, 27 |
| equals | equal | same_amount@L1 | 26 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 17, 3, 0, 1, 0, 4 |
| issued | issue | settling_it@L2 | 26 | 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 25, 0, 0, 0, 0, 0 |
| lowered | low | spatial_position@L1 | 26 | 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 20 |
| volumes | volume | measuring@L2 | 26 | 0, 0, 12, 0, 0, 0, 3, 0, 0, 0, 1, 0, 0, 0, 0, 10 |
| positioning | position | claim_under_test@L6, spatial_position@L2 | 25 | 0, 0, 2, 0, 0, 0, 0, 0, 1, 0, 1, 19, 1, 0, 0, 1 |
| timing | time | duration@L1 | 25 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 2, 19 |
| fired | fire | heat@L1 | 24 | 0, 0, 6, 0, 0, 0, 4, 0, 0, 0, 1, 1, 0, 0, 4, 8 |
| sediments | sediment | material@L2 | 24 | 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 22 |
| sized | size | physical_property@L1 | 24 | 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 10, 1, 2, 10 |
| concerned | concern | feeling@L2 | 21 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 3, 1, 0, 2, 11 |
| fishing | fish | animal@L1 | 21 | 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 4, 1, 3, 0, 0, 10 |
| processed | process | way_of_doing@L2 | 21 | 0, 0, 10, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1, 0, 0, 6 |
| forced | force | force@L1 | 20 | 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 12, 0, 1, 0, 0, 4 |
| outdoors | outdoor | inside_and_outside@L2 | 20 | 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 13, 0, 0, 0, 0, 6 |
| conditioning | condition | latent_condition@L5, physical_property@L2 | 19 | 0, 0, 16, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3 |
| flooded | flood | weather@L2 | 19 | 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 5, 0, 1, 0, 0, 11 |
| interested | interest | finding_out@L2 | 19 | 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 4, 0, 7, 0, 0, 4 |
| blooded | blood | body_part@L2 | 18 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 15 |
| discharges | discharge | liquid@L2 | 18 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 16 |
| news | new | not_always_known@L1, physical_property@L1 | 18 | 0, 0, 0, 0, 0, 1, 2, 0, 0, 0, 4, 0, 0, 0, 2, 9 |
| completed | complete | finished_or_not@L2 | 17 | 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 6, 0, 1, 3, 0, 3 |
| neighboring | neighbor | people_together@L2 | 17 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 10, 0, 0, 6 |
| rounded | round | shape@L1 | 17 | 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 5, 0, 1, 0, 4, 5 |
| viewed | view | opinion@L1 | 17 | 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 8, 1, 2, 2, 1, 1 |
| deposited | deposit | material@L2 | 16 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 14 |
| farming | farm | spatial_position@L2 | 16 | 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 12 |
| vocals | vocal | sound@L2 | 16 | 0, 0, 0, 2, 1, 1, 12, 0, 0, 0, 0, 0, 0, 0, 0, 0 |
| electronics | electronic | physical_property@L2 | 15 | 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 3, 0, 2, 0, 0, 3 |
| filtered | filter | joining_and_separating@L2 | 15 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 4, 10 |
| gaging | gage | measuring@L2 | 15 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 15 |
| greens | green | physical_property@L1 | 15 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 13 |
| modeling | model | toy@L1 | 15 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 2, 0, 0, 3 |
| glasses | glass | material@L1 | 14 | 0, 0, 0, 2, 0, 0, 1, 0, 0, 0, 0, 0, 4, 0, 4, 3 |
| mined | mine | having@L1 | 14 | 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 3 |
| resulted | result | cause_and_effect@L2 | 14 | 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 8 |
| alerts | alert | finding_out@L2 | 13 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 1, 0, 0, 5 |
| discharged | discharge | liquid@L2 | 13 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13 |
| highs | high | spatial_position@L1 | 13 | 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 11, 0, 0, 0, 0, 0 |
| orbited | orbit | cycle@L2 | 13 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 9, 3, 0, 0 |
| persons | person | person@L1 | 13 | 0, 0, 0, 0, 1, 1, 8, 0, 1, 0, 0, 0, 0, 0, 0, 2 |
| watering | water | liquid@L1 | 13 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 9 |
| boating | boat | household_object@L1 | 12 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 8 |
| forested | forest | plant@L1 | 12 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 12 |
| lowers | low | spatial_position@L1 | 12 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 6 |
| lows | low | spatial_position@L1 | 12 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11, 0, 0, 0, 0, 1 |
| openings | open | opening_and_shutting@L1 | 12 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 10 |
| powering | power | force@L2 | 12 | 0, 0, 11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0 |
| seated | seat | household_object@L2 | 12 | 0, 0, 0, 5, 3, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0 |
| taping | tap | touching@L1 | 12 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 3, 0, 0, 0 |
| earths | earth | material@L1 | 11 | 0, 0, 0, 0, 0, 0, 0, 2, 4, 0, 0, 0, 2, 0, 0, 3 |
| goods | good | good_and_bad@L1 | 11 | 1, 0, 5, 0, 0, 0, 4, 0, 0, 0, 1, 0, 0, 0, 0, 0 |
| plastics | plastic | material@L1 | 11 | 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 6 |
| shading | shade | physical_property@L2 | 11 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0, 0, 0, 0, 1 |
| bathing | bath | household_object@L2 | 10 | 0, 0, 3, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 2, 4 |
| blocked | block | toy@L1 | 10 | 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 5, 0, 2, 0, 0, 0 |
| filtering | filter | joining_and_separating@L2 | 10 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 6 |
| lined | line | shape@L1 | 10 | 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 1, 0, 4, 0, 0, 1 |
| lowering | low | spatial_position@L1 | 10 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 8 |
| peaked | peak | spatial_position@L2 | 10 | 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 4 |
| pleased | please | asking_politely@L1 | 10 | 0, 0, 0, 0, 2, 6, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0 |
| readings | read | writing@L1 | 10 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 9 |
| straws | straw | material@L1 | 10 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 7, 0, 2, 0 |
| training | train | moving_and_still@L2 | 10 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 1, 1, 2, 0, 0 |
| valued | value | exchange@L2 | 10 | 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 4 |
| viewing | view | opinion@L1 | 10 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 4, 0, 0, 5 |
| afterwards | afterward | duration@L2 | 9 | 0, 0, 0, 0, 0, 1, 6, 0, 0, 0, 1, 0, 0, 0, 0, 1 |
| aging | age | duration@L2 | 9 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 1, 0, 0, 0, 3 |
| blocking | block | toy@L1 | 9 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 0, 0, 0, 0, 0 |
| housing | house | household_object@L1 | 9 | 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 6 |
| settings | set | activity@L1, correspondence@L1, grouping@L1 | 9 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9 |
| accounting | account | reporting@L2 | 8 | 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 3 |
| forcing | force | force@L1 | 8 | 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 1 |
| grasses | grass | plant@L1 | 8 | 0, 0, 4, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0 |
| sands | sand | material@L1 | 8 | 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1 |
| slows | slow | duration@L1 | 8 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 1, 0, 0, 3 |
| troubled | trouble | danger@L2 | 8 | 0, 0, 0, 0, 0, 2, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0 |
| wasted | waste | using_up@L2 | 8 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8 |
| barking | bark | plant@L2 | 7 | 0, 0, 0, 0, 2, 1, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0 |
| coverings | cover | opening_and_shutting@L1 | 7 | 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 4, 0, 0, 0, 0, 0 |
| fats | fat | physical_property@L1 | 7 | 0, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 |
| modeled | model | toy@L1 | 7 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 1, 0, 0, 2 |
| recharged | recharge | liquid@L2 | 7 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 6 |
| roses | rise | falling@L1 | 7 | 0, 0, 0, 0, 1, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0 |
| screened | screen | household_object@L2 | 7 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 5 |
| secured | secure | danger@L2 | 7 | 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 1, 0, 0, 2 |
| sided | side | shape@L1 | 7 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 5, 0, 0, 1 |
| siding | side | shape@L1 | 7 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0 |
| subjected | subject | knowing@L2 | 7 | 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6 |
| waxing | wax | material@L2 | 7 | 0, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0, 0, 0, 0, 0, 0 |
| drawings | draw | writing@L1 | 6 | 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 2 |
| featured | feature | component_and_system@L2 | 6 | 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 4, 0, 0, 0, 0, 1 |
| forked | fork | household_object@L1 | 6 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 4 |
| frosting | frost | weather@L2 | 6 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0 |
| layered | layer | shape@L2 | 6 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 1, 0, 0, 1 |
| ranging | ring | sound@L1 | 6 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 1, 1 |
| recharging | recharge | liquid@L2 | 6 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6 |
| riches | rich | having@L1 | 6 | 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0 |
| shaded | shade | physical_property@L2 | 6 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 1, 0, 0, 0 |
| strengths | strength | force@L2 | 6 | 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 5, 0, 0, 0, 0, 0 |
| armed | arm | body_part@L1 | 5 | 1, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0 |
| equaled | equal | same_amount@L1 | 5 | 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4 |
| feelings | feel | feeling@L1 | 5 | 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0 |
| inflows | inflow | stock_and_flow@L2 | 5 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5 |
| issuing | issue | settling_it@L2 | 5 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 1 |
| kidding | kid | person@L2 | 5 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 1 |
| logged | log | written_record@L1 | 5 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5 |
| natured | nature | living_and_not_living@L2 | 5 | 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0 |
| normals | normal | tending@L2 | 5 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0 |
| projected | project | plan@L2 | 5 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 4 |
| pulsed | pulse | body_part@L2 | 5 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0 |
| recharges | recharge | liquid@L2 | 5 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5 |
| recordings | record | written_record@L1 | 5 | 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0 |
| rounding | round | shape@L1 | 5 | 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1 |
| bottled | bottle | household_object@L1 | 4 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4 |
| coolers | cool | change@L2, heat@L1 | 4 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4 |
| doubles | double | quantity@L2 | 4 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4 |
| farmed | farm | spatial_position@L2 | 4 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4 |
| grained | grain | plant@L2 | 4 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4 |
| motioning | motion | moving_and_still@L2 | 4 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4 |
| occuring | occur | change@L2 | 4 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4 |
| outflows | outflow | stock_and_flow@L2 | 4 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4 |
| plating | plate | household_object@L1 | 4 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4 |
| poisoning | poison | danger@L2 | 4 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4 |
| screening | screen | household_object@L2 | 4 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4 |
| squared | square | shape@L1 | 4 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0 |
| troubles | trouble | danger@L2 | 4 | 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0 |
| weathering | weather | weather@L1 | 4 | 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4 |

## Ten most frequent strings

**Judgement.** I read two or three matching source lines for each string and compared those uses with the recorded headword sense.

- **united to unit.** No. The EIA lines use United States as a country name. Unit is a size counted in measurement.
- **basics to basic.** No. The sampled EIA and NOAA headings use basics for introductory topic material. Basic is defined here as the opposite of acidic for a liquid.
- **buildings to build.** No. NOAA and USGS lines use buildings for structures. Build is a verb meaning to make something by putting parts together.
- **graphics to graphic.** Probably related. The sampled StarChild lines are image-credit headings, and graphic is defined as a picture or drawing. The evidence is limited to repeated headings.
- **flooding to flood.** Yes, the sampled USGS lines describe water covering coastal land and the frequency of such events. That is close to the recorded flood sense.
- **based to base.** No. NOAA uses based on to mean founded on an assumption or appearance. Base is the bottom part a thing stands on.
- **tornadoes to tornado.** Yes. The NOAA lines name tornado hazards and describe tornadoes as weather events, matching the headword sense.
- **woods to wood.** No. The McGuffey lines use woods for forested places, while wood is defined as material a tree is made of. Some EIA matches are a proper-name heading.
- **causing to cause.** Yes. The NOAA lines describe a force causing a ball to move, matching the sense of what makes a thing happen.
- **accounted to account.** No. The EIA lines use accounted for to mean represented or made up a share. Account is defined as what someone says happened.

## Comparison with the threshold-five review

**Fact.** The fifth-trial review found 17 such strings at threshold five. This threshold-four scan produces 160. Five of the earlier 17 remain in this list: buildings, flooding, graphics, powered and united. The other twelve are now term words or listed forms, reviewed forms, or exclusions.

**Inference.** The larger threshold-four result reflects the lower frequency cutoff and the more extensive scan. A suffix lookup match and occurrence frequency do not establish that the source's sense is carried by the headword.
