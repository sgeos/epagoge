# Brief

Completed at `7011d61131dab25b84f0ae6b70cda0f41c66ea86` and published.
Retained with `COMPLETION_CONDITION.md` as evidence of the completed scope.
Use `HANDOFF.md` for current task status. This brief does not initiate new work.

## Present goals

Complete the level-two lexicon before drafting its content. The verified
baseline has 964 headwords through level two and a gap of 9,036 to the
approximate target. Later goals include schedules, expanded evaluation and
the experimental protocol. Confirmatory training remains blocked. Licensing,
experimental and later-schedule decisions remain with the operator.

## Recommended work

Review tongue, taste, sugar and sweet with explicit senses and parts of
speech. Tongue is the movable mouth organ and belongs to body_part. Taste is
the sensory quality of food or drink and belongs to physical_property. Sugar
is ordinary table sugar and belongs to material. Sweet is the taste adjective
and belongs to physical_property. These are proposed assignments to review,
not permission to admit the words. Tongue supports a grounded taste account.
Sugar and sweet require special scrutiny for circularity and distinguishing
content. Food colour or general pleasantness alone is insufficient.

Add optional per-candidate sense specifications to the existing generator.
A specification records a bounded nonblank sense description and recognized
parts of speech for exactly the candidate set. Invalid structure, duplicate
keys, missing or extra candidates, unknown fields, blank senses and invalid
parts of speech fail before teacher access. With no specification, existing
behavior remains unchanged. The teacher receives the intended senses as
instructions, and the report retains the exact specifications and file hash.
Per-candidate parts of speech reach the mechanical proposal. Sense notes do
not license words or establish correctness.

Retain a bounded teacher run and an entry-by-entry review in
evals/review/level_2_taste_senses. Admit only suitable sourced definitions
that retain complete grounded coverage. Review actual forms, including
comparatives if sweet is admitted and the mass qualifier for table sugar.
Retain all mechanical outcomes, semantic decisions and agent edits. A
candidate may be deferred rather than admitted through a weak definition.
Measure final counts and the remaining gap, and preserve earlier records,
level-one books and the reference checkpoint. Use the existing context limit
of 4096 tokens and check host memory before sequential generation.

## Rationale and prior failures

The fruit batch repeatedly requested taste and sweet. Concept labels alone
do not identify a word sense. Existing skin and stone definitions showed that
surface licensing can pass while the intended meaning is unsupported.
Explicit specifications make the intended meaning auditable but their effect
on acceptance is unmeasured. Do not claim a throughput improvement from this
batch or treat a compliant prompt as proof that the reply followed it.

Do not define sugar through sweet and sweet through sugar without independent
grounding. Do not accept a list of examples as a sufficient definition. Do not
confuse taste with texture, temperature, preference or every sensation in the
mouth. Do not declare a figurative sense merely because it is common.

Do not expand the seed, enlarge the teacher context, weaken validators or
manufacture forms to force admissions. Do not alter prior evidence to make
historical counts current. Separate mechanical acceptance, semantic review
and final admission counts. Agent review has no independent expert audit.

## Verification and publication

Regression tests exercise specification boundaries without a live teacher.
The full gate must pass. Update the handoff with measured results and limits.
The operator authorizes committing and pushing all non-ignored work. Preserve
ignored artifacts and verify the published revision and clean working tree.
Ordering is not a completion criterion.

## Delivered outcome

The generator now supports optional validated sense specifications and retains
them in prompts and reports. The four-word batch mechanically accepted one
reply. Agent review admitted tongue and taste after revisions, and deferred
sugar and sweet because of circularity and inadequate distinguishing content.
Level two now has 966 headwords and a remaining gap of 9,034. Both dictionaries
retain complete grounded coverage. The new review retains every outcome.
