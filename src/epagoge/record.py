"""Corpus record schema and corpus-level validation.

Specification in ``docs/spec/RECORD_SCHEMA.md``. Standard library only.

A record is the unit the generation pipeline emits and the trainer consumes.
Its fields were previously described across three prose documents; this
module is the single authoritative definition, and the validator is what
makes the description enforceable.
"""

from __future__ import annotations

import json
from collections.abc import Collection, Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Final, cast

from epagoge.book import Definition, definition_from_json
from epagoge.concept_graph import ConceptGraph, Violation

PRIMITIVE_PREFIX: Final[str] = "primitive:"
"""Marks a source claim that resolves in the primitive register.

Level one seeds civilisational axioms, which have no citation in the
ordinary sense. They ground in a hand-authored register instead. The
grounding rule is unchanged; only the kind of source is new. See
docs/decisions/PRIMITIVE_REGISTER.md.
"""

MIN_LEVEL: Final[int] = 1
MAX_LEVEL: Final[int] = 7
TERMINAL_LEVEL: Final[int] = MAX_LEVEL


class ClaimClass(Enum):
    """How a record's claim is verified. See docs/spec/CLAIM_TAXONOMY.md."""

    FORMAL = "formal"
    EMPIRICAL = "empirical"
    ATTRIBUTED_POSITION = "attributed_position"
    CONDITIONAL_RESULT = "conditional_result"
    NORMATIVE = "normative"
    DECLARED_FAITH = "declared_faith"
    """Held where checking is not available, and said so.

    **Distinct from unsupported, which is always rejected.** A declared
    faith claim is admitted on two conditions, and the second is what stops
    it laundering a claim that merely lacks support. It states why evidence
    is unavailable, and anything derived from it carries it as an
    assumption. See docs/decisions/FAITH_CLASS.md.
    """

    UNSUPPORTED = "unsupported"


class SimplificationKind(Enum):
    """What was done to a source claim to make it teachable at a level."""

    NONE = "none"
    OMISSION = "omission"
    IDEALISATION = "idealisation"
    SUPERSEDED_MODEL = "superseded_model"
    ANALOGY = "analogy"
    VOCABULARY_LIMITED = "vocabulary_limited"
    """Accurate as far as the available words allow, and no further.

    Distinct from a superseded model, which is wrong. This record is not
    wrong; it is imprecise because the words for precision are not yet
    admitted. Saying that things divide until they cannot be divided further
    is vocabulary-limited. Saying that atoms are tiny balls is a superseded
    model. Both are corrected later, for different reasons.
    """


@dataclass(frozen=True, slots=True)
class Provenance:
    """Where a claim comes from and what it is contingent on.

    Which fields are required depends on the claim class, which is the
    reason they are optional here and enforced by the validator rather than
    by the type. A single record type with class-conditional requirements
    keeps the on-disk format uniform.
    """

    source_claim: str | None = None
    position_holder: str | None = None
    contested_by: tuple[str, ...] = ()
    assumptions: tuple[str, ...] = ()
    method: str | None = None
    validation_status: str | None = None
    why_unavailable: str | None = None
    """Why checking is not available. Required of a declared faith claim.

    A declaration without one is indistinguishable from laziness, which is
    the failure that kept this class out of the taxonomy until a worked
    example arrived.
    """


@dataclass(frozen=True, slots=True)
class Simplification:
    """A declared fidelity relation to the source claim.

    Good pedagogy uses models that are wrong at a higher level. Such a
    record states the kind of departure, the levels over which it holds, and
    the record that corrects it.
    """

    kind: SimplificationKind = SimplificationKind.NONE
    validity_scope: tuple[int, int] | None = None
    superseded_by: str | None = None


@dataclass(frozen=True, slots=True)
class Record:
    """One corpus record."""

    id: str
    level: int
    concepts: tuple[str, ...]
    claim_class: ClaimClass
    content: str
    provenance: Provenance = field(default_factory=Provenance)
    simplification: Simplification = field(default_factory=Simplification)
    defines: Definition | None = None
    """What this record says the meaning of, if anything.

    Carried here rather than on the book, because a book is an ordering of
    records and a definition belongs to the sentence that makes it.
    """


