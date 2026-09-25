"""Tests for the sense-keyed thesaurus.

Two roles, and the second sets the requirements. During authoring this
finds words admitted without their opposite. Afterwards it is level-one
reference material beside the dictionary, so it must cover every sense and
must itself be written in words the level admits.

Antonymy belongs to a sense. `right` opposes `left` as a direction and
`wrong` as a judgement, which a word-keyed list cannot hold.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from epagoge.thesaurus import Entry, Thesaurus, from_json, load, validate
from epagoge.vocabulary import Term, Vocabulary


def vocab(*terms: tuple[str, str, int]) -> Vocabulary:
    return Vocabulary(
        core=frozenset({"up", "down"}),
        terms=tuple(Term(word=w, concept=c, level=lv) for w, c, lv in terms),
    )


class TestCoverage(unittest.TestCase):
    """A sense with no entry is a sense nobody has checked."""

    def test_a_covered_sense_passes(self) -> None:
        v = vocab(("hot", "heat", 1))
        t = Thesaurus((Entry("hot", "heat"),))
        self.assertEqual(validate(t, v), [])

    def test_an_uncovered_sense_is_a_violation(self) -> None:
        v = vocab(("hot", "heat", 1))
        self.assertEqual(
            [x.code for x in validate(Thesaurus(), v)], ["uncovered-sense"]
        )

    def test_a_sense_above_the_level_need_not_be_covered(self) -> None:
        v = vocab(("hot", "heat", 2))
        self.assertEqual(validate(Thesaurus(), v, 1), [])

    def test_each_sense_of_one_word_needs_its_own_entry(self) -> None:
        v = vocab(("right", "direction", 1), ("right", "being_told", 1))
        t = Thesaurus((Entry("right", "direction"),))
        got = validate(t, v)
        self.assertEqual([x.code for x in got], ["uncovered-sense"])
        self.assertIn("being_told", got[0].detail)

    def test_an_entry_with_no_antonym_is_not_a_violation(self) -> None:
        """Most nouns oppose nothing."""
        v = vocab(("cup", "household_object", 1))
        self.assertEqual(
            validate(Thesaurus((Entry("cup", "household_object"),)), v), []
        )


class TestRelations(unittest.TestCase):
    def base(self) -> Vocabulary:
        return vocab(("hot", "heat", 1), ("cold", "heat", 1), ("ice", "water", 2))

    def test_a_symmetric_pair_passes(self) -> None:
        t = Thesaurus(
            (Entry("hot", "heat", ("cold",)), Entry("cold", "heat", ("hot",)))
        )
        self.assertEqual(validate(t, self.base()), [])

    def test_a_one_way_antonym_is_a_violation(self) -> None:
        t = Thesaurus((Entry("hot", "heat", ("cold",)), Entry("cold", "heat")))
        self.assertIn("asymmetric-antonym", [x.code for x in validate(t, self.base())])

    def test_an_antonym_above_the_level_is_not_reachable(self) -> None:
        t = Thesaurus((Entry("hot", "heat", ("ice",)), Entry("cold", "heat")))
        self.assertIn("missing-antonym", [x.code for x in validate(t, self.base())])

    def test_a_word_cannot_oppose_itself(self) -> None:
        t = Thesaurus((Entry("hot", "heat", ("hot",)), Entry("cold", "heat")))
        self.assertIn("self-antonym", [x.code for x in validate(t, self.base())])

    def test_a_core_word_may_be_named_without_an_entry_of_its_own(self) -> None:
        """A function word carries no concept, so it has nothing to hold."""
        v = vocab(("high", "shape", 1))
        t = Thesaurus((Entry("high", "shape", ("up",)),))
        self.assertEqual(validate(t, v), [])

    def test_a_core_word_may_still_have_an_entry_with_no_concept(self) -> None:
        v = vocab()
        t = Thesaurus((Entry("up", "", ("down",)), Entry("down", "", ("up",))))
        self.assertEqual(validate(t, v), [])

    def test_a_concept_free_entry_for_a_non_core_word_is_rejected(self) -> None:
        got = validate(Thesaurus((Entry("banana", ""),)), vocab())
        self.assertEqual([x.code for x in got], ["unknown-sense"])

    def test_an_entry_for_an_absent_sense_is_rejected(self) -> None:
        v = vocab(("hot", "heat", 1))
        got = validate(Thesaurus((Entry("hot", "colour"), Entry("hot", "heat"))), v)
        self.assertIn("unknown-sense", [x.code for x in got])

    def test_a_repeated_entry_is_rejected(self) -> None:
        v = vocab(("hot", "heat", 1))
        got = validate(Thesaurus((Entry("hot", "heat"), Entry("hot", "heat"))), v)
        self.assertIn("duplicate-entry", [x.code for x in got])

    def test_a_synonym_must_also_be_reachable(self) -> None:
        t = Thesaurus((Entry("hot", "heat", synonyms=("ice",)), Entry("cold", "heat")))
        self.assertIn("missing-synonym", [x.code for x in validate(t, self.base())])


class TestParsing(unittest.TestCase):
    def test_a_well_formed_file_loads_and_lowercases(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "t.json"
            path.write_text(
                json.dumps(
                    {
                        "senses": [
                            {"word": "Hot", "concept": "heat", "antonyms": ["Cold"]}
                        ]
                    }
                )
            )
            entry = load(path).entries[0]
            self.assertEqual((entry.word, entry.antonyms), ("hot", ("cold",)))

    def test_a_non_object_payload_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            from_json([])

    def test_a_missing_senses_key_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            from_json({})

    def test_an_entry_without_a_word_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            from_json({"senses": [{"concept": "heat"}]})

    def test_a_non_list_antonyms_field_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            from_json({"senses": [{"word": "a", "concept": "b", "antonyms": "c"}]})

    def test_an_empty_antonym_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            from_json({"senses": [{"word": "a", "concept": "b", "antonyms": [" "]}]})


class TestShipped(unittest.TestCase):
    def test_the_shipped_thesaurus_covers_every_level_one_sense(self) -> None:
        from epagoge.vocabulary import load_vocabulary

        t = load(Path("curriculum/thesaurus.json"))
        v = load_vocabulary(Path("curriculum/vocabulary.json"))
        self.assertEqual(validate(t, v, 1), [])
        self.assertGreater(len(t.entries), 800)

    def test_right_opposes_a_different_word_in_each_sense(self) -> None:
        """The case that forced the restructure."""
        t = load(Path("curriculum/thesaurus.json"))
        direction = t.for_sense("right", "direction")
        judgement = t.for_sense("right", "being_told")
        self.assertIsNotNone(direction)
        self.assertIsNotNone(judgement)
        self.assertIn("left", direction.antonyms)  # type: ignore[union-attr]
        self.assertIn("wrong", judgement.antonyms)  # type: ignore[union-attr]
