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

Optional ``--senses`` reads an object keyed by exactly the candidate words.
Each value contains ``sense`` and ``pos`` strings. Sense descriptions are
limited to 240 characters and parts of speech override the batch default.
These instructions constrain meaning without licensing additional words.

    PYTHONPATH=src:generators python3 generators/define_candidates.py \\
      candidates.json --level 2 --source "manual proposals" \
      --out batch.json --report report.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from collections.abc import Sequence
from pathlib import Path
from typing import TypedDict, cast

from epagoge import prompt as prompts
from epagoge.artifacts import check_outputs, digest, file_digest, write_json
from epagoge.concept_graph import ConceptGraph
from epagoge.vocabulary import (
    RECOGNISED_POS,
    Vocabulary,
    load_vocabulary,
    substitutions_at,
    tokenise,
    unlicensed,
)
from generate import MODEL, NUM_CTX, ask, well_formed
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


def defining_vocabulary(
    vocabulary: Vocabulary,
    level: int,
    corpus: Path,
    selected: Sequence[str] = (),
) -> list[str]:
    """The words a definition is asked to use: seed, function words, common ones.

    **Frequency in the corpus is the ranking**, because a word the books
    already lean on is one a definition can lean on. Words the corpus has not
    used yet fall to the end and are cut first.
    """
    if not 1 <= level <= 7:
        raise ValueError("level must be between one and seven")
    if any(tokenise(word) != [word] for word in selected):
        raise ValueError("invalid selected defining word")
    if len(set(selected)) != len(selected):
        raise ValueError("duplicate selected defining word")
    unavailable = [word for word in selected if unlicensed(vocabulary, word, level)]
    if unavailable:
        raise ValueError(
            f"selected defining words unavailable at level {level}: "
            + " ".join(unavailable)
        )
    counts: Counter[str] = Counter()
    for path in sorted(corpus.glob("*.md")):
        counts.update(WORD_RE.findall(path.read_text(encoding="utf-8").lower()))
    always = {*vocabulary.core, *vocabulary.exempt, *vocabulary.ostensive}
    # Selected licensed words replace ranked slots, never enlarge the budget.
    required = always | set(selected)
    if len(required) > DEFINING_WORDS:
        raise ValueError(
            "mandatory and selected words exceed defining vocabulary limit"
        )
    content = {t.word for t in vocabulary.terms if t.level <= level} - required
    ranked = sorted(content, key=lambda w: (-counts[w], w))
    room = DEFINING_WORDS - len(required)
    return sorted(required | set(ranked[:room]))


class SenseSpec(TypedDict):
    sense: str
    pos: str


def unique_fields(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate field {key}")
        result[key] = value
    return result


def load_senses(path: Path, candidates: dict[str, str]) -> dict[str, SenseSpec]:
    """Reject ambiguous specifications before crossing the teacher boundary."""
    raw = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_fields)
    if not isinstance(raw, dict) or set(cast(dict[str, object], raw)) != set(
        candidates
    ):
        raise ValueError("sense specifications must cover exactly the candidate set")
    specs: dict[str, SenseSpec] = {}
    for word, value in cast(dict[str, object], raw).items():
        if not isinstance(value, dict) or set(cast(dict[str, object], value)) != {
            "sense",
            "pos",
        }:
            raise ValueError(f"{word}: expected only sense and pos fields")
        row = cast(dict[str, object], value)
        sense, pos = row["sense"], row["pos"]
        if not isinstance(sense, str) or not sense.strip() or len(sense) > 240:
            raise ValueError(f"{word}: sense must contain 1 to 240 characters")
        if not isinstance(pos, str):
            raise ValueError(f"{word}: pos must be text")
        parts = pos.split()
        if (
            not parts
            or len(set(parts)) != len(parts)
            or set(parts) - set(RECOGNISED_POS)
            or ("mass" in parts and "noun" not in parts)
            or ("periphrastic" in parts and "adjective" not in parts)
        ):
            raise ValueError(f"{word}: invalid parts of speech")
        specs[word] = {"sense": sense, "pos": pos}
    return specs


