#!/usr/bin/env python3
"""Select a lexicon candidate pool from a scan report by stated rules.

**A pool chosen by code that is not kept cannot be audited.** The first two
agent-authored batches selected their pools with throwaway scripts. This
applies named rules to a `scan_lexicon.py` report and records what each rule
removed, so a pool can be regenerated and its exclusions checked.

The rules, in the order applied:

1. **Term list.** Words matching the private disclosure pattern file, when
   one is given, are removed first and only counted. Applied first so that no
   such word can appear in another rule's named list, because a named list in
   a tracked file would publish what the pattern withholds.
2. **Admissible.** Already admissible at the level under lookup.
3. **Prior decision.** Given any decision in an earlier review record, which
   is carried forward rather than relitigated.
4. **Sources.** Frequent in fewer than the minimum number of sources.
5. **Short.** Shorter than the minimum length, which removes letters and
   most fragments.
6. **Capitalised.** At least the given share of its occurrences across the
   source texts is capitalised. A proxy for proper nouns, and a crude one: a
   common word that often opens a sentence can be removed and a name that is
   also a common word can survive. The review is still responsible for names.

**Missing source texts are refused.** The capitalisation rule cannot run
without them, and a pool that silently skipped it would look filtered.

    PYTHONPATH=src python3 tools/candidate_pool.py tmp/lexicon-sources/scan_f5.json \\
        --level 2 --terms secret/scrub_terms.txt --out pool.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import cast

from epagoge.artifacts import file_digest, write_json
from epagoge.vocabulary import Vocabulary, load_vocabulary

ROOT = Path(__file__).resolve().parent.parent

WORD_RE = re.compile(r"[A-Za-z']+")
NAMED_RULES = ("admissible", "prior_decision", "sources", "short", "capitalised")


def term_pattern(path: Path) -> re.Pattern[str] | None:
    """The disclosure pattern with the scan's semantics, or None if empty."""
    terms = [
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    if not terms:
        return None
    # The optional plural matches `tools/scrub_scan.sh`, which missed plurals
    # of withheld words until 2026-10-07.
    return re.compile(r"\b(" + "|".join(terms) + r")(s|es)?\b", re.IGNORECASE)


def capital_share(texts: list[str]) -> dict[str, float]:
    """For each lowercased word, the share of occurrences written capitalised."""
    capital: Counter[str] = Counter()
    total: Counter[str] = Counter()
    for text in texts:
        for match in WORD_RE.finditer(text):
            word = match.group()
            lower = word.lower()
            total[lower] += 1
            if word[0].isupper():
                capital[lower] += 1
    return {word: capital[word] / n for word, n in total.items()}


def prior_decisions(reviews: list[Path]) -> set[str]:
    """Every word given a decision in an earlier review record."""
    decided: set[str] = set()
    for path in reviews:
        raw: object = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(raw, dict):
            raise ValueError(f"{path}: a review record must be an object")
        decided.update(cast(dict[str, object], raw))
    return decided


def select(
    frequent: dict[str, list[str]],
    vocabulary: Vocabulary,
    level: int,
    shares: dict[str, float],
    decided: set[str],
    pattern: re.Pattern[str] | None,
    *,
    min_sources: int = 2,
    min_length: int = 3,
    max_capital_share: float = 0.5,
) -> tuple[list[str], dict[str, list[str]], int]:
    """The pool, the named removals by rule and the unnamed term-list count."""
    if level < 1 or min_sources < 1 or min_length < 1:
        raise ValueError("level, minimum sources and minimum length must be positive")
    if not 0.0 < max_capital_share <= 1.0:
        raise ValueError("the capitalisation share must be in (0, 1]")
    removed: dict[str, list[str]] = {rule: [] for rule in NAMED_RULES}
    withheld = 0
    pool: list[str] = []
    for word in sorted(frequent):
        if pattern is not None and pattern.search(word):
            withheld += 1
            continue
        term = vocabulary.lookup(word)
        if term is not None and term.level <= level:
            removed["admissible"].append(word)
        elif word in decided:
            removed["prior_decision"].append(word)
        elif len(frequent[word]) < min_sources:
            removed["sources"].append(word)
        elif len(word) < min_length:
            removed["short"].append(word)
        elif shares.get(word, 0.0) >= max_capital_share:
            removed["capitalised"].append(word)
        else:
            pool.append(word)
    return pool, removed, withheld


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scan", type=Path)
    parser.add_argument("--level", type=int, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--terms", type=Path, default=None)
    parser.add_argument("--min-sources", type=int, default=2)
    parser.add_argument("--min-length", type=int, default=3)
    parser.add_argument("--max-capital-share", type=float, default=0.5)
    parser.add_argument(
        "--vocabulary", type=Path, default=ROOT / "curriculum/vocabulary.json"
    )
    args = parser.parse_args(argv[1:])
    report = cast(dict[str, object], json.loads(args.scan.read_text(encoding="utf-8")))
    names = cast(list[str], report["sources"])
    paths = [args.scan.parent / name for name in names]
    missing = [str(p) for p in paths if not p.is_file()]
    if missing:
        print(f"missing source texts: {' '.join(missing)}", file=sys.stderr)
        return 1
    reviews = sorted(ROOT.glob("evals/review/*/review.json"))
    pattern = term_pattern(args.terms) if args.terms is not None else None
    pool, removed, withheld = select(
        cast(dict[str, list[str]], report["frequent"]),
        load_vocabulary(args.vocabulary),
        args.level,
        capital_share([p.read_text(encoding="utf-8", errors="replace") for p in paths]),
        prior_decisions(reviews),
        pattern,
        min_sources=args.min_sources,
        min_length=args.min_length,
        max_capital_share=args.max_capital_share,
    )
    write_json(
        args.out,
        {
            "scan_report_hash": file_digest(args.scan),
            "source_hashes": {
                name: file_digest(p) for name, p in zip(names, paths, strict=True)
            },
            "vocabulary_hash": file_digest(args.vocabulary),
            "level": args.level,
            "rules": {
                "term_list_applied": pattern is not None,
                "min_sources": args.min_sources,
                "min_length": args.min_length,
                "max_capital_share": args.max_capital_share,
                "prior_reviews": [str(p.relative_to(ROOT)) for p in reviews],
            },
            "removed_counts": {
                "term_list": withheld,
                **{rule: len(words) for rule, words in removed.items()},
            },
            "removed": removed,
            "pool": pool,
        },
    )
    print(
        f"{len(pool)} in pool; removed {withheld} by term list, "
        + ", ".join(f"{len(w)} {rule}" for rule, w in removed.items())
    )
    if args.terms is None:
        print(
            "term list not applied: review the pool for withheld terms", file=sys.stderr
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