_REQUIRED_BY_CLASS: Final[Mapping[ClaimClass, tuple[str, ...]]] = {
    ClaimClass.FORMAL: ("source_claim",),
    ClaimClass.EMPIRICAL: ("source_claim",),
    ClaimClass.ATTRIBUTED_POSITION: ("position_holder",),
    ClaimClass.CONDITIONAL_RESULT: ("assumptions", "method", "validation_status"),
    ClaimClass.NORMATIVE: ("position_holder",),
    ClaimClass.DECLARED_FAITH: ("why_unavailable",),
}


def _missing(provenance: Provenance, name: str) -> bool:
    value = getattr(provenance, name)
    if value is None:
        return True
    return isinstance(value, tuple) and not value


def validate_record(record: Record, graph: ConceptGraph) -> list[Violation]:
    """Check one record in isolation and against the concept graph."""
    out: list[Violation] = []
    where = f"record {record.id!r}"

    if not MIN_LEVEL <= record.level <= MAX_LEVEL:
        out.append(
            Violation("level-range", f"{where}: level {record.level} out of range")
        )

    if not record.concepts:
        out.append(Violation("no-concepts", f"{where}: covers no concept"))
    for concept in record.concepts:
        if concept not in graph.nodes:
            out.append(
                Violation("unknown-concept", f"{where}: unknown concept {concept!r}")
            )

    if not record.content.strip():
        out.append(Violation("empty-content", f"{where}: content is empty"))

    if record.claim_class is ClaimClass.UNSUPPORTED:
        out.append(
            Violation("unsupported", f"{where}: unsupported claims are rejected")
        )
    else:
        for name in _REQUIRED_BY_CLASS.get(record.claim_class, ()):
            if _missing(record.provenance, name):
                out.append(
                    Violation(
                        "missing-provenance",
                        f"{where}: class {record.claim_class.value} requires {name}",
                    )
                )

    out.extend(_validate_simplification(record))
    return out


def _validate_simplification(record: Record) -> list[Violation]:
    out: list[Violation] = []
    where = f"record {record.id!r}"
    simp = record.simplification

    if simp.kind is SimplificationKind.NONE:
        if simp.validity_scope is not None or simp.superseded_by is not None:
            out.append(
                Violation(
                    "spurious-simplification",
                    f"{where}: unsimplified record declares scope or supersession",
                )
            )
        return out

    if record.level == TERMINAL_LEVEL:
        out.append(
            Violation(
                "terminal-simplified",
                f"{where}: terminal-level records keep strict entailment",
            )
        )
    if simp.validity_scope is None:
        out.append(
            Violation("no-scope", f"{where}: simplified record declares no scope")
        )
    else:
        low, high = simp.validity_scope
        if not MIN_LEVEL <= low <= high <= MAX_LEVEL:
            out.append(
                Violation("bad-scope", f"{where}: scope {simp.validity_scope} invalid")
            )
        elif not low <= record.level <= high:
            out.append(
                Violation(
                    "scope-excludes-level", f"{where}: level outside its own scope"
                )
            )
    if simp.superseded_by is None:
        out.append(
            Violation(
                "no-supersession", f"{where}: simplified record names no correction"
            )
        )
    return out


