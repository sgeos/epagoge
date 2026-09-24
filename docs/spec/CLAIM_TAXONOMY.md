# Claim taxonomy

**Specified 2026-09-23.** Every corpus record is classified into exactly
one class, which determines how it is verified and what it may assert.

This is an **operational taxonomy for verification**, not a metaphysics. It
says how the pipeline checks a claim. It does not assert what kinds of
truth exist.

## The classes

| Class | Verified by | Rejected when |
| --- | --- | --- |
| Formal | Derivation, proof, or definition | The derivation does not check |
| Empirical | Measurement, with falsifiable consequences | The claim exceeds the evidence, or the source does not resolve |
| Attributed position | Attribution to a named holder | Presented as settled rather than as a position |
| Conditional result | Stated assumptions plus validation status | Assumptions or validation status are absent |
| Normative | Attribution to a holder, or excluded | Presented as a finding |
| Unsupported | Nothing. Always rejected | Always |

## Why a binary would not serve

An earlier framing proposed that whatever is measurable and falsifiable is
science and everything else is faith. The operator withdrew it on
2026-09-23 as too low-fidelity to be useful. The record of why is kept
because the reasoning constrains the taxonomy.

**The residual category is not one thing.** Mathematics is not falsifiable
by measurement and is established by proof. Definitions and analytic truths
are neither empirical nor faith. Normative claims are a separate category
again, over which moral realism and anti-realism are both live positions.

**A purely empirical criterion cannot satisfy itself.** The claim that
falsifiability is the correct demarcation criterion is not falsifiable by
measurement. Any binary of that shape classifies its own rule into the
residual category.

The taxonomy above avoids this by being about verification method rather
than about the nature of truth. It makes no claim to exhaust reality.

## Conditional results. The class simulation forced

A computed or simulated result is not a measurement. It is a derivation
from assumptions, whose bearing on the world depends on validation.

The standard distinction in the field is the one this class encodes.
**Verification** asks whether the equations were solved correctly, which is
formal. **Validation** asks whether the correct equations were solved,
which is empirical.

**Required fields.** A conditional-result record carries its assumptions,
its model or method, and its validation status including the case where
validation is absent.

**Why this is mandatory.** A phrase of the form "the model shows" is among
the most reliable sources of claims that sound empirical and are not.
Without the assumptions and the validation status attached, such a record
would teach the model to assert computed conclusions with empirical
confidence, which is the failure this project exists to prevent.

## Worked example. Falsificationism itself

Applied to the demarcation criterion, to show the rule has teeth on the
question where it is least comfortable.

The claim that a proposition is scientific if and only if it is falsifiable
is **an attributed position**, associated principally with Popper. It is
not an empirical claim, since no measurement refutes it, and it is not
formal, since it follows from no derivation.

It is also contested on substantive grounds recorded here so the corpus
represents the field accurately rather than one position within it.

- **Duhem and Quine.** A hypothesis is never tested alone but conjoined
  with auxiliary assumptions, so a failed prediction shows that something
  in the bundle is wrong without identifying what.
- **Lakatos.** Research programmes protect a hard core with auxiliary
  hypotheses, and doing so is frequently rational rather than dogmatic.
- **Kuhn.** Normal science solves puzzles rather than attempting
  falsification, and anomalies accumulate until crisis.
- **Bayesian epistemology.** Evidence shifts credence rather than
  decisively refuting, which describes much of working statistical
  practice.

Sciences that resist clean falsification, including much of geology,
cosmology, and evolutionary biology, are historical and observational.
Whether string theory is science is the live contemporary instance of the
same dispute.

**Corpus treatment.** Falsificationism is recorded as Popper's position,
with the competing positions attributed to their holders. No record asserts
any of them as the settled answer.

**Why this example is retained in the specification.** It is the operator's
own stated position, applied to the rule rather than exempted from it. A
classification rule that cannot survive contact with its author's
commitments will not survive contact with anything.

## Relationship to the other record types

The taxonomy classifies what a record claims. The curriculum fields in
`../../curriculum/README.md` describe where a record sits in the
progression. A record has both, and they are independent.
