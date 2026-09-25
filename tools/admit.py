#!/usr/bin/env python3
"""Admit words the corpus asked for, with their forms and definitions.

**A word the teacher reached for is evidence, not an error.** The corpus
and the lexicon grow together, so a story that wants `balloon` is a reason
to consider admitting `balloon` rather than a reason to file the story
down. Operator direction, 2026-09-25.

Input is JSON mapping a word to its concept, its parts of speech and its
definition::

    {"balloon": {"concept": "toy", "pos": "noun",
                 "definition": "A balloon is a bag of air you play with."}}

Forms are generated from the parts of speech, so a noun gets its plural
and a verb its inflections without being asked. **Nothing is written
unless every word passes**, including the closure check, because a word
admitted without a grounded definition takes the dictionary out of
self-hosting.

    PYTHONPATH=src python3 tools/admit.py words.json [--level N]
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import cast

from epagoge.inflection import plural, verb_forms

ROOT = Path(__file__).resolve().parent.parent


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument("--level", type=int, default=1)
    args = parser.parse_args(argv[1:])

    wanted = cast(
        dict[str, dict[str, str]], json.loads(args.file.read_text(encoding="utf-8"))
    )
    path = ROOT / "curriculum/vocabulary.json"
    raw = cast(dict[str, object], json.loads(path.read_text(encoding="utf-8")))
    terms = cast(list[dict[str, object]], raw["terms"])
    core = cast(list[str], raw["core"])
    taken = set(core) | {
        f for t in terms for f in [str(t["word"]), *cast(list[str], t.get("forms", []))]
    }
    concepts = {str(t["concept"]) for t in terms}

    problems: list[str] = []
    for word, spec in wanted.items():
        if word in taken:
            problems.append(f"{word}: already admitted")
        if spec.get("concept") not in concepts:
            problems.append(f"{word}: concept {spec.get('concept')!r} is not in use")
        if not spec.get("definition"):
            problems.append(f"{word}: no definition")
        for part in spec.get("pos", "").split():
            if part not in ("verb", "noun"):
                problems.append(f"{word}: unknown part of speech {part!r}")
    if problems:
        print(f"{len(problems)} problem(s), nothing written:", file=sys.stderr)
        for line in problems:
            print(f"  {line}", file=sys.stderr)
        return 1

    added: list[str] = []
    for word, spec in sorted(wanted.items()):
        parts = spec.get("pos", "").split()
        forms: set[str] = set()
        if "noun" in parts and plural(word) != word:
            forms.add(plural(word))
        if "verb" in parts:
            forms.update(verb_forms(word))
        forms -= taken
        entry: dict[str, object] = {
            "word": word,
            "concept": spec["concept"],
            "level": args.level,
        }
        if parts:
            entry["pos"] = " ".join(sorted(set(parts)))
        if forms:
            entry["forms"] = sorted(forms)
        terms.append(entry)
        taken.add(word)
        taken.update(forms)
        added.append(word)
    raw["terms"] = sorted(terms, key=lambda t: (str(t["word"]), str(t["concept"])))
    # **All or nothing.** A first version wrote the lexicon and then found
    # the definitions bad, leaving words admitted with nothing defining
    # them, which takes the dictionary out of self-hosting.
    before = path.read_text(encoding="utf-8")
    path.write_text(
        json.dumps(raw, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    definitions = {w: spec["definition"] for w, spec in wanted.items()}
    payload = json.dumps(definitions)
    result = subprocess.run(  # noqa: S603
        [
            sys.executable,
            str(ROOT / "tools/author_definitions.py"),
            "--level",
            str(args.level),
        ],
        input=payload,
        capture_output=True,
        text=True,
        env={**dict(__import__("os").environ), "PYTHONPATH": str(ROOT / "src")},
        check=False,
    )
    print(result.stdout.strip() or result.stderr.strip(), file=sys.stderr)
    if result.returncode != 0:
        path.write_text(before, encoding="utf-8")
        print("definitions failed; the lexicon is rolled back", file=sys.stderr)
        return 1
    _ = subprocess.run(  # noqa: S603
        [
            sys.executable,
            str(ROOT / "tools/sync_thesaurus.py"),
            "--level",
            str(args.level),
        ],
        capture_output=True,
        text=True,
        env={**dict(__import__("os").environ), "PYTHONPATH": str(ROOT / "src")},
        check=False,
    )
    print(f"admitted {len(added)}: {' '.join(added)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
