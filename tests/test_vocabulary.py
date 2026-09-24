"""Tests for the per-level vocabulary.

Both rules get negative tests, because a vocabulary check that only ever
passes has not been shown to bite.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from epagoge.record import ClaimClass, Provenance, Record
from epagoge.vocabulary import (
    Term,
    Vocabulary,
    load_vocabulary,
    term_levels,
    tokenise,
    unlicensed,
    validate_vocabulary,
)

CONCEPTS = {"counting": 1, "wearing_out": 1, "derivative": 1}


def rec(record_id: str, level: int, concepts: tuple[str, ...], text: str) -> Record:
    return Record(
        record_id,
        level,
        concepts,
        ClaimClass.EMPIRICAL,
        text,
        Provenance(source_claim="s"),
    )


def codes(violations: list[object]) -> set[str]:
    return {v.code for v in violations}  # type: ignore[attr-defined]


def vocab(**kwargs: object) -> Vocabulary:
    defaults: dict[str, object] = {
        "core": frozenset({"the", "a", "you", "it", "is", "and", "when", "gets"}),
        "terms": (Term("count", "counting", 1, ("counts",)),),
        "general": {1: frozenset({"thing"}), 5: frozenset({"apparatus"})},
        "exempt": frozenset({"popper"}),
    }
    defaults.update(kwargs)
    return Vocabulary(**defaults)  # type: ignore[arg-type]


class TestTokenising(unittest.TestCase):
    def test_case_and_punctuation_are_stripped(self) -> None:
        self.assertEqual(tokenise("The Cat, it ran!"), ["the", "cat", "it", "ran"])

    def test_apostrophes_are_kept_inside_words(self) -> None:
        self.assertIn("popper's", tokenise("Popper's account"))

    def test_digits_are_not_words(self) -> None:
        self.assertEqual(tokenise("count 3 things"), ["count", "things"])


class TestLookup(unittest.TestCase):
    def test_a_direct_form_resolves(self) -> None:
        self.assertIsNotNone(vocab().lookup("count"))

    def test_a_declared_form_resolves(self) -> None:
        self.assertIsNotNone(vocab().lookup("counts"))

    def test_suffix_stripping_resolves_an_undeclared_form(self) -> None:
        self.assertIsNotNone(vocab().lookup("counting"))

    def test_an_unrelated_word_does_not_resolve(self) -> None:
        self.assertIsNone(vocab().lookup("elephant"))

    def test_numerals_are_free_at_any_level(self) -> None:
        self.assertTrue(vocab().is_free("42"))

    def test_exempt_words_are_free(self) -> None:
        self.assertTrue(vocab().is_free("popper"))


class TestDerivation(unittest.TestCase):
    def test_a_term_reports_its_authored_level(self) -> None:
        records = [rec("a", 3, ("counting",), "you count the thing")]
        self.assertEqual(term_levels(vocab(), records)["count"], 1)

    def test_a_word_may_not_precede_the_concept_it_names(self) -> None:
        """A concept may be taught before its name, never the reverse."""
        v = vocab(terms=(Term("count", "counting", 1),))
        records = [rec("a", 4, ("counting",), "you count the thing")]
        self.assertIn(
            "term-before-concept", codes(validate_vocabulary(v, records, CONCEPTS))
        )

    def test_a_term_whose_concept_is_never_taught_is_reported(self) -> None:
        v = vocab(terms=(Term("count", "counting", 1),))
        records = [rec("a", 1, ("wearing_out",), "the thing")]
        self.assertIn(
            "term-never-introduced", codes(validate_vocabulary(v, records, CONCEPTS))
        )


class TestCeiling(unittest.TestCase):
    def test_a_term_above_its_level_is_reported(self) -> None:
        v = vocab(terms=(Term("count", "counting", 5, ("counts",)),))
        records = [
            rec("late", 5, ("counting",), "you count the thing"),
            rec("early", 1, ("counting",), "you count the thing"),
        ]
        self.assertIn(
            "vocabulary-ceiling", codes(validate_vocabulary(v, records, CONCEPTS))
        )

    def test_a_general_word_above_its_tier_is_reported(self) -> None:
        records = [rec("a", 1, ("counting",), "you count the apparatus thing")]
        out = validate_vocabulary(vocab(), records, CONCEPTS)
        self.assertIn("vocabulary-ceiling", codes(out))

    def test_a_general_word_at_or_below_its_tier_passes(self) -> None:
        records = [rec("a", 5, ("counting",), "you count the apparatus thing")]
        self.assertNotIn(
            "vocabulary-ceiling", codes(validate_vocabulary(vocab(), records, CONCEPTS))
        )

    def test_an_unlisted_word_is_reported(self) -> None:
        records = [rec("a", 1, ("counting",), "you count the elephant thing")]
        self.assertIn(
            "unknown-word", codes(validate_vocabulary(vocab(), records, CONCEPTS))
        )


class TestCoverage(unittest.TestCase):
    def test_a_term_never_used_at_its_level_is_reported(self) -> None:
        records = [
            rec("a", 1, ("counting",), "the thing"),
            rec("b", 3, ("wearing_out",), "you count the thing"),
        ]
        self.assertIn(
            "vocabulary-uncovered",
            codes(validate_vocabulary(vocab(), records, CONCEPTS)),
        )

    def test_a_term_used_at_its_level_passes(self) -> None:
        records = [rec("a", 1, ("counting",), "you count the thing")]
        self.assertNotIn(
            "vocabulary-uncovered",
            codes(validate_vocabulary(vocab(), records, CONCEPTS)),
        )


class TestLicensing(unittest.TestCase):
    def test_a_term_naming_an_unknown_concept_is_reported(self) -> None:
        v = vocab(terms=(Term("count", "no_such_concept", 1),))
        records = [rec("a", 1, ("counting",), "you count the thing")]
        self.assertIn(
            "unlicensed-term", codes(validate_vocabulary(v, records, CONCEPTS))
        )

    def test_a_form_shared_by_two_terms_is_reported(self) -> None:
        v = vocab(
            terms=(
                Term("count", "counting", 1),
                Term("tally", "wearing_out", 1, ("count",)),
            )
        )
        records = [rec("a", 1, ("counting", "wearing_out"), "you count the thing")]
        self.assertIn(
            "duplicate-form", codes(validate_vocabulary(v, records, CONCEPTS))
        )

    def test_a_word_that_is_both_core_and_licensed_is_reported(self) -> None:
        v = vocab(core=frozenset({"count", "the", "you"}))
        records = [rec("a", 1, ("counting",), "you count the")]
        self.assertIn(
            "core-collision", codes(validate_vocabulary(v, records, CONCEPTS))
        )


class TestLoading(unittest.TestCase):
    def setUp(self) -> None:
        self._dir = tempfile.TemporaryDirectory()
        self.addCleanup(self._dir.cleanup)

    def write(self, payload: object) -> Path:
        path = Path(self._dir.name) / "v.json"
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def test_a_well_formed_vocabulary_loads(self) -> None:
        path = self.write(
            {
                "core": ["The"],
                "general": {"2": ["Shoe"]},
                "terms": [{"word": "Count", "concept": "counting", "level": 1}],
                "exempt": ["Popper"],
            }
        )
        v = load_vocabulary(path)
        self.assertIn("the", v.core)
        self.assertEqual(v.general_level("shoe"), 2)
        self.assertIsNotNone(v.lookup("count"))

    def test_a_non_numeric_general_key_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            load_vocabulary(self.write({"general": {"early": ["shoe"]}}))

    def test_a_term_without_a_concept_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            load_vocabulary(
                self.write({"terms": [{"word": "count", "concept": "counting"}]})
            )

    def test_the_shipped_vocabulary_validates_the_shipped_corpus(self) -> None:
        from epagoge.concept_graph import ConceptGraph
        from epagoge.record import load_corpus

        graph = ConceptGraph.load(Path("curriculum/graph/concepts.json"))
        records = load_corpus(Path("curriculum/graph/sample_corpus.jsonl"))
        v = load_vocabulary(Path("curriculum/vocabulary.json"))
        self.assertEqual(validate_vocabulary(v, records, graph.nodes), [])


if __name__ == "__main__":
    unittest.main()


class TestCompleteness(unittest.TestCase):
    """The unmapped tier measures the graph, not the words.

    Every content word names something. One with no mapping means the
    mapping was not identified, or a concept is missing from the graph.
    """

    def test_a_fully_mapped_vocabulary_is_complete(self) -> None:
        from epagoge.vocabulary import completeness

        v = vocab(general={})
        self.assertEqual(completeness(v).fraction, 1.0)
        self.assertEqual(completeness(v).unmapped, 0)

    def test_unmapped_words_lower_completeness(self) -> None:
        from epagoge.vocabulary import completeness

        done = completeness(vocab())
        self.assertEqual(done.mapped, 1)
        self.assertEqual(done.unmapped, 2)  # noqa: PLR2004
        self.assertLess(done.fraction, 1.0)

    def test_an_empty_vocabulary_is_vacuously_complete(self) -> None:
        from epagoge.vocabulary import completeness

        self.assertEqual(completeness(Vocabulary()).fraction, 1.0)

    def test_the_shipped_vocabulary_is_fully_mapped(self) -> None:
        """Every content word now carries a concept. The tier is empty."""
        from epagoge.vocabulary import completeness, load_vocabulary

        done = completeness(load_vocabulary(Path("curriculum/vocabulary.json")))
        self.assertEqual(done.unmapped, 0)
        self.assertEqual(done.fraction, 1.0)


class TestUnlicensed(unittest.TestCase):
    """The ceiling check used at the generation boundary.

    Separate from the corpus validator because it runs on a single line of
    untrusted teacher output before any record exists around it.
    """

    def vocabulary(self) -> Vocabulary:
        return Vocabulary(
            core=("the", "is"),
            exempt=("iec",),
            terms=(
                Term(word="cup", concept="c", level=1),
                Term(word="ledger", concept="l", level=5),
            ),
        )

    def test_admissible_text_reports_nothing(self) -> None:
        self.assertEqual(unlicensed(self.vocabulary(), "the cup is", 1), [])

    def test_a_word_above_the_level_is_reported(self) -> None:
        self.assertEqual(unlicensed(self.vocabulary(), "the ledger is", 1), ["ledger"])

    def test_the_same_word_is_admissible_at_its_own_level(self) -> None:
        self.assertEqual(unlicensed(self.vocabulary(), "the ledger is", 5), [])

    def test_an_unknown_word_is_reported(self) -> None:
        self.assertEqual(
            unlicensed(self.vocabulary(), "the frobnicator is", 1), ["frobnicator"]
        )

    def test_exempt_words_are_free_at_any_level(self) -> None:
        self.assertEqual(unlicensed(self.vocabulary(), "iec", 1), [])

    def test_every_offender_is_reported_not_just_the_first(self) -> None:
        found = unlicensed(self.vocabulary(), "ledger and frobnicator", 1)
        self.assertEqual(len(found), 3)
