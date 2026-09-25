"""Tests for books and definitions.

A book is where a reader is told what the words mean before they are used.
The rules worth testing are the orderings, because a definition after the
material that uses it is a glossary at the back, and a book about a thing
that never says what the thing is leaves the reader to infer it.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from epagoge.book import (
    Book,
    Definition,
    DefinitionKind,
    books_from_json,
    definition_coverage,
    definition_from_json,
    load_books,
    validate_books,
)

WORDS = {"cup", "water"}
DOMAINS = {"physics"}
TOPICS = {"p1.things"}


def book(**over: object) -> Book:
    base: dict[str, object] = {
        "id": "bk",
        "level": 1,
        "title": "T",
        "subject_kind": DefinitionKind.DOMAIN,
        "subject": "physics",
        "records": ("d1", "s1"),
    }
    base.update(over)
    return Book(**base)  # pyright: ignore[reportArgumentType]


def codes(
    books: list[Book],
    levels: dict[str, int],
    defs: dict[str, Definition],
) -> set[str]:
    return {v.code for v in validate_books(books, levels, defs, WORDS, DOMAINS, TOPICS)}


DOMAIN_DEF = {"d1": Definition(DefinitionKind.DOMAIN, "physics")}


class TestSound(unittest.TestCase):
    def test_a_sound_book_has_no_violations(self) -> None:
        found = validate_books(
            [book()], {"d1": 1, "s1": 1}, DOMAIN_DEF, WORDS, DOMAINS, TOPICS
        )
        self.assertEqual(found, [])


class TestBookRules(unittest.TestCase):
    def test_an_empty_book_is_a_violation(self) -> None:
        self.assertIn("empty-book", codes([book(records=())], {}, {}))

    def test_an_absent_record_is_a_violation(self) -> None:
        self.assertIn("unknown-record", codes([book()], {"d1": 1}, DOMAIN_DEF))

    def test_a_record_at_another_level_is_a_violation(self) -> None:
        self.assertIn(
            "book-level-mismatch", codes([book()], {"d1": 1, "s1": 3}, DOMAIN_DEF)
        )

    def test_a_record_in_two_books_is_a_violation(self) -> None:
        two = [book(), book(id="bk2")]
        self.assertIn("record-in-two-books", codes(two, {"d1": 1, "s1": 1}, DOMAIN_DEF))

    def test_a_book_that_never_defines_its_subject_is_a_violation(self) -> None:
        """A book about a thing that never says what it is leaves the
        reader to infer it, which is the failure this shape exists to fix."""
        self.assertIn("subject-undefined", codes([book()], {"d1": 1, "s1": 1}, {}))

    def test_a_definition_after_the_story_is_a_violation(self) -> None:
        b = book(records=("s1", "d1"))
        self.assertIn(
            "definition-after-use", codes([b], {"d1": 1, "s1": 1}, DOMAIN_DEF)
        )

    def test_a_definition_of_something_absent_is_a_violation(self) -> None:
        defs = {"d1": Definition(DefinitionKind.WORD, "ghost")}
        self.assertIn(
            "definition-unknown-target", codes([book()], {"d1": 1, "s1": 1}, defs)
        )

    def test_every_kind_resolves_against_its_own_namespace(self) -> None:
        defs = {"d1": Definition(DefinitionKind.TOPIC, "p1.things")}
        found = codes(
            [book(subject_kind=DefinitionKind.TOPIC, subject="p1.things")],
            {"d1": 1, "s1": 1},
            defs,
        )
        self.assertNotIn("definition-unknown-target", found)


class TestCoverage(unittest.TestCase):
    def test_coverage_counts_only_the_expected(self) -> None:
        defs = {
            "a": Definition(DefinitionKind.WORD, "cup"),
            "b": Definition(DefinitionKind.WORD, "elsewhere"),
        }
        got = definition_coverage(defs, DefinitionKind.WORD, WORDS)
        self.assertEqual(got.defined, frozenset({"cup"}))
        self.assertEqual(got.undefined, ("water",))
        self.assertAlmostEqual(got.fraction, 0.5)

    def test_coverage_of_nothing_expected_is_complete(self) -> None:
        self.assertEqual(definition_coverage({}, DefinitionKind.WORD, []).fraction, 1.0)

    def test_a_definition_of_another_kind_does_not_count(self) -> None:
        defs = {"a": Definition(DefinitionKind.DOMAIN, "cup")}
        self.assertEqual(
            definition_coverage(defs, DefinitionKind.WORD, WORDS).defined, frozenset()
        )


class TestParsing(unittest.TestCase):
    def payload(self) -> list[object]:
        return [
            {
                "id": "bk",
                "level": 1,
                "title": "T",
                "subject": {"kind": "domain", "target": "physics"},
                "records": ["d1"],
            }
        ]

    def test_a_well_formed_payload_round_trips(self) -> None:
        got = books_from_json(self.payload())
        self.assertEqual(got[0].subject_kind, DefinitionKind.DOMAIN)
        self.assertEqual(got[0].records, ("d1",))

    def test_load_reads_a_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "b.json"
            path.write_text(json.dumps(self.payload()), encoding="utf-8")
            self.assertEqual(load_books(path)[0].id, "bk")

    def test_an_absent_definition_parses_as_none(self) -> None:
        self.assertIsNone(definition_from_json(None, "where"))

    def test_a_well_formed_definition_parses(self) -> None:
        got = definition_from_json({"kind": "word", "target": "cup"}, "where")
        self.assertEqual(got, Definition(DefinitionKind.WORD, "cup"))

    def test_malformed_payloads_are_rejected_at_the_boundary(self) -> None:
        bad: list[object] = [
            "not a list",
            [
                {
                    "id": "b",
                    "level": "1",
                    "title": "t",
                    "subject": {"kind": "domain", "target": "p"},
                    "records": [],
                }
            ],
            [{"id": "b", "level": 1, "title": "t", "subject": "domain", "records": []}],
            [
                {
                    "id": "b",
                    "level": 1,
                    "title": "t",
                    "subject": {"kind": "domain", "target": "p"},
                    "records": "d1",
                }
            ],
            [
                {
                    "id": "b",
                    "level": 1,
                    "title": "t",
                    "subject": {"kind": "domain", "target": "p"},
                    "records": [1],
                }
            ],
            ["not an object"],
        ]
        for payload in bad:
            with self.subTest(payload=payload), self.assertRaises(ValueError):
                books_from_json(payload)

    def test_a_malformed_definition_is_rejected(self) -> None:
        for raw in ("word", {"kind": "word"}, {"kind": "nope", "target": "c"}):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                definition_from_json(raw, "where")
