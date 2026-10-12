"""Group inflected spellings under one citation form.

The scan counts each spelling on its own. Scheduling and long-tail
analysis need the other view. A noun's number joins that noun. A verb's
person, tense and participles join that verb. An adjective or an adverb
joins its compared forms. The optional cross-class view then counts every
class of the same citation together.

**This does not admit a word and it does not loosen the vocabulary
check.** A real stemmer would merge distinct words and the check would
accept the wrong one. A group here is a proposal. A surface the rules send
to two different citation forms is left unresolved and is not added to
either. An admitted headword keeps its own spelling.

The spelling rules are the ones in ``inflection``. A form the irregular
tables explain joins that entry. Where the same spelling is also its own
word, and that word is not an admitted headword, the irregular reading is
the one kept. ``saw`` joins ``see`` until ``saw`` is admitted on its own.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Final

from epagoge.inflection import (
    INFLECTION_SLOTS,
    IRREGULAR,
    IRREGULAR_COMPARISON,
    IRREGULAR_PLURAL,
    comparative,
    describe_inflections,
    past,
    past_participle,
    plural,
    present_participle,
    superlative,
    third_person,
)
from epagoge.vocabulary import Term, Vocabulary

CLASSES: Final[tuple[str, ...]] = ("noun", "verb", "adjective", "adverb")

ORIGIN_ADMITTED: str = "admitted"
ORIGIN_DERIVED: str = "derived"
ORIGIN_LISTED: str = "listed"
ORIGIN_PROPOSED: str = "proposed"
ORIGIN_REGISTERED: str = "registered"

_NOUN_SLOTS = frozenset({"singular", "plural"})
_VERB_SLOTS = frozenset({"third", "past", "past_participle", "present_participle"})
_GRADE_SLOTS = frozenset({"comparative", "superlative"})
_CLOSED_ORIGINS = frozenset(
    {ORIGIN_ADMITTED, ORIGIN_DERIVED, ORIGIN_LISTED, ORIGIN_REGISTERED}
)


@dataclass(frozen=True, slots=True)
class Reading:
    """One way a surface can belong to a citation form."""

    surface: str
    root: str
    pos: str
    slot: str
    origin: str
    level: int | None


@dataclass(frozen=True, slots=True)
class SharedSurface:
    """A count that fits several classes of one root and is not split."""

    surface: str
    count: int
    classes: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class RootCount:
    """Observed occurrences of one citation form."""

    root: str
    total: int
    by_class: tuple[tuple[str, int], ...]
    shared: tuple[SharedSurface, ...]
    earliest_level: int | None
    origins: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class UnresolvedSurface:
    """A spelling the rules send to more than one citation form."""

    surface: str
    count: int
    readings: tuple[Reading, ...]


@dataclass(frozen=True, slots=True)
class CountReport:
    """Grouped counts, unresolved spellings, and closed-class skips.

    ``omitted`` holds a spelling that has no reading in the requested
    class. Its count is not added anywhere.
    """

    roots: tuple[RootCount, ...]
    unresolved: tuple[UnresolvedSurface, ...]
    skipped: tuple[tuple[str, int], ...]
    omitted: tuple[tuple[str, int], ...] = ()


@dataclass(frozen=True, slots=True)
class SensePlacement:
    """One admitted sense of a class, with the surfaces that sense owns."""

    concept: str
    level: int
    surfaces: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ClassPlacement:
    """Every admitted sense of one class of a citation form."""

    pos: str
    senses: tuple[SensePlacement, ...]


@dataclass(frozen=True, slots=True)
class ScheduledRoot:
    """Where an admitted citation form sits, by class and by level."""

    root: str
    placements: tuple[ClassPlacement, ...]
    earliest: int


def analyse(
    surface: str,
    vocabulary: Vocabulary,
    *,
    pos: str | None = None,
    propose_classes: bool = False,
) -> tuple[Reading, ...]:
    """Readings of one spelling.

    Admitted forms win. ``propose_classes`` adds a sibling class of the
    same citation when the spelling rule supports it and the lexicon has
    not declared that class. A part-of-speech filter keeps that class.
    An unspecified citation is read as the requested class, because the
    caller has said which class the base belongs to.
    """
    token = _surface(surface)
    _check_pos(pos)
    found = _readings(token, vocabulary, propose_classes=propose_classes)
    if pos is None:
        return found
    selected = tuple(reading for reading in found if reading.pos == pos)
    if selected:
        return selected
    if len(found) == 1 and found[0].pos == "" and found[0].root == token:
        only = found[0]
        return (
            Reading(only.surface, only.root, pos, only.slot, only.origin, only.level),
        )
    return ()


def count_roots(
    counts: Mapping[str, int],
    vocabulary: Vocabulary,
    *,
    pos: str | None = None,
    propose_classes: bool = False,
    skip_closed: bool = True,
) -> CountReport:
    """Add each observed count once under the citation form it belongs to.

    A spelling with one citation form adds to that root. Several classes
    of that form are kept together on the root and are not divided. A
    spelling with several citation forms is unresolved. Core words and
    exemptions are skipped when ``skip_closed`` is set.
    """
    _check_pos(pos)
    totals: dict[str, int] = {}
    by_class: dict[str, dict[str, int]] = {}
    shared: dict[str, list[SharedSurface]] = {}
    levels: dict[str, list[int]] = {}
    origins: dict[str, set[str]] = {}
    unresolved: list[UnresolvedSurface] = []
    skipped: list[tuple[str, int]] = []
    omitted: list[tuple[str, int]] = []
    for raw, count in counts.items():
        if count < 0:
            raise ValueError(f"count for {raw!r} is negative")
        if count == 0:
            continue
        token = _surface(raw)
        if skip_closed and (token in vocabulary.core or token in vocabulary.exempt):
            skipped.append((token, count))
            continue
        found = analyse(token, vocabulary, pos=pos, propose_classes=propose_classes)
        if not found:
            omitted.append((token, count))
            continue
        roots = tuple(dict.fromkeys(reading.root for reading in found))
        if len(roots) != 1:
            unresolved.append(UnresolvedSurface(token, count, found))
            continue
        root = roots[0]
        totals[root] = totals.get(root, 0) + count
        classes = tuple(dict.fromkeys(reading.pos for reading in found))
        if len(classes) == 1:
            column = by_class.setdefault(root, {})
            column[classes[0]] = column.get(classes[0], 0) + count
        else:
            shared.setdefault(root, []).append(SharedSurface(token, count, classes))
        bucket = levels.setdefault(root, [])
        seen = origins.setdefault(root, set())
        for reading in found:
            seen.add(reading.origin)
            if reading.level is not None:
                bucket.append(reading.level)
    rows = [
        RootCount(
            root=root,
            total=total,
            by_class=tuple(sorted(by_class.get(root, {}).items())),
            shared=tuple(shared.get(root, ())),
            earliest_level=min(levels[root]) if levels[root] else None,
            origins=tuple(sorted(origins[root])),
        )
        for root, total in totals.items()
    ]
    rows.sort(key=lambda row: (-row.total, row.root))
    unresolved.sort(key=lambda row: (-row.count, row.surface))
    skipped.sort(key=lambda row: (-row[1], row[0]))
    omitted.sort(key=lambda row: (-row[1], row[0]))
    return CountReport(tuple(rows), tuple(unresolved), tuple(skipped), tuple(omitted))


def scheduled_roots(
    vocabulary: Vocabulary,
    *,
    across_classes: bool = False,
    level: int | None = None,
) -> tuple[ScheduledRoot, ...]:
    """Admitted citation forms, with the class and level of each sense.

    ``across_classes`` keeps every declared class of a citation on one
    record. Otherwise each class is its own record, so a verb admitted
    early and a noun admitted later stay separate. ``level`` keeps senses
    admitted at that level or earlier.
    """
    if level is not None and level < 1:
        raise ValueError(f"level must be at least 1, got {level}")
    if across_classes:
        return _across_schedule(vocabulary, level)
    merged: dict[tuple[str, str], list[SensePlacement]] = {}
    for term in vocabulary.terms:
        for placement_pos, sense in _term_placements(term):
            if level is not None and sense.level > level:
                continue
            merged.setdefault((term.word, placement_pos), []).append(sense)
    out = [
        ScheduledRoot(
            root,
            (ClassPlacement(pos, tuple(_unique_senses(senses))),),
            min(sense.level for sense in senses),
        )
        for (root, pos), senses in merged.items()
    ]
    out.sort(key=lambda row: (row.earliest, row.root, row.placements[0].pos))
    return tuple(out)


def _across_schedule(
    vocabulary: Vocabulary, level: int | None
) -> tuple[ScheduledRoot, ...]:
    by_root: dict[str, dict[str, list[SensePlacement]]] = {}
    for term in vocabulary.terms:
        for placement_pos, sense in _term_placements(term):
            if level is not None and sense.level > level:
                continue
            by_root.setdefault(term.word, {}).setdefault(placement_pos, []).append(
                sense
            )
    records: list[ScheduledRoot] = []
    for root, classes in by_root.items():
        placements = tuple(
            ClassPlacement(pos, tuple(_unique_senses(senses)))
            for pos, senses in sorted(classes.items())
        )
        earliest = min(
            sense.level for placement in placements for sense in placement.senses
        )
        records.append(ScheduledRoot(root, placements, earliest))
    records.sort(key=lambda row: (row.earliest, row.root))
    return tuple(records)


def _unique_senses(senses: list[SensePlacement]) -> list[SensePlacement]:
    seen: set[tuple[str, int, tuple[str, ...]]] = set()
    out: list[SensePlacement] = []
    for sense in senses:
        key = (sense.concept, sense.level, sense.surfaces)
        if key not in seen:
            seen.add(key)
            out.append(sense)
    return out


def _term_placements(term: Term) -> tuple[tuple[str, SensePlacement], ...]:
    rows = _admitted_rows(term)
    if not rows:
        return ()
    by_pos: dict[str, list[str]] = {}
    for surface, pos, _slot, _origin in rows:
        by_pos.setdefault(pos, [])
        if surface not in by_pos[pos]:
            by_pos[pos].append(surface)
    return tuple(
        (
            pos,
            SensePlacement(term.concept, term.level, tuple(surfaces)),
        )
        for pos, surfaces in by_pos.items()
    )


def _readings(
    surface: str, vocabulary: Vocabulary, *, propose_classes: bool
) -> tuple[Reading, ...]:
    admitted = _admitted(surface, vocabulary)
    if admitted and not propose_classes:
        return _prefer_headword(surface, admitted)
    if admitted:
        siblings = [
            reading
            for reading in _proposed(surface, vocabulary, allow_other_classes=True)
            if reading.pos not in {item.pos for item in admitted}
            and reading.root in {item.root for item in admitted}
        ]
        return _prefer_headword(surface, [*admitted, *siblings])
    proposed = _proposed(surface, vocabulary, allow_other_classes=False)
    if proposed:
        return proposed
    return (Reading(surface, surface, "", "citation", ORIGIN_PROPOSED, None),)


def _prefer_headword(surface: str, readings: list[Reading]) -> tuple[Reading, ...]:
    roots = {reading.root for reading in readings}
    if len(roots) > 1 and any(reading.root == surface for reading in readings):
        readings = [reading for reading in readings if reading.root == surface]
    return _dedupe(readings)


def _admitted(surface: str, vocabulary: Vocabulary) -> list[Reading]:
    found: list[Reading] = []
    for term in vocabulary.terms:
        for form, pos, slot, origin in _admitted_rows(term):
            if form != surface:
                continue
            found.append(Reading(surface, term.word, pos, slot, origin, term.level))
    return found


def _admitted_rows(term: Term) -> tuple[tuple[str, str, str, str], ...]:
    classes = tuple(part for part in term.pos.split() if part in CLASSES)
    registered = dict(term.inflection)
    described = describe_inflections(term.word, term.pos, registered)
    rows: list[tuple[str, str, str, str]] = []
    seen: set[tuple[str, str, str]] = set()

    def add(surface: str, pos: str, slot: str, origin: str) -> None:
        if not surface:
            return
        key = (surface, pos, slot)
        if key in seen:
            return
        seen.add(key)
        rows.append((surface, pos, slot, origin))

    if not classes:
        add(term.word, "", "citation", ORIGIN_ADMITTED)
        for form in term.forms:
            add(form, "", "listed", ORIGIN_LISTED)
        return tuple(rows)
    for pos in classes:
        add(term.word, pos, _citation_slot(term, pos), ORIGIN_ADMITTED)
    for name, form, origin in described:
        if not form:
            continue
        detail = ORIGIN_REGISTERED if origin == "registered" else ORIGIN_DERIVED
        if origin == "citation":
            detail = ORIGIN_ADMITTED
        for pos in _slot_classes(name, classes):
            add(form, pos, name, detail)
    for form in term.forms:
        for pos in classes:
            if any(
                surface == form and row_pos == pos for surface, row_pos, _s, _o in rows
            ):
                continue
            add(form, pos, "listed", ORIGIN_LISTED)
    return tuple(rows)


def _citation_slot(term: Term, pos: str) -> str:
    parts = set(term.pos.split())
    if pos == "noun" and "plural-only" in parts:
        return "plural"
    if pos == "noun":
        return "singular"
    return "citation"


def _slot_classes(slot: str, classes: tuple[str, ...]) -> tuple[str, ...]:
    if slot in _NOUN_SLOTS:
        return tuple(pos for pos in classes if pos == "noun")
    if slot in _VERB_SLOTS:
        return tuple(pos for pos in classes if pos == "verb")
    if slot in _GRADE_SLOTS:
        return tuple(pos for pos in classes if pos in ("adjective", "adverb"))
    return ()


def _proposed(
    surface: str, vocabulary: Vocabulary, *, allow_other_classes: bool
) -> tuple[Reading, ...]:
    found: list[Reading] = []
    for root, pos, slot in _inflectional_bases(surface, vocabulary):
        if _admitted_class_rejects(
            root, pos, surface, vocabulary, allow_other_classes=allow_other_classes
        ):
            continue
        level = _class_level(root, pos, vocabulary)
        origin = ORIGIN_DERIVED if level is not None else ORIGIN_PROPOSED
        found.append(Reading(surface, root, pos, slot, origin, level))
    ly = _ly_reading(surface, vocabulary)
    if ly is not None and all(
        reading.pos != "adverb" or reading.root != ly.root for reading in found
    ):
        found.append(ly)
    if not found:
        return ()
    return _dedupe(found)


def _admitted_class_rejects(
    root: str,
    pos: str,
    surface: str,
    vocabulary: Vocabulary,
    *,
    allow_other_classes: bool,
) -> bool:
    """An admitted citation owns its paradigm.

    A class the lexicon does not declare is not invented, unless the
    caller asked for sibling classes. A manufactured plural of a mass
    noun, or a regular plural beside a registered one, is not added.
    """
    terms = [term for term in vocabulary.terms if term.word == root]
    if not terms:
        return False
    class_terms = [term for term in terms if pos in term.pos.split()]
    if not class_terms:
        return not allow_other_classes
    owned = {
        form
        for term in class_terms
        for form, row_pos, _slot, _origin in _admitted_rows(term)
        if row_pos == pos
    }
    return surface not in owned


def _class_level(root: str, pos: str, vocabulary: Vocabulary) -> int | None:
    levels = [
        term.level
        for term in vocabulary.terms
        if term.word == root and pos in term.pos.split()
    ]
    return min(levels) if levels else None


def _ly_reading(surface: str, vocabulary: Vocabulary) -> Reading | None:
    """An -ly adverb of an admitted adjective, and not of an unknown stem."""
    if len(surface) < 5 or not surface.endswith("ly"):
        return None
    if any(term.word == surface for term in vocabulary.terms):
        return None
    stem = surface[:-3] + "y" if surface.endswith("ily") else surface[:-2]
    level = _class_level(stem, "adjective", vocabulary)
    if level is None:
        return None
    return Reading(surface, stem, "adverb", "ly", ORIGIN_DERIVED, level)


def _inflectional_bases(
    surface: str, vocabulary: Vocabulary
) -> tuple[tuple[str, str, str], ...]:
    found: list[tuple[str, str, str]] = []
    for base in _choose(
        surface, plural, _s_candidates(surface), _irregular_plurals(surface), vocabulary
    ):
        found.append((base, "noun", "plural"))
    for base in _choose(
        surface,
        third_person,
        _s_candidates(surface),
        _irregular_thirds(surface),
        vocabulary,
    ):
        found.append((base, "verb", "third"))
    for base in _choose(
        surface, past, _ed_candidates(surface), _irregular_verbs(surface, 0), vocabulary
    ):
        found.append((base, "verb", "past"))
    for base in _choose(
        surface,
        past_participle,
        _ed_candidates(surface),
        _irregular_verbs(surface, 1),
        vocabulary,
    ):
        found.append((base, "verb", "past_participle"))
    for base in _choose(
        surface,
        present_participle,
        _ing_candidates(surface),
        _irregular_verbs(surface, 2),
        vocabulary,
    ):
        found.append((base, "verb", "present_participle"))
    for base in _choose(
        surface,
        comparative,
        _grade_candidates(surface, "er", "r", "ier"),
        _irregular_grades(surface, 0),
        vocabulary,
    ):
        if not _doubled_grade(base):
            found.append((base, "adjective", "comparative"))
            found.append((base, "adverb", "comparative"))
    for base in _choose(
        surface,
        superlative,
        _grade_candidates(surface, "est", "st", "iest"),
        _irregular_grades(surface, 1),
        vocabulary,
    ):
        if not _doubled_grade(base):
            found.append((base, "adjective", "superlative"))
            found.append((base, "adverb", "superlative"))
    return tuple(found)


def _doubled_grade(word: str) -> bool:
    """True when the comparative is formed by doubling the final consonant.

    A proposed reading does not use that spelling. ``cutter`` is not the
    comparative of an undeclared ``cut``. An admitted adjective still
    contributes the form through its own paradigm.
    """
    if len(word) < 3:
        return False
    return comparative(word) == word + word[-1] + "er"


def _choose(
    surface: str,
    forward: Callable[[str], str],
    regular: tuple[str, ...],
    irregular: tuple[str, ...],
    vocabulary: Vocabulary,
) -> tuple[str, ...]:
    """Bases whose forward rule reproduces ``surface``.

    An admitted headword wins against a spurious extension. An irregular
    base is kept beside it, so ``axes`` is not forced onto ``axe`` while
    ``axis`` remains possible. A silent-e base and its truncation are both
    kept when neither is admitted, and the surface stays unresolved.
    """
    regular_hits = tuple(
        base
        for base in regular
        if len(base) >= 2 and base != surface and forward(base) == surface
    )
    irregular_hits = tuple(
        base for base in irregular if base != surface and forward(base) == surface
    )
    admitted = tuple(
        base
        for base in dict.fromkeys((*irregular_hits, *regular_hits))
        if any(term.word == base for term in vocabulary.terms)
    )
    if admitted:
        extra = tuple(base for base in irregular_hits if base not in admitted)
        return tuple(dict.fromkeys((*admitted, *extra)))
    plain = [base for base in regular_hits if not _silent_e_partner(base, regular_hits)]
    pairs = [base for base in regular_hits if _silent_e_partner(base, regular_hits)]
    chosen = _shortest((tuple(plain), irregular_hits))
    return tuple(dict.fromkeys((*chosen, *pairs)))


def _silent_e_partner(base: str, regular: tuple[str, ...]) -> bool:
    if base.endswith("e") and base[:-1] in regular:
        return True
    return f"{base}e" in regular


def _shortest(groups: tuple[tuple[str, ...], tuple[str, ...]]) -> tuple[str, ...]:
    """Keep the shortest regular base, and every irregular base."""
    regular, irregular = groups
    kept: list[str] = []
    if regular:
        shortest = min(len(base) for base in regular)
        kept.extend(base for base in regular if len(base) == shortest)
    for base in irregular:
        if base not in kept:
            kept.append(base)
    return tuple(kept)


def _s_candidates(surface: str) -> tuple[str, ...]:
    found: list[str] = []
    if len(surface) > 3 and surface.endswith("ies"):
        found.append(surface[:-3] + "y")
    if len(surface) > 2 and surface.endswith("es"):
        found.append(surface[:-2])
    if len(surface) > 1 and surface.endswith("s"):
        found.append(surface[:-1])
    return tuple(dict.fromkeys(found))


def _ed_candidates(surface: str) -> tuple[str, ...]:
    found: list[str] = []
    if len(surface) > 3 and surface.endswith("ied"):
        found.append(surface[:-3] + "y")
    elif len(surface) > 2 and surface.endswith("ed"):
        body = surface[:-2]
        if len(body) > 1 and body[-1] == body[-2] and body[-1] not in "aeiou":
            found.append(body[:-1])
        else:
            found.append(body)
            silent = surface[:-1]
            if silent.endswith("e"):
                found.append(silent)
    return tuple(dict.fromkeys(found))


def _ing_candidates(surface: str) -> tuple[str, ...]:
    found: list[str] = []
    if len(surface) > 4 and surface.endswith("ying"):
        # ``ie`` becomes ``ying``. The truncated stem is the same letters
        # and is not a second base.
        found.append(surface[:-4] + "ie")
    elif len(surface) > 3 and surface.endswith("ing"):
        stem = surface[:-3]
        if len(stem) > 1 and stem[-1] == stem[-2] and stem[-1] not in "aeiou":
            found.append(stem[:-1])
        else:
            found.append(stem)
            found.append(stem + "e")
    return tuple(dict.fromkeys(found))


def _grade_candidates(
    surface: str, suffix: str, after_e: str, y_suffix: str
) -> tuple[str, ...]:
    found: list[str] = []
    if surface.endswith(y_suffix) and len(surface) > len(y_suffix):
        found.append(surface[: -len(y_suffix)] + "y")
    if surface.endswith(suffix) and len(surface) > len(suffix):
        stem = surface[: -len(suffix)]
        found.append(stem)
        if len(stem) > 1 and stem[-1] == stem[-2] and stem[-1] not in "aeiou":
            found.append(stem[:-1])
    if surface.endswith(after_e) and len(surface) > len(after_e):
        found.append(surface[: -len(after_e)])
    return tuple(dict.fromkeys(found))


def _irregular_plurals(surface: str) -> tuple[str, ...]:
    return tuple(base for base, form in IRREGULAR_PLURAL.items() if form == surface)


def _irregular_thirds(surface: str) -> tuple[str, ...]:
    if surface == "is":
        return ("be",)
    if surface == "has":
        return ("have",)
    return ()


def _irregular_verbs(surface: str, index: int) -> tuple[str, ...]:
    return tuple(base for base, forms in IRREGULAR.items() if forms[index] == surface)


def _irregular_grades(surface: str, index: int) -> tuple[str, ...]:
    return tuple(
        base for base, forms in IRREGULAR_COMPARISON.items() if forms[index] == surface
    )


def _dedupe(readings: list[Reading]) -> tuple[Reading, ...]:
    seen: set[tuple[str, str, str, str]] = set()
    out: list[Reading] = []
    for reading in readings:
        key = (reading.root, reading.pos, reading.slot, reading.origin)
        if key in seen:
            continue
        seen.add(key)
        out.append(reading)
    out.sort(key=lambda reading: (_slot_rank(reading.slot), reading.pos, reading.root))
    return tuple(out)


def _slot_rank(slot: str) -> int:
    if slot in _SLOT_RANK:
        return _SLOT_RANK[slot]
    return len(_SLOT_RANK)


def _surface(raw: str) -> str:
    token = raw.strip().lower()
    if not token:
        raise ValueError("surface is empty")
    return token


def _check_pos(pos: str | None) -> None:
    if pos is not None and pos not in CLASSES:
        raise ValueError(f"pos must be one of {', '.join(CLASSES)}, got {pos!r}")


_SLOT_RANK: Final[dict[str, int]] = {
    name: index
    for index, name in enumerate((*INFLECTION_SLOTS, "citation", "listed", "ly"))
}
