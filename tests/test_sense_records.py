"""A second sense keeps its own provenance and its own closure check.

Added 2026-10-30 on operator direction, after review of the stripped-forms
batch found two places that still keyed a sense by its word alone. The
provenance generator let a second sense's source replace the origin of its
word's first sense, and the closure gate read one definition per word, so a
second sense at the level of its word's first record was never checked.
"""

from __future__ import annotations

import contextlib
import io
import json
import os
import subprocess
import tempfile
import unittest
from collections.abc import Mapping
from pathlib import Path
from typing import cast
from unittest.mock import patch

from tools import validate_closure, word_provenance
from tools.word_provenance import second_senses, sense_records

from epagoge.book import dictionary_entries, parse_book, ungrounded_tokens

ROOT = Path(__file__).resolve().parent.parent


def write_batch(root: Path, name: str, admitted: Mapping[str, object]) -> None:
    batch = root / "evals/review" / name
    batch.mkdir(parents=True)
    (batch / "admitted.json").write_text(json.dumps(admitted), encoding="utf-8")


class TestSecondSenses(unittest.TestCase):
    def test_only_flagged_rows_are_second_senses(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_batch(
                root,
                "b1",
                {
                    "well": {"concept": "liquid", "second_sense": True},
                    "mining": {"concept": "raw_and_made"},
                    "soap": {"concept": "liquid", "second_sense": False},
                },
            )
            self.assertEqual(
                second_senses(root), {("well", "liquid"): "evals/review/b1"}
            )

    def test_no_batches_is_no_second_senses(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(second_senses(Path(tmp)), {})

    def test_a_flag_that_is_not_a_bool_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_batch(root, "b1", {"well": {"concept": "liquid", "second_sense": 1}})
            with self.assertRaisesRegex(ValueError, "true or false"):
                second_senses(root)

    def test_a_second_sense_without_a_concept_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_batch(root, "b1", {"well": {"second_sense": True}})
            with self.assertRaisesRegex(ValueError, "names no concept"):
                second_senses(root)

    def test_one_sense_claimed_by_two_batches_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            row = {"well": {"concept": "liquid", "second_sense": True}}
            write_batch(root, "b1", row)
            write_batch(root, "b2", row)
            with self.assertRaisesRegex(ValueError, "already a second sense"):
                second_senses(root)

    def test_a_record_that_is_not_an_object_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_batch(root, "b1", {"well": "liquid"})
            with self.assertRaisesRegex(ValueError, "not an object"):
                second_senses(root)


class TestSenseRecords(unittest.TestCase):
    SECONDS = {("well", "liquid"): "evals/review/b1"}  # noqa: RUF012

    def test_a_second_sense_gets_its_own_record(self) -> None:
        terms: list[dict[str, object]] = [
            {"word": "well", "concept": "good_and_bad"},
            {"word": "well", "concept": "liquid", "source": "scan"},
        ]
        self.assertEqual(
            sense_records(terms, self.SECONDS, {}),
            {
                "well.liquid": {
                    "source": "scan",
                    "evidence": "recorded at admission",
                    "batch": "evals/review/b1",
                }
            },
        )

    def test_a_second_sense_without_a_source_is_refused(self) -> None:
        terms: list[dict[str, object]] = [{"word": "well", "concept": "liquid"}]
        with self.assertRaisesRegex(ValueError, "needs a source"):
            sense_records(terms, self.SECONDS, {})

    def test_a_retired_second_sense_keeps_its_held_record(self) -> None:
        held: dict[str, object] = {
            "well.liquid": {"source": "scan", "evidence": "recorded at admission"}
        }
        self.assertEqual(sense_records([], self.SECONDS, held), held)

    def test_a_second_sense_in_no_term_and_no_record_is_refused(self) -> None:
        with self.assertRaisesRegex(ValueError, "no term and no record"):
            sense_records([], self.SECONDS, {})


class TestProvenanceKeepsTheFirstSense(unittest.TestCase):
    """End to end through git, in the manner of tests/test_handoff.py."""

    def test_a_second_sense_never_rewrites_its_words_record(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "tree"
            (root / "curriculum").mkdir(parents=True)
            history = {
                "GIT_DIR": str(Path(tmp) / "history"),
                "GIT_WORK_TREE": str(root),
            }
            vocab = root / "curriculum/vocabulary.json"
            record = root / "curriculum/provenance.json"
            first = {"word": "well", "concept": "good_and_bad"}
            vocab.write_text(json.dumps({"terms": [first]}))
            record.write_text("{}")

            def git(*args: str) -> None:
                subprocess.run(  # noqa: S603
                    [  # noqa: S607
                        "git",
                        "-c",
                        "user.name=Test",
                        "-c",
                        "user.email=test@example.invalid",
                        *args,
                    ],
                    cwd=root,
                    check=True,
                    capture_output=True,
                )

            def run(*args: str) -> int:
                return word_provenance.main(["provenance", *args])

            with (
                patch.dict(os.environ, history),
                patch.object(word_provenance, "ROOT", root),
                contextlib.redirect_stdout(io.StringIO()),
                contextlib.redirect_stderr(io.StringIO()),
            ):
                git("init")
                git("add", ".")
                git("commit", "-m", "Initial lexicon")
                self.assertEqual(run("--out", str(record)), 0)
                before = json.loads(record.read_text())["words"]["well"]
                self.assertEqual(before["evidence"], "reconstructed from history")

                second = {"word": "well", "concept": "liquid", "source": "scan"}
                vocab.write_text(json.dumps({"terms": [first, second]}))
                write_batch(
                    root,
                    "b1",
                    {"well": {"concept": "liquid", "second_sense": True}},
                )
                self.assertEqual(run("--check"), 1)
                self.assertEqual(run("--out", str(record)), 0)
                self.assertEqual(run("--check"), 0)
                payload = json.loads(record.read_text())
                self.assertEqual(payload["words"]["well"], before)
                self.assertEqual(payload["senses"]["well.liquid"]["source"], "scan")

                # **The negative case.** Without the batch's flag the sense
                # is indistinguishable from a first sense, its source
                # reaches the word's record, and the check notices.
                (root / "evals/review/b1/admitted.json").write_text(
                    json.dumps({"well": {"concept": "liquid"}})
                )
                self.assertEqual(run("--check"), 1)

                # A held sense record that drifts is caught.
                write_batch(
                    root,
                    "b2",
                    {"well": {"concept": "liquid", "second_sense": True}},
                )
                payload["senses"]["well.liquid"]["source"] = "edited"
                record.write_text(json.dumps(payload))
                self.assertEqual(run("--check"), 1)


def seed_book(second: str) -> str:
    """A level-two dictionary book with two records defining one word."""

    def record(concept: str) -> dict[str, object]:
        return {
            "concepts": [concept],
            "claim_class": "formal",
            "defines": {"kind": "word", "target": "experience"},
        }

    head = {
        "id": "bk.dictionary.seed",
        "level": 2,
        "title": "Test words",
        "subject": {"kind": "word", "target": "experience"},
        "records": {
            "dict.2.experience": record("knowing"),
            "dict.2.experience.feeling": record("feeling"),
        },
    }
    return (
        f"---\n{json.dumps(head, indent=2)}\n---\n\n"
        "[dict.2.experience]\nExperience is what you come to know by doing.\n\n"
        f"[dict.2.experience.feeling]\n{second}\n"
    )


class TestDictionaryEntries(unittest.TestCase):
    def test_both_senses_of_one_word_are_listed(self) -> None:
        text = seed_book("To experience something is to feel it.")
        book, records = parse_book(text, "bk.dictionary.seed.md")
        entries = dictionary_entries(
            [book], [cast(dict[str, object], r) for r in records]
        )
        self.assertEqual(
            [(e.record, e.word) for e in entries],
            [
                ("dict.2.experience", "experience"),
                ("dict.2.experience.feeling", "experience"),
            ],
        )
        self.assertEqual(entries[1].text, "To experience something is to feel it.")

    def test_an_ordinary_book_is_not_the_dictionary(self) -> None:
        text = seed_book("x").replace("bk.dictionary.seed", "bk.p2.story")
        book, records = parse_book(text, "bk.p2.story.md")
        rows = [cast(dict[str, object], r) for r in records]
        self.assertEqual(dictionary_entries([book], rows), [])


class TestUngroundedTokens(unittest.TestCase):
    @staticmethod
    def resolve(token: str) -> str | None:
        return token.rstrip("s") or None

    def test_seed_grounded_and_self_ground(self) -> None:
        self.assertEqual(
            ungrounded_tokens(
                "cups hold milk wells",
                "well",
                grounded={"milk"},
                seed={"cup", "hold"},
                tokenise=str.split,
                resolve=self.resolve,
            ),
            [],
        )

    def test_a_token_outside_all_three_is_reported_by_headword(self) -> None:
        self.assertEqual(
            ungrounded_tokens(
                "cups hold rocks",
                "well",
                grounded=set(),
                seed={"cup", "hold"},
                tokenise=str.split,
                resolve=self.resolve,
            ),
            ["rock"],
        )


class TestClosureChecksEveryRecord(unittest.TestCase):
    """The gate's own entry point, against the real lexicon and level one."""

    def run_level_two(self, second: str) -> tuple[int, str]:
        with tempfile.TemporaryDirectory() as tmp:
            books = Path(tmp) / "books"
            (books / "level_2").mkdir(parents=True)
            (books / "level_1").symlink_to(ROOT / "curriculum/books/level_1")
            (books / "level_2/bk.dictionary.seed.md").write_text(
                seed_book(second), encoding="utf-8"
            )
            err = io.StringIO()
            with (
                contextlib.redirect_stdout(io.StringIO()),
                contextlib.redirect_stderr(err),
            ):
                code = validate_closure.main(
                    [
                        "validate_closure",
                        str(ROOT / "curriculum/vocabulary.json"),
                        str(books / "level_2"),
                        "2",
                    ]
                )
            return code, err.getvalue()

    def test_a_licensed_grounded_second_sense_passes(self) -> None:
        code, err = self.run_level_two(
            "To experience something is to feel it, or to have it happen to you."
        )
        self.assertEqual(code, 0, err)

    def test_an_unlicensed_second_sense_at_the_same_level_fails(self) -> None:
        # Before 2026-10-30 this passed, because the closure map held only
        # the word's first record at the level and never read this one.
        code, err = self.run_level_two("To experience something is to feel organics.")
        self.assertEqual(code, 1)
        self.assertIn("dict.2.experience.feeling: outside level 2: organics", err)

    def test_an_ungrounded_second_sense_fails(self) -> None:
        # `mining` is licensed at level two and has no definition in this
        # tree, so the record is inside the ceiling and still does not ground.
        code, err = self.run_level_two("To experience something is to feel mining.")
        self.assertEqual(code, 1)
        self.assertIn("dict.2.experience.feeling: ungrounded, needs mining", err)
        self.assertNotIn("outside level", err)


if __name__ == "__main__":
    unittest.main()
