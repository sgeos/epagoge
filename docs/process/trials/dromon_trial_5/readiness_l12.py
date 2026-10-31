"""Count level-one and level-two dictionary headwords per missing unit."""

import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import cast

Unit = tuple[str, list[str]]


def counts(path: Path) -> Counter[str]:
    """Return dictionary records per concept from a seed book."""
    text = path.read_text()
    book = cast(dict[str, object], json.loads(text.split("---", 2)[1].strip()))
    records = cast(dict[str, object], book["records"])
    result: Counter[str] = Counter()
    for key, record in records.items():
        if key.startswith("dict.") and isinstance(record, dict):
            fields = cast(dict[str, object], record)
            for concept in cast(list[str], fields.get("concepts", [])):
                result[concept] += 1
    return result


def missing_units(root: Path) -> list[Unit]:
    """Return scheduled level-two units without a book."""
    schedule = json.loads((root / "curriculum/schedule/level_02.json").read_text())
    units: list[Unit] = []
    for domain in schedule["domains"]:
        for unit in domain["units"]:
            path = root / "curriculum/books/level_2" / f"bk.{unit['id']}.md"
            if not path.exists():
                concepts = unit.get("teaches", []) + unit.get("revisits", [])
                units.append((unit["id"], concepts))
    return units


def fourth_trial_empty(root: Path) -> list[str]:
    """Read level-two-empty concepts from the fourth-trial delta report."""
    path = root / "docs/process/trials/dromon_trial_4/readiness-delta.md"
    text = path.read_text()
    match = re.search(r"with no level-two headword are: (.+)\.", text)
    if match is None:
        raise ValueError(f"No fourth-trial empty-concept list in {path}")
    return [
        concept.strip().removeprefix("and ") for concept in match.group(1).split(",")
    ]


def main() -> int:
    root = Path(sys.argv[1])
    level_one = counts(root / "curriculum/books/level_1/bk.dictionary.seed.md")
    level_two = counts(root / "curriculum/books/level_2/bk.dictionary.seed.md")
    units = missing_units(root)

    def total(concept: str) -> int:
        return level_one[concept] + level_two[concept]

    print("UNIT COUNTS: concept=L1/L2/combined; sum is combined headwords")
    for unit_id, concepts in units:
        fields = "; ".join(
            f"{concept}={level_one[concept]}/{level_two[concept]}/{total(concept)}"
            for concept in concepts
        )
        zeros = sum(total(concept) == 0 for concept in concepts)
        combined_sum = sum(total(concept) for concept in concepts)
        print(f"{unit_id}\tzero={zeros}\tsum={combined_sum}\t{fields}")

    ranked = sorted(
        units,
        key=lambda unit: (
            sum(total(concept) == 0 for concept in unit[1]),
            -min(total(concept) for concept in unit[1]),
            -sum(total(concept) for concept in unit[1]),
            unit[0],
        ),
    )
    print(
        "RANKING: zeros ascending, minimum combined count descending, "
        "sum descending, ID ascending"
    )
    for unit_id, concepts in ranked[:5]:
        zeros = sum(total(concept) == 0 for concept in concepts)
        minimum = min(total(concept) for concept in concepts)
        combined_sum = sum(total(concept) for concept in concepts)
        print(f"{unit_id}\tzero={zeros}\tmin={minimum}\tsum={combined_sum}")

    concepts = sorted(
        {concept for _, unit_concepts in units for concept in unit_concepts}
    )
    print("EMPTY AT BOTH LEVELS:")
    print(", ".join(concept for concept in concepts if total(concept) == 0))
    print("FOURTH-TRIAL ZERO CONCEPTS AND CURRENT LEVEL-ONE COUNTS:")
    for concept in fourth_trial_empty(root):
        print(f"{concept}\tL1={level_one[concept]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
