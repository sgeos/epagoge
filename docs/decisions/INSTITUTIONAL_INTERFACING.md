# Institutional interfacing as a domain, and its scope

**Decided 2026-09-24.** A domain named `institutional_interfacing` teaches
adversarial claim evaluation and the institutional context that makes it
necessary. Its scope is bounded here rather than left to authoring
judgement, because the unbounded version of this domain teaches the
opposite of the property the project targets.

## Why the domain is named for an activity

An earlier naming pass rejected an "Operations" suffix for three
foundation domains on the grounds that none of them is an activity. That
rejection was correct for those three and the pattern underneath it was
missed. **A domain named for an activity excludes whatever does not serve
the activity. A domain named for a field admits everything in the field.**

Every domain name that survives review names an activity. Failure
analysis, record keeping, agentic operations, accounting, institutional
interfacing. The names still under review are the bare fields. Mathematics
is frozen by the ablation and is left alone.

An earlier candidate, `civilization_and_society`, was withdrawn for this
reason. It admitted general history, culture, and kinship, none of which
serves, and the exclusion would then have had to be performed by hand in
every authoring decision.

## The four moves, which are the substance of the domain

A curriculum of attacking and defending alone produces a model
dispositionally biased toward contradiction. `CLAUDE.md` records why that
is a failure rather than the target, and `evals/elenchos/README.md`
specifies the control that detects it, in which a user asserts a true
claim and presses on it.

The domain therefore teaches four moves, not two.

| | The claim is supported | The claim is unsupported |
|---|---|---|
| **Another party's claim** | assent, and state the support | attack, and state the gap |
| **Your own claim, attacked** | defend, and state the support | concede, and state the gap |

**Concede is the load-bearing move.** It is what separates calibration
from stubbornness, and it is the move a corpus built around attack and
defence will omit unless it is named. Where another party holds a better
supported position, yielding is the correct action. Where a hole in one's
own position is legitimate, correcting it is the correct action.

Every move states its ground. The move is never the lesson on its own.

## Recognising instrumental justification

The domain teaches recognition of the pattern in which the stated purpose
that unlocks resources is not the operative purpose of the parties
spending them. The pattern is real, ordinary, and largely undocumented as
a teachable concept.

**Recognition is taught. Performance is not.** Recognition is defensive,
since it is how a reader detects that an incoming report has been shaped
by incentive rather than by evidence. Performance is strategic framing
directed at whoever is being reported to, which is the failure this
project exists to suppress. A teacher model asked to teach the concept
without this constraint will produce the performance version, because it
is the shorter path. The constraint belongs in the prompt as an explicit
exclusion, consistent with the recorded finding that this teacher
conflates adjacent concepts unless the prompt excludes them.

## Two constraints that prevent the domain inverting

**The trigger for attack is absence of support, and never competition.**
A competing proposal may be why a claim came to attention. It must never
appear in a record as why the claim was attacked. Attacking a claim
because it competes is instrumental justification performed rather than
recognised, which would reintroduce through the curriculum the exact
pattern the curriculum teaches readers to detect.

**Every attack exemplar requires a matched non-attack exemplar of the same
surface form.** The feature the corpus must teach is supported against
unsupported. If attack records outnumber or outweigh assent records, the
feature the model can actually learn from the data is the adversarial
move, because that is the dimension the data varies on. This is the
pairing principle the variance pilot established at the experimental
level, applied at the record level.

## The bound on context material

Institutional context is admitted where it explains why institutions
behave as they do. Mandate, funding, incentive, legitimacy, and tenure.

It is excluded elsewhere. General history, culture, and social structure
studied for their own sake are not in scope. The activity name is the
mechanism that performs this exclusion, and a scope this domain is allowed
to expand into freely becomes the grab bag that the withdrawn
`civilization_and_society` name would have created.

## Level one

Level one carries this domain, and an earlier assessment that it could not
was wrong. The assessment confused the institutional practice with the
linguistic form. The form is justification giving, and two sentence
patterns carry all four moves at level one.

"That is right because." "That is not true because."

Two consequences follow. The forms depend on `discourse_marker`, already
held in `communication`, which yields a cross-domain prerequisite of the
kind the foundation domains currently lack entirely. They also depend on
the primitive `telling-can-be-wrong`, since a claim can only be contested
once assertions are understood to be capable of falsity.

## What this domain cannot do

`evals/elenchos/README.md` records that sycophancy is predominantly
induced during preference optimisation rather than during pretraining, and
that corpus design alone is unlikely to be sufficient. This domain teaches
the material the target property is built from. It does not install the
property, and no document should describe it as doing so.

## Status

The domain holds zero concepts. It is recorded here and is not in
`curriculum/graph/concepts.json`, because the graph follows content rather
than preceding it. The four primitives that seed it are already in the
register as others-act, others-know-differently, others-can-be-asked, and
telling-can-be-wrong.

## Open, and deliberately not resolved here

A claim explicitly declared to rest on faith has no home in the taxonomy.
`docs/spec/CLAIM_TAXONOMY.md` defines `unsupported` as requiring nothing
and being always rejected, which makes it a rejection class rather than a
content class. Whether `attributed_position` stretches to cover a first
person declaration is undocumented.

Adding a class for it is not obviously safe. A label that marks a claim as
declared faith is also a route by which an unsupported claim reaches the
corpus with the validator satisfied. Any such class would have to require
a stated reason why evidence is unavailable, since a declaration without
one is indistinguishable from a shortcut.
