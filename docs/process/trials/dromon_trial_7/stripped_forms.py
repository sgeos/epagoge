"""List admissible scan words resolved only by vocabulary suffix stripping."""

import json
import sys
from collections import Counter
from pathlib import Path
from typing import cast


def main() -> int:
    root = Path(sys.argv[1])
    sys.path.insert(0, str(root / "src"))
    from epagoge.vocabulary import Vocabulary, load_vocabulary, tokenise

    scan_path = root / "tmp/lexicon-sources/longtail/scan_f4.json"
    scan = cast(dict[str, object], json.loads(scan_path.read_text()))
    frequent = cast(dict[str, list[str]], scan["frequent"])
    source_names = cast(list[str], scan["sources"])
    sources = {name: scan_path.parent / name for name in source_names}
    vocabulary: Vocabulary = load_vocabulary(root / "curriculum/vocabulary.json")

    terms = vocabulary.terms
    listed = {form for term in terms for form in term.surface_forms()}
    excluded: set[str] = set()
    for review_path in (root / "evals/review").rglob("review.json"):
        review = cast(dict[str, object], json.loads(review_path.read_text()))
        for word, raw_record in review.items():
            if not isinstance(raw_record, dict):
                continue
            record = cast(dict[str, object], raw_record)
            if record.get("decision") == "exclude":
                excluded.add(word)
            excluded.update(cast(list[str], record.get("reviewed_forms", [])))

    counts_by_source: dict[str, Counter[str]] = {}
    for name, path in sources.items():
        text = path.read_text(encoding="utf-8", errors="replace")
        counts_by_source[name] = Counter(
            token for token in tokenise(text) if token.isalpha()
        )

    rows: list[tuple[str, str, str, dict[str, int]]] = []
    for word in sorted(frequent):
        if word in listed or word in excluded:
            continue
        term = vocabulary.lookup(word)
        if term is None or term.level > int(scan["level"]):
            continue
        senses = sorted(
            {
                f"{sense.concept}@L{sense.level}"
                for sense in vocabulary.senses(term.word)
            }
        )
        source_counts = {name: counts_by_source[name][word] for name in source_names}
        rows.append((word, term.word, ", ".join(senses), source_counts))

    rows.sort(key=lambda row: (-sum(row[3].values()), row[0]))
    print(f"{len(rows)} stripped-form candidates")
    print(
        "word\theadword\theadword concepts and levels\ttotal\tsource occurrence counts"
    )
    for word, headword, senses, source_counts in rows:
        detail = "; ".join(f"{name}={source_counts[name]}" for name in source_names)
        total = sum(source_counts.values())
        print(f"{word}\t{headword}\t{senses}\t{total}\t{detail}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
