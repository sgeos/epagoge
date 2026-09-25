"""Tests for word-level tokenisation over the closed lexicon.

Exact tokenisation is a stricter check than the corpus validator. The
validator accepts a word by stripping suffixes, so `clouds` passes on the
strength of `cloud`, while the tokeniser needs the form itself. Twelve
plurals the corpus was already using were absent from the lexicon and only
this found them.
"""

from __future__ import annotations

import unittest
from pathlib import Path

from epagoge.book import load_book_dir
from epagoge.tokeniser import UNK, WORD_RE, build
from epagoge.vocabulary import Term, Vocabulary, load_vocabulary


def vocab(*words: str) -> Vocabulary:
    return Vocabulary(
        core=frozenset({"the", "is"}),
        terms=tuple(Term(word=w, concept="c", level=1) for w in words),
    )


class TestBuilding(unittest.TestCase):
    def test_specials_come_first_and_are_stable(self) -> None:
        t = build(vocab("cup"), 1)
        self.assertEqual(t.words[:3], ("<pad>", UNK, "<book>"))

    def test_core_and_terms_are_both_included(self) -> None:
        t = build(vocab("cup"), 1)
        for word in ("the", "is", "cup"):
            self.assertIn(word, t.ids)

    def test_a_higher_level_term_is_excluded(self) -> None:
        v = Vocabulary(terms=(Term(word="axiom", concept="c", level=5),))
        self.assertNotIn("axiom", build(v, 1).ids)

    def test_surface_forms_are_included(self) -> None:
        v = Vocabulary(terms=(Term(word="cup", concept="c", level=1, forms=("cups",)),))
        self.assertIn("cups", build(v, 1).ids)

    def test_the_mapping_is_stable_across_builds(self) -> None:
        """A checkpoint is meaningless under a different mapping."""
        self.assertEqual(
            build(vocab("cup", "dog"), 1).words, build(vocab("dog", "cup"), 1).words
        )


class TestEncoding(unittest.TestCase):
    def setUp(self) -> None:
        self.t = build(vocab("cup"), 1)

    def test_encoding_is_case_insensitive(self) -> None:
        self.assertEqual(self.t.encode("The CUP"), self.t.encode("the cup"))

    def test_a_full_stop_is_a_token(self) -> None:
        self.assertEqual(len(self.t.encode("the cup.")), 3)

    def test_an_absent_word_becomes_unknown(self) -> None:
        self.assertIn(self.t.ids[UNK], self.t.encode("the ghost"))

    def test_unknown_lists_what_is_absent(self) -> None:
        self.assertEqual(self.t.unknown("the ghost cup"), ["ghost"])

    def test_a_clean_text_has_no_unknowns(self) -> None:
        self.assertEqual(self.t.unknown("the cup is"), [])

    def test_roundtrip_preserves_the_words(self) -> None:
        self.assertEqual(self.t.decode(self.t.encode("the cup is")), "the cup is")


class TestShippedCorpus(unittest.TestCase):
    def test_the_corpus_tokenises_with_no_unknowns(self) -> None:
        """An unknown token means a word the lexicon does not carry exactly."""
        v = load_vocabulary(Path("curriculum/vocabulary.json"))
        t = build(v, 1)
        _books, records = load_book_dir(Path("curriculum/books/level_1"))
        text = " ".join(str(r["content"]) for r in records)  # type: ignore[index]
        self.assertEqual(sorted(set(t.unknown(text))), [])


class TestPossessives(unittest.TestCase):
    """A possessive is grammar, not vocabulary.

    Matched as part of the word, `boat's` became a token the lexicon could
    never hold, and admitting it would have meant admitting the possessive
    of every noun.
    """

    def test_a_possessive_is_split_from_its_noun(self) -> None:
        self.assertEqual(
            WORD_RE.findall("the boat's sail"), ["the", "boat", "'s", "sail"]
        )

    def test_a_contraction_stays_whole(self) -> None:
        """Its clitic is not `s`, so the rule leaves it alone."""
        self.assertEqual(WORD_RE.findall("don't go"), ["don't", "go"])

    def test_a_plural_is_not_mistaken_for_a_possessive(self) -> None:
        self.assertEqual(WORD_RE.findall("faces and eyes"), ["faces", "and", "eyes"])

    def test_the_possessive_token_is_in_the_vocabulary(self) -> None:
        t = build(vocab("cup", "water"), 1)
        self.assertIn("'s", t.ids)
        self.assertEqual(t.unknown("the cup's water"), [])
