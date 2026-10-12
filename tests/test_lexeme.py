"""Root counting keeps one citation form across its spellings."""

from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from tools.analyse_lexemes import main

from epagoge.lexeme import analyse, count_roots, scheduled_roots
from epagoge.vocabulary import Term, Vocabulary, load_vocabulary


def _term(
    word: str,
    pos: str,
    level: int = 1,
    concept: str = "thing",
    forms: tuple[str, ...] = (),
    inflection: tuple[tuple[str, str], ...] = (),
) -> Term:
    return Term(
        word,
        concept,
        level,
        forms,
        pos,
        "",
        inflection,
    )


class TestClassCounts(unittest.TestCase):
    def test_noun_forms_of_an_unknown_root_count_once(self) -> None:
        report = count_roots({"cut": 2, "cuts": 3}, Vocabulary(), pos="noun")
        self.assertEqual(report.unresolved, ())
        self.assertEqual(len(report.roots), 1)
        root = report.roots[0]
        self.assertEqual(root.root, "cut")
        self.assertEqual(root.total, 5)
        self.assertEqual(root.by_class, (("noun", 5),))

    def test_verb_inflections_of_an_unknown_root_count_once(self) -> None:
        report = count_roots(
            {"cut": 1, "cuts": 4, "cutting": 7}, Vocabulary(), pos="verb"
        )
        self.assertEqual(report.unresolved, ())
        self.assertEqual(report.roots[0].root, "cut")
        self.assertEqual(report.roots[0].total, 12)
        self.assertEqual(report.roots[0].by_class, (("verb", 12),))

    def test_across_classes_counts_each_spelling_once(self) -> None:
        report = count_roots(
            {"cut": 1, "cuts": 4, "cutting": 7},
            Vocabulary(),
            propose_classes=True,
        )
        self.assertEqual(report.unresolved, ())
        root = report.roots[0]
        self.assertEqual(root.total, 12)
        self.assertIn(("", 1), root.by_class)
        self.assertIn(("verb", 7), root.by_class)
        shared = {row.surface: row.classes for row in root.shared}
        self.assertEqual(shared["cuts"], ("noun", "verb"))

    def test_a_part_of_speech_filter_omits_other_classes(self) -> None:
        report = count_roots({"cutting": 3}, Vocabulary(), pos="noun")
        self.assertEqual(report.roots, ())
        self.assertEqual(report.omitted, (("cutting", 3),))

    def test_children_join_child(self) -> None:
        found = analyse("children", Vocabulary())
        self.assertTrue(
            any(
                row.root == "child" and row.pos == "noun" and row.slot == "plural"
                for row in found
            )
        )
        self.assertEqual({row.root for row in found}, {"child"})

    def test_axes_stay_unresolved(self) -> None:
        report = count_roots({"axes": 2}, Vocabulary())
        self.assertEqual(report.roots, ())
        self.assertEqual(len(report.unresolved), 1)
        roots = {row.root for row in report.unresolved[0].readings}
        self.assertIn("axis", roots)
        self.assertTrue("ax" in roots or "axe" in roots)

    def test_leaves_stay_unresolved(self) -> None:
        report = count_roots({"leaves": 1}, Vocabulary())
        roots = {row.root for row in report.unresolved[0].readings}
        self.assertIn("leaf", roots)
        self.assertIn("leave", roots)

    def test_an_admitted_base_beats_a_spurious_extension(self) -> None:
        vocabulary = Vocabulary(
            terms=(_term("walk", "verb"), _term("large", "adjective"))
        )
        walked = analyse("walked", vocabulary, pos="verb")
        self.assertEqual({row.root for row in walked}, {"walk"})
        larger = analyse("larger", vocabulary, pos="adjective")
        self.assertEqual({row.root for row in larger}, {"large"})

    def test_an_unadmitted_silent_e_pair_is_not_truncated(self) -> None:
        report = count_roots({"larger": 1}, Vocabulary(), pos="adjective")
        self.assertEqual(report.roots, ())
        roots = {row.root for row in report.unresolved[0].readings}
        self.assertIn("large", roots)
        self.assertIn("larg", roots)