def load_candidates(path: Path) -> dict[str, str]:
    raw = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_fields)
    if not isinstance(raw, dict):
        raise ValueError(f"{path}: expected an object mapping word to concept")
    out: dict[str, str] = {}
    for word, concept in cast("dict[str, object]", raw).items():
        if WORD_RE.fullmatch(word) is None:
            raise ValueError(f"{path}: invalid candidate word {word!r}")
        if not isinstance(concept, str) or not concept.strip():
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
        "--senses",
        type=Path,
        help="optional JSON mapping every candidate to sense and pos fields",
    )
    parser.add_argument(
        "--defining-word",
        action="append",
        default=[],
        help="licensed word to retain within the list limit; repeatable",
    )
    parser.add_argument(
        "--source",
        required=True,
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
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args(argv[1:])
    if not args.source.strip() or args.attempts < 1 or args.timeout < 1:
        parser.error(
            "source must be nonblank and attempts and timeout must be positive"
        )
    if not 1 <= args.level <= 7:
        parser.error("level must be between one and seven")
    if not args.pos.split() or set(args.pos.split()) - set(RECOGNISED_POS):
        parser.error("unrecognised or empty parts of speech")
    try:
        candidates = load_candidates(args.file)
        senses = load_senses(args.senses, candidates) if args.senses else {}
        graph = ConceptGraph.load(ROOT / "curriculum/graph/concepts.json")
        if set(candidates.values()) - graph.nodes.keys():
            raise ValueError("candidates name unknown concepts")
        check_outputs([args.out, args.report])
        vocabulary = load_vocabulary(ROOT / "curriculum/vocabulary.json")
        admissible = defining_vocabulary(
            vocabulary,
            args.level,
            ROOT / f"curriculum/books/level_{args.level - 1}",
            args.defining_word,
        )
    except (ValueError, OSError) as exc:
        parser.error(str(exc))
    print(f"  defining vocabulary {len(admissible)} words", file=sys.stderr)

    already = [w for w in candidates if vocabulary.lookup(w) is not None]
    if already:
        print(f"  {len(already)} already admissible, skipped", file=sys.stderr)
    wanted = {w: c for w, c in candidates.items() if w not in {*already}}

    requests: list[dict[str, object]] = []
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
            question = prompts.definitions(
                missing,
                args.level,
                admissible,
                substitutions_at(vocabulary, args.level),
            )
            if senses:
                question += (
                    "\n\nDefine only the following senses and parts of speech. "
                    "These notes describe meaning, not additional licensed words. "
                    "Keep the definitions inside the word list above.\n"
                    + json.dumps({word: senses[word] for word, _ in missing})
                )
            events: list[dict[str, object]] = []
            request: dict[str, object] = {
                "requested": [w for w, _ in missing],
                "prompt": question,
                "outcomes": events,
            }
            requests.append(request)
            try:
                raw = ask(question, timeout=args.timeout)
            except (OSError, RuntimeError, ValueError) as exc:
                raw = ""
                request["error"] = str(exc)
            request["response"] = raw
            seen: set[str] = set()
            for line in raw.splitlines():
                match = ENTRY_RE.match(line.strip())
                if not match:
                    events.append({"line": line, "status": "malformed"})
                    continue
                word, text = match.group(1), as_sentence(match.group(2).strip())
                if word not in {w for w, _ in missing} or word in seen:
                    events.append({"word": word, "status": "unexpected_or_duplicate"})
                    continue
                seen.add(word)
                if not well_formed(text):
                    events.append({"word": word, "status": "malformed_definition"})
                    continue
                # **The definition must stay inside the level.** A definition
                # reaching outside it is the failure that produced eight
                # admissible definitions from ninety-six requests before the
                # prompt named the vocabulary, and it is still the common one.
                stray = sorted(set(unlicensed(vocabulary, text, args.level)) - {word})
                if stray:
                    events.append(
                        {"word": word, "status": "outside_vocabulary", "tokens": stray}
                    )
                    for token in stray:
                        outside[token] = outside.get(token, 0) + 1
                    continue
                events.append({"word": word, "status": "mechanically_accepted"})
                accepted[word] = {
                    "concept": wanted[word],
                    "pos": senses[word]["pos"] if senses else args.pos,
                    "definition": text,
                    "source": args.source,
                }

            for word, _ in missing:
                if word not in seen:
                    events.append({"word": word, "status": "omitted"})

    offered = len(wanted)
    print(f"\noffered   {offered}")
    print(f"defined   {len(accepted)}")
    if offered:
        print(f"rate      {len(accepted) / offered:.0%}")
    if outside:
        print("\nwords the teacher reached for and could not have:")
        for token, count in sorted(outside.items(), key=lambda kv: -kv[1])[:15]:
            print(f"  {count:4d}  {token}")
    report: dict[str, object] = {
        "level": args.level,
        "source": args.source,
        "candidates": candidates,
        "input_hash": file_digest(args.file),
        "vocabulary_hash": file_digest(ROOT / "curriculum/vocabulary.json"),
        "graph_hash": file_digest(ROOT / "curriculum/graph/concepts.json"),
        "teacher": MODEL,
        "context": NUM_CTX,
        "attempt_limit": args.attempts,
        "sense_specifications": senses,
        "sense_input_hash": file_digest(args.senses) if args.senses else None,
        "selected_defining_words": args.defining_word,
        "defining_vocabulary": admissible,
        "requests": requests,
        "outcomes": {
            word: "already_admitted"
            if word in already
            else "mechanically_accepted"
            if word in accepted
            else "deferred"
            for word in candidates
        },
        "counts": {
            "input": len(candidates),
            "already_admitted": len(already),
            "offered": offered,
            "mechanically_accepted": len(accepted),
            "deferred": offered - len(accepted),
        },
        "mechanical_acceptance_rate": len(accepted) / offered if offered else None,
        "accepted": accepted,
        "accepted_hash": digest(accepted),
        "note": (
            "Mechanical validation does not establish meaning or dictionary grounding."
        ),
    }
    write_json(args.out, accepted)
    write_json(args.report, report)
    print(f"\nwrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
