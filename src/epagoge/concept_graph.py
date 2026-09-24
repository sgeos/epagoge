"""Concept graph.

The graph that constrains curriculum ordering and supplies structural
difficulty. Specification in ``docs/spec/CONCEPT_GRAPH.md``.

Standard library only. This module is deliberately dependency-free so that
the graph can be validated before any environment decisions are settled.
"""

from __future__ import annotations

import json
import random
from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Final, Iterable, Mapping, Sequence


class NodeKind(Enum):
    """Whether a node belongs to a domain or to the formal layer."""

    DOMAIN_CONCEPT = "domain_concept"
    FORMAL_STRUCTURE = "formal_structure"


@dataclass(frozen=True, slots=True)
class Node:
    """A concept or a formal structure.

    ``domain`` is required for a domain concept and must be absent for a
    formal structure. A structure confined to one domain cannot carry
    transfer, which is the reason for the asymmetry.
    """

    id: str
    name: str
    kind: NodeKind
    domain: str | None = None


@dataclass(frozen=True, slots=True)
class Violation:
    """A single invariant breach.

    Validation collects these rather than raising, so that a graph can be
    audited in one pass instead of one problem at a time.
    """

    code: str
    detail: str


_ROOT_DEPTH: Final[int] = 0


class ConceptGraph:
    """A validated concept graph.

    Construction does not validate. Call :meth:`validate` and inspect the
    result. Every method that depends on acyclicity states so, because a
    caller who skips validation would otherwise get a silent wrong answer
    rather than a loud one.
    """

    def __init__(
        self,
        nodes: Iterable[Node],
        prerequisites: Mapping[str, Iterable[str]],
        instantiates: Mapping[str, Iterable[str]],
    ) -> None:
        self._nodes: dict[str, Node] = {n.id: n for n in nodes}
        self._prerequisites: dict[str, frozenset[str]] = {
            k: frozenset(v) for k, v in prerequisites.items()
        }
        self._instantiates: dict[str, frozenset[str]] = {
            k: frozenset(v) for k, v in instantiates.items()
        }

    # -- accessors ---------------------------------------------------------

    @property
    def nodes(self) -> Mapping[str, Node]:
        return self._nodes

    def prerequisites_of(self, node_id: str) -> frozenset[str]:
        return self._prerequisites.get(node_id, frozenset())

    def structures_of(self, node_id: str) -> frozenset[str]:
        return self._instantiates.get(node_id, frozenset())

    # -- validation --------------------------------------------------------

    def validate(self) -> list[Violation]:
        """Return every invariant breach. An empty list means the graph is sound."""
        out: list[Violation] = []
        out.extend(self._check_references())
        out.extend(self._check_self_loops())
        out.extend(self._check_kind_rules())
        out.extend(self._check_layering())
        out.extend(self._check_acyclic())
        return out

    def _check_references(self) -> list[Violation]:
        out: list[Violation] = []
        for src, targets in (*self._prerequisites.items(), *self._instantiates.items()):
            if src not in self._nodes:
                out.append(Violation("unknown-source", f"edge from undeclared node {src!r}"))
            for t in targets:
                if t not in self._nodes:
                    out.append(
                        Violation("unknown-target", f"edge {src!r} -> undeclared node {t!r}")
                    )
        return out

    def _check_self_loops(self) -> list[Violation]:
        out: list[Violation] = []
        for src, targets in (*self._prerequisites.items(), *self._instantiates.items()):
            if src in targets:
                out.append(Violation("self-loop", f"node {src!r} points at itself"))
        return out

    def _check_kind_rules(self) -> list[Violation]:
        out: list[Violation] = []
        for node in self._nodes.values():
            if node.kind is NodeKind.DOMAIN_CONCEPT and node.domain is None:
                out.append(Violation("missing-domain", f"domain concept {node.id!r} declares no domain"))
            if node.kind is NodeKind.FORMAL_STRUCTURE and node.domain is not None:
                out.append(
                    Violation("domained-structure", f"formal structure {node.id!r} declares a domain")
                )
        for src, targets in self._instantiates.items():
            s = self._nodes.get(src)
            if s is not None and s.kind is not NodeKind.DOMAIN_CONCEPT:
                out.append(Violation("bad-instantiates-source", f"{src!r} is not a domain concept"))
            for t in targets:
                node = self._nodes.get(t)
                if node is not None and node.kind is not NodeKind.FORMAL_STRUCTURE:
                    out.append(
                        Violation("bad-instantiates-target", f"{t!r} is not a formal structure")
                    )
        return out

    def _check_layering(self) -> list[Violation]:
        """The formal layer does not depend on the domains that instantiate it."""
        out: list[Violation] = []
        for src, targets in self._prerequisites.items():
            s = self._nodes.get(src)
            if s is None or s.kind is not NodeKind.FORMAL_STRUCTURE:
                continue
            for t in targets:
                node = self._nodes.get(t)
                if node is not None and node.kind is NodeKind.DOMAIN_CONCEPT:
                    out.append(
                        Violation(
                            "layering",
                            f"formal structure {src!r} requires domain concept {t!r}",
                        )
                    )
        return out

    def _check_acyclic(self) -> list[Violation]:
        colour: dict[str, int] = {}  # 0 unvisited, 1 on stack, 2 done
        out: list[Violation] = []

        def walk(start: str) -> None:
            stack: list[tuple[str, list[str]]] = [(start, sorted(self.prerequisites_of(start)))]
            colour[start] = 1
            path: list[str] = [start]
            while stack:
                node, pending = stack[-1]
                if not pending:
                    colour[node] = 2
                    stack.pop()
                    path.pop()
                    continue
                nxt = pending.pop()
                if nxt not in self._nodes:
                    continue
                state = colour.get(nxt, 0)
                if state == 1:
                    cycle = " -> ".join([*path, nxt])
                    out.append(Violation("cycle", f"prerequisite cycle: {cycle}"))
                    continue
                if state == 2:
                    continue
                colour[nxt] = 1
                path.append(nxt)
                stack.append((nxt, sorted(self.prerequisites_of(nxt))))

        for node_id in sorted(self._nodes):
            if colour.get(node_id, 0) == 0:
                walk(node_id)
        return out

    # -- derived structure -------------------------------------------------

    def prerequisite_depth(self) -> dict[str, int]:
        """Longest path from a root, per node. Requires an acyclic graph.

        Longest rather than shortest: a concept is reachable only once every
        prerequisite is satisfied, so its earliest admissible position is
        governed by its deepest dependency.
        """
        depth: dict[str, int] = {}

        def resolve(node_id: str, seen: frozenset[str]) -> int:
            if node_id in depth:
                return depth[node_id]
            if node_id in seen:
                raise ValueError(f"cycle through {node_id!r}; call validate() first")
            prereqs = [p for p in self.prerequisites_of(node_id) if p in self._nodes]
            value = (
                _ROOT_DEPTH
                if not prereqs
                else 1 + max(resolve(p, seen | {node_id}) for p in prereqs)
            )
            depth[node_id] = value
            return value

        for node_id in sorted(self._nodes):
            resolve(node_id, frozenset())
        return depth

    def transfer_edges(self) -> set[tuple[str, str]]:
        """Derived cross-domain pairs sharing a formal structure.

        Same-domain sharing is not transfer. It is ordinary structure within
        a subject. Pairs are returned with the lower identifier first so the
        relation is symmetric and deduplicated.
        """
        by_structure: dict[str, list[str]] = defaultdict(list)
        for concept_id, structures in self._instantiates.items():
            node = self._nodes.get(concept_id)
            if node is None or node.kind is not NodeKind.DOMAIN_CONCEPT:
                continue
            for s in structures:
                by_structure[s].append(concept_id)

        out: set[tuple[str, str]] = set()
        for members in by_structure.values():
            for i, a in enumerate(sorted(members)):
                for b in sorted(members)[i + 1 :]:
                    da = self._nodes[a].domain
                    db = self._nodes[b].domain
                    if da is not None and db is not None and da != db:
                        out.add((a, b))
        return out

    # -- orderings ---------------------------------------------------------

    def canonical_order(self) -> list[str]:
        """Deterministic topological order, ties broken by identifier.

        Reproducible across runs and machines, which the ablation requires.
        """
        return self._kahn(lambda frontier: min(frontier))

    def random_linear_extension(self, rng: random.Random) -> list[str]:
        """A random topological order. The experimental control.

        NOT uniform over linear extensions. Counting them is #P-complete,
        and frontier-uniform selection biases toward orderings that keep the
        frontier wide. Uniformity is not required for the control, whose
        purpose is to discard the curriculum trajectory while respecting the
        constraints. See docs/spec/CONCEPT_GRAPH.md.
        """
        return self._kahn(lambda frontier: rng.choice(sorted(frontier)))

    def _kahn(self, pick: object) -> list[str]:
        remaining: dict[str, set[str]] = {
            n: {p for p in self.prerequisites_of(n) if p in self._nodes} for n in self._nodes
        }
        dependents: dict[str, set[str]] = defaultdict(set)
        for node_id, prereqs in remaining.items():
            for p in prereqs:
                dependents[p].add(node_id)

        frontier: set[str] = {n for n, p in remaining.items() if not p}
        order: list[str] = []
        chooser = pick  # typed loosely; callers pass a Callable[[set[str]], str]
        while frontier:
            chosen: str = chooser(frontier)  # type: ignore[operator]
            frontier.discard(chosen)
            order.append(chosen)
            for d in sorted(dependents[chosen]):
                remaining[d].discard(chosen)
                if not remaining[d]:
                    frontier.add(d)
        if len(order) != len(self._nodes):
            raise ValueError("graph is cyclic; call validate() first")
        return order

    # -- serialisation -----------------------------------------------------

    @classmethod
    def from_json(cls, payload: Mapping[str, object]) -> ConceptGraph:
        raw_nodes = payload.get("nodes", [])
        if not isinstance(raw_nodes, Sequence):
            raise ValueError("'nodes' must be a list")
        nodes: list[Node] = []
        for entry in raw_nodes:
            if not isinstance(entry, Mapping):
                raise ValueError("each node must be an object")
            nodes.append(
                Node(
                    id=str(entry["id"]),
                    name=str(entry["name"]),
                    kind=NodeKind(str(entry["kind"])),
                    domain=None if entry.get("domain") is None else str(entry["domain"]),
                )
            )
        prereq = payload.get("prerequisites", {})
        inst = payload.get("instantiates", {})
        if not isinstance(prereq, Mapping) or not isinstance(inst, Mapping):
            raise ValueError("'prerequisites' and 'instantiates' must be objects")
        return cls(
            nodes,
            {str(k): [str(x) for x in v] for k, v in prereq.items()},  # type: ignore[union-attr]
            {str(k): [str(x) for x in v] for k, v in inst.items()},  # type: ignore[union-attr]
        )

    @classmethod
    def load(cls, path: Path) -> ConceptGraph:
        return cls.from_json(json.loads(path.read_text(encoding="utf-8")))
