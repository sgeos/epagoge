#!/usr/bin/env python3
"""Admit words the corpus asked for, with their forms and definitions.

**A word the teacher reached for is evidence, not an error.** The corpus
and the lexicon grow together, so a story that wants `balloon` is a reason
to consider admitting `balloon` rather than a reason to file the story
down. Operator direction, 2026-09-25.

Input is JSON mapping a word to its concept, its parts of speech, its
definition and optionally where it came from::

    {"balloon": {"concept": "toy", "pos": "noun",
                 "definition": "A balloon is a bag of air you play with.",
                 "source": "teacher, bk.p1.toys round 3"}}

``source`` is free text and is recorded on the term. This corpus is CC0
and some candidate word lists are not, so knowing where a word was
proposed matters more than the word does.

Forms are generated from the parts of speech, so a noun gets its plural
and a verb its inflections without being asked. An optional ``inflection``
object replaces a derived slot, and an optional ``forms`` list adds any
further surface. **Nothing is written unless every word passes**, including
the closure check, because a word admitted without a grounded definition
takes the dictionary out of self-hosting.

**A second sense of a word already admitted** is requested with
``"second_sense": true`` and is keyed by word and concept. It gets its own
level, part of speech, forms and dictionary record. Without the flag an
admitted word is refused, as it always was. Added 2026-10-30 on operator
direction, for words such as `well` whose admitted sense is not the one a
source uses. ``--level`` is 1 to 7. A level
above the concept's level is allowed. A level below it is not, and that
check belongs to the vocabulary validator rather than to this writer.

    PYTHONPATH=src python3 tools/admit.py words.json [--level N]
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import cast

from epagoge.inflection import owed_forms
from epagoge.vocabulary import parse_inflection, parse_pos

ROOT = Path(__file__).resolve().parent.parent


def _string_list(raw: object) -> list[str] | None:
    """A list of strings, or None when the value is not one."""
    if raw is None:
        return []
    if not isinstance(raw, list):
        return None
    out: list[str] = []
    for item in cast(list[object], raw):
        if not isinstance(item, str):
            return None
        out.append(item)
    return out


def plan_admission(
    wanted: dict[str, dict[str, object]],
    terms: list[dict[str, object]],
    core: list[str],
    concepts: set[str],
    level: int,
) -> tuple[list[str], list[dict[str, object]]]:
    """The problems with a request, or the term entries it would add.

    Pure, so the refusals can be tested without a lexicon on disk. Nothing
    is added unless the problem list is empty.

    **A second sense is admitted only when asked for by name.** A spec with
    ``"second_sense": true`` files a new sense of a word that is already a
    headword at or below ``level``, keyed by word and concept, with its own
    level, part of speech and forms. Without the flag, a word already
    admitted is refused exactly as before, so a batch cannot add a sense
    to an existing word by accident. The flag does not relax anything
    else. The same word and concept are refused at any level, because the
    validator refuses a duplicate sense. A string that is only a form of a
    different headword is refused, because a form shared by two words is
    the duplicate the validator rejects.
    """
    # **Admissible here, not merely present somewhere.** Keyed on presence,
    # `depend` lost `depends` because a level-six term already spelled it,
    # and the verb was admitted at level one without a form it needs there.
    taken = set(core) | {
        f
        for t in terms
        if int(cast(int, t["level"])) <= level
        for f in [str(t["word"]), *cast(list[str], t.get("forms", []))]
    }

    def own_forms(word: str) -> set[str]:
        """Every surface form the word's existing senses already carry."""
        return {
            f
            for t in terms
            if str(t["word"]) == word
            for f in [word, *cast(list[str], t.get("forms", []))]
        }

    problems: list[str] = []
    parsed: dict[str, tuple[str, tuple[tuple[str, str], ...], tuple[str, ...]]] = {}
    for word, spec in wanted.items():
        second = spec.get("second_sense", False)
        if not isinstance(second, bool):
            problems.append(f"{word}: second_sense must be true or false")
            continue
        if second:
            problems.extend(_second_sense_problems(word, spec, terms, core, level))
        elif word in taken:
            problems.append(f"{word}: already admitted")
        if spec.get("concept") not in concepts:
            problems.append(
                f"{word}: concept {spec.get('concept')!r} is not in the graph"
            )
        source = spec.get("source", "")
        if not isinstance(source, str) or not source.strip():
            problems.append(f"{word}: no admission source")
        definition = spec.get("definition", "")
        if not isinstance(definition, str) or not definition:
            problems.append(f"{word}: no definition")
        # **THE LIST USED TO BE SPELLED OUT HERE AND IT DRIFTED.** `mass`
        # was added to the lexicon on 2026-09-26 and `periphrastic` on
        # 2026-09-27, and this tool rejected both, so a qualifier the
        # validator understood could not be admitted through the tool that
        # admits words. That is the field-enumeration defect recorded in
        # `docs/decisions/FIELD_ENUMERATION.md`, a second copy of a list that
        # has one authority. It now reads the authority.
        try:
            pos = parse_pos(spec.get("pos") or "", word)
            inflection = parse_inflection(spec.get("inflection"), pos, word)
        except ValueError as exc:
            problems.append(f"{word}: {exc}")
            continue
        extra = _string_list(spec.get("forms", []))
        if extra is None:
            problems.append(f"{word}: forms must be a list of strings")
            continue
        parsed[word] = (pos, inflection, tuple(extra))
    if problems:
        return problems, []

    entries: list[dict[str, object]] = []
    for word, spec in sorted(wanted.items()):
        pos, inflection, extra = parsed[word]
        parts = pos.split()
        # **The same function the validator uses.** A second copy of the
        # spelling rules drifted once, and a mass noun would have been
        # admitted with the plural the validator then refused to require.
        forms = set(owed_forms(word, pos, dict(inflection)))
        forms.update(item.strip().lower() for item in extra if item.strip())
        forms.discard(word)
        # **A form shared by two senses of one word is ordinary**, so a
        # second sense keeps the forms its own word already carries, as
        # `samples` serves the noun and the verb. A form of any other word
        # is still dropped.
        forms -= taken - own_forms(word)
        entry: dict[str, object] = {
            "word": word,
            "concept": spec["concept"],
            "level": level,
        }
        if parts:
            entry["pos"] = " ".join(sorted(set(parts)))
        if inflection:
            entry["inflection"] = {key: value or None for key, value in inflection}
        # **Where a word came from, recorded at admission.** This corpus is
        # CC0 and some candidate lists are not, so the audit trail for a
        # word is worth more than the word. It also separates a word the
        # teacher reached for from one a scan proposed, which are different
        # kinds of evidence.
        source = str(spec.get("source", "")).strip()
        if source:
            entry["source"] = source
        if forms:
            entry["forms"] = sorted(forms)
        entries.append(entry)
        taken.add(word)
        taken.update(forms)
    return problems, entries


