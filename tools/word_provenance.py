#!/usr/bin/env python3
"""When each word entered the lexicon, and under what reason.

**Post-facto analysis needs to answer, for every word, why it is there.**
Most of the lexicon predates any field recording that, so the answer has
to be recovered rather than invented, and the repository's own history is
the only honest source: the commit that first introduced a word says when
it arrived and, in its message, why.

Walks vocabulary history through the frozen legacy anchor and records the
first commit for each historical word. New words carry direct admission
evidence and are checked before and after their containing commit.
Where a term carries a `source` written at
admission, that is reported alongside and is better evidence, because it
was written when the decision was made rather than reconstructed from it.

**A reconstructed reason is labelled as reconstructed.** A commit subject
is what the commit was about, which is usually but not always why a
particular word was in it.

    PYTHONPATH=src python3 tools/word_provenance.py --out curriculum/provenance.json
"""

from __future__ import annotations

import argparse
import json
import subprocess  # noqa: S404
import sys
from pathlib import Path
from typing import cast

ROOT = Path(__file__).resolve().parent.parent
TRACKED = "curriculum/vocabulary.json"


CRITERIA: dict[str, tuple[str, str]] = {
    "Author a prescriptive level-one lexicon": (
        "prescriptive",
        "Authored as a level-one foundational lexicon before any corpus "
        "existed, chosen for what a child entering kindergarten is expected "
        "to know and for what closing the dictionary required.",
    ),
    "Add a check for concepts with no word": (
        "lexicalisation",
        "Admitted so that a concept the schedule teaches has a word naming "
        "it, which the lexicalisation check requires.",
    ),
    "Add communication, map all vocabulary": (
        "mapping",
        "Mapped from vocabulary the corpus already used, when every term was "
        "given a concept and a level.",
    ),
    "Add per-level vocabulary": (
        "mapping",
        "Admitted when per-level vocabulary was introduced and terms were "
        "assigned the level at which they become admissible.",
    ),
    "Generate whole books": (
        "teacher",
        "Admitted from generation evidence: a word the teacher reached for "
        "and was blocked on, judged suitable for the level.",
    ),
    "Let the corpus feed the lexicon": (
        "teacher",
        "Admitted from generation evidence: a word the teacher reached for "
        "and was blocked on, judged suitable for the level.",
    ),
    "Make verb inflection standard procedure": (
        "inflection",
        "A form of an admitted word, added because a word admitted in one "
        "form is a trap for a generator constrained to the level.",
    ),
    "Remove seven nonsense verb forms": (
        "inflection",
        "An inflection correction, replacing a form the derivation rules had invented.",
    ),
    "Add synonyms to the thesaurus": (
        "thesaurus",
        "Admitted because the thesaurus named it as a synonym or antonym of "
        "an admitted word and the lexicon did not hold it.",
    ),
    "Author the fifty-one missing concepts": (
        "lexicalisation",
        "Admitted alongside a newly authored concept, so that the concept "
        "had a word at its level.",
    ),
    "Build the level-two dictionary and thesaurus": (
        "lexicalisation",
        "Admitted while building the level-two reference material, to "
        "lexicalise a concept or close a definition.",
    ),
    "Draw twenty-six cross-domain prerequisites": (
        "lexicalisation",
        "Admitted while the concept graph gained cross-domain prerequisites, "
        "to lexicalise a concept the change exposed.",
    ),
    "Withdraw the posture ceiling as stated": (
        "operator",
        "Admitted on operator direction, to give the level the vocabulary to "
        "discuss a subject it had been unable to name.",
    ),
    "Admit what kindergarten already knows": (
        "operator",
        "Admitted on operator direction, being a word a reader at this level "
        "plainly knows that the lexicon had missed.",
    ),
    "Build the lexicon sourcing pipeline": (
        "scan",
        "Proposed by a frequency scan of a source and admitted on judgement.",
    ),
}
"""Commit subject prefix to the criterion a word admitted there met.

**Reconstructed 2026-09-25 and of low to moderate fidelity.** No criterion
was recorded at the time for all but one word in the lexicon, so this is
the reason the commit gives for its batch, applied to every word in it. It
is right about the pass and cannot be right about every word in a pass.

The largest group is the least precise. 444 words entered in a single
prescriptive authoring pass, and declaring all of them admitted on that
criterion explains any one of them only loosely. Bootstrapping a closed
lexicon does not decompose into per-word reasons, which is part of why it
is a hard problem.
"""

BOOK_ROUND = (
    "corpus",
    "Admitted during a book-writing round, from a word the teacher was "
    "blocked on and that triage judged suitable for the level.",
)
"""The fallback. Most remaining commits are rounds of corpus writing, and
a word first seen in one arrived the same way: the teacher reached for it
and the triage admitted it."""


def criterion_for(subject: str) -> tuple[str, str]:
    for prefix, answer in CRITERIA.items():
        if subject.startswith(prefix):
            return answer
    return BOOK_ROUND


