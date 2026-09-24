"""Tests for the concept graph.

Written as unittest cases so they run under the standard library today and
under pytest once it is installed.

Coverage is deliberately weighted toward negative cases. Every invariant in
docs/spec/CONCEPT_GRAPH.md has a test that breaks it, because a validator
that has only been shown valid input has not been tested.
"""

from __future__ import annotations

import json
import random
import tempfile
import unittest
from pathlib import Path

from epagoge.concept_graph import ConceptGraph, Node, NodeKind


def concept(node_id: str, domain: str) -> Node:
    return Node(id=node_id, name=node_id, kind=NodeKind.DOMAIN_CONCEPT, domain=domain)


def structure(node_id: str) -> Node:
    return Node(id=node_id, name=node_id, kind=NodeKind.FORMAL_STRUCTURE, domain=None)


def codes(graph: ConceptGraph) -> set[str]:
    return {v.code for v in graph.validate()}


class TestInvariants(unittest.TestCase):
    def test_sound_graph_has_no_violations(self) -> None:
        g = ConceptGraph(
            [concept("a", "math"), concept("b", "math"), structure("s")],
            {"b": ["a"]},
            {"a": ["s"]},
        )
        self.assertEqual(g.validate(), [])

    def test_unknown_target_is_reported(self) -> None:
        g = ConceptGraph([concept("a", "math")], {"a": ["ghost"]}, {})
        self.assertIn("unknown-target", codes(g))

    def test_unknown_source_is_reported(self) -> None:
        g = ConceptGraph([concept("a", "math")], {"ghost": ["a"]}, {})
        self.assertIn("unknown-source", codes(g))

    def test_self_loop_is_reported(self) -> None:
        g = ConceptGraph([concept("a", "math")], {"a": ["a"]}, {})
        self.assertIn("self-loop", codes(g))

    def test_cycle_is_reported(self) -> None:
        g = ConceptGraph(
            [concept("a", "math"), concept("b", "math"), concept("c", "math")],
            {"a": ["c"], "b": ["a"], "c": ["b"]},
            {},
        )
        self.assertIn("cycle", codes(g))

    def test_domain_concept_without_domain_is_reported(self) -> None:
        g = ConceptGraph(
            [Node(id="a", name="a", kind=NodeKind.DOMAIN_CONCEPT, domain=None)], {}, {}
        )
        self.assertIn("missing-domain", codes(g))

    def test_formal_structure_with_domain_is_reported(self) -> None:
        g = ConceptGraph(
            [Node(id="s", name="s", kind=NodeKind.FORMAL_STRUCTURE, domain="math")],
            {},
            {},
        )
        self.assertIn("domained-structure", codes(g))

    def test_instantiates_must_target_a_structure(self) -> None:
        g = ConceptGraph([concept("a", "math"), concept("b", "math")], {}, {"a": ["b"]})
        self.assertIn("bad-instantiates-target", codes(g))

    def test_instantiates_must_originate_at_a_concept(self) -> None:
        g = ConceptGraph([structure("s"), structure("t")], {}, {"s": ["t"]})
        self.assertIn("bad-instantiates-source", codes(g))

    def test_formal_layer_may_not_depend_on_a_domain(self) -> None:
        g = ConceptGraph([structure("s"), concept("a", "math")], {"s": ["a"]}, {})
        self.assertIn("layering", codes(g))

    def test_validate_reports_every_violation_not_only_the_first(self) -> None:
        g = ConceptGraph([concept("a", "math")], {"a": ["a", "ghost"]}, {})
        self.assertGreaterEqual(len(g.validate()), 2)


class TestDepth(unittest.TestCase):
    def test_root_is_depth_zero(self) -> None:
        g = ConceptGraph([concept("a", "math")], {}, {})
        self.assertEqual(g.prerequisite_depth()["a"], 0)

    def test_depth_takes_the_longest_path_not_the_shortest(self) -> None:
        # d depends on a directly and on a through b and c.
        # Shortest path would give 1. Longest gives 3.
        g = ConceptGraph(
            [concept(x, "math") for x in ("a", "b", "c", "d")],
            {"b": ["a"], "c": ["b"], "d": ["a", "c"]},
            {},
        )
        self.assertEqual(g.prerequisite_depth()["d"], 3)


class TestTransfer(unittest.TestCase):
    def test_cross_domain_shared_structure_yields_transfer(self) -> None:
        g = ConceptGraph(
            [concept("m", "math"), concept("f", "failure"), structure("s")],
            {},
            {"m": ["s"], "f": ["s"]},
        )
        self.assertEqual(g.transfer_edges(), {("f", "m")})

    def test_same_domain_shared_structure_is_not_transfer(self) -> None:
        g = ConceptGraph(
            [concept("m1", "math"), concept("m2", "math"), structure("s")],
            {},
            {"m1": ["s"], "m2": ["s"]},
        )
        self.assertEqual(g.transfer_edges(), set())

    def test_no_shared_structure_yields_nothing(self) -> None:
        g = ConceptGraph(
            [
                concept("m", "math"),
                concept("f", "failure"),
                structure("s"),
                structure("t"),
            ],
            {},
            {"m": ["s"], "f": ["t"]},
        )
        self.assertEqual(g.transfer_edges(), set())


