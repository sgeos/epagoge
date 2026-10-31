# Open decisions

Consolidated 2026-10-31 for the holding state. Each entry names a concern
that awaits the operator, where it is recorded, what waits on it, and the
obvious choices. **This list decides nothing.** The choices are the ones
the records name or the ones that follow directly from them, and they are
not exhaustive. Where a record states a default that holds until the
operator decides, the entry says so. Entries marked inferred are open by
this session's reading of a record that was never closed, not by any
statement that they are open.

Line numbers are omitted because they move. Search the named file for the
word in the entry's title.

## A. The experiment protocol

Confirmatory runs are refused until these are settled and the resulting
protocol is implemented and validated. All are recorded in
`evals/PRE_REGISTRATION.md`.

1. **Endpoint step count.** Item 10. The step at which held-out loss is
   read now sets precision rather than the sign of the result, and the seed
   count waits on it.
   - **A.** 800 steps, with the smaller paired standard deviation of
     0.0074 measured on the level-one corpus.
   - **B.** 1,600 steps, at 0.0103.
   - **C.** Defer until a larger corpus exists and measure again.
2. **Kernel estimator.** Item 10. The estimator, the probe set, its size
   and the Hutch++ sample count must be fixed before any run.
   - **A.** Adopt the participation ratio by Hutch++ as the record
     describes, and fix the probe set and sample count now.
   - **B.** Defer until the size floor of entry 4 is known.
3. **Correction procedure for secondary measures.** Item 9. Marked
   pending, with a recorded default that every secondary measure is
   descriptive and carries no significance claim.
   - **A.** Confirm the default.
   - **B.** Name a formal correction procedure after the endpoint is fixed.
4. **Corpus acceptance.** Item 11. Both the residual error ceiling and the
   size floor are pending. The ceiling is recorded as waiting on the first
   audit.
   - **A.** Fix a size floor now and leave the ceiling until an audit.
   - **B.** Leave both until the first audited corpus exists.
5. **Effective-rank floor.** Item 12. The procedure is fixed and the number
   waits on the first measurements, so no choice is due yet.
6. **Budget confirmation.** Inferred, from question 5 of
   `docs/decisions/OPEN_QUESTIONS.md`, which says the budget is worth
   confirming before the pre-registration is committed.
   - **A.** Re-derive the cost against current rental prices before the
     protocol is committed.
   - **B.** Accept the recorded estimate.
7. **Whether confirmatory training proceeds at all.** It stays blocked by
   the items above, and nothing in the holding state changes that.

## B. What the next scope is

8. **The next task.** The holding state has no open scope. Corpus
   generation needs the teacher, and the lexicon needs none.
   - **A.** A further lexicon batch, from the 154 undecided stripped-form
     candidates of entry 13 or from a pool drawn at a threshold of three
     over the sources already on disk, which this session measured at
     about 1,500 strings and did not record in any tracked file.
   - **B.** Complete the experiment protocol of section A.
   - **C.** Resume corpus generation for the level-two units without a
     book, which needs the teacher loaded and the generator draft of
     entry 9 decided.
   - **D.** Fetch further candidates from `docs/decisions/AGENCY_SOURCES.md`.
9. **The generator draft.** The revised draft of the second trial
   follow-up is in the ignored `tmp/dromon-trial-3/` and is unapplied, as
   the operator chose. Its record limit rests on a prompt rule whose effect
   on a teacher is unverified.
   - **A.** Apply it and test it under a teacher run.
   - **B.** Keep it unapplied until generation resumes.
   - **C.** Discard it.

## C. The lexicon

10. **Function words.** Recorded in the handoff under the operator
    decisions of 2026-10-07. Whether the and, of and the other function
    words also need a definition, which needs a rule for classifying a
    record with no concept.
    - **A.** Define them under a new record class.
    - **B.** Leave them undefined, as now.
11. **Archaic, religious and sense-ambiguous deferrals.** Each has a
    reason in its review record, among them thee, thy, thine and unto in
    `evals/review/level_2_scan_10/`.
    - **A.** Keep them deferred.
    - **B.** Admit them at a higher level in their archaic sense.
    - **C.** Exclude them.
12. **Interface-text deferrals.** Page interface words deferred in the
    agency batches and the long-tail batch, recorded in the README of each
    batch under `evals/review/`.
    - **A.** Exclude them as interface text.
    - **B.** Decide each in the sense the page uses.
    - **C.** Keep them deferred.
13. **Stripped-form candidates.** The seventh trial's luna line listed 160
    strings that pass the pool rule only because the lookup strips a suffix
    to another headword. Six already carry a deferral, so 154 are
    undecided. Some reduce to unrelated words, such as rating to rat.
    Recorded in `docs/process/trials/dromon_trial_7/`. Flooding is named
    separately in `docs/process/trials/dromon_trial_6/` as a choice between
    a form of flood and the existing deferral.
    - **A.** Decide all 154 in a batch, as entry 8 A.
    - **B.** Decide only those that reduce to an unrelated headword.
    - **C.** Leave them, accepting that their senses are undecided.
14. **Tornadoes.** The term entry for tornado lists tornados and not
    tornadoes. An earlier batch admitted the word, and the seventh trial
    left it open.
    - **A.** Add tornadoes as a form.
    - **B.** Replace tornados with tornadoes.
    - **C.** Leave it.
15. **Intensive.** Inferred. The first Dromon trial gave the general and
    energy-use senses and not the physical-property sense its reviewer
    named. Recorded in `docs/process/HANDOFF_HISTORY.md`.
    - **A.** Add the physical-property sense at level three.
    - **B.** Leave the two senses.
