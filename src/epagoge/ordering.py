"""Shared schedule-based book ordering for corpus exports and training."""

from __future__ import annotations

import random
from pathlib import Path
from typing import Final, cast

from epagoge import schedule as sched
from epagoge.book import (
    DefinitionKind,
    book_prerequisites,
    linear_extension,
    load_book_dir,
    random_linear_extension,
)
from epagoge.concept_graph import ConceptGraph

ORDERINGS: Final[tuple[str, ...]] = (
    "curriculum",
    "topological",
    "shuffled",
    "length",
    "null",
)

LENGTH_WEIGHT: Final[float] = 0.265
"""How strongly the `length` arm sorts by book length.

Chosen so that arm's position-to-length correlation matches the topological
arm's, which is what makes it a control rather than another variable.
**Both are measured per seed and then averaged**, at +0.211 for topological
and +0.213 for this arm over six seeds, and the weight was tuned against
the arm as implemented rather than against a reconstruction of it.

**Tuned to 0.40 first, against the wrong statistic.** Correlating a book's
*mean* position across seeds against its length gives +0.311 for the
topological arm, because averaging the positions removes the per-run noise.
That is a fact about the arm across seeds, and the quantity a single
training run sees is the per-run one. Matching the wrong target would have
given this arm half again the length ordering it is supposed to hold fixed.
"""


def book_order(
    book_dir: Path, graph: ConceptGraph, seed: int, arm: str, plan: sched.Schedule
) -> tuple[list[str], dict[str, str], dict[str, str]]:
    """Book ids in the arm's order, each book's text, and each book's title.

    **The title is returned because it is trained on**, as an announcement
    line at the head of the work. See `Tokeniser.encode_work` and
    `docs/decisions/STRUCTURAL_TOKENS.md`. It was presentation only until
    2026-09-27.

    **A book teaches what its unit teaches.** Taking the union of every
    record's concepts instead counts a word the book merely defines as a
    concept the book teaches, which manufactures dependencies between books
    that have nothing to do with each other. Measured 2026-09-25 over 144
    books, that reading made the dependency graph cyclic in twenty-four
    places, `bk.a1.person` and `bk.b1.keeping_going` each depending on the
    other, and `linear_extension` returns a short list on a cycle. Thirteen
    books reached the trainer and a hundred and thirty-three did not.
    """
    if arm not in ORDERINGS:
        raise ValueError(f"unknown ordering {arm!r}")
    all_books, records = load_book_dir(book_dir)
    by_id = {
        str(cast(dict[str, object], r)["id"]): cast(dict[str, object], r)
        for r in records
    }
    # A dictionary book spans nearly every concept, so it makes the
    # dependency graph cyclic. It is reference material and is emitted last.
    books = [b for b in all_books if not b.id.startswith("bk.dictionary.")]
    reference = [b for b in all_books if b.id.startswith("bk.dictionary.")]
    by_unit = {u.id: set(u.teaches) for d in plan.domains for u in d.units}
    unknown = sorted(
        {b.subject for b in books if b.subject_kind == DefinitionKind.TOPIC}
        - by_unit.keys()
    )
    if unknown:
        raise ValueError(f"books name unknown schedule units: {unknown}")
    # Domain reference books have no schedule-unit teaching assignment.
    teaches = {b.id: by_unit.get(b.subject, set()) for b in books}
    prerequisites = {n: set(graph.prerequisites_of(n)) for n in graph.nodes}
    deps = book_prerequisites(books, teaches, prerequisites)
    if arm == "length":
        # **The control for the confound found on 2026-09-27.** Orders that
        # respect the prerequisite graph also sort books by length, at
        # +0.311 against +0.062 for a free shuffle, because a book with more
        # prerequisites is placed later and 90 percent of books carry one.
        # Length ordering and graph structure were collinear at -0.76 across
        # the arms, so neither could be credited with the effect.
        #
        # This arm has the length ordering and not the graph. The mixing
        # weight uses the corrected per-seed calibration documented above.
        # Its match must be remeasured whenever the corpus changes.
        generator = random.Random(seed)
        length = {
            b.id: sum(
                len(str(by_id[i]["content"]).split()) for i in b.records if i in by_id
            )
            for b in books
        }
        by_length = sorted(length, key=lambda n: length[n])
        place = {n: i / max(1, len(by_length) - 1) for i, n in enumerate(by_length)}
        names = sorted(
            place,
            key=lambda n: (
                LENGTH_WEIGHT * place[n] + (1.0 - LENGTH_WEIGHT) * generator.random()
            ),
        )
    elif arm == "shuffled":
        # **The flat control, and it did not exist until 2026-09-26.** The two
        # arms above it both respect the prerequisite graph, so the ablation
        # compared two curricula rather than a curriculum against no
        # curriculum. A result from those two says which valid ordering is
        # better, not whether ordering helps.
        #
        # It is also this design's answer to Wu, Dyer and Neyshabur, who
        # found any curriculum benefit attributable to the training set
        # growing rather than to the order, and whose control is a set that
        # grows with random membership. In a trainer that cycles a fixed
        # ordered list, the order IS the growth schedule for the first epoch,
        # so a random order is that control.
        #
        # **The growth confound is smaller here than in their setting and the
        # record should say so.** At 1,458 chunks and batch 8 an epoch is 182
        # batches, so a 1,600-step run is about 8.8 epochs and every arm has
        # seen everything after the first eleven percent. After that, set size
        # cannot explain a difference and only the order within each cycle
        # can.
        shuffled = [b.id for b in books]
        random.Random(seed).shuffle(shuffled)
        names = shuffled
    elif arm in {"topological", "null"}:
        # Independent deterministic streams preserve the existing control.
        order_seed = seed if arm == "topological" else f"null:{seed}"
        names = random_linear_extension(deps, random.Random(order_seed))
    else:
        depth = graph.prerequisite_depth()

        def shallowest(ready: set[str]) -> str:
            return min(
                ready,
                key=lambda name: (
                    max((depth[c] for c in teaches[name] if c in depth), default=0),
                    name,
                ),
            )

        names = linear_extension(deps, shallowest)
    if len(names) != len(books) or len(set(names)) != len(books):
        raise ValueError("book dependencies are cyclic or ordering is incomplete")
    ordered = names + [b.id for b in reference]
    text = {
        b.id: "\n".join(str(by_id[i]["content"]) for i in b.records if i in by_id)
        for b in all_books
    }
    titles = {b.id: b.title or "" for b in all_books}
    return ordered, text, titles