class TestOrderings(unittest.TestCase):
    def build(self) -> ConceptGraph:
        return ConceptGraph(
            [concept(x, "math") for x in ("a", "b", "c", "d")],
            {"b": ["a"], "c": ["a"], "d": ["b", "c"]},
            {},
        )

    def test_canonical_order_is_deterministic(self) -> None:
        g = self.build()
        self.assertEqual(g.canonical_order(), g.canonical_order())

    def test_canonical_order_respects_prerequisites(self) -> None:
        g = self.build()
        order = g.canonical_order()
        pos = {n: i for i, n in enumerate(order)}
        for node_id in g.nodes:
            for p in g.prerequisites_of(node_id):
                self.assertLess(pos[p], pos[node_id])

    def test_random_extension_always_respects_prerequisites(self) -> None:
        g = self.build()
        for seed in range(50):
            order = g.random_linear_extension(random.Random(seed))
            pos = {n: i for i, n in enumerate(order)}
            self.assertEqual(len(order), len(g.nodes))
            for node_id in g.nodes:
                for p in g.prerequisites_of(node_id):
                    self.assertLess(pos[p], pos[node_id])

    def test_random_extension_is_reproducible_from_a_seed(self) -> None:
        g = self.build()
        self.assertEqual(
            g.random_linear_extension(random.Random(7)),
            g.random_linear_extension(random.Random(7)),
        )

    def test_random_extension_actually_varies(self) -> None:
        g = self.build()
        seen = {tuple(g.random_linear_extension(random.Random(s))) for s in range(50)}
        self.assertGreater(len(seen), 1)

    def test_ordering_a_cyclic_graph_raises_rather_than_returning_a_wrong_answer(
        self,
    ) -> None:
        g = ConceptGraph(
            [concept("a", "math"), concept("b", "math")], {"a": ["b"], "b": ["a"]}, {}
        )
        with self.assertRaises(ValueError):
            g.canonical_order()


class TestBoundaryParsing(unittest.TestCase):
    """A graph file is external input. These test that it is treated as such.

    Every case here is a malformed file that must raise at the boundary
    rather than produce a graph whose wrongness surfaces later.
    """

    def test_payload_must_be_an_object(self) -> None:
        with self.assertRaises(ValueError):
            ConceptGraph.from_json([1, 2, 3])

    def test_nodes_must_be_a_list(self) -> None:
        with self.assertRaises(ValueError):
            ConceptGraph.from_json({"nodes": {"id": "a"}})

    def test_node_must_be_an_object(self) -> None:
        with self.assertRaises(ValueError):
            ConceptGraph.from_json({"nodes": ["a"]})

    def test_node_id_must_be_a_string(self) -> None:
        with self.assertRaises(ValueError):
            ConceptGraph.from_json(
                {"nodes": [{"id": 7, "name": "a", "kind": "domain_concept"}]}
            )

    def test_unknown_node_kind_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            ConceptGraph.from_json(
                {"nodes": [{"id": "a", "name": "a", "kind": "nonsense"}]}
            )

    def test_domain_must_be_a_string_when_present(self) -> None:
        with self.assertRaises(ValueError):
            ConceptGraph.from_json(
                {
                    "nodes": [
                        {"id": "a", "name": "a", "kind": "domain_concept", "domain": 3}
                    ]
                }
            )

    def test_edge_map_must_be_an_object(self) -> None:
        with self.assertRaises(ValueError):
            ConceptGraph.from_json({"nodes": [], "prerequisites": ["a"]})

    def test_edge_targets_must_be_a_list(self) -> None:
        with self.assertRaises(ValueError):
            ConceptGraph.from_json({"nodes": [], "prerequisites": {"a": "b"}})

    def test_edge_target_must_be_a_string(self) -> None:
        with self.assertRaises(ValueError):
            ConceptGraph.from_json({"nodes": [], "prerequisites": {"a": [7]}})

    def test_absent_edge_sections_default_to_empty(self) -> None:
        node = {"id": "a", "name": "a", "kind": "domain_concept", "domain": "m"}
        g = ConceptGraph.from_json({"nodes": [node]})
        self.assertEqual(g.validate(), [])
        self.assertEqual(g.canonical_order(), ["a"])


class TestFileLoading(unittest.TestCase):
    def test_load_round_trips_through_a_file(self) -> None:
        payload = {
            "nodes": [
                {"id": "a", "name": "a", "kind": "domain_concept", "domain": "m"},
                {"id": "s", "name": "s", "kind": "formal_structure", "domain": None},
            ],
            "prerequisites": {},
            "instantiates": {"a": ["s"]},
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "g.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            g = ConceptGraph.load(path)
        self.assertEqual(g.validate(), [])
        self.assertEqual(g.structures_of("a"), frozenset({"s"}))
        self.assertEqual(g.structures_of("missing"), frozenset())

    def test_depth_raises_on_a_cycle_rather_than_looping(self) -> None:
        g = ConceptGraph(
            [concept("a", "m"), concept("b", "m")], {"a": ["b"], "b": ["a"]}, {}
        )
        with self.assertRaises(ValueError):
            g.prerequisite_depth()

    def test_edges_to_undeclared_nodes_are_skipped_by_depth(self) -> None:
        g = ConceptGraph([concept("a", "m")], {"a": ["ghost"]}, {})
        self.assertEqual(g.prerequisite_depth()["a"], 0)


if __name__ == "__main__":
    unittest.main()