class TestAdmittedParadigms(unittest.TestCase):
    def test_an_admitted_verb_owns_its_inflections(self) -> None:
        vocabulary = Vocabulary(
            terms=(_term("cut", "verb", forms=("cuts", "cutting")),)
        )
        cuts = analyse("cuts", vocabulary)
        self.assertTrue(any(row.root == "cut" and row.pos == "verb" for row in cuts))
        self.assertFalse(any(row.pos == "noun" for row in cuts))
        proposed = analyse("cuts", vocabulary, propose_classes=True)
        self.assertTrue(
            any(row.pos == "noun" and row.origin == "proposed" for row in proposed)
        )

    def test_a_mass_noun_does_not_absorb_a_plural(self) -> None:
        vocabulary = Vocabulary(terms=(_term("groundwater", "noun mass"),))
        found = analyse("groundwaters", vocabulary)
        self.assertFalse(any(row.root == "groundwater" for row in found))

    def test_a_plural_only_noun_has_no_singular(self) -> None:
        vocabulary = Vocabulary(terms=(_term("bacteria", "noun plural-only"),))
        found = analyse("bacteria", vocabulary, pos="noun")
        self.assertEqual(found[0].root, "bacteria")
        self.assertEqual(found[0].slot, "plural")
        singular = analyse("bacterium", vocabulary)
        self.assertFalse(any(row.root == "bacteria" for row in singular))

    def test_a_registered_plural_joins_its_noun(self) -> None:
        vocabulary = Vocabulary(
            terms=(
                _term(
                    "meniscus",
                    "noun",
                    inflection=(("plural", "menisci"),),
                ),
            )
        )
        found = analyse("menisci", vocabulary, pos="noun")
        self.assertEqual(found[0].root, "meniscus")
        self.assertEqual(found[0].origin, "registered")
        manufactured = analyse("meniscuses", vocabulary)
        self.assertFalse(any(row.root == "meniscus" for row in manufactured))

    def test_an_ly_adverb_joins_an_admitted_adjective(self) -> None:
        vocabulary = Vocabulary(terms=(_term("quick", "adjective"),))
        found = analyse("quickly", vocabulary, pos="adverb")
        self.assertEqual(len(found), 1)
        self.assertEqual(found[0].root, "quick")
        self.assertEqual(found[0].slot, "ly")
        untouched = analyse("family", vocabulary)
        self.assertFalse(any(row.root == "fami" for row in untouched))

    def test_an_admitted_headword_is_not_folded_into_another_root(self) -> None:
        vocabulary = Vocabulary(
            terms=(_term("see", "verb"), _term("saw", "noun", level=2, concept="tool"))
        )
        found = analyse("saw", vocabulary)
        self.assertEqual({row.root for row in found}, {"saw"})

    def test_schedule_keeps_classes_separate_until_asked(self) -> None:
        vocabulary = Vocabulary(
            terms=(
                _term("cut", "verb", level=1, concept="danger"),
                _term("cut", "noun", level=3, concept="shape", forms=("cuts",)),
            )
        )
        split = scheduled_roots(vocabulary)
        verbs = [row for row in split if row.placements[0].pos == "verb"]
        nouns = [row for row in split if row.placements[0].pos == "noun"]
        self.assertEqual(verbs[0].earliest, 1)
        self.assertEqual(nouns[0].earliest, 3)
        early = scheduled_roots(vocabulary, level=2)
        self.assertTrue(all(row.earliest <= 2 for row in early))
        self.assertFalse(any(row.placements[0].pos == "noun" for row in early))
        across = scheduled_roots(vocabulary, across_classes=True)
        self.assertEqual(len(across), 1)
        self.assertEqual(across[0].root, "cut")
        self.assertEqual(across[0].earliest, 1)
        self.assertEqual({item.pos for item in across[0].placements}, {"noun", "verb"})

    def test_closed_words_are_skipped_and_bad_counts_are_refused(self) -> None:
        vocabulary = Vocabulary(core=frozenset({"the"}))
        report = count_roots({"the": 4, "cat": 1}, vocabulary, pos="noun")
        self.assertEqual(report.skipped, (("the", 4),))
        self.assertEqual(report.roots[0].root, "cat")
        with self.assertRaisesRegex(ValueError, "negative"):
            count_roots({"cat": -1}, vocabulary)
        with self.assertRaisesRegex(ValueError, "pos"):
            analyse("cat", vocabulary, pos="particle")


class TestSpellingRules(unittest.TestCase):
    def test_regular_and_irregular_reversals_find_the_base(self) -> None:
        vocabulary = Vocabulary(terms=(_term("happy", "adjective"),))
        cases = {
            "cities": "city",
            "stopped": "stop",
            "tried": "try",
            "hoped": "hope",
            "lying": "lie",
            "hoping": "hope",
            "is": "be",
            "has": "have",
        }
        for surface, root in cases.items():
            found = analyse(surface, Vocabulary())
            self.assertIn(root, {row.root for row in found}, surface)
        happier = analyse("happier", vocabulary, pos="adjective")
        self.assertEqual({row.root for row in happier}, {"happy"})
        happily = analyse("happily", vocabulary, pos="adverb")
        self.assertEqual(happily[0].root, "happy")
        self.assertEqual(happily[0].slot, "ly")
        bigger = analyse("bigger", Vocabulary(), pos="adjective")
        self.assertFalse(any(row.root == "big" for row in bigger))
        biggest = analyse("biggest", Vocabulary(), pos="adjective")
        self.assertFalse(any(row.root == "big" for row in biggest))

    def test_zero_counts_empty_surfaces_and_a_bad_level_are_refused(self) -> None:
        report = count_roots({"cats": 0, "cat": 2}, Vocabulary(), pos="noun")
        self.assertEqual(report.roots[0].total, 2)
        with self.assertRaisesRegex(ValueError, "empty"):
            analyse("  ", Vocabulary())
        with self.assertRaisesRegex(ValueError, "level"):
            scheduled_roots(Vocabulary(), level=0)
        vocabulary = Vocabulary(
            terms=(
                _term("cut", "verb", level=1),
                _term("cut", "noun", level=4, concept="shape"),
            )
        )
        early = scheduled_roots(vocabulary, across_classes=True, level=2)
        self.assertEqual(len(early), 1)
        self.assertEqual({item.pos for item in early[0].placements}, {"verb"})
        both = Vocabulary(
            terms=(
                _term("quick", "adjective"),
                _term("quickly", "adverb", concept="manner"),
            )
        )
        found = analyse("quickly", both, propose_classes=True)
        self.assertEqual({row.root for row in found}, {"quickly"})