16. **Unused headwords.** Boss, forbidden, hook and insect have no book
    reaching for them, recorded in `docs/decisions/UNUSED_FORMS.md` as
    draft or drop. Whether this is still true was not checked.
    - **A.** Draft material that uses them.
    - **B.** Drop them.
    - **C.** Recheck usage first.
17. **Lie, choose, fair and real.** Recorded in
    `docs/decisions/INFORMATION_ASYMMETRY.md` as a thread the operator
    described as still open. Four preschool words serve planned concepts.
    - **A.** Add the four words.
    - **B.** Wait until the concepts are written.
18. **Schedules for levels three to seven.** None exists, and
    `docs/decisions/INFORMATION_ASYMMETRY.md` records them as the
    operator's decision. No options are named.
19. **Thesaurus synonyms.** Recorded as open in
    `docs/decisions/LEXICON.md`, not explicitly as the operator's.
    - **A.** Decide the synonym rule.
    - **B.** Leave the thesaurus as it is.

## D. Records that contradict each other

20. **Training framework.** `docs/decisions/LANGUAGE_CHOICE.md`,
    `CLAUDE.md` and `AGENTS.md` say it is open and blocked on the hardware
    path. Question 10 of `docs/decisions/OPEN_QUESTIONS.md` says it was
    answered on 2026-09-23 for PyTorch, because the hardware path was
    settled as local work plus rented NVIDIA hardware.
    - **A.** Record PyTorch as decided and amend the documents that say
      open.
    - **B.** Reopen question 10 and keep the framework open.
21. **Documentation spelling.** The curriculum uses US English and
    documentation prose is British.
    - **A.** Convert documentation prose to US English.
    - **B.** Keep the split and record it as deliberate.

## E. Licensing and sources

22. **Terminal-stage derived records.** Question 25 of
    `docs/decisions/OPEN_QUESTIONS.md` and `docs/decisions/LICENSING.md`.
    Whether records restating third-party literature carry a licensing
    status other than CC0. Terminal-stage records wait on it.
    - **A.** Add a licensing status field to the record schema.
    - **B.** Dedicate all records under CC0.
23. **Source acquisition.** `docs/decisions/SOURCE_ACQUISITION.md`
    records the drafted manifest scheme as deliberately not adopted, and
    `LICENSING.md` calls third-party licensing unexamined. The first
    acquisition triggers it.
    - **A.** Adopt the drafted scheme before the first acquisition.
    - **B.** Leave it until an acquisition is due.
24. **Non-United-States agency pages.** `docs/decisions/AGENCY_SOURCES.md`
    records one candidate under the Open Government Licence as awaiting the
    operator's licensing judgement, and one under Crown copyright as
    unverified.
    - **A.** Accept attribution-licensed text as a word-list source.
    - **B.** Exclude both.
25. **Wikipedia for module coverage.** `docs/decisions/REFERENCE_SOURCES.md`
    records using it to decide what a module covers as the operator's open
    judgement.
    - **A.** Allow it for coverage only.
    - **B.** Forbid it.

## F. Process and tooling

26. **The local Dromon project file.** It still carries the seventh
    trial's settings, with the reviewer line on the Fable model and raised
    cost limits. The backup is the ignored `tmp/dromon.toml.before-trial-7`.
    - **A.** Keep the Fable reviewer for large batches.
    - **B.** Restore the Haiku reviewer and the earlier limits by
      `dromon rebind`.
27. **Level-three measurement.** No level-three batch records an increment
    measurement, so level-three counts have no check. Noted by the
    reviewers of the sixth and seventh trials.
    - **A.** Extend the measurement to level-three batches.
    - **B.** Accept the gap and record it.
28. **Harness requests.** The trial lines asked for a cross-batch decision
    lookup, a saved base for the by-key diff, process visibility, an
    in-place edit tool for read-only lines and visible truncation. These
    belong to the harness, not to this repository.
    - **A.** Forward them to the harness project.
    - **B.** Build the decision lookup here as a tool.
    - **C.** Leave them as recorded.
29. **A clone without `secret/`.** `AGENTS.md` records that a clone cannot
    discharge the code-name obligation of `CLAUDE.md`.
    - **A.** Supply the private directory to such environments.
    - **B.** Leave tracked prose to agents that have it.
    - **C.** Accept the exposure knowingly.
30. **Commit authorization.** Every commit needs a fresh instruction, as
    the operator decisions of 2026-10-07 in the handoff record.
    - **A.** Keep it per request.
    - **B.** Grant a standing authorization for scoped work that passes
      the gate.

## Possibly stale

These are recorded as the operator's and may have been overtaken. Check
before deciding. The concepts that would unblock level-one units, whether
level one can reach level two, a concept-complexity target, whether a
definition needs its own claim class, whether the null arm is enough,
whether multi-head latent attention is admissible, and the measure of
unrequested action are in the superseded handoffs of
`docs/process/HANDOFF_HISTORY.md`. The licensing of the New General Service
List and Dale-Chall in `docs/decisions/READING_LEVEL_RESEARCH.md` is likely
moot, since briefs forbid consulting them. Whether the eleven-hour training
run was worth its gain is recorded as the operator's call in
`evals/pilot/LEVEL_ONE_INTERACTION.md`. The ternary pilot is deferred to the
follow-on in `docs/decisions/OPEN_QUESTIONS.md`. The domain proportions in
the same file no longer gate generation.
