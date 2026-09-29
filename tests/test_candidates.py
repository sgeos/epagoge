"""Candidate accounting must survive rejected replies and absent teacher output."""

import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "generators"))
import define_candidates as generator  # noqa: E402
from epagoge.vocabulary import Term, Vocabulary  # noqa: E402


class TestSenseSpecifications(unittest.TestCase):
    def test_invalid_specs_fail_before_teacher_access(self) -> None:
        values: list[object] = [
            [],
            {},
            {"other": {"sense": "A plant", "pos": "noun"}},
            {"zibble": "plant"},
            {"zibble": {"sense": "A plant"}},
            *[
                {"zibble": {"sense": sense, "pos": "noun"}}
                for sense in (None, "", " ", "x" * 241, " " * 240 + "x")
            ],
            *[
                {"zibble": {"sense": "A plant", "pos": pos}}
                for pos in (None, "", "noun noun", "unknown", "mass", "periphrastic")
            ],
            {"zibble": {"sense": "A plant", "pos": "noun", "extra": True}},
        ]
        bodies = [json.dumps(value) for value in values] + [
            '{"zibble":{"sense":"one","sense":"two","pos":"noun"}}',
            '{"zibble":{"sense":"one","pos":"noun"},"zibble":{}}',
            '{"zibble":',
        ]
        for body in bodies:
            with self.subTest(body=body), tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp)
                (path / "candidates.json").write_text('{"zibble":"plant"}')
                (path / "senses.json").write_text(body)
                with (
                    patch.object(generator, "ask") as ask,
                    contextlib.redirect_stderr(io.StringIO()),
                    self.assertRaises(SystemExit),
                ):
                    generator.main(
                        [
                            "define",
                            str(path / "candidates.json"),
                            "--senses",
                            str(path / "senses.json"),
                            "--source",
                            "manual",
                            "--out",
                            str(path / "out.json"),
                            "--report",
                            str(path / "report.json"),
                        ]
                    )
                ask.assert_not_called()
                self.assertFalse((path / "out.json").exists())

    def test_specs_reach_prompt_report_and_proposal(self) -> None:
        specs = {
            "zibble": {"sense": "Material sense only", "pos": "noun mass"},
            "zorple": {"sense": "Physical quality only", "pos": "adjective"},
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            (path / "candidates.json").write_text(
                '{"zibble":"material","zorple":"physical_property"}'
            )
            senses = path / "senses.json"
            senses.write_text(json.dumps(specs))
            with (
                patch.object(
                    generator,
                    "ask",
                    return_value=(
                        "zibble: A thing you can hold.\nzorple: A very small thing."
                    ),
                ) as ask,
                contextlib.redirect_stdout(io.StringIO()),
                contextlib.redirect_stderr(io.StringIO()),
            ):
                generator.main(
                    [
                        "define",
                        str(path / "candidates.json"),
                        "--senses",
                        str(senses),
                        "--source",
                        "manual",
                        "--out",
                        str(path / "out.json"),
                        "--report",
                        str(path / "report.json"),
                    ]
                )
            report = json.loads((path / "report.json").read_text())
            self.assertEqual(report["sense_specifications"], specs)
            self.assertEqual(report["sense_input_hash"], generator.file_digest(senses))
            for word, spec in specs.items():
                self.assertIn(spec["sense"], ask.call_args.args[0])
                self.assertEqual(report["accepted"][word]["pos"], spec["pos"])


class TestDefiningSelection(unittest.TestCase):
    def test_selection_retains_seed_and_displaces_ranked_words(self) -> None:
        vocabulary = Vocabulary(
            core=frozenset({"a"}),
            exempt=frozenset({"the"}),
            ostensive=frozenset({"eye"}),
            terms=(Term("apple", "plant", 1), Term("fruit", "plant", 2)),
        )
        with (
            tempfile.TemporaryDirectory() as tmp,
            patch.object(generator, "DEFINING_WORDS", 4),
        ):
            corpus = Path(tmp)
            (corpus / "book.md").write_text("apple apple apple")
            self.assertEqual(
                generator.defining_vocabulary(vocabulary, 2, corpus),
                ["a", "apple", "eye", "the"],
            )
            self.assertEqual(
                generator.defining_vocabulary(vocabulary, 2, corpus, ["fruit"]),
                ["a", "eye", "fruit", "the"],
            )
            self.assertEqual(
                generator.defining_vocabulary(vocabulary, 2, corpus, ["a"]),
                ["a", "apple", "eye", "the"],
            )
            with self.assertRaisesRegex(ValueError, "exceed"):
                generator.defining_vocabulary(vocabulary, 2, corpus, ["apple", "fruit"])

    def test_invalid_selections_never_contact_teacher(self) -> None:
        for words in (
            ["not-a-word"],
            ["'"],
            ["Fruit"],
            ["fruit", "fruit"],
            ["zqxv"],
            ["fruit"],
        ):
            with self.subTest(words=words), tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp)
                candidate = path / "input.json"
                candidate.write_text('{"zibble":"plant"}')
                with (
                    patch.object(generator, "ask") as ask,
                    contextlib.redirect_stderr(io.StringIO()),
                    self.assertRaises(SystemExit),
                ):
                    generator.main(
                        [
                            "define",
                            str(candidate),
                            "--level",
                            "1",
                            "--source",
                            "manual",
                            "--out",
                            str(path / "out.json"),
                            "--report",
                            str(path / "report.json"),
                            *[
                                arg
                                for word in words
                                for arg in ("--defining-word", word)
                            ],
                        ]
                    )
                ask.assert_not_called()
                self.assertFalse((path / "out.json").exists())

    def test_excessive_selection_never_contacts_teacher(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            candidate = path / "input.json"
            candidate.write_text('{"zibble":"plant"}')
            with (
                patch.object(generator, "DEFINING_WORDS", 1),
                patch.object(generator, "ask") as ask,
                contextlib.redirect_stderr(io.StringIO()),
                self.assertRaises(SystemExit),
            ):
                generator.main(
                    [
                        "define",
                        str(candidate),
                        "--source",
                        "manual",
                        "--defining-word",
                        "fruit",
                        "--out",
                        str(path / "out.json"),
                        "--report",
                        str(path / "report.json"),
                    ]
                )
            ask.assert_not_called()
            self.assertFalse((path / "out.json").exists())

    def test_selection_is_recorded_and_does_not_relax_reply_validation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            candidate = path / "input.json"
            candidate.write_text('{"zibble":"plant"}')
            with (
                patch.object(
                    generator, "ask", return_value="zibble: A zqxv fruit."
                ) as ask,
                contextlib.redirect_stdout(io.StringIO()),
                contextlib.redirect_stderr(io.StringIO()),
            ):
                generator.main(
                    [
                        "define",
                        str(candidate),
                        "--source",
                        "manual",
                        "--attempts",
                        "1",
                        "--defining-word",
                        "fruit",
                        "--out",
                        str(path / "out.json"),
                        "--report",
                        str(path / "report.json"),
                    ]
                )
            data = json.loads((path / "report.json").read_text())
            self.assertEqual(data["selected_defining_words"], ["fruit"])
            self.assertIn("fruit", data["defining_vocabulary"])
            self.assertLessEqual(len(data["defining_vocabulary"]), 700)
            self.assertIn(" ".join(data["defining_vocabulary"]), ask.call_args.args[0])
            self.assertEqual(data["accepted"], {})
            self.assertEqual(data["requests"][0]["outcomes"][0]["tokens"], ["zqxv"])


class TestCandidates(unittest.TestCase):
    def test_invalid_input_never_contacts_teacher(self) -> None:
        inputs = [
            "[]",
            "{}",
            '{"bad word":"plant"}',
            '{"zibble":"unknown"}',
            '{"zibble":1}',
            '{"zibble":"plant","zibble":"plant"}',
        ]
        for body in inputs:
            with self.subTest(body=body), tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp)
                candidate = path / "input.json"
                candidate.write_text(body)
                with (
                    patch.object(generator, "ask") as ask,
                    contextlib.redirect_stderr(io.StringIO()),
                    self.assertRaises(SystemExit),
                ):
                    generator.main(
                        [
                            "define",
                            str(candidate),
                            "--source",
                            "manual",
                            "--out",
                            str(path / "out.json"),
                            "--report",
                            str(path / "report.json"),
                        ]
                    )
                ask.assert_not_called()
                self.assertFalse((path / "out.json").exists())

    def test_source_and_output_guards_precede_teacher(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            candidate = path / "input.json"
            candidate.write_text('{"zibble":"plant"}')
            out = path / "out.json"
            report = path / "report.json"
            for source, target, occupied in [
                (" ", report, False),
                ("manual", out, False),
                ("manual", report, True),
            ]:
                if occupied:
                    out.write_text("preserve")
                with (
                    patch.object(generator, "ask") as ask,
                    contextlib.redirect_stderr(io.StringIO()),
                    self.assertRaises(SystemExit),
                ):
                    generator.main(
                        [
                            "define",
                            str(candidate),
                            "--source",
                            source,
                            "--out",
                            str(out),
                            "--report",
                            str(target),
                        ]
                    )
                ask.assert_not_called()
            self.assertEqual(out.read_text(), "preserve")

    def test_all_candidates_and_replies_are_accounted_for(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            candidate = path / "input.json"
            candidate.write_text('{"zibble":"plant","zorple":"plant","zapple":"plant"}')
            reply = (
                "zibble: A thing you can hold.\nzorple: .\n"
                "zapple: A zqxv you can hold.\nnot an entry"
            )
            out = path / "out.json"
            report = path / "report.json"
            with (
                patch.object(generator, "ask", return_value=reply),
                contextlib.redirect_stdout(io.StringIO()),
                contextlib.redirect_stderr(io.StringIO()),
            ):
                self.assertEqual(
                    generator.main(
                        [
                            "define",
                            str(candidate),
                            "--attempts",
                            "1",
                            "--source",
                            "manual",
                            "--out",
                            str(out),
                            "--report",
                            str(report),
                        ]
                    ),
                    0,
                )
            data = json.loads(report.read_text())
            self.assertEqual(data["requests"][0]["response"], reply)
            self.assertEqual(
                data["counts"],
                {
                    "input": 3,
                    "already_admitted": 0,
                    "offered": 3,
                    "mechanically_accepted": 1,
                    "deferred": 2,
                },
            )
            self.assertEqual(set(data["outcomes"]), {"zibble", "zorple", "zapple"})
            self.assertEqual(data["accepted"], json.loads(out.read_text()))
            self.assertEqual(data["sense_specifications"], {})
            self.assertIsNone(data["sense_input_hash"])
            self.assertEqual(data["accepted"]["zibble"]["pos"], "noun")

    def test_teacher_failure_is_recorded_as_deferred(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp)
            candidate = path / "input.json"
            candidate.write_text('{"zibble":"plant"}')
            with (
                patch.object(generator, "ask", side_effect=RuntimeError("unavailable")),
                contextlib.redirect_stdout(io.StringIO()),
                contextlib.redirect_stderr(io.StringIO()),
            ):
                generator.main(
                    [
                        "define",
                        str(candidate),
                        "--attempts",
                        "1",
                        "--source",
                        "manual",
                        "--out",
                        str(path / "out.json"),
                        "--report",
                        str(path / "report.json"),
                    ]
                )
            data = json.loads((path / "report.json").read_text())
            self.assertEqual(data["counts"]["deferred"], 1)
            self.assertEqual(data["requests"][0]["error"], "unavailable")
            self.assertEqual(data["outcomes"]["zibble"], "deferred")


class TestIncrementMeasurement(unittest.TestCase):
    def test_forged_generator_count_is_rejected(self) -> None:
        sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
        from tools.measure_lexicon_increment import measure

        root = Path(__file__).resolve().parents[1] / "evals/review/level_2_increment"
        with tempfile.TemporaryDirectory() as tmp:
            batch = Path(tmp)
            for source in root.glob("*.json"):
                (batch / source.name).write_bytes(source.read_bytes())
            path = batch / "generation.json"
            report = json.loads(path.read_text())
            report["counts"]["mechanically_accepted"] = 24
            path.write_text(json.dumps(report))
            with self.assertRaisesRegex(ValueError, "counts differ"):
                measure(batch)
