# Grounding level one

**Decided 2026-09-24.** Level-one records ground in a hand-authored
primitive register rather than in citations.

## The problem, which was raised in discussion and not recorded until now

**Level one breaks the grounding rule.** Every record must carry a
resolvable `source_claim`, and the empirical class requires one. But level
one seeds civilisational axioms.

What is the source for "living things die"? For "things break"? For "the
dropping came first and made the falling happen"?

These are not empirical claims with citations, not formal derivations, not
attributed positions, not conditional results, and not normative claims.
They are **primitives that everything else presupposes**, which is exactly
how `../spec/CURRICULUM_LEVELS.md` defines the level.

Left unresolved, a generator has three options and two are bad. Fail
validation, fabricate citations, or find an honest home for axioms. The
second is the Galactica failure arriving in the very first records written.

**So level one is the hardest case for the verification layer, not the
easiest.** That is an argument for building it early, where the problem is
cheapest to fix.

## Rejected approaches

**Require citations anyway.** Produces strained or fabricated sources. This
is the failure mode the project exists to prevent, and it would appear at
the foundation where everything downstream presupposes it.

**Exempt level one from grounding.** Simplest, and it creates an unaudited
stratum precisely where an unsupported assertion does the most damage.

**A new claim class with no verifier.** A `primitive` class that nothing
checks is a dumping ground. "Things break" and "hard work leads to success"
would enter by the same door, and the second is a contested normative claim
wearing a primitive's clothes.

## The decision

**A primitive register.** A small, hand-authored, reviewed set of
civilisational axioms, held in version control and audited as a unit.

**Level-one records cite a register entry as their `source_claim`**, using
the `primitive:` prefix. The grounding rule is therefore unchanged. Only the
kind of source is new, and it resolves like any other.

### Admission criteria for the register

An entry must be all of the following.

1. **Directly observable** without instrumentation or inference.
2. **Uncontested.** If reasonable people disagree, it is an attributed
   position or a normative claim, not a primitive.
3. **Not derivable** from other registered primitives. The register is a
   basis, not a catalogue.
4. **Accompanied by the observation that grounds it**, in the entry itself.

### The generator may write about primitives. It may not add to the register

This is the load-bearing rule.

The register is small, on the order of dozens to low hundreds of entries.
It is where an unsupported assertion does the most damage, because
everything above it inherits the error. **It is hand-authored and reviewed,
and a machine may not extend it.**

The generator produces records that *teach* registered primitives, and each
such record resolves to an entry. A record citing an unregistered primitive
is rejected.

## Why this is better than the alternatives

It **preserves the grounding rule unchanged**, so there is no exemption to
police. It **puts human review exactly where it matters most**, at the
foundation rather than spread thinly across millions of generated records.
And it **keeps the audit trail intact**, because a level-one claim traces to
a reviewed entry rather than to nothing.

## Reversible

This is a design decision taken without the operator present. If a
different resolution is preferred, the register is a small artifact and the
validation is one rule.
