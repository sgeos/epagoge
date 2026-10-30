"""Count admitted headwords per concept for level-two units with no book.

Written by the luna line in the third Dromon trial and made lint-clean by
the operator's session without changing its output. A headword count
measures vocabulary on file, not whether a module can be written.

    python3 -I docs/process/trials/dromon_trial_3/readiness.py "$PWD"
"""

import json
import sys
from collections import Counter
from pathlib import Path
from typing import cast

Unit = tuple[str, list[str]]


def front(path: Path) -> dict[str, object]:
    """The JSON front matter of a book."""
    text = path.read_text()
    return cast("dict[str, object]", json.loads(text.split("---", 2)[1].strip()))


def counts(path: Path) -> Counter[str]:
    """Dictionary records per concept in one seed book."""
    records = cast("dict[str, object]", front(path)["records"])
    result: Counter[str] = Counter()
    for key, record in records.items():
        if key.startswith("dict.") and isinstance(record, dict):
            fields = cast("dict[str, object]", record)
            for concept in cast("list[str]", fields.get("concepts", [])):
                result[concept] += 1
    return result


def missing_units(root: Path) -> list[Unit]:
    """Level-two schedule units without a book, with their concepts."""
    schedule = json.loads((root / "curriculum/schedule/level_02.json").read_text())
    units: list[Unit] = []
    for domain in schedule["domains"]:
        for unit in domain["units"]:
            book = root / "curriculum/books/level_2" / f"bk.{unit['id']}.md"
            if book.exists():
                continue
            concepts = unit.get("teaches", []) + unit.get("revisits", [])
            units.append((unit["id"], concepts))
    return units


def main() -> int:
    root = Path(sys.argv[1])
    lvl2 = counts(root / "curriculum/books/level_2/bk.dictionary.seed.md")
    lvl1 = counts(root / "curriculum/books/level_1/bk.dictionary.seed.md")
    units = missing_units(root)

    def zeros(cs: list[str]) -> int:
        return sum(lvl2[c] == 0 for c in cs)

    print("UNIT COUNTS: concept=L2/L1; sum is sum of L2 counts")
    for unit_id, cs in units:
        details = "; ".join(f"{c}={lvl2[c]} L2/{lvl1[c]} L1" for c in cs)
        total = sum(lvl2[c] for c in cs)
        print(f"{unit_id}\tzero={zeros(cs)}\tsum={total}\t{details}")

    # Ranking: ascending zero-count concepts, then descending minimum L2
    # count, then descending sum of L2 counts, then ascending unit ID.
    ranked = sorted(
        units,
        key=lambda item: (
            zeros(item[1]),
            -min((lvl2[c] for c in item[1]), default=0),
            -sum(lvl2[c] for c in item[1]),
            item[0],
        ),
    )
    print(
        "RANKING: zero concepts ascending, minimum L2 count descending, "
        "L2 sum descending, unit ID ascending"
    )
    for unit_id, cs in ranked[:5]:
        low = min(lvl2[c] for c in cs)
        total = sum(lvl2[c] for c in cs)
        print(f"{unit_id}\tzero={zeros(cs)}\tmin={low}\tsum={total}")
    print("THIN CONCEPTS: concepts scheduled in missing units grouped by L2 count")
    concepts = sorted({c for _, cs in units for c in cs})
    for n in sorted({lvl2[c] for c in concepts}):
        print(f"{n}: " + ", ".join(c for c in concepts if lvl2[c] == n))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
