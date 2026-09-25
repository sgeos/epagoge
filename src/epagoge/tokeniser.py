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

from epagoge.vocabulary import Vocabulary

WORD_RE: Final[re.Pattern[str]] = re.compile(r"[a-z']+|[0-9]+|[.,!?;:]")
"""Words, numerals, and the punctuation the corpus actually uses."""

PAD: Final[str] = "<pad>"
UNK: Final[str] = "<unk>"
BOOK: Final[str] = "<book>"
SPECIALS: Final[tuple[str, ...]] = (PAD, UNK, BOOK)


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
        return [self.ids.get(t, unk) for t in WORD_RE.findall(text.lower())]

    def decode(self, tokens: list[int]) -> str:
        return " ".join(
            self.words[t] if 0 <= t < len(self.words) else UNK for t in tokens
        )

    def unknown(self, text: str) -> list[str]:
        """Tokens the lexicon does not carry. Should be empty for a valid corpus."""
        return [t for t in WORD_RE.findall(text.lower()) if t not in self.ids]


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
