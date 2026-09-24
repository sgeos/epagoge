"""Per-level vocabulary.

Three categories, because two were not enough.

**Core.** Function words, available from level one, naming no concept.

**General.** Content words not yet mapped to a concept. **This is a holding
pen for unfinished work, not a permanent category.** A content word names
something, so a word with no mapping means either the mapping has not been
identified or a concept is missing from the graph. Only function words
genuinely name nothing.

Its size is therefore a measure of how incomplete the graph is, and it
should shrink toward zero as concepts are added.

**Terms.** Words that name a graph concept. **Their level is authored**, and
the graph supplies a lower bound: a word may not be introduced before the
concept it names has been taught.

An earlier design derived the level from the concept instead of bounding it.
That was wrong, because **a concept can be taught before its name is
introduced.** The level-one record teaching causation never uses the word
"cause", and children grasp causation long before they say it. Deriving
equality admitted thirty-three words at levels where nothing used them.

Two rules, both checkable.

**Ceiling.** A record at level L uses no term whose level exceeds L.

**Coverage.** Every term first admitted at level L appears in at least one
level-L record. Admitting a word is a commitment to teach it.

Specification in ``docs/spec/VOCABULARY.md``. Standard library only.
"""

from __future__ import annotations

import json
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Final, cast

from epagoge.concept_graph import Violation
from epagoge.record import Record

WORD_RE: Final[re.Pattern[str]] = re.compile(r"[a-z]+(?:'[a-z]+)?")
NUMERAL_RE: Final[re.Pattern[str]] = re.compile(r"^\d+$")

_SUFFIXES: Final[tuple[str, ...]] = ("'s", "es", "ed", "ing", "s")
"""Stripped in order when a surface form is not itself a known term.

Deliberately crude. A real stemmer would silently conflate distinct words,
and a vocabulary check that quietly accepts the wrong word is worse than one
that reports a form it does not recognise. Explicit ``forms`` on an entry
override this entirely.
"""


@dataclass(frozen=True, slots=True)
class Term:
    """A content word, and the concept that licenses it."""

    word: str
    concept: str
    level: int
    """Authored. The graph bounds it from below; it is not derived."""

    forms: tuple[str, ...] = ()

    def surface_forms(self) -> tuple[str, ...]:
        return (self.word, *self.forms)


@dataclass(frozen=True, slots=True)
class Vocabulary:
    """Core function words, licensed terms, and standing exemptions."""

    core: frozenset[str] = frozenset()
    """Available from level one. Function words name no concept."""

    terms: tuple[Term, ...] = ()
    general: Mapping[int, frozenset[str]] = field(
        default_factory=dict[int, frozenset[str]]
    )
    """Authored tiers. Ordinary content words that name no concept."""

    exempt: frozenset[str] = frozenset()
    """Proper nouns, units, and anything else outside the level system."""

    # The generic alias is the factory so that the element types are known.
    # A bare ``dict`` leaves them unknown under strict checking.
    _by_form: dict[str, Term] = field(
        default_factory=dict[str, Term], repr=False, compare=False
    )
    _general_level: dict[str, int] = field(
        default_factory=dict[str, int], repr=False, compare=False
    )

    def __post_init__(self) -> None:
        index: dict[str, Term] = {}
        for term in self.terms:
            for form in term.surface_forms():
                index[form] = term
        object.__setattr__(self, "_by_form", index)
        tiers: dict[str, int] = {}
        for level, words in self.general.items():
            for word in words:
                if word not in tiers or level < tiers[word]:
                    tiers[word] = level
        object.__setattr__(self, "_general_level", tiers)

    def general_level(self, token: str) -> int | None:
        """Authored level of a general word, trying crude suffix stripping."""
        direct = self._general_level.get(token)
        if direct is not None:
            return direct
        for suffix in _SUFFIXES:
            if token.endswith(suffix) and len(token) > len(suffix) + 1:
                stem = token[: -len(suffix)]
                for candidate in (stem, stem + "e"):
                    found = self._general_level.get(candidate)
                    if found is not None:
                        return found
        return None

    def lookup(self, token: str) -> Term | None:
        """Resolve a surface form to its term, trying crude suffix stripping."""
        direct = self._by_form.get(token)
        if direct is not None:
            return direct
        for suffix in _SUFFIXES:
            if token.endswith(suffix) and len(token) > len(suffix) + 1:
                stem = token[: -len(suffix)]
                found = self._by_form.get(stem)
                if found is not None:
                    return found
                if suffix in ("es", "ed", "ing") and self._by_form.get(stem + "e"):
                    return self._by_form[stem + "e"]
        return None

    def is_free(self, token: str) -> bool:
        """Whether a token is usable at any level without licensing."""
        return (
            token in self.core or token in self.exempt or bool(NUMERAL_RE.match(token))
        )


