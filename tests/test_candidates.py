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


class TestAgentAuthoredMeasurement(unittest.TestCase):
    """A batch with no teacher still states where its input came from."""

    def setUp(self) -> None:
        sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
        from tools import measure_lexicon_increment as tool

        self.tool = tool
        self._dir = tempfile.TemporaryDirectory()
        self.addCleanup(self._dir.cleanup)
        self.batch = Path(self._dir.name)
        self.candidates = {"orange": "physical_property"}
        (self.batch / "candidates.json").write_text(json.dumps(self.candidates))
        self.before: dict[str, object] = {"vocabulary_hash": "v" * 64}
        self.declaration: dict[str, object] = {
            "level": 2,
            "teacher": None,
            "candidates": self.candidates,
            "input_hash": tool.file_digest(self.batch / "candidates.json"),
            "vocabulary_hash": "v" * 64,
            "source": "scan overlap pool",
            "pool_report_hash": "p" * 64,
            "reason": "host memory",
        }

    def account(self) -> tuple[int, dict[str, object], tuple[str, ...]]:
        (self.batch / "authoring.json").write_text(json.dumps(self.declaration))
        return self.tool._agent_accounting(  # noqa: SLF001
            self.batch, self.before, dict(self.candidates)
        )

    def test_a_consistent_declaration_is_accounted(self) -> None:
        level, extra, names = self.account()
        self.assertEqual(level, 2)
        self.assertIsNone(extra["teacher"])
        self.assertIn("authoring.json", names)
        self.assertNotIn("generation.json", names)

    def test_a_named_teacher_is_refused(self) -> None:
        self.declaration["teacher"] = "some-model"
        with self.assertRaisesRegex(ValueError, "no teacher ran"):
            self.account()

    def test_a_changed_candidate_file_is_refused(self) -> None:
        self.declaration["input_hash"] = "0" * 64
        with self.assertRaisesRegex(ValueError, "input hash"):
            self.account()

    def test_a_different_baseline_is_refused(self) -> None:
        self.declaration["vocabulary_hash"] = "w" * 64
        with self.assertRaisesRegex(ValueError, "baseline vocabulary"):
            self.account()

    def test_a_blank_pool_report_is_refused(self) -> None:
        self.declaration["pool_report_hash"] = "  "
        with self.assertRaisesRegex(ValueError, "pool_report_hash"):
            self.account()

    def test_a_teacher_report_beside_the_declaration_is_refused(self) -> None:
        (self.batch / "generated.json").write_text("{}")
        with self.assertRaisesRegex(ValueError, "both a teacher and no teacher"):
            self.account()

    def test_a_batch_with_neither_report_is_refused(self) -> None:
        for name in ("before.json", "review.json", "admitted.json"):
            (self.batch / name).write_text("{}")
        (self.batch / "review.json").write_text(json.dumps({"orange": {}}))
        with self.assertRaisesRegex(ValueError, "exactly one of"):
            self.tool.measure(self.batch)