def _second_sense_problems(
    word: str,
    spec: dict[str, object],
    terms: list[dict[str, object]],
    core: list[str],
    level: int,
) -> list[str]:
    """Why a requested second sense cannot be filed, or nothing."""
    if word in core:
        return [f"{word}: a core word takes no sense"]
    same = [t for t in terms if str(t["word"]) == word]
    if not any(int(cast(int, t["level"])) <= level for t in same):
        return [
            f"{word}: second_sense needs a sense already admitted at or below "
            f"level {level}"
        ]
    out: list[str] = []
    concept = spec.get("concept")
    for t in same:
        if t["concept"] == concept:
            out.append(
                f"{word}: already admitted under {concept!r} at level {t['level']}"
            )
    for t in terms:
        if str(t["word"]) != word and word in cast(list[str], t.get("forms", [])):
            out.append(f"{word}: already a form of {t['word']!r}")
    return out


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument("--level", type=int, default=1)
    args = parser.parse_args(argv[1:])
    if not 1 <= args.level <= 7:
        parser.error("level must be from 1 to 7")

    wanted = cast(
        dict[str, dict[str, object]],
        json.loads(args.file.read_text(encoding="utf-8")),
    )
    path = ROOT / "curriculum/vocabulary.json"
    raw = cast(dict[str, object], json.loads(path.read_text(encoding="utf-8")))
    terms = cast(list[dict[str, object]], raw["terms"])
    core = cast(list[str], raw["core"])
    # **Checked against the graph, not against the terms already filed.**
    # Keyed on the terms, the first word of a newly authored concept could
    # never be admitted, which is exactly when admitting one matters.
    graph_path = ROOT / "curriculum/graph/concepts.json"
    graph = cast(dict[str, object], json.loads(graph_path.read_text(encoding="utf-8")))
    nodes = cast(list[dict[str, object]], graph["nodes"])
    concepts = {str(node["id"]) for node in nodes}

    problems, entries = plan_admission(wanted, terms, core, concepts, args.level)
    if problems:
        print(f"{len(problems)} problem(s), nothing written:", file=sys.stderr)
        for line in problems:
            print(f"  {line}", file=sys.stderr)
        return 1

    terms.extend(entries)
    added = [str(entry["word"]) for entry in entries]
    raw["terms"] = sorted(terms, key=lambda t: (str(t["word"]), str(t["concept"])))
    # **All or nothing.** A first version wrote the lexicon and then found
    # the definitions bad, leaving words admitted with nothing defining
    # them, which takes the dictionary out of self-hosting.
    before = path.read_text(encoding="utf-8")
    path.write_text(
        json.dumps(raw, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    definitions: dict[str, object] = {
        w: (
            {"concept": spec["concept"], "definition": str(spec["definition"])}
            if spec.get("second_sense") is True
            else str(spec["definition"])
        )
        for w, spec in wanted.items()
    }
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
