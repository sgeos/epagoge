"""Tests for books and definitions.

A book is where a reader is told what the words mean before they are used.
The rules worth testing are the orderings, because a definition after the
material that uses it is a glossary at the back, and a book about a thing
that never says what the thing is leaves the reader to infer it.
"""

from __future__ import annotations

import json
import random
import tempfile
import unittest
from pathlib import Path
from typing import cast

from epagoge.book import (
    Book,
    Closure,
    Definition,
    DefinitionKind,
    book_prerequisites,
    books_from_json,
    definition_coverage,
    definition_from_json,
    dictionary_closure,
    extend_records,
    linear_extension,
    load_book_dir,
    load_books,
    normalise_definition,
    parse_book,
    random_linear_extension,
    render_book,
    topological_orders_exist,
    validate_books,
    word_definitions,
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


class TestMarkdownFormat(unittest.TestCase):
    """Prose with its annotation above it, rather than prose inside JSON.

    A level-one book of 173 words occupied 260 lines of JSON structure, and
    the project's own sequence makes reading the corpus the step that
    decides whether generation continues.
    """

    def head(self) -> dict[str, object]:
        return {
            "id": "bk",
            "level": 1,
            "title": "T",
            "subject": {"kind": "domain", "target": "physics"},
        }

    def records(self) -> list[dict[str, object]]:
        return [
            {"id": "bk.r1", "level": 1, "content": "One.", "concepts": ["a"]},
            {
                "id": "bk.r2",
                "level": 1,
                "content": "Two.\n\nStill two.",
                "concepts": ["b"],
            },
        ]

    def test_a_book_round_trips(self) -> None:
        text = render_book(self.head(), self.records())
        got, records = parse_book(text)
        self.assertEqual(got.id, "bk")
        self.assertEqual(got.records, ("bk.r1", "bk.r2"))
        self.assertEqual(cast(dict[str, object], records[0])["concepts"], ["a"])

    def test_a_multi_paragraph_record_survives(self) -> None:
        """A level-five record is a paragraph and a level-seven one is more."""
        _, records = parse_book(render_book(self.head(), self.records()))
        self.assertEqual(
            cast(dict[str, object], records[1])["content"], "Two.\n\nStill two."
        )

    def test_the_prose_is_not_escaped(self) -> None:
        text = render_book(self.head(), self.records())
        self.assertIn("\n[bk.r1]\nOne.", text)

    def test_missing_front_matter_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            parse_book("[bk.r1]\nOne.\n")

    def test_unclosed_front_matter_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            parse_book('---\n{"id": "bk"}\n')

    def test_a_block_with_no_annotation_is_rejected(self) -> None:
        text = render_book(self.head(), self.records()) + "\n[bk.r3]\nThree.\n"
        with self.assertRaises(ValueError):
            parse_book(text)

    def test_an_annotation_with_no_block_is_rejected(self) -> None:
        text = render_book(self.head(), self.records())
        text = text.replace("[bk.r2]\nTwo.\n\nStill two.\n", "")
        with self.assertRaises(ValueError):
            parse_book(text)

    def test_a_repeated_block_is_rejected(self) -> None:
        """Blocks are marked rather than positional, so a repeat is not
        silently the second one winning."""
        text = render_book(self.head(), self.records()) + "\n[bk.r1]\nAgain.\n"
        with self.assertRaises(ValueError):
            parse_book(text)

    def test_malformed_front_matter_is_rejected(self) -> None:
        for bad in ('---\n"a string"\n---\n\n', '---\n{"id":"b","level":"1"}\n---\n\n'):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                parse_book(bad)

    def test_the_shipped_books_load(self) -> None:
        books, records = load_book_dir(Path("curriculum/books/level_1"))
        self.assertTrue(books)
        self.assertTrue(records)


class TestBookOrdering(unittest.TestCase):
    """The ablation orders books, so the topological constraint lives here.

    A control arm that ignores it is not a curriculum in any ordering, so it
    would be weaker than the design asks for rather than merely different.
    """

    def books(self) -> list[Book]:
        return [book(id=name, records=()) for name in ("early", "late", "loose")]

    TEACHES = {"early": {"a"}, "late": {"b"}, "loose": {"z"}}
    PREREQ = {"a": set[str](), "b": {"a"}, "z": set[str]()}

    def deps(self) -> dict[str, set[str]]:
        return book_prerequisites(self.books(), self.TEACHES, self.PREREQ)

    def test_a_book_depends_on_the_book_teaching_its_prerequisite(self) -> None:
        self.assertEqual(self.deps()["late"], {"early"})

    def test_an_unconstrained_book_depends_on_nothing(self) -> None:
        self.assertEqual(self.deps()["loose"], set())

    def test_a_prerequisite_taught_in_the_same_book_is_not_a_dependency(self) -> None:
        one = [book(id="both", records=())]
        found = book_prerequisites(one, {"both": {"a", "b"}}, self.PREREQ)
        self.assertEqual(found["both"], set())

    def test_every_extension_respects_the_dependency(self) -> None:
        deps = self.deps()
        for seed in range(12):
            order = random_linear_extension(deps, random.Random(seed))
            self.assertEqual(len(order), 3)
            self.assertLess(order.index("early"), order.index("late"))

    def test_extensions_actually_differ_across_seeds(self) -> None:
        """A control that always returns the same order is not a control."""
        deps = self.deps()
        seen = {
            tuple(random_linear_extension(deps, random.Random(s))) for s in range(20)
        }
        self.assertGreater(len(seen), 1)

    def test_a_deterministic_extension_is_reproducible(self) -> None:
        deps = self.deps()
        first = linear_extension(deps, min)
        self.assertEqual(first, linear_extension(deps, min))

    def test_a_cycle_is_reported_rather_than_raised(self) -> None:
        cyclic = {"a": {"b"}, "b": {"a"}}
        self.assertFalse(topological_orders_exist(cyclic))
        self.assertEqual(linear_extension(cyclic, min), [])

    def test_an_acyclic_graph_reports_orderable(self) -> None:
        self.assertTrue(topological_orders_exist(self.deps()))


class TestDictionaryClosure(unittest.TestCase):
    """The self-hosting check. A lexicon that defines itself, or does not.

    A dictionary in which every word is defined in terms of other words can
    still be vacuous. A compiler written in its own language needs a seed
    compiler written in something else, and the seed here is the function
    words, which name nothing.
    """

    SEED = {"a", "the", "is", "not"}

    def closure(self, definitions: dict[str, str]) -> object:
        return dictionary_closure(
            definitions,
            self.SEED,
            lambda t: t.lower().replace(".", "").split(),
            lambda t: t,
        )

    def test_a_definition_using_only_seed_words_is_grounded(self) -> None:
        got = cast(Closure, self.closure({"cup": "a the is not"}))
        self.assertEqual(got.grounded, frozenset({"cup"}))

    def test_a_word_may_appear_in_its_own_definition(self) -> None:
        got = cast(Closure, self.closure({"cup": "a cup is not the"}))
        self.assertIn("cup", got.grounded)

    def test_grounding_chains(self) -> None:
        got = cast(Closure, self.closure({"a1": "the is", "b1": "a1 is"}))
        self.assertEqual(got.grounded, frozenset({"a1", "b1"}))

    def test_a_word_resting_on_an_undefined_word_is_blocked_not_cyclic(self) -> None:
        """An earlier version called this a cycle. It is stuck, not circular,
        and the two need different fixes."""
        got = cast(Closure, self.closure({"cup": "the ghost"}))
        self.assertEqual(got.undefined, ("ghost",))
        self.assertEqual(got.blocked, ("cup",))
        self.assertEqual(got.cycles, ())

    def test_a_real_cycle_is_reported_as_one(self) -> None:
        got = cast(Closure, self.closure({"x1": "the y1", "y1": "the x1"}))
        self.assertEqual(got.cycles, (("x1", "y1"),))
        self.assertEqual(got.blocked, ())

    def test_a_chain_onto_a_cycle_is_blocked_by_it(self) -> None:
        defs = {"x1": "the y1", "y1": "the x1", "z1": "the x1"}
        got = cast(Closure, self.closure(defs))
        self.assertIn(("x1", "y1"), got.cycles)

    def test_an_empty_dictionary_is_vacuously_complete(self) -> None:
        self.assertEqual(cast(Closure, self.closure({})).fraction, 1.0)

    def test_the_fraction_counts_only_defined_words(self) -> None:
        got = cast(Closure, self.closure({"a1": "the is", "b1": "the ghost"}))
        self.assertAlmostEqual(got.fraction, 0.5)


class AccumulatingIntoABook(unittest.TestCase):
    """A rewrite must not drop what earlier runs wrote.

    The dictionary generator filtered its new records against the ids
    already in the book and then rendered the file from that filtered list,
    so a second run would have replaced every accumulated definition. These
    fail against that behaviour rather than merely passing against the fix.
    """

    def records(self, *ids: str) -> list[dict[str, object]]:
        return [{"id": i, "content": f"the {i}", "level": 1} for i in ids]

    def test_existing_records_survive_a_run_that_adds_none(self) -> None:
        existing = self.records("a", "b")
        got = extend_records(existing, [])
        self.assertEqual([str(r["id"]) for r in got], ["a", "b"])

    def test_existing_records_survive_a_run_that_adds_some(self) -> None:
        got = extend_records(self.records("a", "b"), self.records("c"))
        self.assertEqual([str(r["id"]) for r in got], ["a", "b", "c"])

    def test_the_result_is_never_the_new_records_alone(self) -> None:
        """The exact shape of the defect, named so it cannot come back."""
        new = self.records("c")
        got = extend_records(self.records("a", "b"), new)
        self.assertNotEqual([str(r["id"]) for r in got], [str(r["id"]) for r in new])

    def test_a_repeated_id_is_not_duplicated_and_keeps_the_original(self) -> None:
        existing = self.records("a")
        new = [{"id": "a", "content": "rewritten", "level": 1}]
        got = extend_records(existing, new)
        self.assertEqual(len(got), 1)
        self.assertEqual(str(got[0]["content"]), "the a")

    def test_new_records_repeating_each_other_collapse(self) -> None:
        got = extend_records([], self.records("a", "a", "b"))
        self.assertEqual([str(r["id"]) for r in got], ["a", "b"])

    def test_the_inputs_are_not_mutated(self) -> None:
        existing = self.records("a")
        extend_records(existing, self.records("b"))
        self.assertEqual(len(existing), 1)


class SeedWordsAndTheirInflections(unittest.TestCase):
    """Two defects in the closure itself, found on 2026-09-25.

    `arm` sat in the ostensive seed and was reported on the frontier,
    because the seed was tested against the surface token rather than the
    resolved headword, so every inflection of a seed word looked undefined.
    """

    def closure(self, definitions: dict[str, str], seed: set[str]) -> Closure:
        def resolve(token: str) -> str | None:
            return token[:-1] if token.endswith("s") and len(token) > 2 else token

        return dictionary_closure(definitions, seed, str.split, resolve)

    def test_an_inflection_of_a_seed_word_is_not_undefined(self) -> None:
        got = self.closure({"hug": "two arms"}, {"two"} | {"arm"})
        self.assertEqual(got.undefined, ())
        self.assertIn("hug", got.grounded)

    def test_the_surface_form_alone_still_counts(self) -> None:
        got = self.closure({"hug": "two arm"}, {"two", "arm"})
        self.assertIn("hug", got.grounded)

    def test_a_seed_word_with_a_definition_is_grounded(self) -> None:
        """It reduces to the seed trivially, definition or not."""
        got = self.closure({"arm": "a ghost thing"}, {"arm"})
        self.assertIn("arm", got.grounded)

    def test_a_non_seed_word_still_has_to_earn_it(self) -> None:
        got = self.closure({"cup": "a ghost thing"}, {"a"})
        self.assertNotIn("cup", got.grounded)
        self.assertEqual(set(got.undefined), {"ghost", "thing"})


class CanonicalDefinitions(unittest.TestCase):
    """Which definition reaches the stream must not depend on file order.

    Fifty-two words carried two or more different definitions, because a
    book defines its words in context and the dictionary defines them
    again. That is the design. What was not the design is that every
    caller built the map by assignment in record order.
    """

    def build(
        self, *books: tuple[str, list[tuple[str, str, str]]]
    ) -> tuple[list[Book], list[dict[str, object]]]:
        made: list[Book] = []
        records: list[dict[str, object]] = []
        for book_id, entries in books:
            ids = [rid for rid, _w, _t in entries]
            made.append(
                Book(
                    id=book_id,
                    level=1,
                    title=book_id,
                    subject_kind=DefinitionKind.WORD,
                    subject="x",
                    records=tuple(ids),
                )
            )
            for rid, word, text in entries:
                records.append(
                    {
                        "id": rid,
                        "content": text,
                        "defines": {"kind": "word", "target": word},
                    }
                )
        return made, records

    def test_the_dictionary_definition_wins(self) -> None:
        books, records = self.build(
            ("bk.story", [("a", "empty", "Having nothing inside.")]),
            (
                "bk.dictionary.1",
                [("b", "empty", "A thing is empty when it has nothing in it.")],
            ),
        )
        got = word_definitions(books, records)
        self.assertEqual(got["empty"], "A thing is empty when it has nothing in it.")

    def test_it_wins_whichever_book_is_read_first(self) -> None:
        books, records = self.build(
            ("bk.dictionary.1", [("b", "empty", "canonical")]),
            ("bk.story", [("a", "empty", "in context")]),
        )
        self.assertEqual(word_definitions(books, records)["empty"], "canonical")

    def test_among_ordinary_books_the_first_is_kept(self) -> None:
        """So adding an unrelated book does not move an existing entry."""
        books, records = self.build(
            ("bk.one", [("a", "cup", "first")]),
            ("bk.two", [("b", "cup", "second")]),
        )
        self.assertEqual(word_definitions(books, records)["cup"], "first")

    def test_a_word_defined_once_is_unchanged(self) -> None:
        books, records = self.build(("bk.one", [("a", "cup", "only")]))
        self.assertEqual(word_definitions(books, records), {"cup": "only"})

    def test_records_that_define_nothing_are_ignored(self) -> None:
        books = [
            Book(
                id="bk.one",
                level=1,
                title="t",
                subject_kind=DefinitionKind.WORD,
                subject="x",
                records=("a",),
            )
        ]
        records = [{"id": "a", "content": "a story line"}]
        self.assertEqual(word_definitions(books, records), {})


class TestNormaliseDefinition(unittest.TestCase):
    """A definition is a capitalised fragment, which is not a sentence.

    The dictionary reads "Checking that something is true.", so a teacher
    who writes "checking that something is true" has written an acceptable
    entry in the wrong case rather than an unusable one.
    """

    def test_a_lowercase_fragment_is_capitalised_and_terminated(self) -> None:
        self.assertEqual(
            normalise_definition("a small number of something"),
            "A small number of something.",
        )

    def test_an_already_shaped_definition_is_unchanged(self) -> None:
        text = "Checking that something is true."
        self.assertEqual(normalise_definition(text), text)

    def test_other_terminators_are_kept(self) -> None:
        self.assertEqual(normalise_definition("Is it so?"), "Is it so?")

    def test_surrounding_space_is_dropped(self) -> None:
        self.assertEqual(normalise_definition("  near, not far  "), "Near, not far.")

    def test_an_empty_line_stays_empty(self) -> None:
        self.assertEqual(normalise_definition("   "), "")

    def test_only_the_first_letter_moves(self) -> None:
        """Casing inside the line is the teacher's and is not touched."""
        self.assertEqual(
            normalise_definition("what a McTaggart series is"),
            "What a McTaggart series is.",
        )