def validate_corpus(
    records: Iterable[Record],
    graph: ConceptGraph,
    primitives: Collection[str] | None = None,
    scheduled_relations: Collection[tuple[str, str]] | None = None,
    scheduled_levels: Mapping[str, int] | None = None,
) -> list[Violation]:
    """Check a whole corpus. Returns every violation, never raising.

    Three checks exist only at corpus level and are the reason this function
    is separate from :func:`validate_record`. Supersession must resolve to a
    later record, every prerequisite of a covered concept must already have
    been taught, and every primitive cited must be registered.

    ``primitives`` is the register. Passing ``None`` skips that check, which
    is correct for a corpus that cites no primitives and wrong for one that
    does, so a corpus citing primitives without a register is reported.
    """
    collected = list(records)
    out: list[Violation] = []
    by_id: dict[str, Record] = {}

    for record in collected:
        if record.id in by_id:
            out.append(Violation("duplicate-id", f"record id {record.id!r} repeats"))
        by_id[record.id] = record
        out.extend(validate_record(record, graph))

    out.extend(_validate_supersession(collected, by_id))
    out.extend(_validate_primitives(collected, primitives))
    out.extend(_validate_relation_coverage(collected, graph, scheduled_relations))
    out.extend(_validate_prerequisite_coverage(collected, graph, scheduled_levels))
    out.extend(_validate_faith_inheritance(collected))
    return out


def _validate_relation_coverage(
    records: Sequence[Record],
    graph: ConceptGraph,
    scheduled: Collection[tuple[str, str]] | None = None,
) -> list[Violation]:
    """A specialisation asserted in the graph must be taught in the corpus.

    **The relation is content, not only structure.** A graph that says a
    teddy bear is a toy, with no record teaching it, asserts a link the model
    never sees. The corpus is what the model reads.

    A record covering both endpoints teaches the relation. Nothing further is
    required of it, because requiring a declaration would let a record claim
    to teach a relation it does not.

    ``scheduled`` is the set of pairs a curriculum schedule covers. A
    relation scheduled to be taught is not a defect in a corpus that has not
    reached it yet, which is the same distinction the vocabulary lower bound
    draws between what a schedule states and what records show so far.

    **The asymmetry is the part that must be taught.** A teddy bear is a toy
    and a toy is not necessarily a teddy bear, which is the same structure as
    a square being a rectangle while a rectangle need not be a square. That
    one-directional implication is a level-one primitive underpinning all
    later classification, and it is invisible in an edge that merely points.
    """
    covered: set[tuple[str, str]] = set(scheduled or ())
    for record in records:
        concepts = set(record.concepts)
        for specific in concepts:
            for general in graph.generalisations_of(specific):
                if general in concepts:
                    covered.add((specific, general))

    out: list[Violation] = []
    for specific in sorted(graph.nodes):
        for general in sorted(graph.generalisations_of(specific)):
            if general not in graph.nodes:
                continue
            if (specific, general) not in covered:
                out.append(
                    Violation(
                        "relation-untaught",
                        f"the graph says {specific!r} is a kind of {general!r}, "
                        "but no record teaches it",
                    )
                )
    return out


def _validate_faith_inheritance(records: Sequence[Record]) -> list[Violation]:
    """Anything derived from a declared faith claim carries it.

    **This is the rule the class exists for.** A premise held without
    evidence is sometimes necessary and sometimes correct. The failure is
    not holding it, it is letting the conclusions drawn from it stop
    carrying it, so that by the third step nothing is labelled as resting
    on something unchecked.

    So a record whose source is a declared faith claim must itself be a
    conditional result, and must name that source among its assumptions.
    """
    faith = {r.id for r in records if r.claim_class is ClaimClass.DECLARED_FAITH}
    out: list[Violation] = []
    for record in records:
        source = record.provenance.source_claim
        if source is None or source not in faith:
            continue
        where = f"record {record.id!r}"
        if record.claim_class is not ClaimClass.CONDITIONAL_RESULT:
            out.append(
                Violation(
                    "faith-not-inherited",
                    f"{where} rests on declared faith {source!r} and is class"
                    f" {record.claim_class.value}, not a conditional result",
                )
            )
        if source not in record.provenance.assumptions:
            out.append(
                Violation(
                    "faith-unstated",
                    f"{where} rests on declared faith {source!r} without"
                    " naming it among its assumptions",
                )
            )
    return out


