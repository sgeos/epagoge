#!/usr/bin/env python3
"""Count spellings under one citation form, and show where that form is admitted.

A noun's singular and plural count as one. A verb's inflections count as
one. Pass ``--pos`` to stay inside one class. Pass ``--across-classes`` to
count every class of the same citation together. ``--propose-classes``
adds a sibling class the spelling rule allows when the lexicon has
declared a different class of the same citation.

A spelling the rules send to two citation forms is reported as unresolved
and is not added to either. The vocabulary check is not changed.

    PYTHONPATH=src python3 tools/analyse_lexemes.py read cuts
    PYTHONPATH=src python3 tools/analyse_lexemes.py counts counts.json --pos noun
    PYTHONPATH=src python3 tools/analyse_lexemes.py text source.txt --across-classes
    PYTHONPATH=src python3 tools/analyse_lexemes.py schedule --across-classes --level 2
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import cast

from epagoge.lexeme import (
    CLASSES,
    CountReport,
    Reading,
    ScheduledRoot,
    analyse,
    count_roots,
    scheduled_roots,
)
from epagoge.vocabulary import load_vocabulary, tokenise

ROOT = Path(__file__).resolve().parent.parent


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--vocabulary",
        type=Path,
        default=ROOT / "curriculum/vocabulary.json",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    read = sub.add_parser("read", help="print the readings of one spelling")
    read.add_argument("surface")
    _add_analysis_flags(read)

    counts = sub.add_parser("counts", help="group a JSON object of spelling to count")
    counts.add_argument("path", type=Path)
    _add_analysis_flags(counts)

    text = sub.add_parser("text", help="tokenise a text and group the counts")
    text.add_argument("path", type=Path)
    _add_analysis_flags(text)

    schedule = sub.add_parser("schedule", help="list admitted roots by class and level")
    schedule.add_argument("--across-classes", action="store_true")
    schedule.add_argument("--level", type=int, default=None)

    args = parser.parse_args(argv[1:])
    vocabulary = load_vocabulary(args.vocabulary)
    if args.command == "read":
        found = analyse(
            args.surface,
            vocabulary,
            pos=args.pos,
            propose_classes=args.propose_classes,
        )
        _print(
            {
                "surface": args.surface.strip().lower(),
                "readings": [_reading(row) for row in found],
            }
        )
        return 0
    if args.command == "schedule":
        rows = scheduled_roots(
            vocabulary, across_classes=args.across_classes, level=args.level
        )
        _print(
            {
                "across_classes": args.across_classes,
                "roots": [_root(row) for row in rows],
            }
        )
        return 0
    observed = (
        _load_counts(args) if args.command == "counts" else _count_text(args.path)
    )
    if observed is None:
        return 2
    report = count_roots(
        observed,
        vocabulary,
        pos=args.pos,
        propose_classes=args.propose_classes,
    )
    _print(_report(report, across_classes=args.across_classes))
    return 0


def _add_analysis_flags(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--pos", choices=CLASSES, default=None)
    parser.add_argument("--across-classes", action="store_true")
    parser.add_argument("--propose-classes", action="store_true")


def _load_counts(args: argparse.Namespace) -> dict[str, int] | None:
    parsed: object = json.loads(args.path.read_text(encoding="utf-8"))
    if not isinstance(parsed, dict):
        print("counts must be a JSON object of spelling to integer", file=sys.stderr)
        return None
    body = cast(dict[object, object], parsed)
    out: dict[str, int] = {}
    for key, value in body.items():
        if (
            not isinstance(key, str)
            or not isinstance(value, int)
            or isinstance(value, bool)
        ):
            print(
                "counts must be a JSON object of spelling to integer", file=sys.stderr
            )
            return None
        out[key] = value
    return out


def _count_text(path: Path) -> dict[str, int]:
    text = path.read_text(encoding="utf-8", errors="replace")
    return dict(Counter(token for token in tokenise(text) if token.isalpha()))


def _print(payload: dict[str, object]) -> None:
    print(json.dumps(payload, indent=2))


def _reading(row: Reading) -> dict[str, object]:
    return {
        "surface": row.surface,
        "root": row.root,
        "pos": row.pos,
        "slot": row.slot,
        "origin": row.origin,
        "level": row.level,
    }


def _root(row: ScheduledRoot) -> dict[str, object]:
    return {
        "root": row.root,
        "earliest": row.earliest,
        "placements": [
            {
                "pos": placement.pos,
                "senses": [
                    {
                        "concept": sense.concept,
                        "level": sense.level,
                        "surfaces": list(sense.surfaces),
                    }
                    for sense in placement.senses
                ],
            }
            for placement in row.placements
        ],
    }


def _report(report: CountReport, *, across_classes: bool) -> dict[str, object]:
    rows: list[dict[str, object]] = []
    for root in report.roots:
        if across_classes:
            rows.append(
                {
                    "root": root.root,
                    "count": root.total,
                    "level": root.earliest_level,
                    "origins": list(root.origins),
                }
            )
            continue
        for pos, count in root.by_class:
            rows.append(
                {
                    "root": root.root,
                    "pos": pos,
                    "count": count,
                    "level": root.earliest_level,
                    "shared": False,
                }
            )
        for shared in root.shared:
            rows.append(
                {
                    "root": root.root,
                    "pos": list(shared.classes),
                    "count": shared.count,
                    "surface": shared.surface,
                    "shared": True,
                }
            )
    return {
        "across_classes": across_classes,
        "rows": rows,
        "unresolved": [
            {
                "surface": row.surface,
                "count": row.count,
                "readings": [_reading(reading) for reading in row.readings],
            }
            for row in report.unresolved
        ],
        "skipped": [
            {"surface": surface, "count": count} for surface, count in report.skipped
        ],
        "omitted": [
            {"surface": surface, "count": count} for surface, count in report.omitted
        ],
    }


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