class TestBlockingWords(unittest.TestCase):
    """The ranking is a record of evidence, so a bad report is refused."""

    def setUp(self) -> None:
        sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
        from tools import blocking_words as tool

        self.tool = tool
        self._dir = tempfile.TemporaryDirectory()
        self.addCleanup(self._dir.cleanup)
        self.vocabulary = Vocabulary(
            core=frozenset({"a", "is"}),
            terms=(Term("food", "food", 1), Term("cook", "food", 3)),
        )

    def report(self, name: str, outcomes: object) -> Path:
        path = Path(self._dir.name) / name
        path.write_text(json.dumps({"requests": [{"outcomes": outcomes}]}))
        return path

    def test_blockers_rank_by_rejections_and_name_what_they_blocked(self) -> None:
        first = self.report(
            "one.json",
            [
                {"word": "soup", "status": "outside_vocabulary", "tokens": ["boil"]},
                {"word": "jam", "status": "outside_vocabulary", "tokens": ["boil"]},
                {"word": "bun", "status": "mechanically_accepted"},
            ],
        )
        second = self.report(
            "two.json",
            [
                {
                    "word": "tea",
                    "status": "outside_vocabulary",
                    "tokens": ["boil", "leaf"],
                }
            ],
        )
        got = self.tool.rank([first, second], self.vocabulary, 2)
        self.assertEqual((got.reports, got.rejected_definitions), (2, 3))
        self.assertEqual(
            [(b.word, b.rejections, b.blocked) for b in got.blockers],
            [("boil", 3, ("jam", "soup", "tea")), ("leaf", 1, ("tea",))],
        )

    def test_a_token_repeated_in_one_reply_counts_once(self) -> None:
        path = self.report(
            "r.json",
            [
                {
                    "word": "tea",
                    "status": "outside_vocabulary",
                    "tokens": ["leaf", "leaf"],
                }
            ],
        )
        [blocker] = self.tool.rank([path], self.vocabulary, 2).blockers
        self.assertEqual(blocker.rejections, 1)

    def test_admitted_blockers_are_dropped_only_at_their_level(self) -> None:
        path = self.report(
            "r.json",
            [
                {
                    "word": "soup",
                    "status": "outside_vocabulary",
                    "tokens": ["cook", "food"],
                }
            ],
        )
        self.assertEqual(
            [b.word for b in self.tool.rank([path], self.vocabulary, 2).blockers],
            ["cook"],
        )
        self.assertEqual(self.tool.rank([path], self.vocabulary, 3).blockers, ())

    def test_a_rejection_without_tokens_is_refused(self) -> None:
        path = self.report("r.json", [{"word": "soup", "status": "outside_vocabulary"}])
        with self.assertRaisesRegex(ValueError, "names no tokens"):
            self.tool.rank([path], self.vocabulary, 2)

    def test_a_report_without_requests_is_refused(self) -> None:
        path = Path(self._dir.name) / "r.json"
        path.write_text(json.dumps({"outcomes": []}))
        with self.assertRaisesRegex(ValueError, "requests must be a list"):
            self.tool.rank([path], self.vocabulary, 2)

    def test_an_unreadable_report_is_refused(self) -> None:
        path = Path(self._dir.name) / "r.json"
        path.write_text("{not json")
        with self.assertRaisesRegex(ValueError, "unreadable"):
            self.tool.rank([path], self.vocabulary, 2)

    def test_a_level_below_one_is_refused(self) -> None:
        with self.assertRaisesRegex(ValueError, "at least 1"):
            self.tool.rank([], self.vocabulary, 0)


