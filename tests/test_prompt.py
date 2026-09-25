"""Tests for generation prompts.

The prompt is the one place where a mistake is invisible in the output. A
prompt that omits an exclusion produces fluent text that blurs the
distinction the curriculum exists to draw, passes schema validation, and
reads well. So the prompt's content is asserted rather than its shape.
"""

from __future__ import annotations

import unittest

from epagoge import prompt as prompts
from epagoge.concept_graph import ConceptGraph, Node, NodeKind


def concept(node_id: str, domain: str, name: str | None = None) -> Node:
    return Node(
        id=node_id,
        name=name or node_id.replace("_", " "),
        kind=NodeKind.DOMAIN_CONCEPT,
        domain=domain,
    )


def graph() -> ConceptGraph:
    return ConceptGraph(
        [
            concept("breaks", "fa"),
            concept("wears", "fa"),
            concept("snaps", "fa"),
            concept("parts", "fa"),
            concept("elsewhere", "other"),
            Node("shape", "shape", NodeKind.FORMAL_STRUCTURE, None),
        ],
        {"wears": ["breaks"], "snaps": ["breaks"], "parts": ["wears"]},
        {},
    )


WORDS = ("a", "thing", "wears", "out")


class TestNeighbours(unittest.TestCase):
    def test_a_prerequisite_is_an_exclusion(self) -> None:
        """The recorded conflation was with a prerequisite, not a sibling."""
        self.assertIn("breaks", prompts.neighbours(graph(), "wears"))

    def test_a_dependent_is_not_an_exclusion(self) -> None:
        """A general concept is taught through its instances.

        Excluding dependents starved the hub concepts. Material, change and
        sound produced nothing at all in a measured run while carrying five
        or six exclusions each.
        """
        self.assertNotIn("parts", prompts.neighbours(graph(), "wears"))

    def test_a_sibling_sharing_a_prerequisite_is_an_exclusion(self) -> None:
        self.assertIn("snaps", prompts.neighbours(graph(), "wears"))

    def test_a_concept_is_never_its_own_exclusion(self) -> None:
        self.assertNotIn("wears", prompts.neighbours(graph(), "wears"))

    def test_another_domain_is_not_an_exclusion(self) -> None:
        """Cross-domain confusion is a different problem and a rarer one."""
        self.assertNotIn("elsewhere", prompts.neighbours(graph(), "wears"))

    def test_the_list_is_capped(self) -> None:
        g = ConceptGraph(
            [concept("root", "d"), *(concept(f"c{i}", "d") for i in range(20))],
            {f"c{i}": ["root"] for i in range(20)},
            {},
        )
        self.assertEqual(len(prompts.neighbours(g, "c0")), prompts.MAX_EXCLUSIONS)

    def test_a_root_concept_has_no_exclusions(self) -> None:
        """Nothing above it to be confused with, so nothing is withheld."""
        g = ConceptGraph(
            [concept("root", "d"), concept("leaf", "d")], {"leaf": ["root"]}, {}
        )
        self.assertEqual(prompts.neighbours(g, "root"), [])

    def test_the_order_is_stable(self) -> None:
        g = graph()
        self.assertEqual(prompts.neighbours(g, "wears"), prompts.neighbours(g, "wears"))

    def test_an_absent_concept_yields_nothing(self) -> None:
        self.assertEqual(prompts.neighbours(graph(), "ghost"), [])


class TestTargetFor(unittest.TestCase):
    def test_exclusions_are_derived_and_named(self) -> None:
        t = prompts.target_for(graph(), "wears", "form", {})
        self.assertIn("breaks", t.exclusions)
        self.assertEqual(t.domain, "fa")

    def test_only_cited_primitives_are_carried(self) -> None:
        t = prompts.target_for(
            graph(), "wears", "form", {"p": "observed text", "q": "other"}, ("p",)
        )
        self.assertEqual(t.primitives, (("p", "observed text"),))

    def test_an_uncited_primitive_is_silently_absent(self) -> None:
        t = prompts.target_for(graph(), "wears", "form", {}, ("missing",))
        self.assertEqual(t.primitives, ())

    def test_a_formal_structure_is_not_teachable(self) -> None:
        with self.assertRaises(ValueError):
            prompts.target_for(graph(), "shape", "form", {})


class TestBuild(unittest.TestCase):
    def target(self) -> prompts.Target:
        return prompts.target_for(
            graph(), "wears", "the register line", {"p": "an observation"}, ("p",)
        )

    def test_the_prompt_names_the_concept_and_its_exclusions(self) -> None:
        text = prompts.build(self.target(), 1, WORDS)
        self.assertIn("wears", text)
        self.assertIn("breaks", text)
        self.assertIn("an observation", text)

    def test_every_admissible_word_appears(self) -> None:
        text = prompts.build(self.target(), 1, WORDS)
        for word in WORDS:
            self.assertIn(word, text)

    def test_the_requested_count_appears(self) -> None:
        self.assertIn("Write 7 ", prompts.build(self.target(), 1, WORDS, count=7))

    def test_a_target_without_primitives_omits_the_grounding_block(self) -> None:
        bare = prompts.Target("c", "c", "d", "form")
        self.assertNotIn("Ground each sentence", prompts.build(bare, 1, WORDS))

    def test_a_target_without_exclusions_omits_the_exclusion_block(self) -> None:
        bare = prompts.Target("c", "c", "d", "form")
        self.assertNotIn("DO NOT write about", prompts.build(bare, 1, WORDS))

    def test_a_count_below_one_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            prompts.build(self.target(), 1, WORDS, count=0)

    def test_an_empty_vocabulary_is_rejected(self) -> None:
        """Silently asking for unconstrained output is the worse failure."""
        with self.assertRaises(ValueError):
            prompts.build(self.target(), 1, ())


class TestRetry(unittest.TestCase):
    def test_the_retry_names_the_offending_words(self) -> None:
        t = prompts.target_for(graph(), "wears", "form", {})
        text = prompts.retry(t, 1, WORDS, ["a bad line"], ["snapped", "chain"])
        self.assertIn("snapped", text)
        self.assertIn("chain", text)
        self.assertIn("a bad line", text)

    def test_the_retry_still_carries_the_full_prompt(self) -> None:
        t = prompts.target_for(graph(), "wears", "form", {})
        text = prompts.retry(t, 1, WORDS, ["bad"], ["nope"])
        self.assertIn("DO NOT write about", text)
        self.assertIn("breaks", text)
