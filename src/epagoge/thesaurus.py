"""A thesaurus entry per lexicon sense.

**Two roles, and the second one sets the requirements.** During authoring
this is an analysis tool that finds words admitted without their opposite.
Afterwards it is level-one reference material sitting beside the
dictionary, which means it must cover every sense and must itself be
written in words the level admits.

**Antonymy is a property of a sense, not of a word.** `right` opposes
`left` as a direction and `wrong` as a judgement, and a word-keyed list
cannot hold both. That is the same lesson the lexicon learned when one
concept per word could not hold `set`.

Coverage is the point of the first role. A sense with no entry is a sense
nobody has looked at, so an uncovered sense is a violation while an entry
with no antonym is not. Most nouns oppose nothing.

Standard library only, matching the rest of the package.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import cast

from epagoge.concept_graph import Violation
from epagoge.vocabulary import Vocabulary


@dataclass(frozen=True, slots=True)
class Entry:
    """One sense, and what it stands against and beside."""

    word: str
    concept: str
    antonyms: tuple[str, ...] = ()
    synonyms: tuple[str, ...] = ()

    @property
    def sense(self) -> tuple[str, str]:
        return (self.word, self.concept)


@dataclass(frozen=True, slots=True)
class Thesaurus:
    """Authored. Pairs are a judgement and are not derived from anything."""

    entries: tuple[Entry, ...] = ()

    def words(self) -> frozenset[str]:
        return frozenset(entry.word for entry in self.entries)

    def for_sense(self, word: str, concept: str) -> Entry | None:
        return next(
            (e for e in self.entries if e.word == word and e.concept == concept), None
        )

    def antonyms_of(self, word: str) -> frozenset[str]:
        """Across every sense, since a target is a bare word."""
        return frozenset(a for e in self.entries if e.word == word for a in e.antonyms)


def admissible_at(vocabulary: Vocabulary, word: str, level: int) -> bool:
    """Whether a generator constrained to ``level`` can reach ``word``."""
    if word in vocabulary.core or word in vocabulary.exempt:
        return True
    return any(sense.level <= level for sense in vocabulary.senses(word))


def validate(
    thesaurus: Thesaurus, vocabulary: Vocabulary, level: int = 1
) -> list[Violation]:
    """Every breach. Empty means the thesaurus is sound at ``level``."""
    out: list[Violation] = []
    seen: set[tuple[str, str]] = set()
    licensed = {term.word for term in vocabulary.terms} | {
        entry.word for entry in thesaurus.entries if entry.concept == ""
    }

    for entry in thesaurus.entries:
        # **An entry above the level is out of scope, not in breach.**
        # Validating at level one asks whether the level-one thesaurus is
        # sound. A level-two entry naming a level-two word is correct and
        # judging it here reported seventeen false violations.
        if entry.concept != "" and not admissible_at(vocabulary, entry.word, level):
            continue
        if entry.sense in seen:
            out.append(
                Violation(
                    "duplicate-entry",
                    f"{entry.word!r} under {entry.concept!r} appears twice",
                )
            )
        seen.add(entry.sense)
        # **A core function word may have an entry with no concept.** It
        # names nothing, so it has no sense, but `up` against `down` and
        # `yes` against `no` are exactly the pairs a level-one reader
        # wants, and dropping them would make the reference material worse
        # to serve the analysis tool.
        if entry.concept == "":
            if entry.word not in vocabulary.core:
                out.append(
                    Violation(
                        "unknown-sense",
                        f"{entry.word!r} has no concept and is not a core word",
                    )
                )
        elif not any(s.concept == entry.concept for s in vocabulary.senses(entry.word)):
            out.append(
                Violation(
                    "unknown-sense",
                    f"{entry.word!r} under {entry.concept!r} is not in the lexicon",
                )
            )
        for kind, related in (("antonym", entry.antonyms), ("synonym", entry.synonyms)):
            for other in related:
                if other == entry.word:
                    out.append(
                        Violation(f"self-{kind}", f"{entry.word!r} is its own {kind}")
                    )
                elif not admissible_at(vocabulary, other, level):
                    out.append(
                        Violation(
                            f"missing-{kind}",
                            f"{entry.word!r} names {other!r} as its {kind} and it "
                            f"is not admissible at level {level}",
                        )
                    )

    # **Coverage is the first role.** A sense nobody has written an entry
    # for is a sense nobody has checked for a missing opposite.
    for term in vocabulary.terms:
        if term.level <= level and (term.word, term.concept) not in seen:
            out.append(
                Violation(
                    "uncovered-sense",
                    f"{term.word!r} under {term.concept!r} is admitted at level "
                    f"{term.level} and has no thesaurus entry",
                )
            )

    # Antonymy runs both ways. Only between licensed words, since a core
    # function word carries no concept and so has no entry to hold the
    # other half.
    for entry in thesaurus.entries:
        if entry.concept != "" and not admissible_at(vocabulary, entry.word, level):
            continue
        for other in entry.antonyms:
            if other in licensed and entry.word not in thesaurus.antonyms_of(other):
                out.append(
                    Violation(
                        "asymmetric-antonym",
                        f"{entry.word!r} names {other!r} as its opposite and "
                        f"{other!r} does not name {entry.word!r}",
                    )
                )
    return out


def _str_list(raw: object, where: str) -> tuple[str, ...]:
    if raw is None:
        return ()
    if not isinstance(raw, list):
        raise ValueError(f"{where}: expected a list")
    items = cast(list[object], raw)
    for entry in items:
        if not isinstance(entry, str) or not entry.strip():
            raise ValueError(f"{where}: words must be non-empty strings")
    return tuple(w.lower() for w in cast(list[str], items))


def from_json(payload: object) -> Thesaurus:
    if not isinstance(payload, dict):
        raise ValueError("thesaurus must be a JSON object")
    body = cast(dict[object, object], payload)
    raw = body.get("senses")
    if not isinstance(raw, list):
        raise ValueError("'senses' must be a list")
    entries: list[Entry] = []
    for index, item in enumerate(cast(list[object], raw)):
        where = f"senses[{index}]"
        if not isinstance(item, dict):
            raise ValueError(f"{where}: expected an object")
        fields = cast(dict[object, object], item)
        word, concept = fields.get("word"), fields.get("concept")
        if not isinstance(word, str) or not isinstance(concept, str):
            raise ValueError(f"{where}: 'word' and 'concept' must be strings")
        entries.append(
            Entry(
                word=word.lower(),
                concept=concept,
                antonyms=_str_list(fields.get("antonyms"), f"{where}.antonyms"),
                synonyms=_str_list(fields.get("synonyms"), f"{where}.synonyms"),
            )
        )
    return Thesaurus(entries=tuple(entries))


def load(path: Path) -> Thesaurus:
    parsed: object = json.loads(path.read_text(encoding="utf-8"))
    return from_json(parsed)
