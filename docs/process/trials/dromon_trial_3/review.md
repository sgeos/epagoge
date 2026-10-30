# Review of the fourth agency batch and of the level-two readiness report

Reviewer line. Recorded 2026-10-29. No tracked file was edited. The gate was not run, as instructed. Labels: **[F]** fact measured on this tree, **[I]** inference, **[H]** judgement.

**[F]** The worktree is at `80ff5cd`. The third batch and its follow-up are committed there, so the diffs below are the fourth batch alone.

## Part A. Fourth agency batch

### A.1 Completion clauses and commands

| Clause | Result | Command |
|---|---|---|
| Pool drawn and every word decided | **[F]** Level two: 213 records (151 admit, 44 exclude, 18 defer). Level three: 18 admit. The candidate keys equal the review keys at both levels. | Python set comparison. |
| Increment measurement matches the tree | **[F]** Passed, exit 0. | `tools/measure_lexicon_increment.py evals/review/level_2_agency_04 --check .../measurement.json` |
| Closure, levels one to three | **[F]** 849, 2,630 and 2,699 defined, all closure 100.0%. Each exited 0. | `tools/validate_closure.py` at each level |
| No prior decision changed | **[F]** No key of this batch appears in any prior `review.json`. | Python set comparison. |

### A.2 Admitted definitions

I read all 169 admitted definitions. The following need change or comment. The rest are correct at level, grounded, and make no claim beyond the source. **[H]** That judgement is mine and not independently reviewed.

**Proposed replacements.** I checked each against the level ceiling with `epagoge.vocabulary.unlicensed`, which is the check `keep_sentences` applies. **[F]** Every proposal returns no unlicensed word. **[F]** I did not run `tools/author_definitions.py`, because it writes to tracked files. The full closure check for each proposal is therefore unverified.

- **advanced** (L2). Currently "more developed, newer or harder than others of its kind." "Harder" is not part of the meaning. Proposed: "Advanced means more developed or more modern than others of its kind." **[F]** Ceiling clear.
- **crust** (L2). Two senses in one definition, which the README flags. Proposed: "A crust is the hard outer layer of something, such as the rocky outer layer of the earth." **[F]** Ceiling clear.
- **fan** (L2). Two senses, a machine and a folded paper. Proposed: "A fan is a thing that moves air, such as a machine with turning blades." **[F]** Ceiling clear.
- **film** (L2). Two senses, a layer and a camera film. Proposed: "A film is a thin layer or sheet of something." **[F]** Ceiling clear.
- **screen** (L2). The wire-mesh sense is a second sense. Proposed: "A screen is a flat surface where pictures are shown, such as the front of a computer or a phone." **[F]** Ceiling clear.
- **astrology** (L2). "It is not a science, because its claims do not rest on evidence." This is an evaluation stated as the dictionary's own claim. Proposed: "Astrology is the idea that the places of the sun, the moon and the planets in the sky can tell about the lives of people. Most scientists do not accept it, because its claims have not been shown by evidence." **[F]** Ceiling clear. **[H]** This is the one change I would most want to see.
- **ion** (L3). "An atom or a particle that has an electric charge" is loose. Proposed: "An ion is an atom or group of atoms that has an electric charge." **[F]** Ceiling clear.
- **laser** (L3). "One color" is not strictly true of every laser. Proposed: "A laser is a machine that makes a narrow, very bright beam of light that is almost one color." **[F]** Ceiling clear.

The remainder are sound as written.

### A.3 Deferrals and exclusions

**Deferrals (18).** **[I]** Each reason is sound, with the following notes.
- **Interface words (8):** articles, bookmarks, brochure, dimension, informative, postcards, poster, printable. The reason is the batch's evidence rule. **[H]** The same weakness I raised for `date` in the third batch applies. "Articles" and "poster" are common words, and a site's catalogue is a confounded source. The rule is applied consistently.
- **Clipped or combining forms (4):** hex, litho, mini, topo. Sound.
- **Specialised senses (3):** coma, mantle, tissue. Sound as a conservative choice.
- **Trade names (2):** popsicle, styrofoam. Sound. The filing policy for trade names is a separate decision.
- **Farthest.** **[I]** The reason, that adding `farthest` would change the `far` entry decided before this batch, is sound under the brief's rule that prior decisions stay decided.

