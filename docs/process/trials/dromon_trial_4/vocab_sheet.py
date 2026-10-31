"""List dictionary headwords filed under the concepts in r2.measure."""

import json
import re
import sys
from pathlib import Path

CONCEPTS = ("cycle", "how_sure", "measuring", "sequence", "spatial_position", "unit")
ENTRY = re.compile(r"^\[dict\.([12])\.([^]]+)\]\s*\n(.*?)(?=^\[dict\.|\Z)", re.M | re.S)


def records(path: Path) -> dict[str, dict[str, object]]:
    """Return dictionary metadata from a book's JSON front matter."""
    body = path.read_text().split("---", 2)[1].strip()
    return json.loads(body)["records"]


def main() -> int:
    root = Path(sys.argv[1])
    books = [
        root / f"curriculum/books/level_{level}/bk.dictionary.seed.md"
        for level in (1, 2)
    ]
    metadata = {level: records(book) for level, book in zip((1, 2), books, strict=True)}
    definitions: dict[tuple[str, str], str] = {}
    for book in books:
        for match in ENTRY.finditer(book.read_text().split("---", 2)[2]):
            level, headword, definition = match.groups()
            definitions[(level, headword)] = definition.strip()

    for concept in CONCEPTS:
        print(f"## {concept}")
        for level in (1, 2):
            prefix = f"dict.{level}."
            print(f"### Level {level}")
            entries = sorted(
                (
                    key.removeprefix(prefix),
                    definitions[(str(level), key.removeprefix(prefix))],
                )
                for key, record in metadata[level].items()
                if key.startswith(prefix) and concept in record.get("concepts", [])
            )
            for headword, definition in entries:
                print(f"- **{headword}**: {definition}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
