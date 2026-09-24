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

from epagoge.concept_graph import ConceptGraph, Domain, Node, NodeKind


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


class TestSpecialisation(unittest.TestCase):
    """A concrete concept is an instance of a general one. A third relation."""

    def chain(self) -> ConceptGraph:
        return ConceptGraph(
            [concept(x, "materials") for x in ("crayon", "teddy", "wax", "fuel")],
            {"fuel": ["wax"]},
            {},
            {"crayon": ["wax"]},
        )

    def test_a_specialisation_is_recorded(self) -> None:
        self.assertEqual(self.chain().generalisations_of("crayon"), frozenset({"wax"}))

    def test_a_sound_chain_validates(self) -> None:
        self.assertEqual(self.chain().validate(), [])

    def test_specialising_a_formal_structure_is_rejected(self) -> None:
        g = ConceptGraph([concept("a", "m"), structure("s")], {}, {}, {"a": ["s"]})
        self.assertIn("bad-specialises-target", codes(g))

    def test_a_formal_structure_may_not_specialise(self) -> None:
        g = ConceptGraph([structure("s"), concept("a", "m")], {}, {}, {"s": ["a"]})
        self.assertIn("bad-specialises-source", codes(g))

    def test_specialising_an_undeclared_node_is_rejected(self) -> None:
        g = ConceptGraph([concept("a", "m")], {}, {}, {"a": ["ghost"]})
        self.assertIn("unknown-target", codes(g))

    def test_self_specialisation_is_rejected(self) -> None:
        g = ConceptGraph([concept("a", "m")], {}, {}, {"a": ["a"]})
        self.assertIn("self-loop", codes(g))


class TestReach(unittest.TestCase):
    def chain(self) -> ConceptGraph:
        return ConceptGraph(
            [concept(x, "materials") for x in ("crayon", "teddy", "wax", "fuel")],
            {"fuel": ["wax"]},
            {},
            {"crayon": ["wax"]},
        )

    def test_downstream_reach_counts_what_rests_on_a_concept(self) -> None:
        self.assertEqual(self.chain().downstream_reach()["wax"], 2)

    def test_an_anchor_has_no_downstream_reach(self) -> None:
        reach = self.chain().downstream_reach()
        self.assertEqual(reach["crayon"], 0)
        self.assertEqual(reach["teddy"], 0)

    def test_anchor_reach_separates_a_useful_anchor_from_a_useless_one(self) -> None:
        """The whole point. Downstream reach cannot tell these apart."""
        anchors = self.chain().anchor_reach()
        self.assertGreater(anchors["crayon"], 0)
        self.assertEqual(anchors["teddy"], 0)

    def test_anchor_reach_includes_what_rests_on_the_anchored_concept(self) -> None:
        # crayon anchors wax, and fuel rests on wax
        self.assertEqual(self.chain().anchor_reach()["crayon"], 2)

    def test_a_concept_does_not_count_itself(self) -> None:
        self.assertNotIn(-1, self.chain().anchor_reach().values())


class TestDomainRegistry(unittest.TestCase):
    """Domains are declared, not inferred from membership.

    The registry exists so that a domain decided upon but not yet written can
    be seen. Inference cannot represent that state at all, which is why these
    cases are about absence rather than about presence.
    """

    def test_declared_domain_with_no_concepts_is_not_a_violation(self) -> None:
        g = ConceptGraph(
            [concept("a", "math")],
            {},
            {},
            domains=[Domain("math", "n"), Domain("later", "awaiting content")],
        )
        self.assertEqual(g.validate(), [])
        self.assertEqual(g.empty_domains(), ["later"])

    def test_undeclared_domain_is_a_violation(self) -> None:
        g = ConceptGraph(
            [concept("a", "math"), concept("b", "smuggled")],
            {},
            {},
            domains=[Domain("math", "n")],
        )
        self.assertIn("undeclared-domain", codes(g))

    def test_registry_absent_means_the_check_is_skipped(self) -> None:
        """A test fragment must not be obliged to carry the registry."""
        g = ConceptGraph([concept("a", "anything")], {}, {})
        self.assertNotIn("undeclared-domain", codes(g))
        self.assertEqual(g.empty_domains(), [])

    def test_formal_structures_are_exempt_from_declaration(self) -> None:
        g = ConceptGraph(
            [concept("a", "math"), structure("s")],
            {},
            {"a": ["s"]},
            domains=[Domain("math", "n")],
        )
        self.assertNotIn("undeclared-domain", codes(g))

    def test_concepts_in_reports_membership(self) -> None:
        g = ConceptGraph(
            [concept("a", "math"), concept("b", "math"), concept("c", "other")],
            {},
            {},
            domains=[Domain("math", "n"), Domain("other", "n")],
        )
        self.assertEqual(g.concepts_in("math"), frozenset({"a", "b"}))
        self.assertEqual(g.concepts_in("absent"), frozenset())

    def test_domains_round_trip_through_json(self) -> None:
        payload = {
            "domains": [{"id": "math", "note": "quantity and proof"}],
            "nodes": [
                {"id": "a", "name": "a", "kind": "domain_concept", "domain": "math"}
            ],
            "prerequisites": {},
            "instantiates": {},
        }
        g = ConceptGraph.from_json(payload)
        self.assertEqual(sorted(g.domains), ["math"])
        self.assertEqual(g.domains["math"].note, "quantity and proof")
        self.assertEqual(g.validate(), [])

    def test_malformed_registry_is_rejected_at_the_boundary(self) -> None:
        for bad in (
            {"domains": "math"},
            {"domains": ["math"]},
            {"domains": [{"id": "math"}]},
            {"domains": [{"id": 1, "note": "n"}]},
        ):
            with self.subTest(bad=bad):
                payload = {
                    "nodes": [],
                    "prerequisites": {},
                    "instantiates": {},
                    **bad,
                }
                with self.assertRaises(ValueError):
                    ConceptGraph.from_json(payload)
