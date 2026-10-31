"""A second sense of an admitted word is filed by word and concept.

Added 2026-10-30 on operator direction. `tools/admit.py` refused every word
already admitted, and `tools/author_definitions.py` filed a new record
under the concept of the word's earliest sense, so a source's sense of
`well` as a water hole could not be filed beside the adverb. These tests
pin the new path and, as much, the refusals that still stand.
"""

from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from typing import cast
from unittest import mock

import tools.author_definitions as authoring
from tools.admit import plan_admission
from tools.author_definitions import (
    is_sense_record,
    new_seed_text,
    sense_record_id,
    split_drafts,
)

from epagoge.book import parse_book, sense_definition

CONCEPTS = {"good_and_bad", "liquid", "quantity", "checking", "standing_for"}


def term(word: str, concept: str, level: int, **extra: object) -> dict[str, object]:
    return {"word": word, "concept": concept, "level": level, **extra}


def spec(concept: str, pos: str, **extra: object) -> dict[str, object]:
    return {
        "concept": concept,
        "pos": pos,
        "definition": "A definition.",
        "source": "test",
        **extra,
    }


class TestPlanAdmission(unittest.TestCase):
    def setUp(self) -> None:
        self.terms = [
            term("well", "good_and_bad", 1),
            term("sample", "quantity", 2, pos="noun", forms=["samples"]),
            term("meaning", "standing_for", 1),
            term("mean", "good_and_bad", 1, pos="verb", forms=["meaning", "means"]),
            term("high", "quantity", 6),
        ]
        self.core = ["the", "a"]

    def plan(
        self, wanted: dict[str, dict[str, object]], level: int = 2
    ) -> tuple[list[str], list[dict[str, object]]]:
        return plan_admission(wanted, self.terms, self.core, CONCEPTS, level)

    def test_a_new_word_is_admitted_as_before(self) -> None:
        problems, entries = self.plan({"pond": spec("liquid", "noun")})
        self.assertEqual(problems, [])
        self.assertEqual(entries[0]["forms"], ["ponds"])
        self.assertEqual(entries[0]["level"], 2)

    def test_an_admitted_word_without_the_flag_is_still_refused(self) -> None:
        problems, entries = self.plan({"well": spec("liquid", "noun")})
        self.assertEqual(problems, ["well: already admitted"])
        self.assertEqual(entries, [])

    def test_a_second_sense_gets_its_own_level_concept_and_forms(self) -> None:
        problems, entries = self.plan(
            {"well": spec("liquid", "noun", second_sense=True)}
        )
        self.assertEqual(problems, [])
        self.assertEqual(
            entries,
            [
                {
                    "word": "well",
                    "concept": "liquid",
                    "level": 2,
                    "pos": "noun",
                    "source": "test",
                    "forms": ["wells"],
                }
            ],
        )
        self.assertNotIn("second_sense", entries[0])

    def test_a_second_sense_keeps_a_form_its_own_word_carries(self) -> None:
        problems, entries = self.plan(
            {"sample": spec("checking", "verb", second_sense=True)}
        )
        self.assertEqual(problems, [])
        self.assertEqual(entries[0]["forms"], ["sampled", "samples", "sampling"])

    def test_a_second_sense_drops_a_form_of_another_word(self) -> None:
        problems, entries = self.plan(
            {"mean": spec("standing_for", "verb", second_sense=True)}
        )
        self.assertEqual(problems, [])
        # `meaning` belongs to `mean` itself, so it stays.
        self.assertIn("meaning", cast(list[str], entries[0]["forms"]))
        self.terms.append(term("meant", "quantity", 1))
        problems, entries = self.plan(
            {"mean": spec("standing_for", "verb", second_sense=True)}
        )
        self.assertNotIn("meant", cast(list[str], entries[0]["forms"]))

    def test_the_same_word_and_concept_is_refused(self) -> None:
        problems, entries = self.plan(
            {"sample": spec("quantity", "noun", second_sense=True)}
        )
        self.assertEqual(
            problems, ["sample: already admitted under 'quantity' at level 2"]
        )
        self.assertEqual(entries, [])

    def test_the_same_word_and_concept_at_a_higher_level_is_refused(self) -> None:
        self.terms.append(term("well", "liquid", 5))
        problems, _ = self.plan({"well": spec("liquid", "noun", second_sense=True)})
        self.assertEqual(problems, ["well: already admitted under 'liquid' at level 5"])

    def test_a_word_that_is_not_a_headword_is_refused(self) -> None:
        problems, _ = self.plan({"pond": spec("liquid", "noun", second_sense=True)})
        self.assertEqual(len(problems), 1)
        self.assertIn("needs a sense already admitted", problems[0])

    def test_a_word_admitted_only_above_the_level_is_refused(self) -> None:
        problems, _ = self.plan(
            {"high": spec("liquid", "adjective", second_sense=True)}
        )
        self.assertEqual(len(problems), 1)
        self.assertIn("at or below level 2", problems[0])

    def test_a_headword_that_is_also_a_form_of_another_word_is_refused(self) -> None:
        problems, _ = self.plan(
            {"meaning": spec("checking", "noun", second_sense=True)}
        )
        self.assertEqual(problems, ["meaning: already a form of 'mean'"])

    def test_a_core_word_is_refused(self) -> None:
        problems, _ = self.plan({"the": spec("checking", "noun", second_sense=True)})
        self.assertEqual(problems, ["the: a core word takes no sense"])

    def test_a_flag_that_is_not_a_boolean_is_refused(self) -> None:
        problems, entries = self.plan(
            {"well": spec("liquid", "noun", second_sense="yes")}
        )
        self.assertEqual(problems, ["well: second_sense must be true or false"])
        self.assertEqual(entries, [])

    def test_one_refusal_admits_nothing(self) -> None:
        problems, entries = self.plan(
            {
                "pond": spec("liquid", "noun"),
                "sample": spec("quantity", "noun", second_sense=True),
            }
        )
        self.assertEqual(len(problems), 1)
        self.assertEqual(entries, [])

    def test_the_other_checks_still_apply_to_a_second_sense(self) -> None:
        problems, _ = self.plan(
            {"well": spec("nowhere", "noun", second_sense=True, source="")}
        )
        self.assertEqual(
            problems,
            [
                "well: concept 'nowhere' is not in the graph",
                "well: no admission source",
            ],
        )