**Exclusions (44).** **[F]** Every exclusion carries an inflected-form reason pointing to a citation form in the batch or at level three. **[I]** These are sound under the batch rule.

### A.4 Changes outside the batch

- **`src/epagoge/inflection.py`.** `drive` becomes `drove`, `driven`, `driving`. `hypothesis` takes plural `hypotheses`. **[F]** Both are correct. **[I]** Necessary, since the rule gave `drived` and `hypothesises`.
- **`NO_DOUBLE_MULTISYLLABIC`.** Adds `flatten`, `focus`, `gather` and `transit`. **[I]** Each has an unstressed final syllable, so the no-doubling entry is correct. **[F]** The rule already gave the right forms, per the README. The entries therefore record facts, and they add no behaviour change.
- **Test.** One line adds `level_2_agency_04` to the measurement test. **[F]** Correct.
- **Measurement files.** **[F]** Thirteen tracked `measurement.json` files changed. Each changed only `after/2`, `remaining_gap`, and `closure/2` (`defined`, `required`, `validator_output`). **[I]** Those are the expected fields. The README says thirteen, and that matches.

### A.5 Prior decisions

**[F]** No change. No overlap of keys with prior review files.

## Part B. Luna's readiness report

### B.1 Rerun

**[F]** `python -I tmp/dromon-trial-4/readiness.py "$PWD"` printed 26 units, exit 0. The worker's counts were stale by the time I ran it. **[F]** The report's own note allowed for this.

**[F]** Three units recounted by hand with `grep` on the level-two seed:

| Concept | Report | Rerun | Text match |
|---|---|---|---|
| `spatial_position` (L2) | 108 | 119 | 119 |
| `plant` (L2) | 53 | 55 | 55 |
| `stock_and_flow` (L2) | 7 | 7 | 7 |

**[F]** `vocabulary.json` agrees for `r2.measure` (216). For `p2.force` it differs by one, in `household_object` (68 in the seed, 69 in the vocabulary).

### B.2 Rankings

**[F]** The rerun sums of level-two counts for the five units ranked are: `r2.measure` 216, `p2.force` 281, `p2.matter` 318 with one zero, `b2.keeping_going` 84, `ac2.flow` 18.

**[F]** Units with no zero count and a higher sum than `ac2.flow` include `m2.howmuch` (100), `r2.record` (90), `b2.mending` (63) and `m2.number` (55).

**[F]** `p2.matter` has one zero concept, `presence`, and ranks above units with none.

**[I]** The ranking does not follow from the stated rule of "favoring high counts and few zero-count concepts." The order is not reproducible from the rule. A rule that fits the order is not obvious.

### B.3 What the report claims

**[F]** The report labels its per-unit sums as facts. They are stale.

**[F]** The thin-concept list is also stale. In the rerun, `not_always_known`, `counting` and `taking_on_faith` are no longer zero, and `opinion` is zero but absent from the list.

**[I]** The report claims more than a headword count shows in two places: "comparatively well provisioned," and "best placed to draft first." Both are framed as judgement. The closing caveat says counts do not establish usable examples or feasibility. **[H]** The caveat is correct, and the headings should carry it too.

**[F]** Each record in the level-two seed has exactly one concept, so a record count is a headword count for that concept. That part of the method is sound.

## Summary

- Part A: the batch is sound. Seven definitions merit the wording above, and `astrology` matters most.
- Part B: the counts are right in method, stale in value. The ranking does not follow from its stated rule. The thin-concept list needs refreshing.

**Limits.** No gate run. Wordings checked for ceiling only. No teacher loaded.
