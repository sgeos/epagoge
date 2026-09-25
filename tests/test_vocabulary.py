"""Tests for the per-level vocabulary.

Both rules get negative tests, because a vocabulary check that only ever
passes has not been shown to bite.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from epagoge.inflection import verb_forms
from epagoge.record import ClaimClass, Provenance, Record
from epagoge.vocabulary import (
    Term,
    Vocabulary,
    load_vocabulary,
    term_levels,
    tokenise,
    unlexicalised,
    unlicensed,
    utilisation,
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
    """The coverage rule is retired. These pin that it stays retired.

    It required every admitted term to be used at its level, which held only
    while the vocabulary was derived from the corpus. A prescriptive lexicon
    is authored ahead of its corpus, so an unused licensed word is the
    expected state.
    """

    def test_an_unused_term_is_no_longer_a_violation(self) -> None:
        records = [
            rec("a", 1, ("counting",), "the thing"),
            rec("b", 3, ("wearing_out",), "you count the thing"),
        ]
        self.assertNotIn(
            "vocabulary-uncovered",
            codes(validate_vocabulary(vocab(), records, CONCEPTS)),
        )

    def test_utilisation_reports_the_number_instead(self) -> None:
        records = [rec("a", 1, ("counting",), "you count the thing")]
        result = utilisation(vocab(), records, 1)
        self.assertGreater(result.admitted, 0)
        self.assertLessEqual(result.used, result.admitted)
        self.assertAlmostEqual(result.fraction, result.used / result.admitted)

    def test_utilisation_of_an_empty_level_is_zero_not_an_error(self) -> None:
        self.assertEqual(utilisation(vocab(), [], 1).fraction, 0.0)


class TestLowerBoundAgainstSchedule(unittest.TestCase):
    def test_a_scheduled_concept_satisfies_the_lower_bound(self) -> None:
        """A word may be licensed before its corpus is written."""
        found = validate_vocabulary(vocab(), [], CONCEPTS, {"counting": 1})
        self.assertNotIn("term-never-introduced", {v.code for v in found})

    def test_without_a_schedule_an_unwritten_concept_still_reports(self) -> None:
        found = validate_vocabulary(vocab(), [], CONCEPTS)
        self.assertIn("term-never-introduced", {v.code for v in found})

    def test_the_schedule_wins_where_it_is_earlier_than_the_records(self) -> None:
        records = [rec("a", 5, ("counting",), "you count the thing")]
        found = validate_vocabulary(vocab(), records, CONCEPTS, {"counting": 1})
        self.assertNotIn("term-before-concept", {v.code for v in found})


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
        from epagoge import schedule as sched

        scheduled: dict[str, int] = {}
        for path in sorted(Path("curriculum/schedule").glob("level_*.json")):
            scheduled.update(sched.assignment(sched.load(path)))
        self.assertEqual(validate_vocabulary(v, records, graph.nodes, scheduled), [])


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


class TestLexicalisation(unittest.TestCase):
    """A concept with no word cannot be taught.

    The other vocabulary rules run the opposite way, requiring a word to
    name a real concept and to not precede it. Neither fires when a concept
    has no word, because an unlexicalised concept breaks no rule as written.
    It is simply unwritable.
    """

    def vocabulary(self) -> Vocabulary:
        return Vocabulary(
            core=("the",),
            terms=(
                Term(word="cup", concept="vessel", level=1),
                Term(word="ledger", concept="ledger", level=5),
            ),
        )

    def test_a_concept_with_a_word_at_its_level_is_clear(self) -> None:
        self.assertEqual(unlexicalised(self.vocabulary(), {"vessel": 1}), [])

    def test_a_concept_with_no_word_at_all_is_reported(self) -> None:
        self.assertEqual(unlexicalised(self.vocabulary(), {"ghost": 1}), [("ghost", 1)])

    def test_a_word_above_the_concepts_level_does_not_license_it(self) -> None:
        """The word arrives too late to be usable where the concept is taught."""
        self.assertEqual(
            unlexicalised(self.vocabulary(), {"ledger": 2}), [("ledger", 2)]
        )

    def test_a_word_below_the_concepts_level_does_license_it(self) -> None:
        self.assertEqual(unlexicalised(self.vocabulary(), {"vessel": 3}), [])

    def test_the_earliest_word_decides(self) -> None:
        v = Vocabulary(
            terms=(
                Term(word="late", concept="c", level=5),
                Term(word="early", concept="c", level=1),
            )
        )
        self.assertEqual(unlexicalised(v, {"c": 2}), [])

    def test_a_planned_concept_is_exempt_through_the_validator(self) -> None:
        """A term must name a graph concept, so planning and lexicalising
        are the same step and the rule would fire on every plan."""
        found = validate_vocabulary(
            self.vocabulary(), [], {"vessel": object()}, {"vessel": 1, "planned": 1}
        )
        self.assertNotIn("concept-unlexicalised", {v.code for v in found})

    def test_a_graph_concept_with_no_word_is_a_violation(self) -> None:
        found = validate_vocabulary(
            self.vocabulary(), [], {"vessel": object(), "bare": object()}, {"bare": 1}
        )
        self.assertIn("concept-unlexicalised", {v.code for v in found})


class TestSubstitutionParsing(unittest.TestCase):
    """The table is a record of a triage decision, so it is validated."""

    def setUp(self) -> None:
        self._dir = tempfile.TemporaryDirectory()
        self.addCleanup(self._dir.cleanup)

    def write(self, payload: object) -> Path:
        path = Path(self._dir.name) / "v.json"
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def test_substitutions_load(self) -> None:
        got = load_vocabulary(
            self.write({"core": ["a"], "terms": [], "substitutions": {"x": "y"}})
        )
        self.assertEqual(dict(got.substitutions), {"x": "y"})

    def test_absent_substitutions_give_an_empty_table(self) -> None:
        got = load_vocabulary(self.write({"core": ["a"], "terms": []}))
        self.assertEqual(dict(got.substitutions), {})

    def test_a_non_object_table_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            load_vocabulary(
                self.write({"core": ["a"], "terms": [], "substitutions": ["x"]})
            )

    def test_an_empty_replacement_is_rejected(self) -> None:
        """A banned word with no replacement is a ban, not a substitution."""
        with self.assertRaises(ValueError):
            load_vocabulary(
                self.write({"core": ["a"], "terms": [], "substitutions": {"x": "  "}})
            )

    def test_a_non_string_replacement_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            load_vocabulary(
                self.write({"core": ["a"], "terms": [], "substitutions": {"x": 3}})
            )


class TestVerbInflection(unittest.TestCase):
    """Operator direction: every verb carries every inflection.

    A verb admitted in one form is a trap, because a generator constrained
    to the level reaches for an inflection that is not there. Forty such
    gaps were found by reading what a generator was blocked by, which is an
    expensive way to discover a missing plural.
    """

    def test_regular_verbs(self) -> None:
        self.assertEqual(verb_forms("walk"), ("walks", "walked", "walking"))

    def test_a_consonant_before_y_gives_ies_and_ied(self) -> None:
        self.assertEqual(verb_forms("carry"), ("carries", "carried", "carrying"))

    def test_a_vowel_before_y_keeps_the_y(self) -> None:
        self.assertEqual(verb_forms("play"), ("plays", "played", "playing"))

    def test_a_sibilant_takes_es(self) -> None:
        self.assertEqual(verb_forms("push")[0], "pushes")
        self.assertEqual(verb_forms("mix")[0], "mixes")

    def test_a_single_syllable_consonant_vowel_consonant_doubles(self) -> None:
        self.assertEqual(verb_forms("stop"), ("stops", "stopped", "stopping"))

    def test_w_x_and_y_never_double(self) -> None:
        """`allow`, not `show`, because show is in the irregular table."""
        self.assertEqual(verb_forms("allow"), ("allows", "allowed", "allowing"))
        self.assertEqual(verb_forms("play"), ("plays", "played", "playing"))

    def test_a_longer_word_does_not_double(self) -> None:
        """Approximated by syllable count, since stress is not in spelling."""
        self.assertEqual(verb_forms("visit"), ("visits", "visited", "visiting"))

    def test_a_final_e_is_dropped_for_ing_and_kept_for_d(self) -> None:
        self.assertEqual(verb_forms("move"), ("moves", "moved", "moving"))

    def test_ie_becomes_ying(self) -> None:
        self.assertEqual(verb_forms("tie"), ("ties", "tied", "tying"))

    def test_ee_keeps_both_letters(self) -> None:
        self.assertEqual(verb_forms("free"), ("frees", "freed", "freeing"))

    def test_irregular_verbs_come_from_the_table(self) -> None:
        self.assertEqual(verb_forms("eat"), ("eats", "ate", "eaten", "eating"))
        self.assertEqual(verb_forms("go"), ("goes", "went", "gone", "going"))

    def test_be_and_have_are_special_in_the_present(self) -> None:
        self.assertEqual(verb_forms("be")[0], "is")
        self.assertEqual(verb_forms("have")[0], "has")

    def test_a_past_equal_to_the_participle_is_not_repeated(self) -> None:
        self.assertEqual(verb_forms("buy"), ("buys", "bought", "buying"))

    def test_a_form_equal_to_the_base_is_dropped(self) -> None:
        """`cut` is its own past, so it must not appear as an inflection."""
        self.assertNotIn("cut", verb_forms("cut"))

    def test_the_shipped_lexicon_has_no_missing_inflection(self) -> None:
        v = load_vocabulary(Path("curriculum/vocabulary.json"))
        verbs = [t for t in v.terms if t.pos == "verb"]
        self.assertGreater(len(verbs), 100)
        missing = [
            (t.word, f)
            for t in verbs
            for f in verb_forms(t.word)
            if f not in v.core
            and not (v.lookup(f) is not None and v.lookup(f).level <= t.level)  # type: ignore[union-attr]
        ]
        self.assertEqual(missing, [])

    def test_an_unknown_part_of_speech_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "v.json"
            path.write_text(
                json.dumps(
                    {
                        "core": ["a"],
                        "terms": [
                            {
                                "word": "cup",
                                "concept": "c",
                                "level": 1,
                                "pos": "noun",
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            with self.assertRaises(ValueError):
                load_vocabulary(path)


class TestSenses(unittest.TestCase):
    """A word has senses and a dictionary gives more than one definition.

    `set` is a noun and a verb, `swallow` is an action and a bird, and
    `ground` is the earth and the past of grind. The model held one concept
    per word, so admitting a word silently asserted it meant one thing.
    Only admitted senses are listed, which is how the lexicon says the bird
    and the grinding are not level-one material.
    """

    def vocab(self, *terms: Term) -> Vocabulary:
        return Vocabulary(core=frozenset({"the"}), terms=terms)

    def test_two_senses_of_one_word_are_allowed(self) -> None:
        v = self.vocab(
            Term(word="set", concept="grouping", level=1),
            Term(word="set", concept="activity", level=1, pos="verb"),
        )
        got = validate_vocabulary(v, [], {"grouping": 1, "activity": 1})
        self.assertEqual([x.code for x in got if x.code == "duplicate-form"], [])

    def test_a_form_shared_by_two_different_words_is_rejected(self) -> None:
        """Nothing can decide which concept the token carries."""
        v = self.vocab(
            Term(word="saw", concept="tool", level=1),
            Term(word="see", concept="knowing", level=1, forms=("saw",)),
        )
        got = validate_vocabulary(v, [], {"tool": 1, "knowing": 1})
        self.assertIn("duplicate-form", [x.code for x in got])

    def test_the_same_word_and_concept_twice_is_rejected(self) -> None:
        v = self.vocab(
            Term(word="set", concept="grouping", level=1),
            Term(word="set", concept="grouping", level=2),
        )
        got = validate_vocabulary(v, [], {"grouping": 1})
        self.assertIn("duplicate-sense", [x.code for x in got])

    def test_senses_returns_every_sense(self) -> None:
        v = self.vocab(
            Term(word="set", concept="grouping", level=2),
            Term(word="set", concept="activity", level=1),
        )
        self.assertEqual({t.concept for t in v.senses("set")}, {"grouping", "activity"})

    def test_lookup_returns_the_earliest_admitted_sense(self) -> None:
        v = self.vocab(
            Term(word="set", concept="grouping", level=2),
            Term(word="set", concept="activity", level=1),
        )
        found = v.lookup("set")
        self.assertIsNotNone(found)
        self.assertEqual(found.level, 1)  # type: ignore[union-attr]

    def test_senses_of_an_absent_word_is_empty(self) -> None:
        self.assertEqual(self.vocab().senses("nothing"), ())

    def test_words_counts_bases_not_senses(self) -> None:
        v = self.vocab(
            Term(word="set", concept="grouping", level=1),
            Term(word="set", concept="activity", level=1),
        )
        self.assertEqual(len(v.terms), 2)
        self.assertEqual(v.words(), frozenset({"set"}))

    def test_an_inflection_is_satisfied_by_any_sense(self) -> None:
        """The verb needs `sets`; the noun sense supplying it is enough."""
        v = self.vocab(
            Term(word="set", concept="grouping", level=1, forms=("sets",)),
            Term(
                word="set", concept="activity", level=1, pos="verb", forms=("setting",)
            ),
        )
        got = validate_vocabulary(v, [], {"grouping": 1, "activity": 1})
        self.assertEqual([x.code for x in got if x.code == "missing-inflection"], [])

    def test_the_shipped_lexicon_carries_multi_sense_words(self) -> None:
        v = load_vocabulary(Path("curriculum/vocabulary.json"))
        self.assertGreater(len(v.terms), len(v.words()))
        self.assertGreaterEqual(len(v.senses("set")), 2)