def git(*args: str) -> str:
    return subprocess.run(  # noqa: S603
        ["git", *args],  # noqa: S607
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout


def words_at(revision: str) -> set[str]:
    """The headwords present in one revision of the lexicon."""
    try:
        blob = git("show", f"{revision}:{TRACKED}")
    except subprocess.CalledProcessError:
        return set()
    try:
        payload = cast("dict[str, object]", json.loads(blob))
    except json.JSONDecodeError:
        return set()
    terms = cast("list[dict[str, object]]", payload.get("terms", []))
    return {str(t["word"]) for t in terms if "word" in t}


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=None)
    # **A provenance record that has drifted is worse than none**, because
    # it reads as evidence. The gate regenerates and compares rather than
    # trusting the file.
    parser.add_argument(
        "--check",
        action="store_true",
        help="compare curriculum/provenance.json against the history",
    )
    parser.add_argument("--top", type=int, default=12)
    args = parser.parse_args(argv[1:])

    if git("rev-parse", "--is-shallow-repository").strip() == "true":
        print("full history is required to verify provenance", file=sys.stderr)
        return 1
    path = ROOT / "curriculum/provenance.json"
    held = cast(dict[str, object], json.loads(path.read_text(encoding="utf-8")))
    # Freeze the legacy reconstruction. New admissions carry evidence directly,
    # so their validity cannot depend on the hash of the commit containing them.
    anchor = str(held.get("history_through", git("rev-parse", "HEAD").strip()))
    history = [
        line.split("\t", 2)
        for line in git(
            "log",
            anchor,
            "--reverse",
            "--format=%H\t%ad\t%s",
            "--date=short",
            "--",
            TRACKED,
        ).splitlines()
        if line.strip()
    ]
    if not history:
        print("no history for the vocabulary", file=sys.stderr)
        return 2
    current = cast(dict[str, object], json.loads((ROOT / TRACKED).read_text()))
    baseline = cast(dict[str, object], json.loads(git("show", f"{anchor}:{TRACKED}")))
    sources: dict[str, str] = {}
    for payload in (baseline, current):
        for term in cast(list[dict[str, object]], payload.get("terms", [])):
            source = str(term.get("source", "")).strip()
            if source:
                sources[str(term["word"])] = source
    working = {str(t["word"]) for t in cast(list[dict[str, object]], current["terms"])}

    # **Words that have left the lexicon are kept.** The record is a
    # history and a word folded into its base word still happened.
    first: dict[str, dict[str, str]] = {}
    seen: set[str] = set()
    for commit, date, subject in history:
        present = words_at(commit)
        for word in sorted(present - seen):
            first[word] = {
                "commit": commit[:12],
                "date": date,
                "commit_subject": subject,
            }
        seen |= present

    for word, entry in first.items():
        kind, reason = criterion_for(entry["commit_subject"])
        entry["criterion"] = kind
        entry["admitted_because"] = reason
        if word in sources:
            entry["source"] = sources[word]
            entry["evidence"] = "recorded at admission"
        else:
            entry["evidence"] = "reconstructed from history"

    recorded_words = cast(dict[str, object], held.get("words", {}))
    for word in sorted((working | recorded_words.keys()) - first.keys()):
        source = sources.get(word)
        if word not in working:
            # Retired direct admissions remain as historical evidence.
            entry = recorded_words[word]
            if not isinstance(entry, dict) or set(cast(dict[str, object], entry)) != {
                "source",
                "evidence",
            }:
                print(f"invalid retired admission for {word}", file=sys.stderr)
                return 1
            archived = cast(dict[str, str], entry)
            if archived.get("evidence") != "recorded at admission":
                return 1
            source = archived.get("source")
        if not isinstance(source, str) or not source.strip():
            print(f"{word} needs a source recorded at admission", file=sys.stderr)
            return 1
        first[word] = {"source": source, "evidence": "recorded at admission"}

    recorded = sum(
        1 for e in first.values() if e["evidence"] == "recorded at admission"
    )
    print(f"revisions of the lexicon      {len(history)}")
    print(f"words with provenance         {len(first)}")
    print(f"  source recorded at admission  {recorded}")
    print(f"  reconstructed from history    {len(first) - recorded}")
    print()
    by_date: dict[str, int] = {}
    for entry in first.values():
        date = entry.get("date", "direct admission")
        by_date[date] = by_date.get(date, 0) + 1
    print("words first seen, by date")
    for date in sorted(by_date):
        print(f"  {date}  {by_date[date]:>5}")
    print()
    by_criterion: dict[str, int] = {}
    for entry in first.values():
        key = entry.get("criterion", "direct admission")
        by_criterion[key] = by_criterion.get(key, 0) + 1
    print("admission criterion, reconstructed and of low to moderate fidelity")
    for kind, n in sorted(by_criterion.items(), key=lambda kv: -kv[1]):
        print(f"  {kind:<16} {n:>5}")

    if args.check:
        changed = sorted(
            word
            for word in first.keys() | recorded_words.keys()
            if first.get(word) != recorded_words.get(word)
        )
        if (
            "history_through" not in held
            or changed
            or held.get("revisions") != len(history)
        ):
            print(
                f"provenance is stale ({len(changed)} entries). "
                "Regenerate before committing.",
                file=sys.stderr,
            )
            for word in changed[:10]:
                print(f"  {word}", file=sys.stderr)
            return 1
        print("provenance fields and admission coverage match")
        return 0

    if args.out is not None:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(
            json.dumps(
                {
                    "_comment": (
                        "Legacy history is frozen at history_through. New words "
                        "carry direct source evidence without a commit hash. "
                        "When each word entered the lexicon. 'recorded at "
                        "admission' is evidence written when the decision was "
                        "made. 'reconstructed from history' is the commit that "
                        "first contained the word, which is what the commit was "
                        "about rather than necessarily why that word was in it. "
                        "'admitted_because' is the criterion that commit's "
                        "batch met, applied to every word in it: right about "
                        "the pass and not necessarily about each word. Low to "
                        "moderate fidelity, and lowest for the 444-word "
                        "prescriptive pass, because bootstrapping a closed "
                        "lexicon does not decompose into per-word reasons."
                    ),
                    "history_through": anchor,
                    "revisions": len(history),
                    "words": dict(sorted(first.items())),
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        print(f"\nwrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
