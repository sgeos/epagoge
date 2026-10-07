# Level-two era-overlap batch

Recorded 2026-10-07. This batch accounts for every remaining word in the
overlap pool of the lexicon scan of 2026-09-27. The pool is the set of
strings frequent at threshold five in at least one historical reader and in
at least one modern federal source. Such words are neither archaic nor
narrowly technical, which is a reason for selection rather than a rank. The
scan admitted 47 of them at the time. On 2026-10-07, 139 pool strings were
not admissible at level two. Seven bases of scanned inflections were added
as candidates, so the review covers 146 entries.

## Measured outcome

Agent review admitted 83 words, deferred 20 and excluded 43. Level two rose
from 966 to 1,049 distinct headwords, leaving 8,951 to the approximate
ten-thousand-word target. Level one remains at 849. Required definition
coverage is 812 of 812 at level one and 1,012 of 1,012 at level two. Both
dictionaries are completely grounded. All 523 level-one books and the
reference checkpoint match their recorded hashes. The 64 earlier review
artifacts match `preservation.json`.

The 43 exclusions are 20 single letters, six fragments or abbreviations,
five proper nouns or words derived from them, one spelling variant and
eleven inflections whose base is reviewed as its own candidate. The 20 deferrals
each state a reason. Most are words whose two eras use different senses, so
overlap frequency supports no single sense. Examples are band, cell,
conduct, fine, matter, state and vessel. Three overlaps are artifacts. Mass
is frequent in the historical readers as an abbreviation of a state name,
and fort and march are frequent in the modern sources as a place name and
a month. Present, produce, rather and therefore are already admitted at
levels five and six, and lowering a level is an authored decision outside
this batch. Skies is recorded as a finding below.

## How the definitions were written

No teacher ran. Host swap stood at 7.9 of 9.2 gigabytes with about 140
megabytes of free pages before work began, and the teacher needs about
eighteen gigabytes resident. `authoring.json` records that declaration, the
candidate and vocabulary hashes, the pool rule and the hash of the scan
report under the ignored `tmp/lexicon-sources/scan_f5.json`.

Every definition was written by the agent and checked against the exact
level-two vocabulary before admission. The admission tool then applied its
own licensing and closure checks to all 83 together. Six definitions
depend on other words in the batch. Nearly uses almost, unless uses except,
sudden and suddenly use expect, and dollar and war use the plural of
country. None of those words depends back on its dependant, so no pair is
defined only through each other.

Sense choices follow the sources rather than ease of definition. Where a
word is admitted at a higher level under another concept, position and
support receive distinct level-two senses under spatial_position and force.
The higher-level entries are unchanged.

## Agent edits after admission

The generated past form striked was replaced by struck, and strike was added
to the irregular verb table after the gate refused the hand edit alone. Offer,
scatter and travel were classified as not doubling. Common and usually
were first assigned to tending, whose admitted words concern caring for
something, and were moved to cycle beside often and sometimes. The change
was made in the vocabulary, the dictionary record and the thesaurus entry.
Species was added to the irregular plural table with an unchanged plural, so
it declares noun without generating specieses. Travel follows the single-l
spelling of the modern sources.

## Findings outside the batch

**Prompts banned admitted words.** The prompt builder printed every
substitution key as banned at every level. Twelve keys were admissible at
level two and seven at level one, and this batch admits more, including
beneath, beyond, during, form, object and position. Prompts now drop keys
admissible at the prompted level. The gate reports the remaining
contradictions without failing. At level one these are beside, cause, great,
greater, length, single and unknown. Color is admitted at level two although
the substitution table maps it to colour, which looks like the spelling
decision that refused gray, and is left for the operator.

**Sky has no plural.** The level-one headword sky declares no part of speech,
so skies is not admissible anywhere. Adding it changes a closed level-one
entry and is recorded rather than made.

**Sweet and sour.** These are sensory qualities of the same kind as the
colours this lexicon grounds ostensively. An ostensive admission would
enlarge the seed and is recommended to the operator rather than made.

## Evidence and verification

`candidates.json` records every entry and its proposed concept.
`authoring.json` declares that no teacher ran. `review.json` gives every
decision with a reason, and for admitted words the definition, concept,
part of speech, source and reviewed forms. `admitted.json` is the admission
input. `before.json` and `measurement.json` retain the measured change.
`preservation.json` holds the hashes of earlier review artifacts.

    .venv/bin/python tools/measure_lexicon_increment.py \
      evals/review/level_2_era_overlap \
      --check evals/review/level_2_era_overlap/measurement.json

## Limits

This is one agent-authored batch from a stated pool. It does not measure
general throughput, and the pool is now exhausted. Semantic review is agent
review without independent expert validation. Several definitions are
introductory simplifications, such as species without interbreeding and
south by the rising sun. No word in this batch is yet used by a level-two
book, so the coverage rule is unmet for level two as it was before.
