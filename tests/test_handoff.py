"""Regression tests for the handoff failures and restart boundaries."""

from __future__ import annotations

import contextlib
import io
import json
import subprocess
import sys
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch

from epagoge import schedule
from epagoge.artifacts import (
    atomic_output,
    check_outputs,
    digest,
    input_manifest,
    write_json,
)
from epagoge.book import load_book_dir
from epagoge.concept_graph import ConceptGraph
from epagoge.ordering import book_order

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools import (  # noqa: E402
    admit,
    build_corpus,
    sample_level,
    train_level,
    word_provenance,
)


class TestOrdering(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = ROOT / "curriculum/books/level_1"
        self.graph = ConceptGraph.load(ROOT / "curriculum/graph/concepts.json")
        self.plan = schedule.load(ROOT / "curriculum/schedule/level_01.json")

    def test_builder_and_trainer_cover_identical_books_in_identical_order(self) -> None:
        for arm in ("curriculum", "topological"):
            with self.subTest(arm=arm), tempfile.TemporaryDirectory() as tmp:
                out = Path(tmp) / "corpus.jsonl"
                with contextlib.redirect_stdout(io.StringIO()):
                    status = build_corpus.main(
                        [
                            "build",
                            str(self.directory),
                            str(out),
                            "--order",
                            arm,
                            "--seed",
                            "7",
                            "--no-dictionary",
                            "--no-thesaurus",
                        ]
                    )
                self.assertEqual(status, 0)
                exported = [
                    json.loads(line)["id"] for line in out.read_text().splitlines()
                ]
                trained, _, _ = train_level.book_order(1, self.graph, 7, arm, self.plan)
                books, _ = load_book_dir(self.directory)
                self.assertEqual(exported, trained)
                self.assertEqual(set(exported), {b.id for b in books})
                self.assertEqual(len(exported), len(books))

    def test_null_is_reproducible_and_distinct_from_control(self) -> None:
        control, text, _ = book_order(
            self.directory, self.graph, 1, "topological", self.plan
        )
        null, _, _ = book_order(self.directory, self.graph, 1, "null", self.plan)
        again, _, _ = book_order(self.directory, self.graph, 1, "null", self.plan)
        self.assertEqual(null, again)
        self.assertNotEqual(null, control)
        self.assertEqual(set(null), set(text))

    def test_length_and_shuffle_are_complete_permutations(self) -> None:
        for arm in ("length", "shuffled"):
            names, text, _ = book_order(self.directory, self.graph, 2, arm, self.plan)
            self.assertEqual(len(names), len(text))
            self.assertEqual(set(names), set(text))

    def test_invalid_arm_missing_unit_and_cycle_fail(self) -> None:
        with self.assertRaises(ValueError):
            book_order(self.directory, self.graph, 0, "typo", self.plan)
        with (
            patch("epagoge.ordering.linear_extension", return_value=[]),
            self.assertRaises(ValueError),
        ):
            book_order(self.directory, self.graph, 0, "curriculum", self.plan)
        with self.assertRaises(ValueError):
            book_order(
                self.directory,
                self.graph,
                0,
                "curriculum",
                replace(self.plan, domains=()),
            )

    def test_cli_rejects_unknown_arm_and_confirmatory_run(self) -> None:
        for flags in (["--arms", "typo"], ["--purpose", "confirmatory"]):
            with (
                self.subTest(flags=flags),
                contextlib.redirect_stderr(io.StringIO()),
                self.assertRaises(SystemExit) as raised,
            ):
                train_level.main(["train", "--out", "unused-result.json", *flags])
            self.assertEqual(raised.exception.code, 2)


class TestArtifacts(unittest.TestCase):
    def test_exclusive_atomic_writes_and_explicit_replacement(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "artifact.json"
            write_json(path, {"old": True})
            with self.assertRaises(FileExistsError):
                write_json(path, {"new": True})
            self.assertEqual(json.loads(path.read_text()), {"old": True})
            with (
                self.assertRaises(ValueError),
                atomic_output(path, overwrite=True) as handle,
            ):
                handle.write(b"partial")
                raise ValueError("interrupted")
            self.assertEqual(json.loads(path.read_text()), {"old": True})
            write_json(path, {"new": True}, overwrite=True)
            self.assertEqual(json.loads(path.read_text()), {"new": True})
            self.assertEqual(list(Path(tmp).iterdir()), [path])
            with self.assertRaises(ValueError):
                check_outputs([path, path], overwrite=True)
            with self.assertRaises(FileExistsError):
                check_outputs([path])
            link = Path(tmp) / "link"
            link.symlink_to(path)
            with self.assertRaises(FileExistsError):
                check_outputs([link], overwrite=True)
            with (
                self.assertRaises(FileExistsError),
                atomic_output(link, overwrite=True),
            ):
                pass

    def test_manifest_tracks_inputs_and_digest_is_order_independent(self) -> None:
        manifest = input_manifest(ROOT, 1)
        self.assertIn("curriculum/graph/concepts.json", manifest["inputs"])
        self.assertEqual(digest({"a": 1, "b": 2}), digest({"b": 2, "a": 1}))
        self.assertNotEqual(digest([1, 2]), digest([2, 1]))

    def test_sampling_refuses_existing_weights_before_training(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            weights = Path(tmp) / "reference.pt"
            weights.write_bytes(b"reference")
            with (
                contextlib.redirect_stderr(io.StringIO()),
                self.assertRaises(SystemExit),
            ):
                sample_level.main(
                    [
                        "sample",
                        "--weights",
                        str(weights),
                        "--out",
                        str(Path(tmp) / "result.json"),
                    ]
                )
            self.assertEqual(weights.read_bytes(), b"reference")


class TestProvenance(unittest.TestCase):
    def test_admission_refuses_missing_source_before_writing(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "curriculum/graph").mkdir(parents=True)
            vocab = root / "curriculum/vocabulary.json"
            vocab.write_text('{"terms": [], "core": []}')
            (root / "curriculum/graph/concepts.json").write_text(
                '{"nodes": [{"id": "thing"}]}'
            )
            candidate = root / "candidate.json"
            candidate.write_text(
                '{"new": {"concept": "thing", "definition": "a thing"}}'
            )
            before = vocab.read_bytes()
            with (
                patch.object(admit, "ROOT", root),
                contextlib.redirect_stderr(io.StringIO()),
            ):
                self.assertEqual(admit.main(["admit", str(candidate)]), 1)
            self.assertEqual(vocab.read_bytes(), before)

    def test_admission_is_valid_before_and_after_commit_and_fields_are_checked(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "curriculum").mkdir()
            vocab = root / "curriculum/vocabulary.json"
            record = root / "curriculum/provenance.json"
            vocab.write_text(json.dumps({"terms": [{"word": "old"}]}))
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

            git("init")
            git("add", ".")
            git("commit", "-m", "Initial lexicon")
            with (
                patch.object(word_provenance, "ROOT", root),
                contextlib.redirect_stdout(io.StringIO()),
                contextlib.redirect_stderr(io.StringIO()),
            ):
                self.assertEqual(
                    word_provenance.main(["provenance", "--out", str(record)]), 0
                )
                vocab.write_text(
                    json.dumps(
                        {
                            "terms": [
                                {"word": "old"},
                                {"word": "new", "source": "manual review"},
                            ]
                        }
                    )
                )
                self.assertEqual(word_provenance.main(["provenance", "--check"]), 1)
                self.assertEqual(
                    word_provenance.main(["provenance", "--out", str(record)]), 0
                )
                self.assertEqual(word_provenance.main(["provenance", "--check"]), 0)
                git("add", ".")
                git("commit", "-m", "Admit new with evidence")
                self.assertEqual(word_provenance.main(["provenance", "--check"]), 0)
                payload = json.loads(record.read_text())
                payload["words"]["old"]["date"] = "1900-01-01"
                record.write_text(json.dumps(payload))
                self.assertEqual(word_provenance.main(["provenance", "--check"]), 1)
                vocab.write_text(json.dumps({"terms": [{"word": "unsourced"}]}))
                self.assertEqual(
                    word_provenance.main(["provenance", "--out", str(record)]), 1
                )


class TestRestart(unittest.TestCase):
    def test_resume_matches_uninterrupted_cpu_training(self) -> None:
        import torch

        from epagoge.pilot import (
            ModelConfig,
            RunProgress,
            TrainConfig,
            train_diagnostic,
        )

        chunks = [[1, 2, 3, 4, 5], [5, 4, 3, 2, 1], [2, 3, 4, 5, 6]]
        model = ModelConfig(vocab_size=8, d_model=8, n_layers=1, seq_len=4, dropout=0.1)
        for optimiser in ("adamw", "muon"):
            with (
                self.subTest(optimiser=optimiser),
                tempfile.TemporaryDirectory() as tmp,
            ):
                config = TrainConfig(
                    steps=4, batch_size=1, optimiser=optimiser, token_replacement=0.2
                )
                full = train_diagnostic(
                    chunks, [0, 1], [chunks[2]], model, config, 4, torch.device("cpu")
                )
                path = Path(tmp) / "restart.pt"
                train_diagnostic(
                    chunks,
                    [0, 1],
                    [chunks[2]],
                    model,
                    config,
                    4,
                    torch.device("cpu"),
                    progress=RunProgress(path, every=1, stop_after=2),
                )
                resumed = train_diagnostic(
                    chunks,
                    [0, 1],
                    [chunks[2]],
                    model,
                    config,
                    4,
                    torch.device("cpu"),
                    progress=RunProgress(path, resume=path),
                )
                for name, value in full.model.state_dict().items():
                    self.assertTrue(
                        torch.equal(value, resumed.model.state_dict()[name]), name
                    )
                self.assertEqual(full.held_out_loss, resumed.held_out_loss)
                with self.assertRaises(ValueError):
                    train_diagnostic(
                        chunks,
                        [1, 0],
                        [chunks[2]],
                        model,
                        config,
                        4,
                        torch.device("cpu"),
                        progress=RunProgress(path, resume=path),
                    )
                with self.assertRaises(FileExistsError):
                    train_diagnostic(
                        chunks,
                        [0, 1],
                        [chunks[2]],
                        model,
                        config,
                        4,
                        torch.device("cpu"),
                        progress=RunProgress(path),
                    )