@dataclass(frozen=True, slots=True)
class Completeness:
    """How much of the content vocabulary has reached the graph."""

    mapped: int
    unmapped: int

    @property
    def total(self) -> int:
        return self.mapped + self.unmapped

    @property
    def fraction(self) -> float:
        return self.mapped / self.total if self.total else 1.0


def completeness(vocabulary: Vocabulary) -> Completeness:
    """Fraction of content words carrying a concept.

    **A low figure is a statement about the graph, not about the words.**
    Every content word names something. One that maps to nothing means the
    mapping was not identified, or a concept that belongs in the graph is
    absent from it. Function words are excluded because they genuinely name
    nothing.
    """
    unmapped = sum(len(words) for words in vocabulary.general.values())
    return Completeness(mapped=len(vocabulary.terms), unmapped=unmapped)


def tokenise(text: str) -> list[str]:
    """Lowercased word forms. Punctuation and digits are handled separately."""
    return WORD_RE.findall(text.lower())


def concept_levels(records: Sequence[Record]) -> dict[str, int]:
    """Earliest level at which each concept is taught."""
    out: dict[str, int] = {}
    for record in records:
        for concept in record.concepts:
            current = out.get(concept)
            if current is None or record.level < current:
                out[concept] = record.level
    return out


def term_levels(vocabulary: Vocabulary, records: Sequence[Record]) -> dict[str, int]:
    """Authored level of each term. ``records`` is unused and kept for callers."""
    del records
    return {term.word: term.level for term in vocabulary.terms}


def _check_lower_bound(
    vocabulary: Vocabulary, records: Sequence[Record]
) -> list[Violation]:
    """A word may not be introduced before the concept it names is taught.

    This is the graph's only claim on the vocabulary. It bounds a word from
    below and leaves the placement above that bound to the schedule, which
    is a distribution problem the graph does not express.
    """
    taught = concept_levels(records)
    out: list[Violation] = []
    for term in vocabulary.terms:
        concept_level = taught.get(term.concept)
        if concept_level is None:
            out.append(
                Violation(
                    "term-never-introduced",
                    f"term {term.word!r} names concept {term.concept!r}, "
                    "which is never taught",
                )
            )
        elif term.level < concept_level:
            out.append(
                Violation(
                    "term-before-concept",
                    f"term {term.word!r} is admitted at level {term.level} but "
                    f"its concept {term.concept!r} is not taught until "
                    f"{concept_level}",
                )
            )
    return out


def validate_vocabulary(
    vocabulary: Vocabulary,
    records: Sequence[Record],
    known_concepts: Mapping[str, object],
) -> list[Violation]:
    """Check the ceiling rule, the coverage rule, and licensing."""
    out: list[Violation] = []
    out.extend(_check_licensing(vocabulary, known_concepts))
    out.extend(_check_lower_bound(vocabulary, records))
    levels = term_levels(vocabulary, records)
    out.extend(_check_ceiling(vocabulary, records, levels))
    out.extend(_check_coverage(vocabulary, records, levels))
    return out


def _check_licensing(
    vocabulary: Vocabulary, known_concepts: Mapping[str, object]
) -> list[Violation]:
    out: list[Violation] = []
    seen: set[str] = set()
    for term in vocabulary.terms:
        if term.concept not in known_concepts:
            out.append(
                Violation(
                    "unlicensed-term",
                    f"term {term.word!r} names concept {term.concept!r}, "
                    "which is not in the graph",
                )
            )
        for form in term.surface_forms():
            if form in seen:
                out.append(
                    Violation("duplicate-form", f"form {form!r} maps to two terms")
                )
            seen.add(form)
            if form in vocabulary.core:
                out.append(
                    Violation(
                        "core-collision", f"form {form!r} is both core and licensed"
                    )
                )
    return out


