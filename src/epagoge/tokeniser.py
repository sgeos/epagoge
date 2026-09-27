"""Word-level tokenisation over a closed lexicon.

**The lexicon is closed, so the vocabulary is known before the corpus is
written.** That is unusual and it is worth using. A word-level vocabulary
of about a thousand entries beats bytes here, because the corpus is small
enough that byte-level would spend its capacity learning spelling that the
lexicon already fixes.

An unknown token is a defect rather than a fallback. The corpus validator
rejects any record using a word outside the level, so a stream that
produces unknowns has come from somewhere the validator did not check.

Standard library only, matching the rest of the package.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Final

from epagoge.vocabulary import Vocabulary, fold_typography

WORD_RE: Final[re.Pattern[str]] = re.compile(
    r"[a-z]+(?:'(?!s\b)[a-z]+)*|'s\b|[0-9]+|[.,!?;:]"
)
"""Words, numerals, and the punctuation the corpus actually uses.

**A possessive is grammar, not vocabulary.** Matched as part of the word,
`boat's` became a token the lexicon could never hold, and admitting it
would have meant admitting the possessive of every noun. The trailing
`'s` is split off and carried as its own token, while a contraction such
as `don't` stays whole because its clitic is not `s`.
"""

POSSESSIVE: Final[str] = "'s"

PAD: Final[str] = "<pad>"
UNK: Final[str] = "<unk>"
BOOK: Final[str] = "<book>"

EOT: Final[str] = "<eot>"
"""End of text. **A work has to be able to end.**

Until 2026-09-27 nothing in the vocabulary meant "this work is finished", so
`pilot.sample` had no stopping condition and emitted exactly the number of
tokens it was asked for, stopping mid-clause wherever that fell.

`docs/decisions/STRUCTURAL_TOKENS.md` has the grounds. The short form is
that this is universal practice, that GPT-2 shipped `<|endoftext|>` as
essentially its only special token, and that TinyStories, which is the
closest published precedent to this corpus, separates stories with it.
"""

RESERVED_COUNT: Final[int] = 16
"""Unused token slots, held so the next structural token is not a migration.

**Adding a token changes the vocabulary size, which invalidates every
checkpoint on disk.** Llama 3 ships 256 reserved slots for this reason. That
count is proportionate to a vocabulary of 128,000 and not to one of 2,250,
so sixteen is held here instead, costing sixteen embedding rows.

**They are never emitted, so their rows stay near initialisation.** That is
the same property that made `<book>` useless as a sampling seed, and it is
correct here: a reserved slot is a placeholder, not a token with a meaning
waiting to be learned.
"""

RESERVED: Final[tuple[str, ...]] = tuple(
    f"<reserved_{n}>" for n in range(RESERVED_COUNT)
)

SPECIALS: Final[tuple[str, ...]] = (PAD, UNK, BOOK, EOT, POSSESSIVE) + RESERVED


@dataclass(frozen=True, slots=True)
class Tokeniser:
    """A fixed word-to-id map built from the lexicon."""

    ids: dict[str, int] = field(default_factory=dict[str, int])
    words: tuple[str, ...] = ()

    @property
    def size(self) -> int:
        return len(self.words)

    def encode(self, text: str) -> list[int]:
        unk = self.ids[UNK]
        return [
            self.ids.get(t, unk) for t in WORD_RE.findall(fold_typography(text).lower())
        ]

    def encode_work(self, text: str) -> list[int]:
        """Token ids for one complete work, announced as one.

        **A work begins with `<book>` and ends with `<eot>`**, which is the
        shape Llama 3 uses with `<|begin_of_text|>` and `<|end_of_text|>`.

        Two defects close here. `<book>` was the seed
        `tools/sample_level.py` and `tools/talk.py` start an unprompted
        sample from, and it occurred **zero times in 356,975 training
        tokens**, so every such sample began from a row training never
        visited. And nothing marked an ending, so the model had no way to
        stop and no way to learn that a book is a bounded thing.

        Use this wherever a whole book becomes a stream. Use `encode` for a
        fragment, such as a prompt, which is not a work and must not claim
        to be one.
        """
        return [self.ids[BOOK], *self.encode(text), self.ids[EOT]]

    def decode(self, tokens: list[int]) -> str:
        return " ".join(
            self.words[t] if 0 <= t < len(self.words) else UNK for t in tokens
        )

    def unknown(self, text: str) -> list[str]:
        """Tokens the lexicon does not carry. Should be empty for a valid corpus."""
        return [
            t
            for t in WORD_RE.findall(fold_typography(text).lower())
            if t not in self.ids
        ]


def build(vocabulary: Vocabulary, level: int) -> Tokeniser:
    """Every surface form admissible at ``level``, plus digits and stops.

    Sorted so the mapping is stable across runs, which matters because a
    checkpoint trained under one mapping is meaningless under another.
    """
    words: set[str] = set(vocabulary.core) | set(vocabulary.exempt)
    for term in vocabulary.terms:
        if term.level <= level:
            words.update(term.surface_forms())
    ordered = list(SPECIALS) + sorted(words) + [str(d) for d in range(10)]
    ordered += [c for c in ".,!?;:" if c not in ordered]
    seen: dict[str, int] = {}
    unique: list[str] = []
    for word in ordered:
        if word not in seen:
            seen[word] = len(unique)
            unique.append(word)
    return Tokeniser(ids=seen, words=tuple(unique))