class TestSplitDrafts(unittest.TestCase):
    def test_strings_and_sense_objects_are_separated(self) -> None:
        plain, senses, problems = split_drafts(
            {"pond": "text", "well": {"concept": "liquid", "definition": "other"}}
        )
        self.assertEqual(plain, {"pond": "text"})
        self.assertEqual(senses, {"well": ("liquid", "other")})
        self.assertEqual(problems, [])

    def test_a_malformed_value_is_refused(self) -> None:
        for value in (
            3,
            None,
            {"concept": "liquid"},
            {"concept": "liquid", "definition": "x", "level": 2},
            {"concept": "", "definition": "x"},
            {"concept": "liquid", "definition": 4},
        ):
            with self.subTest(value=value):
                plain, senses, problems = split_drafts({"well": value})
                self.assertEqual((plain, senses), ({}, {}))
                self.assertEqual(len(problems), 1)

    def test_input_that_is_not_an_object_is_refused(self) -> None:
        self.assertEqual(split_drafts(["well"])[2], ["input must be a JSON object"])

    def test_record_ids_name_the_sense(self) -> None:
        self.assertEqual(sense_record_id(2, "well", "liquid"), "dict.2.well.liquid")
        entry: dict[str, object] = {"id": "dict.2.well.liquid", "concepts": ["liquid"]}
        self.assertTrue(is_sense_record(entry, 2, "well"))
        self.assertFalse(is_sense_record(entry, 3, "well"))
        self.assertFalse(
            is_sense_record({"id": "dict.2.well", "concepts": ["liquid"]}, 2, "well")
        )