def _validate_primitives(
    records: Sequence[Record], primitives: Collection[str] | None
) -> list[Violation]:
    """Every cited primitive must resolve in the register.

    The register is hand-authored and a generator may not extend it. A
    record citing an unregistered primitive is therefore asserting an axiom
    nobody reviewed, which is the failure this whole arrangement exists to
    prevent.
    """
    out: list[Violation] = []
    for record in records:
        source = record.provenance.source_claim
        if source is None or not source.startswith(PRIMITIVE_PREFIX):
            continue
        name = source[len(PRIMITIVE_PREFIX) :]
        if primitives is None:
            out.append(
                Violation(
                    "no-register",
                    f"record {record.id!r} cites primitive {name!r} "
                    "but no register was supplied",
                )
            )
        elif name not in primitives:
            out.append(
                Violation(
                    "unregistered-primitive",
                    f"record {record.id!r} cites unregistered primitive {name!r}",
                )
            )
    return out


def load_primitives(path: Path) -> dict[str, str]:
    """Read the primitive register: identifier to grounding observation."""
    parsed: object = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(parsed, dict):
        raise ValueError("primitive register must be a JSON object")
    body = cast(dict[object, object], parsed)
    entries = body.get("primitives")
    if not isinstance(entries, list):
        raise ValueError("register must hold a 'primitives' list")
    items = cast(list[object], entries)
    out: dict[str, str] = {}
    for index, entry in enumerate(items):
        where = f"primitives[{index}]"
        if not isinstance(entry, dict):
            raise ValueError(f"{where}: expected an object")
        fields = cast(dict[object, object], entry)
        name = _require_str(fields.get("id"), f"{where}.id")
        if name in out:
            raise ValueError(f"{where}: duplicate primitive {name!r}")
        out[name] = _require_str(fields.get("observation"), f"{where}.observation")
    return out


def _validate_supersession(
    records: Sequence[Record], by_id: Mapping[str, Record]
) -> list[Violation]:
    out: list[Violation] = []
    for record in records:
        target_id = record.simplification.superseded_by
        if target_id is None:
            continue
        target = by_id.get(target_id)
        if target is None:
            out.append(
                Violation(
                    "dangling-supersession",
                    f"record {record.id!r} superseded by unknown {target_id!r}",
                )
            )
        elif target.level <= record.level:
            out.append(
                Violation(
                    "supersession-order",
                    f"record {record.id!r} superseded by {target_id!r} at level "
                    f"{target.level}, not later than {record.level}",
                )
            )
    return out


def _validate_prerequisite_coverage(
    records: Sequence[Record],
    graph: ConceptGraph,
    scheduled: Mapping[str, int] | None = None,
) -> list[Violation]:
    """A concept may not be taught before its prerequisites have been.

    This is the mechanism that ties record levels to the concept graph.

    ``scheduled`` is the curriculum's concept-to-level assignment, and where
    it is given it counts as a prerequisite having a level. **This is the
    fourth rule here to need that distinction**, after the vocabulary lower
    bound, the vocabulary coverage rule and relation coverage. A schedule
    states where a concept is taught. Records only show where it has been
    taught so far, and a rule written against records alone fires on
    everything not yet written.

    **The ordering claim is not weakened.** The schedule validator enforces
    the same relation over the plan, and it enforces it more strictly,
    since a schedule cannot place a concept before its prerequisite at all.
    What this stops doing is reporting an unwritten corpus as a
    mis-ordered one.
    """
    placed = dict(scheduled or {})
    earliest: dict[str, int] = {}
    for record in records:
        for concept in record.concepts:
            prior = earliest.get(concept)
            if prior is None or record.level < prior:
                earliest[concept] = record.level

    out: list[Violation] = []
    for concept, level in sorted(earliest.items()):
        if concept not in graph.nodes:
            continue
        for prerequisite in sorted(graph.prerequisites_of(concept)):
            taught = earliest.get(prerequisite, placed.get(prerequisite))
            if taught is None:
                out.append(
                    Violation(
                        "prerequisite-untaught",
                        f"concept {concept!r} taught at level {level} but "
                        f"prerequisite {prerequisite!r} is never taught",
                    )
                )
            elif taught > level:
                out.append(
                    Violation(
                        "prerequisite-late",
                        f"concept {concept!r} taught at level {level} but "
                        f"prerequisite {prerequisite!r} not until level {taught}",
                    )
                )
    return out


