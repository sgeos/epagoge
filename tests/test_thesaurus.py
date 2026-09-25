"""Tests for antonym completeness.

A lexicon can be complete in every word it has and still be unable to say
the opposite of them. The level-one lexicon held `true` without `false`
and `agree` without `disagree` while the curriculum planned a concept
named for agreeing and disagreeing. No existing check could see it, since
the word that is missing is not there to be checked.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from epagoge.thesaurus import Thesaurus, from_json, load, validate
from epagoge.vocabulary import Term, Vocabulary


def vocab(*terms: tuple[str, int]) -> Vocabulary:
    return Vocabulary(
        core=frozenset({"the"}),
        terms=tuple(Term(word=w, concept="c", level=lv) for w, lv in terms),
    )


class TestAntonymCompleteness(unittest.TestCase):
    def test_a_complete_pair_passes(self) -> None:
        got = validate(Thesaurus((("hot", "cold"),)), vocab(("hot", 1), ("cold", 1)))
        self.assertEqual(got, [])

    def test_one_end_missing_is_a_violation(self) -> None:
        got = validate(Thesaurus((("hot", "cold"),)), vocab(("hot", 1)))
        self.assertEqual([v.code for v in got], ["missing-antonym"])
        self.assertIn("'cold'", got[0].detail)

    def test_the_violation_names_which_end_is_missing(self) -> None:
        got = validate(Thesaurus((("hot", "cold"),)), vocab(("cold", 1)))
        self.assertIn("'cold' is admissible", got[0].detail)
        self.assertIn("'hot' is not", got[0].detail)

    def test_an_end_above_the_level_counts_as_missing(self) -> None:
        """Admitted at level two is not reachable by a level-one generator."""
        got = validate(Thesaurus((("hot", "cold"),)), vocab(("hot", 1), ("cold", 2)))
        self.assertEqual([v.code for v in got], ["missing-antonym"])

    def test_neither_end_present_is_not_a_violation(self) -> None:
        """The dimension may belong to a later level."""
        self.assertEqual(validate(Thesaurus((("hot", "cold"),)), vocab()), [])

    def test_a_core_word_counts_as_admissible(self) -> None:
        got = validate(Thesaurus((("the", "cold"),)), vocab(("cold", 1)))
        self.assertEqual(got, [])

    def test_a_word_paired_with_itself_is_rejected(self) -> None:
        got = validate(Thesaurus((("hot", "hot"),)), vocab(("hot", 1)))
        self.assertEqual([v.code for v in got], ["degenerate-pair"])

    def test_a_repeated_pair_is_rejected_in_either_order(self) -> None:
        pairs = Thesaurus((("hot", "cold"), ("cold", "hot")))
        got = validate(pairs, vocab(("hot", 1), ("cold", 1)))
        self.assertEqual([v.code for v in got], ["duplicate-pair"])

    def test_words_lists_both_ends(self) -> None:
        self.assertEqual(Thesaurus((("a", "b"),)).words(), frozenset({"a", "b"}))


class TestParsing(unittest.TestCase):
    def test_a_well_formed_file_loads_and_is_lowercased(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "t.json"
            path.write_text(json.dumps({"antonyms": [["Hot", "Cold"]]}))
            self.assertEqual(load(path).antonyms, (("hot", "cold"),))

    def test_a_non_object_payload_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            from_json([])

    def test_a_missing_antonyms_key_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            from_json({})

    def test_a_triple_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            from_json({"antonyms": [["a", "b", "c"]]})

    def test_a_non_list_pair_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            from_json({"antonyms": ["ab"]})

    def test_an_empty_word_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            from_json({"antonyms": [["a", " "]]})


class TestShippedThesaurus(unittest.TestCase):
    def test_the_shipped_pairs_are_complete_at_level_one(self) -> None:
        from epagoge.vocabulary import load_vocabulary

        t = load(Path("curriculum/thesaurus.json"))
        v = load_vocabulary(Path("curriculum/vocabulary.json"))
        self.assertGreater(len(t.antonyms), 90)
        self.assertEqual(validate(t, v, 1), [])