class TestAuthorSecondSense(unittest.TestCase):
    """The authoring tool end to end, on a lexicon of a few words."""

    def setUp(self) -> None:
        self.directory = tempfile.TemporaryDirectory()
        self.root = Path(self.directory.name)
        curriculum = self.root / "curriculum"
        (curriculum / "books" / "level_1").mkdir(parents=True)
        (curriculum / "books" / "level_2").mkdir(parents=True)
        seeds = ["good", "way", "hole", "ground", "water", "part", "test", "take"]
        terms: list[dict[str, object]] = [term(w, "quantity", 1) for w in seeds]
        terms += [
            term("well", "good_and_bad", 1),
            term("well", "liquid", 2, pos="noun", forms=["wells"]),
            term("sample", "quantity", 2, pos="noun", forms=["samples"]),
            term(
                "sample",
                "checking",
                2,
                pos="noun verb",
                forms=["sampled", "samples", "sampling"],
            ),
            term("pond", "liquid", 2),
        ]
        (curriculum / "vocabulary.json").write_text(
            json.dumps(
                {
                    "core": ["a", "an", "in", "is", "of", "the", "to", "for", "you"],
                    "terms": terms,
                    "ostensive": seeds,
                }
            ),
            encoding="utf-8",
        )
        self.patch = mock.patch.object(authoring, "ROOT", self.root)
        self.patch.start()
        self.assertEqual(self.author({"well": "Well is in a good way."}, 1), 0)
        self.assertEqual(
            self.author({"sample": "A sample is a part of the water."}, 2), 0
        )

    def tearDown(self) -> None:
        self.patch.stop()
        self.directory.cleanup()

    def author(self, drafts: object, level: int) -> int:
        path = self.root / "drafts.json"
        path.write_text(json.dumps(drafts), encoding="utf-8")
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            return authoring.main(
                ["author_definitions.py", str(path), "--level", str(level)]
            )

    def records(self, level: int) -> dict[str, dict[str, object]]:
        path = self.root / f"curriculum/books/level_{level}/bk.dictionary.seed.md"
        _book, records = parse_book(path.read_text(encoding="utf-8"), path.name)
        entries = [cast(dict[str, object], r) for r in records]
        return {str(entry["id"]): entry for entry in entries}

    def test_a_second_sense_gets_its_own_record_and_concept(self) -> None:
        status = self.author(
            {
                "well": {
                    "concept": "liquid",
                    "definition": "A well is a hole in the ground for water.",
                }
            },
            2,
        )
        self.assertEqual(status, 0)
        record = self.records(2)["dict.2.well.liquid"]
        self.assertEqual(record["concepts"], ["liquid"])
        self.assertEqual(record["content"], "A well is a hole in the ground for water.")
        self.assertEqual(
            self.records(1)["dict.1.well"]["content"], "Well is in a good way."
        )

    def test_a_second_sense_beside_a_first_at_the_same_level(self) -> None:
        sense = {
            "concept": "checking",
            "definition": "To sample is to take a part to test.",
        }
        self.assertEqual(self.author({"sample": sense}, 2), 0)
        records = self.records(2)
        self.assertEqual(
            records["dict.2.sample"]["content"], "A sample is a part of the water."
        )
        self.assertEqual(records["dict.2.sample"]["concepts"], ["quantity"])
        self.assertEqual(
            records["dict.2.sample.checking"]["content"],
            "To sample is to take a part to test.",
        )
        # Rewording each one touches only its own record.
        self.assertEqual(
            self.author(
                {
                    "sample": {
                        "concept": "checking",
                        "definition": "To sample is to test a part.",
                    }
                },
                2,
            ),
            0,
        )
        self.assertEqual(self.author({"sample": "A sample is a part."}, 2), 0)
        records = self.records(2)
        self.assertEqual(records["dict.2.sample"]["content"], "A sample is a part.")
        self.assertEqual(
            records["dict.2.sample.checking"]["content"], "To sample is to test a part."
        )
        self.assertEqual(len([r for r in records if r.startswith("dict.2.sample")]), 2)

    def assert_refused(self, drafts: object, level: int, needle: str) -> None:
        before = {
            p: p.read_text(encoding="utf-8")
            for p in sorted((self.root / "curriculum/books").rglob("*.md"))
        }
        path = self.root / "drafts.json"
        path.write_text(json.dumps(drafts), encoding="utf-8")
        err = io.StringIO()
        with redirect_stdout(io.StringIO()), redirect_stderr(err):
            status = authoring.main(
                ["author_definitions.py", str(path), "--level", str(level)]
            )
        self.assertEqual(status, 1)
        self.assertIn(needle, err.getvalue())
        after = {
            p: p.read_text(encoding="utf-8")
            for p in sorted((self.root / "curriculum/books").rglob("*.md"))
        }
        self.assertEqual(after, before)

    def test_a_sense_that_is_not_filed_is_refused(self) -> None:
        self.assert_refused(
            {"well": {"concept": "checking", "definition": "A hole."}},
            2,
            "no sense under 'checking'",
        )

    def test_a_sense_filed_at_another_level_is_refused(self) -> None:
        self.assert_refused(
            {"well": {"concept": "liquid", "definition": "A hole."}},
            1,
            "filed at level 2, not 1",
        )

    def test_an_only_sense_takes_a_plain_definition(self) -> None:
        self.assert_refused(
            {"pond": {"concept": "liquid", "definition": "A hole of water."}},
            2,
            "only sense at or below level 2",
        )

    def test_a_sense_outside_the_level_is_refused(self) -> None:
        self.assert_refused(
            {"well": {"concept": "liquid", "definition": "A deep shaft."}},
            2,
            "outside level 2",
        )

    def test_an_ungrounded_sense_is_refused(self) -> None:
        self.assert_refused(
            {"well": {"concept": "liquid", "definition": "A well is a pond."}},
            2,
            "ungrounded, needs pond",
        )

    def test_a_malformed_value_is_refused(self) -> None:
        self.assert_refused(
            {"well": {"concept": "liquid"}}, 2, "an object with exactly"
        )

    def test_a_dry_run_writes_nothing(self) -> None:
        path = self.root / "drafts.json"
        path.write_text(
            json.dumps(
                {"well": {"concept": "liquid", "definition": "A hole for water."}}
            ),
            encoding="utf-8",
        )
        before = self.records(2)
        with redirect_stdout(io.StringIO()):
            status = authoring.main(
                ["author_definitions.py", str(path), "--level", "2", "--dry-run"]
            )
        self.assertEqual(status, 0)
        self.assertEqual(self.records(2), before)


class TestSenseDefinition(unittest.TestCase):
    def test_a_sense_record_is_found_by_id(self) -> None:
        records: list[dict[str, object]] = [
            {"id": "dict.2.sample", "content": "A part."},
            {"id": "dict.2.sample.checking", "content": "To test a part."},
        ]
        canonical = {"sample": "A part."}
        self.assertEqual(
            sense_definition(records, canonical, 2, "sample", "checking"),
            "To test a part.",
        )

    def test_a_first_sense_falls_back_to_the_canonical_definition(self) -> None:
        records: list[dict[str, object]] = [
            {"id": "dict.2.sample", "content": "A part."}
        ]
        self.assertEqual(
            sense_definition(records, {"sample": "A part."}, 2, "sample", "quantity"),
            "A part.",
        )
        self.assertIsNone(sense_definition(records, {}, 2, "pond", "liquid"))


class TestSeedText(unittest.TestCase):
    def test_the_seed_text_still_names_the_level(self) -> None:
        self.assertIn("level two", new_seed_text(2, "well"))


if __name__ == "__main__":
    unittest.main()