def record_from_json(payload: object) -> Record:
    """Parse one record, validating types at the boundary."""
    if not isinstance(payload, dict):
        raise ValueError("record must be a JSON object")
    body = cast(dict[object, object], payload)
    prov = _parse_provenance(body.get("provenance"))
    simp = _parse_simplification(body.get("simplification"))
    level_raw = body.get("level")
    if not isinstance(level_raw, int) or isinstance(level_raw, bool):
        raise ValueError("record.level must be an integer")
    return Record(
        id=_require_str(body.get("id"), "record.id"),
        level=level_raw,
        concepts=tuple(_require_str_list(body.get("concepts"), "record.concepts")),
        claim_class=ClaimClass(
            _require_str(body.get("claim_class"), "record.claim_class")
        ),
        content=_require_str(body.get("content"), "record.content"),
        provenance=prov,
        simplification=simp,
        defines=definition_from_json(body.get("defines"), "record.defines"),
    )


def load_corpus(path: Path) -> list[Record]:
    """Read newline-delimited JSON records."""
    out: list[Record] = []
    for number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        stripped = line.strip()
        if not stripped:
            continue
        try:
            parsed: object = json.loads(stripped)
            out.append(record_from_json(parsed))
        except ValueError as exc:
            raise ValueError(f"{path}:{number}: {exc}") from exc
    return out


def _require_str(value: object, where: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{where}: expected a string, got {type(value).__name__}")
    return value


def _require_str_list(value: object, where: str) -> list[str]:
    if not isinstance(value, list):
        raise ValueError(f"{where}: expected a list")
    items = cast(list[object], value)
    return [_require_str(item, f"{where}[{i}]") for i, item in enumerate(items)]


def _optional_str(value: object, where: str) -> str | None:
    return None if value is None else _require_str(value, where)


def _parse_provenance(raw: object) -> Provenance:
    if raw is None:
        return Provenance()
    if not isinstance(raw, dict):
        raise ValueError("record.provenance must be an object")
    body = cast(dict[object, object], raw)
    contested = body.get("contested_by")
    assumptions = body.get("assumptions")
    return Provenance(
        source_claim=_optional_str(body.get("source_claim"), "provenance.source_claim"),
        position_holder=_optional_str(
            body.get("position_holder"), "provenance.position_holder"
        ),
        contested_by=(
            ()
            if contested is None
            else tuple(_require_str_list(contested, "provenance.contested_by"))
        ),
        assumptions=(
            ()
            if assumptions is None
            else tuple(_require_str_list(assumptions, "provenance.assumptions"))
        ),
        method=_optional_str(body.get("method"), "provenance.method"),
        why_unavailable=_optional_str(
            body.get("why_unavailable"), "provenance.why_unavailable"
        ),
        validation_status=_optional_str(
            body.get("validation_status"), "provenance.validation_status"
        ),
    )


def _parse_simplification(raw: object) -> Simplification:
    if raw is None:
        return Simplification()
    if not isinstance(raw, dict):
        raise ValueError("record.simplification must be an object")
    body = cast(dict[object, object], raw)
    scope_raw = body.get("validity_scope")
    scope: tuple[int, int] | None = None
    if scope_raw is not None:
        if not isinstance(scope_raw, list) or len(cast(list[object], scope_raw)) != 2:
            raise ValueError("simplification.validity_scope must be a pair")
        pair = cast(list[object], scope_raw)
        low, high = pair[0], pair[1]
        if not isinstance(low, int) or not isinstance(high, int):
            raise ValueError("simplification.validity_scope must hold integers")
        scope = (low, high)
    return Simplification(
        kind=SimplificationKind(
            _require_str(body.get("kind", "none"), "simplification.kind")
        ),
        validity_scope=scope,
        superseded_by=_optional_str(
            body.get("superseded_by"), "simplification.superseded_by"
        ),
    )
