"""Count distinct vocabulary terms per concept for missing level-two units."""

import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import cast

type Unit = tuple[str, list[str]]
type WordSets = dict[str, dict[str, set[str]]]


def read_terms(path: Path) -> list[dict[str, object]]:
    """Read term entries from the authoritative vocabulary manifest."""
    data = cast(dict[str, object], json.loads(path.read_text()))
    return cast(list[dict[str, object]], data["terms"])


def missing_units(root: Path) -> list[Unit]:
    """Return level-two schedule units without a book."""
    schedule = json.loads((root / "curriculum/schedule/level_02.json").read_text())
    units: list[Unit] = []
    for domain in schedule["domains"]:
        for unit in domain["units"]:
            path = root / "curriculum/books/level_2" / f"bk.{unit['id']}.md"
            if not path.exists():
                concepts = unit.get("teaches", []) + unit.get("revisits", [])
                units.append((unit["id"], concepts))
    return units


def main() -> int:
    root = Path(sys.argv[1])
    terms = read_terms(root / "curriculum/vocabulary.json")
    words: WordSets = defaultdict(lambda: {"1": set(), "2": set()})
    for term in terms:
        level = term.get("level")
        if level in (1, 2):
            concept = cast(str, term["concept"])
            word = cast(str, term["word"])
            words[concept][str(level)].add(word)

    def counts(concept: str) -> tuple[int, int, int]:
        level_one = words[concept]["1"]
        level_two = words[concept]["2"]
        return len(level_one), len(level_two), len(level_one | level_two)

    units = missing_units(root)
    print("UNIT COUNTS: concept=L1/L2/combined; distinct words per concept")
    for unit_id, concepts in units:
        fields = "; ".join(
            f"{concept}={counts(concept)[0]}/{counts(concept)[1]}/{counts(concept)[2]}"
            for concept in concepts
        )
        zero_count = sum(counts(concept)[2] == 0 for concept in concepts)
        combined_sum = sum(counts(concept)[2] for concept in concepts)
        print(f"{unit_id}\tzero={zero_count}\tsum={combined_sum}\t{fields}")

    ranked = sorted(
        units,
        key=lambda unit: (
            sum(counts(concept)[2] == 0 for concept in unit[1]),
            -min(counts(concept)[2] for concept in unit[1]),
            -sum(counts(concept)[2] for concept in unit[1]),
            unit[0],
        ),
    )
    print(
        "RANKING: zeros ascending, minimum combined count descending, "
        "sum descending, ID ascending"
    )
    for unit_id, concepts in ranked[:5]:
        zero_count = sum(counts(concept)[2] == 0 for concept in concepts)
        minimum = min(counts(concept)[2] for concept in concepts)
        combined_sum = sum(counts(concept)[2] for concept in concepts)
        print(f"{unit_id}\tzero={zero_count}\tmin={minimum}\tsum={combined_sum}")

    all_concepts = sorted({concept for _, concepts in units for concept in concepts})
    thinnest = sorted(all_concepts, key=lambda concept: (counts(concept)[2], concept))[
        :10
    ]
    print("TEN THINNEST SCHEDULED CONCEPTS: distinct words, with level")
    for concept in thinnest:
        entries = [
            *(f"{word} (L1)" for word in sorted(words[concept]["1"])),
            *(f"{word} (L2)" for word in sorted(words[concept]["2"])),
        ]
        print(f"{concept}\tcombined={counts(concept)[2]}\t" + ", ".join(entries))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
