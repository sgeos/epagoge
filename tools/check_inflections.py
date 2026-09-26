"""Compare the inflections this project generates against WordNet's.

**Every irregular form this project got wrong by hand is in WordNet's
exception files.** `thiefs` for `thieves`, `farrer` for `farther`,
`lighted` where `lit` belongs, and `copieds` from a participle filed as a
headword. All four were found on 2026-09-26 by reading 535 unused surface
forms one at a time, which is the most expensive way to find them.

WordNet ships `noun.exc`, `verb.exc` and `adj.exc`: one line per
irregular form, the form first and its base second. That is exactly the
table `epagoge.inflection` maintains by hand, and comparing the two turns
a reading exercise into a check.

**REPORTED, NEVER GATED, and the reference is not in the repository.**
`docs/decisions/REFERENCE_SOURCES.md` says where to fetch it and why it is
not vendored. Absent the files this skips loudly rather than passing
silently, which is the same discipline the disclosure scan follows and for
the same reason: a check that quietly does nothing is worse than no check.

**WordNet is a reference, not an authority here.** It records what English
does; this project decides what a level admits. A mismatch is a question,
not a defect, and the operator's rule that archaic inflections need not be
admitted means some mismatches are correct.

    PYTHONPATH=src python3 tools/check_inflections.py --level 1
"""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from pathlib import Path

from epagoge.inflection import comparison, plural, verb_forms
from epagoge.vocabulary import load_vocabulary

ROOT = Path(__file__).resolve().parent.parent
REFERENCE = ROOT / "tmp/references/dict"
EXCEPTIONS = ("noun.exc", "verb.exc", "adj.exc")


def wordnet_exceptions(directory: Path) -> dict[tuple[str, str], set[str]]:
    """(base, part of speech) to the irregular forms WordNet records.

    Each line is ``form base [base...]``. A form may have more than one
    base, and a base more than one form, so both directions are sets.

    **The part of speech is which file the line came from**, and keying on
    it is what makes this check usable. WordNet lists `cupped` under verbs
    because `cup` is also a verb in English. This project admits `cup` as a
    noun only, so `cupped` is not a gap. Keyed on the word alone the check
    reported 89 such non-gaps and buried the four real ones.
    """
    out: dict[tuple[str, str], set[str]] = defaultdict(set)
    for name in EXCEPTIONS:
        path = directory / name
        if not path.exists():
            continue
        stem: str = name.split(".")[0]
        pos: str = "adjective" if stem == "adj" else stem
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            parts = line.split()
            if len(parts) < 2:
                continue
            form, bases = parts[0], parts[1:]
            for base in bases:
                out[(base, pos)].add(form)
    return out


def generated(word: str, pos: str) -> set[str]:
    """Every form this project's rules produce for a word."""
    parts = pos.split()
    forms: set[str] = set()
    if "verb" in parts:
        forms |= set(verb_forms(word))
    if "noun" in parts and "mass" not in parts:
        forms.add(plural(word))
    if "adjective" in parts:
        forms |= {f for f in comparison(word) if f}
    return {f for f in forms if f and f != word}


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--level", type=int, default=1)
    parser.add_argument("--show", type=int, default=40)
    args = parser.parse_args(argv[1:])

    if not REFERENCE.exists():
        print(f"SKIPPED: {REFERENCE.relative_to(ROOT)} absent.")
        print("  See docs/decisions/REFERENCE_SOURCES.md for how to fetch it.")
        return 0

    exceptions = wordnet_exceptions(REFERENCE)
    if not exceptions:
        print(f"SKIPPED: {REFERENCE.relative_to(ROOT)} holds no exception files.")
        return 0

    vocabulary = load_vocabulary(ROOT / "curriculum/vocabulary.json")
    # **core and exempt count as admitted and the first version of this
    # omitted them**, so it reported `leaves` as missing from `leaf` when
    # the lexicon carries it. A check whose own denominator is wrong
    # manufactures findings, which is the failure this file exists to
    # catch in the inflection rules.
    admitted = (
        {
            f
            for t in vocabulary.terms
            if t.level <= args.level
            for f in (*(t.forms or ()), t.word)
        }
        | set(vocabulary.core)
        | set(vocabulary.exempt)
    )

    missing: list[tuple[str, str]] = []
    manufactured: list[tuple[str, str, str]] = []
    for term in vocabulary.terms:
        if term.level > args.level or not term.pos:
            continue
        claimed = [p for p in term.pos.split() if p in ("noun", "verb", "adjective")]
        irregular: set[str] = set()
        for pos in claimed:
            irregular |= exceptions.get((term.word, pos), set())
        if not irregular:
            continue
        ours = generated(term.word, term.pos)
        for form in sorted(irregular):
            if form not in admitted:
                missing.append((term.word, form))
        # A form we generate that WordNet does not list, for a word WordNet
        # says is irregular, is the shape that produced `thiefs`.
        for form in sorted(ours - irregular):
            if form not in admitted:
                manufactured.append((term.word, form, ", ".join(sorted(irregular))))

    print(
        f"  WordNet exception entries  {len(exceptions)} word and part-of-speech pairs"
    )
    print(f"  irregular forms WordNet has and this level does not  {len(missing)}")
    for word, form in missing[: args.show]:
        print(f"    {word:14s} wants {form}")
    if len(missing) > args.show:
        print(f"    ... and {len(missing) - args.show} more")
    print(
        f"  forms this project generates for a word WordNet calls irregular  "
        f"{len(manufactured)}"
    )
    for word, form, listed in manufactured[: args.show]:
        print(f"    {word:14s} generates {form:16s} WordNet says {listed}")
    if len(manufactured) > args.show:
        print(f"    ... and {len(manufactured) - args.show} more")
    print("  reported, never gated; WordNet records English and this project")
    print("  decides what a level admits, so a mismatch is a question")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
