"""Antonym pairs, so that a missing opposite is a gate failure.

**A lexicon can be complete in every word it has and still be unable to
say the opposite of them.** On 2026-09-25 the level-one lexicon held
`true` without `false`, `king` without `queen`, `safe` without `unsafe`,
`fall` without `rise`, and `agree` without `disagree` while the curriculum
planned a concept named for agreeing and disagreeing. Nineteen such gaps.

None was visible to any existing check. The vocabulary validator asks
whether a word names a concept and whether it arrives after that concept
is taught. Neither question notices that one end of a dimension is absent,
because the word that is missing is not there to be checked.

**An antonym is licensed by the same concept as its partner.** A pair
names one dimension, so hot and cold are one property and not two, which
is why this file records pairs rather than adding a field to each term.

Standard library only, matching the rest of the package.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import cast

from epagoge.concept_graph import Violation
from epagoge.vocabulary import Vocabulary


@dataclass(frozen=True, slots=True)
class Thesaurus:
    """Authored. Pairs are a judgement and are not derived from anything."""

    antonyms: tuple[tuple[str, str], ...] = ()

    def words(self) -> frozenset[str]:
        return frozenset(w for pair in self.antonyms for w in pair)


def admissible_at(vocabulary: Vocabulary, word: str, level: int) -> bool:
    """Whether a generator constrained to ``level`` can reach ``word``."""
    if word in vocabulary.core or word in vocabulary.exempt:
        return True
    found = vocabulary.lookup(word)
    return found is not None and found.level <= level


def validate(
    thesaurus: Thesaurus, vocabulary: Vocabulary, level: int = 1
) -> list[Violation]:
    """Both ends of a pair must be reachable, or neither.

    A pair with one end present is the defect. A pair with neither end is
    not, since the dimension may simply belong to a later level, and
    treating it as an error would force words in by the back door.
    """
    out: list[Violation] = []
    seen: set[tuple[str, str]] = set()
    for first, second in thesaurus.antonyms:
        if first == second:
            out.append(Violation("degenerate-pair", f"{first!r} is paired with itself"))
            continue
        key = (first, second) if first < second else (second, first)
        if key in seen:
            out.append(
                Violation("duplicate-pair", f"{first!r} and {second!r} appear twice")
            )
        seen.add(key)
        here = admissible_at(vocabulary, first, level)
        there = admissible_at(vocabulary, second, level)
        if here != there:
            have, missing = (first, second) if here else (second, first)
            out.append(
                Violation(
                    "missing-antonym",
                    f"{have!r} is admissible at level {level} and its opposite "
                    f"{missing!r} is not",
                )
            )
    return out


def from_json(payload: object) -> Thesaurus:
    if not isinstance(payload, dict):
        raise ValueError("thesaurus must be a JSON object")
    body = cast(dict[object, object], payload)
    raw = body.get("antonyms")
    if not isinstance(raw, list):
        raise ValueError("'antonyms' must be a list")
    pairs: list[tuple[str, str]] = []
    for index, item in enumerate(cast(list[object], raw)):
        where = f"antonyms[{index}]"
        if not isinstance(item, list):
            raise ValueError(f"{where}: expected a pair")
        entries = cast(list[object], item)
        if len(entries) != 2:
            raise ValueError(f"{where}: expected exactly two words")
        for entry in entries:
            if not isinstance(entry, str) or not entry.strip():
                raise ValueError(f"{where}: words must be non-empty strings")
        first, second = cast(list[str], entries)
        pairs.append((first.lower(), second.lower()))
    return Thesaurus(antonyms=tuple(pairs))


def load(path: Path) -> Thesaurus:
    parsed: object = json.loads(path.read_text(encoding="utf-8"))
    return from_json(parsed)