class TestRealLexicon(unittest.TestCase):
    def test_the_admitted_verb_cut_is_the_root_of_cutting(self) -> None:
        vocabulary = load_vocabulary(Path("curriculum/vocabulary.json"))
        found = analyse("cutting", vocabulary, pos="verb")
        self.assertTrue(any(row.root == "cut" and row.level == 1 for row in found))


class TestAnalyseLexemesCommand(unittest.TestCase):
    def vocabulary(self, directory: str) -> Path:
        path = Path(directory) / "vocabulary.json"
        path.write_text(
            json.dumps(
                {
                    "core": ["the"],
                    "terms": [
                        {
                            "word": "cut",
                            "concept": "danger",
                            "level": 1,
                            "pos": "verb",
                            "forms": ["cuts", "cutting"],
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        return path

    def test_counts_and_schedule_use_the_shipped_command(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            vocabulary = self.vocabulary(directory)
            counts = Path(directory) / "counts.json"
            counts.write_text(
                json.dumps({"cut": 1, "cuts": 2, "cutting": 3, "the": 9}),
                encoding="utf-8",
            )
            with redirect_stdout(io.StringIO()) as captured:
                status = main(
                    [
                        "analyse_lexemes.py",
                        "--vocabulary",
                        str(vocabulary),
                        "counts",
                        str(counts),
                        "--pos",
                        "verb",
                    ]
                )
            self.assertEqual(status, 0)
            payload = json.loads(captured.getvalue())
            self.assertEqual(
                payload["rows"],
                [
                    {
                        "root": "cut",
                        "pos": "verb",
                        "count": 6,
                        "level": 1,
                        "shared": False,
                    }
                ],
            )
            self.assertEqual(payload["skipped"], [{"surface": "the", "count": 9}])
            text = Path(directory) / "source.txt"
            text.write_text("The cut cuts cutting.\n", encoding="utf-8")
            with redirect_stdout(io.StringIO()) as captured:
                status = main(
                    [
                        "analyse_lexemes.py",
                        "--vocabulary",
                        str(vocabulary),
                        "text",
                        str(text),
                        "--across-classes",
                    ]
                )
            self.assertEqual(status, 0)
            grouped = json.loads(captured.getvalue())
            self.assertEqual(grouped["rows"][0]["root"], "cut")
            self.assertEqual(grouped["rows"][0]["count"], 3)
            with redirect_stdout(io.StringIO()) as captured:
                status = main(
                    [
                        "analyse_lexemes.py",
                        "--vocabulary",
                        str(vocabulary),
                        "schedule",
                        "--across-classes",
                        "--level",
                        "1",
                    ]
                )
            self.assertEqual(status, 0)
            scheduled = json.loads(captured.getvalue())
            self.assertEqual(scheduled["roots"][0]["root"], "cut")
            self.assertEqual(scheduled["roots"][0]["earliest"], 1)
            with redirect_stdout(io.StringIO()) as captured:
                status = main(
                    [
                        "analyse_lexemes.py",
                        "--vocabulary",
                        str(vocabulary),
                        "read",
                        "cuts",
                        "--propose-classes",
                    ]
                )
            self.assertEqual(status, 0)
            readings = json.loads(captured.getvalue())["readings"]
            classes = {row["pos"] for row in readings}
            self.assertIn("verb", classes)
            self.assertIn("noun", classes)

    def test_a_counts_file_that_is_not_an_object_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            vocabulary = self.vocabulary(directory)
            counts = Path(directory) / "counts.json"
            counts.write_text("[1]", encoding="utf-8")
            status = main(
                [
                    "analyse_lexemes.py",
                    "--vocabulary",
                    str(vocabulary),
                    "counts",
                    str(counts),
                ]
            )
            self.assertEqual(status, 2)


if __name__ == "__main__":
    unittest.main()
