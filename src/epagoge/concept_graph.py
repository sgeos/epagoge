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
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Final, cast


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
class Domain:
    """A declared subject area.

    Domains are declared rather than inferred from node membership. An
    inferred set cannot distinguish a domain that holds no concepts yet from
    one that was never intended, so a domain awaiting content would be
    invisible exactly when it most needs to be visible.
    """

    id: str
    note: str


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
        specialises: Mapping[str, Iterable[str]] | None = None,
        domains: Iterable[Domain] | None = None,
    ) -> None:
        self._nodes: dict[str, Node] = {n.id: n for n in nodes}
        self._domains: dict[str, Domain] = {d.id: d for d in (domains or ())}
        self._prerequisites: dict[str, frozenset[str]] = {
            k: frozenset(v) for k, v in prerequisites.items()
        }
        self._instantiates: dict[str, frozenset[str]] = {
            k: frozenset(v) for k, v in instantiates.items()
        }
        self._specialises: dict[str, frozenset[str]] = {
            k: frozenset(v) for k, v in (specialises or {}).items()
        }

    # -- accessors ---------------------------------------------------------

    @property
    def nodes(self) -> Mapping[str, Node]:
        return self._nodes

    @property
    def domains(self) -> Mapping[str, Domain]:
        """Declared domains, whether or not any concept belongs to one."""
        return self._domains

    def concepts_in(self, domain_id: str) -> frozenset[str]:
        return frozenset(
            n for n, node in self._nodes.items() if node.domain == domain_id
        )

    def isolated_concepts(self) -> list[str]:
        """Concepts carrying no edge of any kind, in either direction.

        Stronger than an unreached concept. A node here is not merely
        depended on by nothing, it participates in no relation at all, so it
        contributes vocabulary and no structure.
        """
        touched: set[str] = set()
        for layer in (self._prerequisites, self._instantiates, self._specialises):
            for target, sources in layer.items():
                touched.add(target)
                touched.update(sources)
        return sorted(n for n in self._nodes if n not in touched)

    def cross_domain_prerequisites(self) -> list[tuple[str, str]]:
        """Prerequisite edges whose endpoints sit in different domains.

        Reported because both the presence and the absence of these are
        claims about the curriculum. Zero asserts that every domain can be
        taught without any other, which is a strong claim and is more likely
        to mean the edges have not been drawn.
        """
        out: list[tuple[str, str]] = []
        for target, sources in self._prerequisites.items():
            t = self._nodes.get(target)
            for source in sources:
                s = self._nodes.get(source)
                if t is None or s is None or s.domain is None or t.domain is None:
                    continue
                if s.domain != t.domain:
                    out.append((target, source))
        return sorted(out)

    def within_domain_depth(self, domain_id: str) -> int:
        """Longest prerequisite path using only edges inside one domain.

        Distinct from :meth:`prerequisite_depth`, which measures distance
        from a global root and therefore rises for every domain sitting
        downstream of a deep one. Once domains are connected, global depth
        stops describing a domain's own structure and starts describing
        where it sits in the graph. The ordering ablation contrasts internal
        structure, so it needs this quantity and not that one.
        """
        members = self.concepts_in(domain_id)
        memo: dict[str, int] = {}

        def depth_of(node_id: str) -> int:
            cached = memo.get(node_id)
            if cached is not None:
                return cached
            memo[node_id] = _ROOT_DEPTH
            inside = [p for p in self.prerequisites_of(node_id) if p in members]
            value = 1 + max((depth_of(p) for p in inside), default=-1) if inside else 0
            memo[node_id] = value
            return value

        return max((depth_of(n) for n in members), default=_ROOT_DEPTH)

    def inert_structures(self) -> list[str]:
        """Formal structures instantiated fewer than twice.

        A structure needs two instantiations in different domains to yield a
        transfer edge. One or none makes it declared and load-free.
        """
        counts: dict[str, int] = {}
        for sources in self._instantiates.values():
            for s in sources:
                counts[s] = counts.get(s, 0) + 1
        return sorted(
            n.id
            for n in self._nodes.values()
            if n.kind is NodeKind.FORMAL_STRUCTURE and counts.get(n.id, 0) < 2
        )

    def empty_domains(self) -> list[str]:
        """Declared domains holding no concept.

        Reported rather than rejected. A domain is declared once decided and
        populated once content exists, so emptiness is an expected interim
        state that should be visible rather than an error.
        """
        return sorted(d for d in self._domains if not self.concepts_in(d))

    def prerequisites_of(self, node_id: str) -> frozenset[str]:
        return self._prerequisites.get(node_id, frozenset())

    def structures_of(self, node_id: str) -> frozenset[str]:
        return self._instantiates.get(node_id, frozenset())

    def generalisations_of(self, node_id: str) -> frozenset[str]:
        """Concepts this one is a concrete instance of."""
        return self._specialises.get(node_id, frozenset())

    def downstream_reach(self) -> dict[str, int]:
        """How many concepts each concept eventually unlocks.

        Counts everything transitively reachable by following prerequisite
        and specialisation edges in reverse, so a concept's reach is the set
        of things that depend on it however remotely.

        This measures foundational importance: how much rests on a concept.
        It is **not** the right measure for a concrete anchor, which is a
        leaf and on which nothing rests. For that see :meth:`anchor_reach`.
        """
        dependents: dict[str, set[str]] = defaultdict(set)
        for node_id in self._nodes:
            for target in self.prerequisites_of(node_id) | self.generalisations_of(
                node_id
            ):
                if target in self._nodes:
                    dependents[target].add(node_id)

        out: dict[str, int] = {}
        for start in self._nodes:
            seen: set[str] = set()
            stack = list(dependents[start])
            while stack:
                node = stack.pop()
                if node in seen:
                    continue
                seen.add(node)
                stack.extend(dependents[node] - seen)
            out[start] = len(seen)
        return out

    # -- validation --------------------------------------------------------

    def validate(self) -> list[Violation]:
        """Return every invariant breach. An empty list means the graph is sound."""
        out: list[Violation] = []
        out.extend(self._check_references())
        out.extend(self._check_self_loops())
        out.extend(self._check_kind_rules())
        out.extend(self._check_domain_declarations())
        out.extend(self._check_layering())
        out.extend(self._check_specialisation())
        out.extend(self._check_acyclic())
        return out

    def anchor_reach(self) -> dict[str, int]:
        """What a concept gives concrete access to, through specialisation.

        Follows specialisation edges forward to the abstractions a concept
        instantiates, then counts everything that rests on those.

        **This is what lets a concrete concept earn a place at level one.**
        A human curriculum introduces crayons because children use crayons. A
        model has no such reason. A crayon earns its place only as a cheap
        concrete anchor for a chain that matters later, and this makes that
        argument countable.

        The distinction from :meth:`downstream_reach` matters. An anchor is a
        leaf, so nothing depends on it and its downstream reach is zero. A
        crayon and a teddy bear are indistinguishable by that measure and are
        separated by this one.
        """
        dependents = self._dependents()
        out: dict[str, int] = {}
        for start in self._nodes:
            # abstractions this concept instantiates, transitively
            anchored: set[str] = set()
            stack = [g for g in self.generalisations_of(start) if g in self._nodes]
            while stack:
                node = stack.pop()
                if node in anchored:
                    continue
                anchored.add(node)
                stack.extend(
                    g for g in self.generalisations_of(node) if g in self._nodes
                )
            # and everything that rests on them
            reached: set[str] = set(anchored)
            stack = [d for a in anchored for d in dependents[a]]
            while stack:
                node = stack.pop()
                if node in reached:
                    continue
                reached.add(node)
                stack.extend(dependents[node] - reached)
            reached.discard(start)
            out[start] = len(reached)
        return out

    def _dependents(self) -> dict[str, set[str]]:
        dependents: dict[str, set[str]] = defaultdict(set)
        for node_id in self._nodes:
            for target in self.prerequisites_of(node_id) | self.generalisations_of(
                node_id
            ):
                if target in self._nodes:
                    dependents[target].add(node_id)
        return dependents

    def _check_specialisation(self) -> list[Violation]:
        """A specialisation links two domain concepts.

        It never runs into the formal layer, which is what ``instantiates``
        is for.
        """
        out: list[Violation] = []
        for src, targets in self._specialises.items():
            node = self._nodes.get(src)
            if node is not None and node.kind is not NodeKind.DOMAIN_CONCEPT:
                out.append(
                    Violation(
                        "bad-specialises-source", f"{src!r} is not a domain concept"
                    )
                )
            for target in targets:
                if target == src:
                    out.append(
                        Violation("self-loop", f"node {src!r} specialises itself")
                    )
                other = self._nodes.get(target)
                if other is None:
                    out.append(
                        Violation(
                            "unknown-target",
                            f"specialises {src!r} -> undeclared {target!r}",
                        )
                    )
                elif other.kind is not NodeKind.DOMAIN_CONCEPT:
                    out.append(
                        Violation(
                            "bad-specialises-target",
                            f"{target!r} is a formal structure, not a general concept",
                        )
                    )
        return out

    def _check_references(self) -> list[Violation]:
        out: list[Violation] = []
        for src, targets in (*self._prerequisites.items(), *self._instantiates.items()):
            if src not in self._nodes:
                out.append(
                    Violation("unknown-source", f"edge from undeclared node {src!r}")
                )
            for t in targets:
                if t not in self._nodes:
                    out.append(
                        Violation(
                            "unknown-target", f"edge {src!r} -> undeclared node {t!r}"
                        )
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
                out.append(
                    Violation(
                        "missing-domain",
                        f"domain concept {node.id!r} declares no domain",
                    )
                )
            if node.kind is NodeKind.FORMAL_STRUCTURE and node.domain is not None:
                out.append(
                    Violation(
                        "domained-structure",
                        f"formal structure {node.id!r} declares a domain",
                    )
                )
        for src, targets in self._instantiates.items():
            s = self._nodes.get(src)
            if s is not None and s.kind is not NodeKind.DOMAIN_CONCEPT:
                out.append(
                    Violation(
                        "bad-instantiates-source", f"{src!r} is not a domain concept"
                    )
                )
            for t in targets:
                node = self._nodes.get(t)
                if node is not None and node.kind is not NodeKind.FORMAL_STRUCTURE:
                    out.append(
                        Violation(
                            "bad-instantiates-target",
                            f"{t!r} is not a formal structure",
                        )
                    )
        return out

    def _check_domain_declarations(self) -> list[Violation]:
        """Every domain a node claims must be declared.

        Skipped entirely when no domain is declared, so that a graph fragment
        written for a test is not obliged to carry the registry.
        """
        if not self._domains:
            return []
        return [
            Violation(
                "undeclared-domain",
                f"node {node.id!r} claims undeclared domain {node.domain!r}",
            )
            for node in self._nodes.values()
            if node.domain is not None and node.domain not in self._domains
        ]

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
            stack: list[tuple[str, list[str]]] = [
                (start, sorted(self.prerequisites_of(start)))
            ]
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
        # S311: `random` is correct here and a cryptographic generator would be
        # wrong. The control must be reproducible from a declared seed, which is
        # precisely the property a CSPRNG does not offer.
        return self._kahn(lambda frontier: rng.choice(sorted(frontier)))  # noqa: S311

    def _kahn(self, pick: Callable[[set[str]], str]) -> list[str]:
        remaining: dict[str, set[str]] = {
            n: {p for p in self.prerequisites_of(n) if p in self._nodes}
            for n in self._nodes
        }
        dependents: dict[str, set[str]] = defaultdict(set)
        for node_id, prereqs in remaining.items():
            for p in prereqs:
                dependents[p].add(node_id)

        frontier: set[str] = {n for n, p in remaining.items() if not p}
        order: list[str] = []
        while frontier:
            chosen = pick(frontier)
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
    def from_json(cls, payload: object) -> ConceptGraph:
        """Build a graph from parsed JSON, validating types at the boundary.

        A graph file is external input. Every field is checked rather than
        assumed, and a malformed file raises here rather than producing a
        graph whose wrongness surfaces later as a confusing result.
        """
        if not isinstance(payload, dict):
            raise ValueError("graph payload must be a JSON object")
        # Sound by construction: every Python value is an object, so widening
        # the element types of an already-narrowed dict cannot be wrong.
        body = cast(dict[object, object], payload)
        return cls(
            _parse_nodes(body.get("nodes")),
            _parse_edges(body.get("prerequisites"), "prerequisites"),
            _parse_edges(body.get("instantiates"), "instantiates"),
            _parse_edges(body.get("specialises"), "specialises"),
            _parse_domains(body.get("domains")),
        )

    @classmethod
    def load(cls, path: Path) -> ConceptGraph:
        parsed: object = json.loads(path.read_text(encoding="utf-8"))
        return cls.from_json(parsed)


def _require_str(value: object, where: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{where}: expected a string, got {type(value).__name__}")
    return value


def _parse_nodes(raw: object) -> list[Node]:
    if not isinstance(raw, list):
        raise ValueError("'nodes' must be a list")
    entries = cast(list[object], raw)
    out: list[Node] = []
    for index, entry in enumerate(entries):
        where = f"nodes[{index}]"
        if not isinstance(entry, dict):
            raise ValueError(f"{where}: expected an object")
        fields = cast(dict[object, object], entry)
        domain_raw = fields.get("domain")
        out.append(
            Node(
                id=_require_str(fields.get("id"), f"{where}.id"),
                name=_require_str(fields.get("name"), f"{where}.name"),
                kind=NodeKind(_require_str(fields.get("kind"), f"{where}.kind")),
                domain=(
                    None
                    if domain_raw is None
                    else _require_str(domain_raw, f"{where}.domain")
                ),
            )
        )
    return out


def _parse_domains(raw: object) -> list[Domain]:
    if raw is None:
        return []
    if not isinstance(raw, list):
        raise ValueError("'domains' must be a list")
    entries = cast(list[object], raw)
    out: list[Domain] = []
    for index, entry in enumerate(entries):
        where = f"domains[{index}]"
        if not isinstance(entry, dict):
            raise ValueError(f"{where}: expected an object")
        fields = cast(dict[object, object], entry)
        out.append(
            Domain(
                id=_require_str(fields.get("id"), f"{where}.id"),
                note=_require_str(fields.get("note"), f"{where}.note"),
            )
        )
    return out


def _parse_edges(raw: object, where: str) -> dict[str, list[str]]:
    if raw is None:
        return {}
    if not isinstance(raw, dict):
        raise ValueError(f"'{where}' must be an object")
    mapping = cast(dict[object, object], raw)
    out: dict[str, list[str]] = {}
    for key, value in mapping.items():
        source = _require_str(key, f"{where} key")
        if not isinstance(value, list):
            raise ValueError(f"{where}[{source!r}]: expected a list")
        items = cast(list[object], value)
        out[source] = [
            _require_str(item, f"{where}[{source!r}][{i}]")
            for i, item in enumerate(items)
        ]
    return out
