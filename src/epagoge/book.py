"""Books, and the definitions they carry.

A record teaches a concept. **A book is where a reader is told what the
words mean before they are used**, and where the material that uses them
follows in one thread rather than as unconnected assertions.

Specification in ``docs/spec/BOOKS.md``. Standard library only.

The shape is three parts in order. The subject is defined, then the words
are defined, then a story uses them. That ordering is the point. A
definition with nothing following it is a glossary, and a story with no
definitions in front of it assumes vocabulary the reader does not have.

**Every definition is written in the vocabulary of its own level.** At level
one that means seven hundred words defining themselves, which is a closure
property the lexicon was not authored for and may not have.
"""

from __future__ import annotations

import json
from collections.abc import Collection, Iterable, Mapping, Sequence
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import cast

from epagoge.concept_graph import Violation


class DefinitionKind(Enum):
    """What a definition is about."""

    WORD = "word"
    DOMAIN = "domain"
    TOPIC = "topic"
    """A schedule unit. The smallest thing a book can be about."""


@dataclass(frozen=True, slots=True)
class Definition:
    """A record's claim to say what something is.

    Carried on the record rather than on the book, because a book is an
    ordering of records and the definition belongs to the sentence that
    makes it.
    """

    kind: DefinitionKind
    target: str


@dataclass(frozen=True, slots=True)
class Book:
    """An ordered run of records with one subject."""

    id: str
    level: int
    title: str
    subject_kind: DefinitionKind
    subject: str
    records: tuple[str, ...] = ()


@dataclass(frozen=True, slots=True)
class Coverage:
    """What has a definition and what does not."""

    defined: frozenset[str]
    undefined: tuple[str, ...]

    @property
    def fraction(self) -> float:
        total = len(self.defined) + len(self.undefined)
        return len(self.defined) / total if total else 1.0


def definition_coverage(
    definitions: Mapping[str, Definition], kind: DefinitionKind, expected: Iterable[str]
) -> Coverage:
    """Which of ``expected`` carry a definition of ``kind``.

    Reported rather than enforced while the corpus is being written. A word
    with no definition is not a defect in an unfinished corpus and is one in
    a finished level.
    """
    defined = {d.target for d in definitions.values() if d.kind is kind}
    wanted = set(expected)
    return Coverage(
        defined=frozenset(defined & wanted),
        undefined=tuple(sorted(wanted - defined)),
    )


def validate_books(
    books: Sequence[Book],
    record_levels: Mapping[str, int],
    definitions: Mapping[str, Definition],
    known_words: Collection[str],
    known_domains: Collection[str],
    known_topics: Collection[str],
) -> list[Violation]:
    """Return every breach. Empty means the books are sound."""
    out: list[Violation] = []
    seen: dict[str, str] = {}
    targets = {
        DefinitionKind.WORD: set(known_words),
        DefinitionKind.DOMAIN: set(known_domains),
        DefinitionKind.TOPIC: set(known_topics),
    }

    for record_id, definition in sorted(definitions.items()):
        if definition.target not in targets[definition.kind]:
            out.append(
                Violation(
                    "definition-unknown-target",
                    f"record {record_id!r} defines {definition.kind.value}"
                    f" {definition.target!r}, which does not exist",
                )
            )

    for book in books:
        if not book.records:
            out.append(Violation("empty-book", f"book {book.id!r} holds no record"))
        for record_id in book.records:
            if record_id not in record_levels:
                out.append(
                    Violation(
                        "unknown-record",
                        f"book {book.id!r} names absent record {record_id!r}",
                    )
                )
                continue
            if record_levels[record_id] != book.level:
                out.append(
                    Violation(
                        "book-level-mismatch",
                        f"book {book.id!r} at level {book.level} holds record"
                        f" {record_id!r} at level {record_levels[record_id]}",
                    )
                )
            if record_id in seen:
                out.append(
                    Violation(
                        "record-in-two-books",
                        f"record {record_id!r} is in {seen[record_id]!r}"
                        f" and {book.id!r}",
                    )
                )
            seen[record_id] = book.id

        # The subject must be defined inside the book that is about it. A
        # book about a thing that never says what the thing is leaves the
        # reader to infer it, which is the failure this shape exists to fix.
        defined_here = {
            (d.kind, d.target)
            for r in book.records
            if (d := definitions.get(r)) is not None
        }
        if (book.subject_kind, book.subject) not in defined_here:
            out.append(
                Violation(
                    "subject-undefined",
                    f"book {book.id!r} is about {book.subject_kind.value}"
                    f" {book.subject!r} and no record in it defines that",
                )
            )

        # Definition before use. A word defined after the story that uses it
        # is a glossary at the back, which is not what this ordering is for.
        first_story = next(
            (i for i, r in enumerate(book.records) if r not in definitions),
            len(book.records),
        )
        for index, record_id in enumerate(book.records):
            if index > first_story and record_id in definitions:
                out.append(
                    Violation(
                        "definition-after-use",
                        f"book {book.id!r} defines in {record_id!r} after the"
                        " material that uses it has begun",
                    )
                )
    return out


def _require(fields: Mapping[object, object], key: str, where: str) -> str:
    value = fields.get(key)
    if not isinstance(value, str):
        raise ValueError(f"{where}.{key}: expected a string")
    return value


def definition_from_json(raw: object, where: str) -> Definition | None:
    if raw is None:
        return None
    if not isinstance(raw, dict):
        raise ValueError(f"{where}: 'defines' must be an object")
    fields = cast(dict[object, object], raw)
    return Definition(
        kind=DefinitionKind(_require(fields, "kind", where)),
        target=_require(fields, "target", where),
    )


def books_from_json(payload: object) -> list[Book]:
    if not isinstance(payload, list):
        raise ValueError("books payload must be a JSON list")
    out: list[Book] = []
    for index, entry in enumerate(cast(list[object], payload)):
        where = f"books[{index}]"
        if not isinstance(entry, dict):
            raise ValueError(f"{where}: expected an object")
        fields = cast(dict[object, object], entry)
        level = fields.get("level")
        if not isinstance(level, int):
            raise ValueError(f"{where}.level: expected an integer")
        raw_subject = fields.get("subject")
        if not isinstance(raw_subject, dict):
            raise ValueError(f"{where}.subject: expected an object")
        subject = cast(dict[object, object], raw_subject)
        raw_records = fields.get("records")
        if not isinstance(raw_records, list):
            raise ValueError(f"{where}.records: expected a list")
        records = cast(list[object], raw_records)
        for position, record in enumerate(records):
            if not isinstance(record, str):
                raise ValueError(f"{where}.records[{position}]: expected a string")
        out.append(
            Book(
                id=_require(fields, "id", where),
                level=level,
                title=_require(fields, "title", where),
                subject_kind=DefinitionKind(_require(subject, "kind", where)),
                subject=_require(subject, "target", where),
                records=tuple(cast(list[str], records)),
            )
        )
    return out


def load_books(path: Path) -> list[Book]:
    return books_from_json(json.loads(path.read_text(encoding="utf-8")))
