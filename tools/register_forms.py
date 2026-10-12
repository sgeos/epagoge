#!/usr/bin/env python3
"""Show or register the alternates of a word already in the lexicon.

This does not admit a headword. Admission is ``tools/admit.py``. This tool
records, for one existing sense, the part of speech and any slot the
spelling rules get wrong.

``show`` prints every slot. A noun has a singular and a plural. A verb has
its inflections. An adjective or an adverb has comparison, or none. A word
with an empty part of speech is printed as undeclared and is not checked.

``apply`` reads a JSON object. Each key is a headword. The value may carry
``concept`` when the word has more than one sense, ``pos``, and
``inflection``. An inflection value of null means that alternate does not
exist. A string replaces the derived form. The validator is reloaded
afterwards, and the file is restored if the registration does not pass.

    PYTHONPATH=src python3 tools/register_forms.py show sheep
    PYTHONPATH=src python3 tools/register_forms.py apply registration.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import cast

from epagoge.inflection import describe_inflections, owed_forms
from epagoge.vocabulary import (
    declared_form_violations,
    load_vocabulary,
    parse_inflection,
    parse_pos,
)

ROOT = Path(__file__).resolve().parent.parent

_NOTES: dict[str, str] = {
    "mass": "mass noun. The citation form is singular and there is no plural.",
    "plural-only": (
        "plural-only noun, pluralia tantum. The citation form is plural "
        "and there is no singular."
    ),
    "periphrastic": "compares with more and most, not with a suffix.",
    "ungraded": "no comparative and no superlative.",
}


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("show", "apply"))
    parser.add_argument("target", help="a headword, or a JSON file when applying")
    parser.add_argument("--pos", default="", help="preview this class instead")
    parser.add_argument("--concept", default="")
    parser.add_argument(
        "--vocabulary",
        type=Path,
        default=ROOT / "curriculum/vocabulary.json",
    )
    parser.add_argument(
        "--inflection",
        default="",
        help="JSON object of slots, used only by a preview",
    )
    args = parser.parse_args(argv[1:])
    if args.command == "show":
        return _show(args)
    return _apply(args)


def _show(args: argparse.Namespace) -> int:
    vocabulary = load_vocabulary(args.vocabulary)
    senses = [term for term in vocabulary.terms if term.word == args.target]
    if args.concept:
        senses = [term for term in senses if term.concept == args.concept]
    if not senses and not args.pos:
        print(f"{args.target}: not a headword", file=sys.stderr)
        return 1
    if not senses:
        _print_table(args.target, "", 0, args.pos, _preview_inflection(args))
        return 0
    for term in senses:
        pos = args.pos or term.pos
        registered = dict(term.inflection)
        if args.inflection:
            registered = _preview_inflection(args)
        _print_table(term.word, term.concept, term.level, pos, registered)
    return 0


def _preview_inflection(args: argparse.Namespace) -> dict[str, str]:
    if not args.inflection:
        return {}
    raw = cast(object, json.loads(args.inflection))
    pos = args.pos
    if not pos:
        vocabulary = load_vocabulary(args.vocabulary)
        matches = [term for term in vocabulary.terms if term.word == args.target]
        if args.concept:
            matches = [term for term in matches if term.concept == args.concept]
        if len(matches) != 1:
            raise SystemExit(f"{args.target}: name the concept or the part of speech")
        pos = matches[0].pos
    parsed = parse_inflection(raw, pos, args.target)
    return dict(parsed)


def _print_table(
    word: str, concept: str, level: int, pos: str, registered: dict[str, str]
) -> None:
    try:
        pos = parse_pos(pos, word) if pos else ""
    except ValueError as exc:
        print(exc, file=sys.stderr)
        raise SystemExit(1) from exc
    where = f"concept={concept} level={level}" if concept else "not admitted"
    print(f"{word}  {where}  pos={pos or '(undeclared)'}")
    if not pos:
        print("  no class declared, so no alternate is checked")
        return
    rows = describe_inflections(word, pos, registered)
    for name, form, origin in rows:
        shown = form if form else "none"
        print(f"  {name:<20} {shown:<16} {origin}")
    owed = owed_forms(word, pos, registered)
    print("  owed distinct forms: " + (" ".join(owed) if owed else "none"))
    parts = set(pos.split())
    if "noun" in parts and "mass" not in parts and "plural-only" not in parts:
        plural = next((form for name, form, _origin in rows if name == "plural"), "")
        if plural == word:
            print(
                "  note: the plural spelling matches the singular. "
                "No number flag is needed."
            )
    for flag, note in _NOTES.items():
        if flag in parts:
            print(f"  note: {note}")


def _apply(args: argparse.Namespace) -> int:
    path = Path(args.target)
    payload = cast(
        dict[str, dict[str, object]],
        json.loads(path.read_text(encoding="utf-8")),
    )
    vocab_path = args.vocabulary
    original = vocab_path.read_text(encoding="utf-8")
    raw = cast(dict[str, object], json.loads(original))
    terms = cast(list[dict[str, object]], raw["terms"])
    core = set(cast(list[str], raw.get("core", [])))
    problems: list[str] = []
    for word, spec in payload.items():
        matches = [term for term in terms if str(term["word"]) == word]
        concept = str(spec.get("concept", ""))
        if concept:
            matches = [term for term in matches if str(term["concept"]) == concept]
        if len(matches) != 1:
            problems.append(f"{word}: expected one sense, found {len(matches)}")
            continue
        term = matches[0]
        pos = str(spec["pos"]) if "pos" in spec else str(term.get("pos", ""))
        try:
            pos = parse_pos(pos, word)
            raw_inflection = (
                spec["inflection"] if "inflection" in spec else term.get("inflection")
            )
            inflection = parse_inflection(raw_inflection, pos, word)
        except ValueError as exc:
            problems.append(str(exc))
            continue
        _write_sense(term, terms, core, word, pos, inflection)
    if problems:
        print(f"{len(problems)} problem(s), nothing written:", file=sys.stderr)
        for line in problems:
            print(f"  {line}", file=sys.stderr)
        return 1
    vocab_path.write_text(
        json.dumps(raw, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    try:
        vocabulary = load_vocabulary(vocab_path)
    except ValueError as exc:
        vocab_path.write_text(original, encoding="utf-8")
        print(f"registration failed to load: {exc}", file=sys.stderr)
        return 1
    violations = declared_form_violations(vocabulary)
    if violations:
        vocab_path.write_text(original, encoding="utf-8")
        print(
            f"{len(violations)} form check(s) failed, file restored:",
            file=sys.stderr,
        )
        for item in violations[:20]:
            print(f"  [{item.code}] {item.detail}", file=sys.stderr)
        return 1
    print(f"registered {len(payload)} sense(s)")
    return 0


def _write_sense(
    term: dict[str, object],
    terms: list[dict[str, object]],
    core: set[str],
    word: str,
    pos: str,
    inflection: tuple[tuple[str, str], ...],
) -> None:
    old_pos = str(term.get("pos", ""))
    old_registered = _stored_inflection(term.get("inflection"))
    old_owed = set(owed_forms(word, old_pos, old_registered))
    new_owed = set(owed_forms(word, pos, dict(inflection)))
    blocked = set(core)
    for other in terms:
        if other is term:
            continue
        if str(other["word"]) == word:
            continue
        blocked.add(str(other["word"]))
        blocked.update(str(form) for form in cast(list[object], other.get("forms", [])))
    existing = [str(form) for form in cast(list[object], term.get("forms", []))]
    kept = [
        form
        for form in existing
        if form not in old_owed and form not in new_owed and form != word
    ]
    forms = sorted(form for form in (new_owed | set(kept)) if form not in blocked)
    if pos:
        term["pos"] = " ".join(sorted(set(pos.split())))
    elif "pos" in term:
        del term["pos"]
    if inflection:
        term["inflection"] = {key: value or None for key, value in inflection}
    elif "inflection" in term:
        del term["inflection"]
    if forms:
        term["forms"] = forms
    elif "forms" in term:
        del term["forms"]


def _stored_inflection(raw: object) -> dict[str, str]:
    if not isinstance(raw, dict):
        return {}
    out: dict[str, str] = {}
    for key, value in cast(dict[object, object], raw).items():
        if isinstance(key, str):
            out[key] = "" if value is None else str(value)
    return out


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
