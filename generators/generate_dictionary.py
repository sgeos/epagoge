#!/usr/bin/env python3
"""Close a level's lexicon by defining its words in its own words.

**This is the self-hosting case and level one is the hard one.** Level two
builds on a lexicon that is already closed. Level one has nothing under it
but the function words, which name nothing, so it has to define itself.

The closure check drives the order. Words that other definitions already
use and that nothing defines are the frontier, and closing them is the
shortest path to a lexicon that reduces to the seed.

    PYTHONPATH=src:generators python3 generators/generate_dictionary.py \
        --batches 4 --size 12
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import cast

from generate import ask, well_formed
from generate_books import admissible_words
from epagoge import prompt as prompts
from epagoge.book import dictionary_closure, load_book_dir, render_book
from epagoge.vocabulary import load_vocabulary, tokenise, unlicensed

ROOT = Path(__file__).resolve().parent.parent

ENTRY_RE = re.compile(r"^(?:WORD\s+)?([a-z][a-z']*)\s*:\s*(.+)$")
"""The prefix is optional because the teacher drops it.

Asked for `WORD cup: ...` it returns `cup: ...`, which is the better format
and is what a dictionary looks like. Requiring the prefix rejected every
line of six consecutive batches while the definitions themselves were fine.
"""


def as_sentence(text: str) -> str:
    """A dictionary entry reads lower case. A corpus record is a sentence."""
    return text[:1].upper() + text[1:] if text else text


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--level", type=int, default=1)
    parser.add_argument("--batches", type=int, default=2)
    parser.add_argument("--size", type=int, default=12, help="words per batch")
    parser.add_argument("--timeout", type=int, default=600)
    args = parser.parse_args(argv[1:])

    book_dir = ROOT / f"curriculum/books/level_{args.level}"
    vocabulary = load_vocabulary(ROOT / "curriculum/vocabulary.json")
    admissible = admissible_words(vocabulary, args.level)
    seed = set(vocabulary.core) | set(vocabulary.exempt)
    concept_of = {t.word: t.concept for t in vocabulary.terms if t.level <= args.level}

    _, records = load_book_dir(book_dir)
    defined: dict[str, str] = {}
    for record in records:
        entry = cast(dict[str, object], record)
        definition = cast(dict[str, object], entry.get("defines") or {})
        if definition.get("kind") == "word":
            defined[str(definition["target"])] = str(entry["content"])

    def resolve(token: str) -> str | None:
        found = vocabulary.lookup(token)
        return found.word if found is not None else None

    written: list[dict[str, object]] = []
    for batch in range(args.batches):
        closure = dictionary_closure(defined, seed, tokenise, resolve)
        # The frontier first. A word other definitions already lean on, with
        # nothing under it, is what keeps the lexicon from reducing.
        frontier = [w for w in closure.undefined if w in concept_of]
        rest = sorted(w for w in concept_of if w not in defined and w not in frontier)
        todo = (frontier + rest)[: args.size]
        if not todo:
            print("nothing left to define", file=sys.stderr)
            break

        print(
            f"batch {batch + 1}: {len(todo)} words, {len(frontier)} on the frontier",
            file=sys.stderr,
        )
        raw = ask(
            prompts.definitions(
                {w: concept_of[w] for w in todo}, args.level, admissible
            ),
            timeout=args.timeout,
        )
        kept = 0
        for line in raw.splitlines():
            match = ENTRY_RE.match(line.strip())
            if match is None:
                continue
            word, text = match.group(1), as_sentence(match.group(2).strip())
            if word not in todo or word in defined:
                continue
            if not well_formed(text) or unlicensed(vocabulary, text, args.level):
                continue
            defined[word] = text
            written.append(
                {
                    "id": f"dict.{args.level}.{word}",
                    "level": args.level,
                    "concepts": [concept_of[word]],
                    "claim_class": "formal",
                    "content": text,
                    "provenance": {"source_claim": f"lexicon:{word}"},
                    "defines": {"kind": "word", "target": word},
                }
            )
            kept += 1
        print(f"  kept {kept} of {len(todo)}", file=sys.stderr)

    if written:
        head = {
            "id": f"bk.dictionary.{args.level}",
            "level": args.level,
            "title": f"Words at level {args.level}",
            "subject": {"kind": "word", "target": str(written[0]["defines"]["target"])},  # type: ignore[index]
        }
        path = book_dir / f"bk.dictionary.{args.level}.md"
        if path.exists():
            _, old = load_book_dir(book_dir)
            have = {str(cast(dict[str, object], r)["id"]) for r in old}
            written = [r for r in written if str(r["id"]) not in have]
        path.write_text(render_book(head, written), encoding="utf-8")

    closure = dictionary_closure(defined, seed, tokenise, resolve)
    print(
        f"defined {len(defined)} of {len(concept_of)}"
        f" | grounded {len(closure.grounded)}"
        f" | undefined-but-used {len(closure.undefined)}"
        f" | cycles {len(closure.cycles)}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