def _check_ceiling(
    vocabulary: Vocabulary, records: Sequence[Record], levels: Mapping[str, int | None]
) -> list[Violation]:
    """No record may use a term admitted above its own level."""
    out: list[Violation] = []
    for record in records:
        for token in tokenise(record.content):
            if vocabulary.is_free(token):
                continue
            general = vocabulary.general_level(token)
            if general is not None:
                if general > record.level:
                    out.append(
                        Violation(
                            "vocabulary-ceiling",
                            f"record {record.id!r} at level {record.level} uses "
                            f"{token!r}, a general word admitted at level {general}",
                        )
                    )
                continue
            term = vocabulary.lookup(token)
            if term is None:
                out.append(
                    Violation(
                        "unknown-word",
                        f"record {record.id!r} uses {token!r}, "
                        "which is neither core, exempt, nor a licensed term",
                    )
                )
                continue
            level = levels.get(term.word)
            if level is not None and level > record.level:
                out.append(
                    Violation(
                        "vocabulary-ceiling",
                        f"record {record.id!r} at level {record.level} uses "
                        f"{token!r}, admitted at level {level}",
                    )
                )
    return out


def _check_coverage(
    vocabulary: Vocabulary, records: Sequence[Record], levels: Mapping[str, int | None]
) -> list[Violation]:
    """Every term admitted at level L must appear in some level-L record.

    Admitting a word is a commitment to teach it. A word admitted and never
    used was never taught, and the level's vocabulary would be a claim the
    corpus does not support.
    """
    used_at: dict[int, set[str]] = {}
    for record in records:
        bucket = used_at.setdefault(record.level, set())
        for token in tokenise(record.content):
            term = vocabulary.lookup(token)
            if term is not None:
                bucket.add(term.word)

    out: list[Violation] = []
    for term in vocabulary.terms:
        level = levels.get(term.word)
        if level is None:
            continue
        if term.word not in used_at.get(level, set()):
            out.append(
                Violation(
                    "vocabulary-uncovered",
                    f"term {term.word!r} is admitted at level {level} "
                    "but never used there",
                )
            )
    return out


def load_vocabulary(path: Path) -> Vocabulary:
    parsed: object = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(parsed, dict):
        raise ValueError("vocabulary must be a JSON object")
    body = cast(dict[object, object], parsed)
    return Vocabulary(
        core=frozenset(_str_list(body.get("core"), "core")),
        terms=tuple(_parse_terms(body.get("terms"))),
        general=_parse_general(body.get("general")),
        exempt=frozenset(_str_list(body.get("exempt"), "exempt")),
    )


def _parse_general(raw: object) -> dict[int, frozenset[str]]:
    if raw is None:
        return {}
    if not isinstance(raw, dict):
        raise ValueError("'general' must be an object keyed by level")
    body = cast(dict[object, object], raw)
    out: dict[int, frozenset[str]] = {}
    for key, value in body.items():
        if not isinstance(key, str) or not key.isdigit():
            raise ValueError(f"general key {key!r} must be a level number")
        out[int(key)] = frozenset(_str_list(value, f"general[{key}]"))
    return out


def _str_list(raw: object, where: str) -> list[str]:
    if raw is None:
        return []
    if not isinstance(raw, list):
        raise ValueError(f"'{where}' must be a list")
    items = cast(list[object], raw)
    out: list[str] = []
    for index, item in enumerate(items):
        if not isinstance(item, str):
            raise ValueError(f"{where}[{index}]: expected a string")
        out.append(item.lower())
    return out


def _parse_terms(raw: object) -> list[Term]:
    if raw is None:
        return []
    if not isinstance(raw, list):
        raise ValueError("'terms' must be a list")
    items = cast(list[object], raw)
    out: list[Term] = []
    for index, item in enumerate(items):
        where = f"terms[{index}]"
        if not isinstance(item, dict):
            raise ValueError(f"{where}: expected an object")
        entry = cast(dict[object, object], item)
        word = entry.get("word")
        concept = entry.get("concept")
        level = entry.get("level")
        if not isinstance(word, str) or not isinstance(concept, str):
            raise ValueError(f"{where}: 'word' and 'concept' must be strings")
        if not isinstance(level, int) or isinstance(level, bool):
            raise ValueError(f"{where}: 'level' must be an integer")
        out.append(
            Term(
                word=word.lower(),
                concept=concept,
                level=level,
                forms=tuple(_str_list(entry.get("forms"), f"{where}.forms")),
            )
        )
    return out