class TestCandidatePool(unittest.TestCase):
    """Each rule removes what it says, and the term list names nothing."""

    def setUp(self) -> None:
        sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
        from tools import candidate_pool as tool

        self.tool = tool
        self.vocabulary = Vocabulary(
            core=frozenset({"a"}), terms=(Term("food", "food", 1),)
        )
        self.frequent = {
            "food": ["x", "y"],
            "foods": ["x", "y"],
            "honey": ["x", "y"],
            "lemon": ["x"],
            "ox": ["x", "y"],
            "boston": ["x", "y"],
            "secretword": ["x", "y"],
            "decided": ["x", "y"],
        }
        self.shares = self.tool.capital_share(["Boston is far. Boston. honey honey"])

    def run_rules(
        self, pattern: object = None
    ) -> tuple[list[str], dict[str, list[str]], int]:
        return self.tool.select(
            self.frequent,
            self.vocabulary,
            2,
            self.shares,
            {"decided"},
            pattern,  # type: ignore[arg-type]
        )

    def test_each_rule_removes_its_words(self) -> None:
        pool, removed, withheld = self.run_rules()
        self.assertEqual(pool, ["honey", "secretword"])
        self.assertEqual(removed["admissible"], ["food", "foods"])
        self.assertEqual(removed["prior_decision"], ["decided"])
        self.assertEqual(removed["sources"], ["lemon"])
        self.assertEqual(removed["short"], ["ox"])
        self.assertEqual(removed["capitalised"], ["boston"])
        self.assertEqual(withheld, 0)

    def test_term_list_words_are_counted_and_never_named(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "terms.txt"
            path.write_text("# comment\nsecret\\w*\nlemon\n")
            pool, removed, withheld = self.run_rules(self.tool.term_pattern(path))
        self.assertEqual(withheld, 2)
        named = [w for words in removed.values() for w in words] + pool
        self.assertNotIn("secretword", named)
        self.assertNotIn("lemon", named)

    def test_a_plural_of_a_term_is_withheld(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "terms.txt"
            path.write_text("honey\n")
            pattern = self.tool.term_pattern(path)
        if pattern is None:
            self.fail("a nonempty term file must give a pattern")
        self.assertTrue(pattern.search("Honeys"))
        self.assertFalse(pattern.search("honeycomb"))

    def test_an_empty_term_file_applies_no_pattern(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "terms.txt"
            path.write_text("# only a comment\n")
            self.assertIsNone(self.tool.term_pattern(path))

    def test_invalid_parameters_are_refused(self) -> None:
        with self.assertRaisesRegex(ValueError, "positive"):
            self.tool.select({}, self.vocabulary, 2, {}, set(), None, min_sources=0)
        with self.assertRaisesRegex(ValueError, "share"):
            self.tool.select(
                {}, self.vocabulary, 2, {}, set(), None, max_capital_share=0
            )

    def test_missing_source_texts_are_refused(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            scan = Path(tmp) / "scan.json"
            scan.write_text(json.dumps({"sources": ["absent.txt"], "frequent": {}}))
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                status = self.tool.main(
                    [
                        "candidate_pool.py",
                        str(scan),
                        "--level",
                        "2",
                        "--out",
                        str(Path(tmp) / "o.json"),
                    ]
                )
            self.assertEqual(status, 1)
            self.assertIn("missing source texts", err.getvalue())
            self.assertFalse((Path(tmp) / "o.json").exists())


class TestEnvironmentCheck(unittest.TestCase):
    """The sandbox fallback must still catch what uv sync --locked catches."""

    PYPROJECT = (
        '[project]\nname = "demo"\ndependencies = []\n'
        '[project.optional-dependencies]\ntrain = ["numpy==2.0.0"]\n'
        '[dependency-groups]\ndev = ["ruff==0.1.0"]\n'
    )
    LOCK = (
        '[[package]]\nname = "demo"\nversion = "0.0.0"\n'
        "[package.metadata]\n"
        'requires-dist = [{ name = "numpy", specifier = "==2.0.0" }]\n'
        "[package.metadata.requires-dev]\n"
        'dev = [{ name = "ruff", specifier = "==0.1.0" }]\n'
        '[[package]]\nname = "numpy"\nversion = "2.0.0"\n'
        '[[package]]\nname = "ruff"\nversion = "0.1.0"\n'
    )

    def setUp(self) -> None:
        sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
        from tools import check_environment as tool

        self.tool = tool
        self.installed = {"demo": "0.0.0", "numpy": "2.0.0", "ruff": "0.1.0"}

    def test_a_matching_environment_passes(self) -> None:
        self.assertEqual(
            self.tool.problems(self.PYPROJECT, self.LOCK, self.installed), []
        )

    def test_a_stale_lock_is_reported(self) -> None:
        changed = self.PYPROJECT.replace("numpy==2.0.0", "numpy==2.1.0")
        found = self.tool.problems(
            changed, self.LOCK, {**self.installed, "numpy": "2.1.0"}
        )
        self.assertTrue(any("stale" in line for line in found))

    def test_a_version_drift_is_reported(self) -> None:
        found = self.tool.problems(
            self.PYPROJECT, self.LOCK, {**self.installed, "ruff": "0.2.0"}
        )
        self.assertIn("ruff is 0.2.0, uv.lock has 0.1.0", found)

    def test_an_unlocked_distribution_is_reported(self) -> None:
        found = self.tool.problems(
            self.PYPROJECT, self.LOCK, {**self.installed, "Extra_Pkg": "1"}
        )
        self.assertIn("Extra_Pkg 1 is installed and not in uv.lock", found)

    def test_a_missing_requirement_is_reported(self) -> None:
        installed = {k: v for k, v in self.installed.items() if k != "ruff"}
        found = self.tool.problems(self.PYPROJECT, self.LOCK, installed)
        self.assertIn("ruff==0.1.0 is required and None is installed", found)

    def test_an_unpinned_requirement_is_refused(self) -> None:
        loose = self.PYPROJECT.replace("ruff==0.1.0", "ruff>=0.1")
        with self.assertRaisesRegex(ValueError, "not an exact pin"):
            self.tool.problems(loose, self.LOCK, self.installed)
