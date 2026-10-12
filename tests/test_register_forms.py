"""Registration writes alternates onto an existing sense and checks them."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.author_definitions import new_seed_text, write_seed_if_missing
from tools.register_forms import main

from epagoge.book import parse_book


class TestRegisterForms(unittest.TestCase):
    def vocabulary(self, directory: str) -> Path:
        path = Path(directory) / "vocabulary.json"
        path.write_text(
            json.dumps(
                {
                    "core": ["the"],
                    "terms": [
                        {
                            "word": "ox",
                            "concept": "animal",
                            "level": 1,
                            "pos": "noun",
                            "forms": ["oxes"],
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        return path

    def test_apply_replaces_the_derived_plural(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            vocabulary = self.vocabulary(directory)
            registration = Path(directory) / "registration.json"
            registration.write_text(
                json.dumps({"ox": {"pos": "noun", "inflection": {"plural": "oxen"}}}),
                encoding="utf-8",
            )
            status = main(
                [
                    "register_forms.py",
                    "apply",
                    str(registration),
                    "--vocabulary",
                    str(vocabulary),
                ]
            )
            self.assertEqual(status, 0)
            stored = json.loads(vocabulary.read_text(encoding="utf-8"))
            term = stored["terms"][0]
            self.assertEqual(term["forms"], ["oxen"])
            self.assertEqual(term["inflection"], {"plural": "oxen"})

    def test_apply_refuses_a_word_that_is_not_there(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            vocabulary = self.vocabulary(directory)
            before = vocabulary.read_text(encoding="utf-8")
            registration = Path(directory) / "registration.json"
            registration.write_text(
                json.dumps({"zebra": {"pos": "noun"}}),
                encoding="utf-8",
            )
            status = main(
                [
                    "register_forms.py",
                    "apply",
                    str(registration),
                    "--vocabulary",
                    str(vocabulary),
                ]
            )
            self.assertEqual(status, 1)
            self.assertEqual(vocabulary.read_text(encoding="utf-8"), before)

    def test_show_names_an_undeclared_word(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            vocabulary = self.vocabulary(directory)
            status = main(
                [
                    "register_forms.py",
                    "show",
                    "ox",
                    "--vocabulary",
                    str(vocabulary),
                ]
            )
            self.assertEqual(status, 0)


class TestLevelSeed(unittest.TestCase):
    def test_a_missing_level_receives_a_dictionary(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "level_3" / "bk.dictionary.seed.md"
            created = write_seed_if_missing(path, 3, "glacier")
            self.assertTrue(created)
            book, records = parse_book(path.read_text(encoding="utf-8"), path.name)
            self.assertEqual(book.level, 3)
            self.assertEqual(book.subject, "glacier")
            self.assertEqual(book.licence, "CC0-1.0")
            self.assertEqual(records, [])
            self.assertFalse(write_seed_if_missing(path, 3, "other"))
            self.assertIn("level three", new_seed_text(3, "glacier"))

    def test_a_level_outside_the_ladder_is_refused(self) -> None:
        with self.assertRaises(ValueError):
            new_seed_text(8, "glacier")
