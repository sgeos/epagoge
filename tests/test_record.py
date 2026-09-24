"""Tests for the corpus record schema and corpus validation.

Weighted toward negative cases. Every rule in docs/spec/RECORD_SCHEMA.md has
a test that breaks it, because a validator shown only valid input has not
been tested.
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from epagoge.concept_graph import ConceptGraph, Node, NodeKind
from epagoge.record import (
    ClaimClass,
    Provenance,
    Record,
    Simplification,
    SimplificationKind,
    load_corpus,
    load_primitives,
    record_from_json,
    validate_corpus,
    validate_record,
)


def graph() -> ConceptGraph:
    return ConceptGraph(
        [
            Node("a", "a", NodeKind.DOMAIN_CONCEPT, "math"),
            Node("b", "b", NodeKind.DOMAIN_CONCEPT, "math"),
            Node("c", "c", NodeKind.DOMAIN_CONCEPT, "math"),
        ],
        {"b": ["a"], "c": ["b"]},
        {},
    )


def rec(
    record_id: str = "r1",
    level: int = 1,
    concepts: tuple[str, ...] = ("a",),
    claim_class: ClaimClass = ClaimClass.EMPIRICAL,
    provenance: Provenance | None = None,
    simplification: Simplification | None = None,
) -> Record:
    return Record(
        id=record_id,
        level=level,
        concepts=concepts,
        claim_class=claim_class,
        content="text",
        provenance=provenance or Provenance(source_claim="src:1"),
        simplification=simplification or Simplification(),
    )


def codes(violations: list[object]) -> set[str]:
    return {v.code for v in violations}  # type: ignore[attr-defined]


class TestRecordRules(unittest.TestCase):
    def test_valid_record_passes(self) -> None:
        self.assertEqual(validate_record(rec(), graph()), [])

    def test_level_out_of_range(self) -> None:
        self.assertIn("level-range", codes(validate_record(rec(level=8), graph())))
        self.assertIn("level-range", codes(validate_record(rec(level=0), graph())))

    def test_no_concepts(self) -> None:
        self.assertIn("no-concepts", codes(validate_record(rec(concepts=()), graph())))

    def test_unknown_concept(self) -> None:
        self.assertIn(
            "unknown-concept", codes(validate_record(rec(concepts=("ghost",)), graph()))
        )

    def test_empty_content(self) -> None:
        r = Record("r", 1, ("a",), ClaimClass.EMPIRICAL, "   ", Provenance("s"))
        self.assertIn("empty-content", codes(validate_record(r, graph())))

    def test_unsupported_class_is_always_rejected(self) -> None:
        r = rec(claim_class=ClaimClass.UNSUPPORTED)
        self.assertIn("unsupported", codes(validate_record(r, graph())))


class TestClassRequirements(unittest.TestCase):
    def test_empirical_requires_source(self) -> None:
        r = rec(claim_class=ClaimClass.EMPIRICAL, provenance=Provenance())
        self.assertIn("missing-provenance", codes(validate_record(r, graph())))

    def test_formal_requires_source(self) -> None:
        r = rec(claim_class=ClaimClass.FORMAL, provenance=Provenance())
        self.assertIn("missing-provenance", codes(validate_record(r, graph())))

    def test_attributed_position_requires_a_holder(self) -> None:
        r = rec(claim_class=ClaimClass.ATTRIBUTED_POSITION, provenance=Provenance())
        self.assertIn("missing-provenance", codes(validate_record(r, graph())))

    def test_attributed_position_with_a_holder_passes(self) -> None:
        r = rec(
            claim_class=ClaimClass.ATTRIBUTED_POSITION,
            provenance=Provenance(position_holder="Popper"),
        )
        self.assertEqual(validate_record(r, graph()), [])

    def test_normative_requires_a_holder(self) -> None:
        r = rec(claim_class=ClaimClass.NORMATIVE, provenance=Provenance())
        self.assertIn("missing-provenance", codes(validate_record(r, graph())))

    def test_conditional_result_requires_all_three_fields(self) -> None:
        r = rec(
            claim_class=ClaimClass.CONDITIONAL_RESULT,
            provenance=Provenance(assumptions=("x",), method="sim"),
        )
        self.assertIn("missing-provenance", codes(validate_record(r, graph())))

    def test_conditional_result_complete_passes(self) -> None:
        r = rec(
            claim_class=ClaimClass.CONDITIONAL_RESULT,
            provenance=Provenance(
                assumptions=("x",), method="sim", validation_status="unvalidated"
            ),
        )
        self.assertEqual(validate_record(r, graph()), [])

    def test_conditional_result_rejects_empty_assumptions(self) -> None:
        r = rec(
            claim_class=ClaimClass.CONDITIONAL_RESULT,
            provenance=Provenance(method="sim", validation_status="none"),
        )
        self.assertIn("missing-provenance", codes(validate_record(r, graph())))


class TestSimplification(unittest.TestCase):
    def simplified(
        self, level: int = 2, scope: tuple[int, int] | None = (1, 3)
    ) -> Record:
        return rec(
            level=level,
            simplification=Simplification(
                SimplificationKind.SUPERSEDED_MODEL, scope, "r_later"
            ),
        )

    def test_simplified_record_is_well_formed(self) -> None:
        self.assertEqual(validate_record(self.simplified(), graph()), [])

    def test_simplified_without_scope_is_rejected(self) -> None:
        self.assertIn(
            "no-scope", codes(validate_record(self.simplified(scope=None), graph()))
        )

    def test_simplified_without_correction_is_rejected(self) -> None:
        r = rec(simplification=Simplification(SimplificationKind.ANALOGY, (1, 3), None))
        self.assertIn("no-supersession", codes(validate_record(r, graph())))

    def test_level_outside_its_own_scope_is_rejected(self) -> None:
        r = self.simplified(level=5, scope=(1, 3))
        self.assertIn("scope-excludes-level", codes(validate_record(r, graph())))

    def test_inverted_scope_is_rejected(self) -> None:
        r = self.simplified(level=2, scope=(4, 2))
        self.assertIn("bad-scope", codes(validate_record(r, graph())))

    def test_terminal_level_may_not_be_simplified(self) -> None:
        r = self.simplified(level=7, scope=(1, 7))
        self.assertIn("terminal-simplified", codes(validate_record(r, graph())))

    def test_unsimplified_record_may_not_declare_scope(self) -> None:
        r = rec(simplification=Simplification(SimplificationKind.NONE, (1, 3), None))
        self.assertIn("spurious-simplification", codes(validate_record(r, graph())))


class TestCorpusRules(unittest.TestCase):
    def test_duplicate_id(self) -> None:
        out = validate_corpus([rec("dup"), rec("dup")], graph())
        self.assertIn("duplicate-id", codes(out))

    def test_supersession_must_resolve(self) -> None:
        r = rec(
            simplification=Simplification(SimplificationKind.OMISSION, (1, 3), "ghost")
        )
        self.assertIn("dangling-supersession", codes(validate_corpus([r], graph())))

    def test_supersession_must_point_later(self) -> None:
        early = rec(
            "early",
            level=3,
            simplification=Simplification(SimplificationKind.OMISSION, (1, 3), "late"),
        )
        late = rec("late", level=2)
        self.assertIn(
            "supersession-order", codes(validate_corpus([early, late], graph()))
        )

    def test_prerequisite_never_taught(self) -> None:
        out = validate_corpus([rec("r", 1, ("b",))], graph())
        self.assertIn("prerequisite-untaught", codes(out))

    def test_prerequisite_taught_too_late(self) -> None:
        out = validate_corpus([rec("r_b", 1, ("b",)), rec("r_a", 3, ("a",))], graph())
        self.assertIn("prerequisite-late", codes(out))

    def test_prerequisite_taught_at_the_same_level_is_allowed(self) -> None:
        out = validate_corpus([rec("r_a", 2, ("a",)), rec("r_b", 2, ("b",))], graph())
        self.assertEqual(out, [])

    def test_a_well_formed_corpus_passes(self) -> None:
        out = validate_corpus(
            [rec("r_a", 1, ("a",)), rec("r_b", 2, ("b",)), rec("r_c", 3, ("c",))],
            graph(),
        )
        self.assertEqual(out, [])


class TestBoundaryParsing(unittest.TestCase):
    def minimal(self) -> dict[str, object]:
        return {
            "id": "r",
            "level": 1,
            "concepts": ["a"],
            "claim_class": "empirical",
            "content": "text",
            "provenance": {"source_claim": "s"},
        }

    def test_minimal_record_parses(self) -> None:
        self.assertEqual(record_from_json(self.minimal()).id, "r")

    def test_payload_must_be_an_object(self) -> None:
        with self.assertRaises(ValueError):
            record_from_json(["not", "an", "object"])

    def test_level_must_be_an_integer(self) -> None:
        body = self.minimal() | {"level": "1"}
        with self.assertRaises(ValueError):
            record_from_json(body)

    def test_boolean_is_not_accepted_as_a_level(self) -> None:
        body = self.minimal() | {"level": True}
        with self.assertRaises(ValueError):
            record_from_json(body)

    def test_unknown_claim_class_is_rejected(self) -> None:
        body = self.minimal() | {"claim_class": "vibes"}
        with self.assertRaises(ValueError):
            record_from_json(body)

    def test_concepts_must_be_strings(self) -> None:
        body = self.minimal() | {"concepts": [1]}
        with self.assertRaises(ValueError):
            record_from_json(body)

    def test_validity_scope_must_be_a_pair(self) -> None:
        body = self.minimal() | {
            "simplification": {"kind": "omission", "validity_scope": [1]}
        }
        with self.assertRaises(ValueError):
            record_from_json(body)

    def test_validity_scope_must_hold_integers(self) -> None:
        body = self.minimal() | {
            "simplification": {"kind": "omission", "validity_scope": ["1", "3"]}
        }
        with self.assertRaises(ValueError):
            record_from_json(body)


class TestPrimitiveRegister(unittest.TestCase):
    """Level one grounds in a hand-authored register, not in citations.

    The register is where an unsupported assertion does the most damage,
    since everything above it inherits the error, so the guard that a
    generator cannot extend it is tested harder than the happy path.
    """

    def primitive_record(self, name: str) -> Record:
        return rec(provenance=Provenance(source_claim=f"primitive:{name}"))

    def test_a_registered_primitive_passes(self) -> None:
        out = validate_corpus(
            [self.primitive_record("things-break")], graph(), {"things-break"}
        )
        self.assertEqual(out, [])

    def test_an_unregistered_primitive_is_rejected(self) -> None:
        out = validate_corpus(
            [self.primitive_record("hard-work-brings-success")],
            graph(),
            {"things-break"},
        )
        self.assertIn("unregistered-primitive", codes(out))

    def test_citing_a_primitive_with_no_register_is_reported(self) -> None:
        out = validate_corpus([self.primitive_record("things-break")], graph(), None)
        self.assertIn("no-register", codes(out))

    def test_an_ordinary_source_is_unaffected_by_the_register(self) -> None:
        out = validate_corpus([rec()], graph(), {"things-break"})
        self.assertEqual(out, [])

    def test_an_ordinary_source_needs_no_register(self) -> None:
        self.assertEqual(validate_corpus([rec()], graph(), None), [])

    def test_the_prefix_is_matched_exactly(self) -> None:
        r = rec(provenance=Provenance(source_claim="primitives:things-break"))
        self.assertEqual(validate_corpus([r], graph(), None), [])


class TestRegisterLoading(unittest.TestCase):
    def setUp(self) -> None:
        self._dir = tempfile.TemporaryDirectory()
        self.addCleanup(self._dir.cleanup)

    def write(self, payload: object) -> Path:
        path = Path(self._dir.name) / "primitives.json"
        path.write_text(json.dumps(payload), encoding="utf-8")
        return path

    def test_a_well_formed_register_loads(self) -> None:
        path = self.write(
            {"primitives": [{"id": "a", "observation": "a thing is observed"}]}
        )
        self.assertEqual(load_primitives(path), {"a": "a thing is observed"})

    def test_a_register_must_be_an_object(self) -> None:
        with self.assertRaises(ValueError):
            load_primitives(self.write([{"id": "a"}]))

    def test_a_register_must_hold_a_list(self) -> None:
        with self.assertRaises(ValueError):
            load_primitives(self.write({"primitives": {"id": "a"}}))

    def test_every_entry_needs_a_grounding_observation(self) -> None:
        with self.assertRaises(ValueError):
            load_primitives(self.write({"primitives": [{"id": "a"}]}))

    def test_duplicate_identifiers_are_rejected(self) -> None:
        payload = {
            "primitives": [
                {"id": "a", "observation": "one"},
                {"id": "a", "observation": "two"},
            ]
        }
        with self.assertRaises(ValueError):
            load_primitives(self.write(payload))

    def test_the_shipped_register_loads_and_every_entry_is_grounded(self) -> None:
        register = load_primitives(Path("curriculum/primitives.json"))
        self.assertGreater(len(register), 20)
        self.assertTrue(all(v.strip() for v in register.values()))


class TestCorpusLoading(unittest.TestCase):
    def setUp(self) -> None:
        self._dir = tempfile.TemporaryDirectory()
        self.addCleanup(self._dir.cleanup)

    def write(self, text: str) -> Path:
        path = Path(self._dir.name) / "corpus.jsonl"
        path.write_text(text, encoding="utf-8")
        return path

    def test_blank_lines_are_skipped(self) -> None:
        body = json.dumps(
            {
                "id": "r",
                "level": 1,
                "concepts": ["a"],
                "claim_class": "empirical",
                "content": "text",
                "provenance": {"source_claim": "s"},
            }
        )
        path = self.write(f"\n{body}\n\n")
        self.assertEqual(len(load_corpus(path)), 1)

    def test_a_bad_line_reports_its_line_number(self) -> None:
        path = self.write('{"id": 1}\n')
        with self.assertRaises(ValueError) as ctx:
            load_corpus(path)
        self.assertIn(":1:", str(ctx.exception))

    def test_provenance_must_be_an_object(self) -> None:
        with self.assertRaises(ValueError):
            record_from_json(
                {
                    "id": "r",
                    "level": 1,
                    "concepts": ["a"],
                    "claim_class": "empirical",
                    "content": "t",
                    "provenance": "source",
                }
            )

    def test_simplification_must_be_an_object(self) -> None:
        with self.assertRaises(ValueError):
            record_from_json(
                {
                    "id": "r",
                    "level": 1,
                    "concepts": ["a"],
                    "claim_class": "empirical",
                    "content": "t",
                    "provenance": {"source_claim": "s"},
                    "simplification": "none",
                }
            )

    def test_concepts_absent_from_the_graph_are_ignored_by_coverage(self) -> None:
        out = validate_corpus([rec("r", 1, ("ghost",))], graph())
        self.assertIn("unknown-concept", codes(out))
        self.assertNotIn("prerequisite-untaught", codes(out))

    def test_a_normative_record_with_a_holder_passes(self) -> None:
        r = rec(
            claim_class=ClaimClass.NORMATIVE,
            provenance=Provenance(position_holder="the operator"),
        )
        self.assertEqual(validate_record(r, graph()), [])


if __name__ == "__main__":
    unittest.main()


class TestRelationCoverage(unittest.TestCase):
    """A specialisation in the graph must be taught somewhere in the corpus.

    The relation is content, not only structure. A graph that says a teddy
    bear is a toy, with no record teaching it, asserts a link the model never
    reads.
    """

    def graph_with_relation(self) -> ConceptGraph:
        return ConceptGraph(
            [
                Node("teddy", "teddy", NodeKind.DOMAIN_CONCEPT, "everyday"),
                Node("toy", "toy", NodeKind.DOMAIN_CONCEPT, "everyday"),
            ],
            {},
            {},
            {"teddy": ["toy"]},
        )

    def test_an_untaught_relation_is_reported(self) -> None:
        records = [rec("r", 1, ("teddy",)), rec("s", 1, ("toy",))]
        out = validate_corpus(records, self.graph_with_relation())
        self.assertIn("relation-untaught", codes(out))

    def test_a_record_covering_both_endpoints_teaches_it(self) -> None:
        records = [rec("r", 1, ("teddy", "toy"))]
        out = validate_corpus(records, self.graph_with_relation())
        self.assertNotIn("relation-untaught", codes(out))

    def test_covering_the_endpoints_separately_is_not_enough(self) -> None:
        """Two records mentioning each end never state the relation between them."""
        records = [
            rec("r", 1, ("teddy",)),
            rec("s", 2, ("toy",)),
            rec("t", 3, ("teddy",)),
        ]
        out = validate_corpus(records, self.graph_with_relation())
        self.assertIn("relation-untaught", codes(out))

    def test_a_graph_without_specialisations_passes_vacuously(self) -> None:
        out = validate_corpus([rec("r", 1, ("a",))], graph())
        self.assertNotIn("relation-untaught", codes(out))

    def test_the_illustrative_corpus_teaches_its_taxonomy(self) -> None:
        from epagoge.record import load_corpus

        g = ConceptGraph.load(Path("docs/spec/examples/enabling_chain.json"))
        records = load_corpus(Path("docs/spec/examples/enabling_corpus.jsonl"))
        untaught = {
            v.detail
            for v in validate_corpus(records, g)
            if v.code == "relation-untaught"
        }
        for pair in (
            "'teddy_bear' is a kind of 'toy'",
            "'square' is a kind of 'rectangle'",
        ):
            self.assertFalse(
                any(pair in d for d in untaught), f"{pair} should be taught"
            )
