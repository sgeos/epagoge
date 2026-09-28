"""Draft definitions for candidate words, so they can be admitted.

**The pipeline had a hole in the middle.** `tools/admit.py` refuses a word
without a definition, correctly, because a word admitted without a grounded
one takes the dictionary out of self-hosting. `generate_dictionary.py` writes
definitions for words that are *already* admitted. **Nothing took a candidate
and produced the definition that would let it in**, so the only route was
writing them by hand, which is what the 47-word batch of 2026-09-27 did.

Nine thousand words at a hundred a session is ninety sessions. This is the
missing step, and the point of it is that every later batch is cheap rather
than that this one is large.

**The teacher proposes and the tools decide.** A definition that reaches
outside the level's vocabulary is dropped here, and `admit.py` then re-checks
every survivor against the whole dictionary's closure. **Nothing is admitted by
this file.** It writes the input that the admission tool judges.

**Archaism is invisible to this and will stay so.** The candidates come from a
frequency scan over public-domain sources, which are public domain because they
are old, and neither the counter nor the teacher can see that a word was
ordinary in 1880 and wrong for a child now. See
`docs/decisions/LEXICON_SOURCING.md`.

Input is JSON mapping a word to the concept it names:

    {"tide": "cycle", "shore": "spatial_position"}

Output is what `tools/admit.py` consumes, with the source recorded.

    PYTHONPATH=src:generators python3 generators/define_candidates.py \\
      candidates.json --level 2 --out batch.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import cast

from epagoge import prompt as prompts
from epagoge.vocabulary import Vocabulary, load_vocabulary, unlicensed
from generate import ask
from generate_dictionary import ENTRY_RE, as_sentence

ROOT = Path(__file__).resolve().parents[1]

WORD_RE = re.compile(r"[a-z']+")

BATCH = 12
"""Words per request to the teacher.

Batched because related words define each other more consistently when the
teacher sees them together, and because one call per word spends the budget on
prompt overhead. Twelve is the size `generate_dictionary.py` settled on.
"""

DEFINING_WORDS = 700
"""How many words the teacher is asked to write definitions in.

**The prompt used to list the whole lexicon, so it grew with the thing being
built.** At 934 admissible words it reached 3,494 tokens against a budget of
3,328 and `ask` refused. At the ten-thousand-word target the list alone is
roughly fifteen thousand tokens, so no context this machine can hold would be
enough, and raising it to 6,144 drove swap to 14.9 GB of 16.4 GB.

**So the ask is narrowed and the acceptance is not.** The teacher is given the
seed, the function words and the most-used content words; a definition is
accepted if it stays inside the level, which is the real constraint. Asking for
less than is allowed costs nothing and a definition written in common words is
better grounded anyway.

700 is chosen to leave headroom in the budget rather than to fill it.
"""


def defining_vocabulary(vocabulary: Vocabulary, level: int, corpus: Path) -> list[str]:
    """The words a definition is asked to use: seed, function words, common ones.

    **Frequency in the corpus is the ranking**, because a word the books
    already lean on is one a definition can lean on. Words the corpus has not
    used yet fall to the end and are cut first.
    """
    counts: Counter[str] = Counter()
    for path in sorted(corpus.glob("*.md")):
        counts.update(WORD_RE.findall(path.read_text(encoding="utf-8").lower()))
    always = {*vocabulary.core, *vocabulary.exempt, *vocabulary.ostensive}
    content = {t.word for t in vocabulary.terms if t.level <= level} - always
    ranked = sorted(content, key=lambda w: (-counts[w], w))
    room = max(DEFINING_WORDS - len(always), 0)
    return sorted(always | set(ranked[:room]))


def load_candidates(path: Path) -> dict[str, str]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(f"{path}: expected an object mapping word to concept")
    out: dict[str, str] = {}
    for word, concept in cast("dict[str, object]", raw).items():
        if not isinstance(concept, str) or not concept:
            raise ValueError(f"{path}: {word} has no concept")
        out[word] = concept
    if not out:
        raise ValueError(f"{path}: no candidates")
    return out


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    parser.add_argument("--level", type=int, default=2)
    parser.add_argument("--attempts", type=int, default=3)
    parser.add_argument("--timeout", type=int, default=240)
    parser.add_argument("--pos", default="noun", help="part of speech for the batch")
    parser.add_argument(
        "--source",
        default="",
        help="where these words were proposed, recorded on every term",
    )
    # Required, because three tools defaulted their output to a tracked record
    # and one of them was overwritten twice before the default was removed.
    parser.add_argument(
        "--out",
        type=Path,
        required=True,
        help="where to write the admission batch",
    )
    args = parser.parse_args(argv[1:])

    candidates = load_candidates(args.file)
    vocabulary = load_vocabulary(ROOT / "curriculum/vocabulary.json")
    admissible = defining_vocabulary(
        vocabulary, args.level, ROOT / f"curriculum/books/level_{args.level - 1}"
    )
    print(f"  defining vocabulary {len(admissible)} words", file=sys.stderr)

    already = [w for w in candidates if vocabulary.lookup(w) is not None]
    if already:
        print(f"  {len(already)} already admissible, skipped", file=sys.stderr)
    wanted = {w: c for w, c in candidates.items() if w not in {*already}}

    accepted: dict[str, dict[str, str]] = {}
    outside: dict[str, int] = {}
    words = sorted(wanted)
    for start in range(0, len(words), BATCH):
        chunk = words[start : start + BATCH]
        pairs = [(w, wanted[w]) for w in chunk]
        print(f"  defining {len(chunk)}: {' '.join(chunk)}", file=sys.stderr)
        for _attempt in range(args.attempts):
            missing = [p for p in pairs if p[0] not in accepted]
            if not missing:
                break
            raw = ask(
                prompts.definitions(
                    missing, args.level, admissible, vocabulary.substitutions
                ),
                timeout=args.timeout,
            )
            for line in raw.splitlines():
                match = ENTRY_RE.match(line.strip())
                if not match:
                    continue
                word, text = match.group(1), as_sentence(match.group(2).strip())
                if word not in wanted or word in accepted:
                    continue
                # **The definition must stay inside the level.** A definition
                # reaching outside it is the failure that produced eight
                # admissible definitions from ninety-six requests before the
                # prompt named the vocabulary, and it is still the common one.
                stray = sorted(set(unlicensed(vocabulary, text, args.level)) - {word})
                if stray:
                    for token in stray:
                        outside[token] = outside.get(token, 0) + 1
                    continue
                accepted[word] = {
                    "concept": wanted[word],
                    "pos": args.pos,
                    "definition": text,
                    "source": args.source,
                }

    offered = len(wanted)
    print(f"\noffered   {offered}")
    print(f"defined   {len(accepted)}")
    if offered:
        print(f"rate      {len(accepted) / offered:.0%}")
    if outside:
        print("\nwords the teacher reached for and could not have:")
        for token, count in sorted(outside.items(), key=lambda kv: -kv[1])[:15]:
            print(f"  {count:4d}  {token}")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(accepted, indent=2) + "\n", encoding="utf-8")
    print(f"\nwrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
