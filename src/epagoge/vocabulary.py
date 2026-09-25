"""Per-level vocabulary.

Three categories, because two were not enough.

**Core.** Function words, available from level one, naming no concept.

**General.** Content words not yet mapped to a concept. **This is a holding
pen for unfinished work, not a permanent category.** A content word names
something, so a word with no mapping means either the mapping has not been
identified or a concept is missing from the graph. Only function words
genuinely name nothing.

Its size is therefore a measure of how incomplete the graph is, and it
should shrink toward zero as concepts are added.

**Terms.** Words that name a graph concept. **Their level is authored**, and
the graph supplies a lower bound: a word may not be introduced before the
concept it names has been taught.

An earlier design derived the level from the concept instead of bounding it.
That was wrong, because **a concept can be taught before its name is
introduced.** The level-one record teaching causation never uses the word
"cause", and children grasp causation long before they say it. Deriving
equality admitted thirty-three words at levels where nothing used them.

One enforced rule, and one retired.

**Ceiling, enforced.** A record at level L uses no term whose level
exceeds L.

**Coverage, retired 2026-09-24.** It required every term admitted at level
L to appear in some level-L record. That held only while this file was
**descriptive**, derived to describe the words a sample corpus happened to
use, where every admitted word was used by construction.

The file is now **prescriptive**. It is authored ahead of the corpus to
license what may be written, so a licensed word no record has reached yet
is the expected state. Enforcing the old rule would require a corpus to
exhaust its lexicon before the lexicon could be written. Utilisation is
reported instead, as a number rather than as a violation.

Specification in ``docs/spec/VOCABULARY.md``. Standard library only.
"""

from __future__ import annotations

import json
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Final, cast

from epagoge.concept_graph import Violation
from epagoge.inflection import comparison, doubling_is_ambiguous, plural, verb_forms
from epagoge.record import Record

WORD_RE: Final[re.Pattern[str]] = re.compile(r"[a-z]+(?:'[a-z]+)?")
NUMERAL_RE: Final[re.Pattern[str]] = re.compile(r"^\d+$")

_SUFFIXES: Final[tuple[str, ...]] = ("'s", "es", "ed", "ing", "s")
"""Stripped in order when a surface form is not itself a known term.

Deliberately crude. A real stemmer would silently conflate distinct words,
and a vocabulary check that quietly accepts the wrong word is worse than one
that reports a form it does not recognise. Explicit ``forms`` on an entry
override this entirely.
"""


@dataclass(frozen=True, slots=True)
class Term:
    """A content word, and the concept that licenses it."""

    word: str
    concept: str
    level: int
    """Authored. The graph bounds it from below; it is not derived."""

    forms: tuple[str, ...] = ()

    pos: str = ""
    """Parts of speech, space separated. ``verb``, ``noun``, ``adjective``.

    **A word can be several.** `answer`, `lock` and `brush` are each a noun
    and a verb, and the enforcement differs, since a verb owes its
    inflections and a noun owes its plural. Twenty-eight such words were
    found by reading how their own dictionary entries begin.

    A verb admitted in one form is a trap, since the generator is
    constrained to admissible words and will reach for an inflection that
    is not there. Marking a term a verb obliges every inflection of it to
    be admissible at the same level, which ``_check_inflections`` checks.
    """

    def surface_forms(self) -> tuple[str, ...]:
        return (self.word, *self.forms)


@dataclass(frozen=True, slots=True)
class Vocabulary:
    """Core function words, licensed terms, and standing exemptions."""

    core: frozenset[str] = frozenset()
    """Available from level one. Function words name no concept."""

    terms: tuple[Term, ...] = ()
    general: Mapping[int, frozenset[str]] = field(
        default_factory=dict[int, frozenset[str]]
    )
    """Authored tiers. Ordinary content words that name no concept."""

    exempt: frozenset[str] = frozenset()
    """Proper nouns, units, and anything else outside the level system."""

    ostensive: frozenset[str] = frozenset()
    """Words the corpus teaches by showing, and the dictionary never defines.

    **A self-hosted compiler needs a seed compiler written in something
    else. Here that something else is experience.** Measured on 2026-09-25,
    a dictionary restricted to definitions reducing to the function words
    accepted nothing at all in twenty-four attempts, and the words doing
    the blocking were `body`, `food`, `hand`, `head`, `mouth` and `one`.
    Nobody defines those. They are pointed at.

    So the seed is the function words, which name nothing, plus these,
    which name something that cannot be said without circularity. Keeping
    the set small and stated is what stops self-hosting becoming true by
    fiat, since a large enough seed makes any lexicon close.

    Each must also be an admitted term, so that the books still teach it.
    The dictionary declining to define a word is not the corpus omitting
    it.
    """

    substitutions: Mapping[str, str] = field(default_factory=dict[str, str])
    """Words deliberately NOT admitted, and what to write instead.

    **Naming a banned word is not the same as supplying the replacement.**
    Measured on 2026-09-25, the generator's retry named each offending word
    and the teacher reached for it again. The words doing the blocking were
    overwhelmingly ones with an ordinary substitute already in the lexicon,
    `location` for `place` and `amount` for `how much`, so the failure was
    not that the level cannot express the idea.

    This is also the record of a triage decision. A word here was judged
    outside what a child in kindergarten knows AND expressible with what is
    already admitted, which is the operator's second branch. A word that
    passes the first branch is admitted as a term instead.
    """

    # The generic alias is the factory so that the element types are known.
    # A bare ``dict`` leaves them unknown under strict checking.
    _by_form: dict[str, tuple[Term, ...]] = field(
        default_factory=dict[str, tuple[Term, ...]], repr=False, compare=False
    )
    """Form to every sense carrying it.

    **A word has senses and a dictionary gives more than one definition.**
    `set` is a noun and a verb, `swallow` is an action and a bird, and
    `ground` is the earth and the past of grind. The model held one concept
    per word, so admitting a word silently asserted that it meant one
    thing, and the inflection check exposed this on 2026-09-25 by demanding
    a verb form of a noun.

    **Only admitted senses are listed.** A word's absent senses are absent
    on purpose, which is how the lexicon says that the bird and the
    grinding are not level-one material.
    """
    _general_level: dict[str, int] = field(
        default_factory=dict[str, int], repr=False, compare=False
    )

    def __post_init__(self) -> None:
        index: dict[str, list[Term]] = {}
        for term in self.terms:
            for form in term.surface_forms():
                index.setdefault(form, []).append(term)
        object.__setattr__(
            self,
            "_by_form",
            {form: tuple(senses) for form, senses in index.items()},
        )
        tiers: dict[str, int] = {}
        for level, words in self.general.items():
            for word in words:
                if word not in tiers or level < tiers[word]:
                    tiers[word] = level
        object.__setattr__(self, "_general_level", tiers)

    def general_level(self, token: str) -> int | None:
        """Authored level of a general word, trying crude suffix stripping."""
        direct = self._general_level.get(token)
        if direct is not None:
            return direct
        for suffix in _SUFFIXES:
            if token.endswith(suffix) and len(token) > len(suffix) + 1:
                stem = token[: -len(suffix)]
                for candidate in (stem, stem + "e"):
                    found = self._general_level.get(candidate)
                    if found is not None:
                        return found
        return None

    def senses(self, token: str) -> tuple[Term, ...]:
        """Every admitted sense carrying ``token``, exactly as written."""
        return self._by_form.get(token, ())

    def words(self) -> frozenset[str]:
        """Distinct base words, which is smaller than the number of senses."""
        return frozenset(term.word for term in self.terms)

    @staticmethod
    def _earliest(senses: tuple[Term, ...]) -> Term | None:
        """The sense admitted soonest.

        Admissibility asks whether a generator at a level can reach the
        form, and it can as soon as any one of its senses is admitted.
        """
        return min(senses, key=lambda term: term.level) if senses else None

    def lookup(self, token: str) -> Term | None:
        """Resolve a surface form, trying crude suffix stripping.

        Returns the earliest-admitted sense. Callers wanting all of them,
        such as a dictionary writing one entry per sense, use ``senses``.
        """
        direct = self._earliest(self._by_form.get(token, ()))
        if direct is not None:
            return direct
        for suffix in _SUFFIXES:
            if token.endswith(suffix) and len(token) > len(suffix) + 1:
                stem = token[: -len(suffix)]
                found = self._earliest(self._by_form.get(stem, ()))
                if found is not None:
                    return found
                if suffix in ("es", "ed", "ing"):
                    with_e = self._earliest(self._by_form.get(stem + "e", ()))
                    if with_e is not None:
                        return with_e
                # A doubled final consonant, as in stopped from stop. Narrow
                # enough not to conflate distinct words, and it was failing
                # on every regular past tense of a short verb.
                if len(stem) > 2 and stem[-1] == stem[-2] and stem[-1] not in "aeiou":
                    undoubled = self._earliest(self._by_form.get(stem[:-1], ()))
                    if undoubled is not None:
                        return undoubled
        return None

    def seed_words(self) -> frozenset[str]:
        """Everything available without a definition, forms included.

        **If a word is ostensive then all of its forms are.** `eye` sat in
        the ostensive set while `eyes` was a term of its own, so `eyes`
        resolved to itself, missed the seed, and put `face` on the frontier
        for want of a plural. The same shape as the verb inflection gap,
        arriving in the seed.
        """
        out = set(self.core) | set(self.exempt)
        for word in self.ostensive:
            out.add(word)
            for sense in self.senses(word):
                out.update(sense.surface_forms())
            for term in self.terms:
                if term.word == word:
                    out.update(term.surface_forms())
        return frozenset(out)

    def is_free(self, token: str) -> bool:
        """Whether a token is usable at any level without licensing."""
        return (
            token in self.core or token in self.exempt or bool(NUMERAL_RE.match(token))
        )


@dataclass(frozen=True, slots=True)
class Completeness:
    """How much of the content vocabulary has reached the graph."""

    mapped: int
    unmapped: int

    @property
    def total(self) -> int:
        return self.mapped + self.unmapped

    @property
    def fraction(self) -> float:
        return self.mapped / self.total if self.total else 1.0


def completeness(vocabulary: Vocabulary) -> Completeness:
    """Fraction of content words carrying a concept.

    **A low figure is a statement about the graph, not about the words.**
    Every content word names something. One that maps to nothing means the
    mapping was not identified, or a concept that belongs in the graph is
    absent from it. Function words are excluded because they genuinely name
    nothing.
    """
    unmapped = sum(len(words) for words in vocabulary.general.values())
    return Completeness(mapped=len(vocabulary.terms), unmapped=unmapped)


TYPOGRAPHIC: Final[dict[int, str]] = str.maketrans(
    {
        "\u2018": "'",
        "\u2019": "'",
        "\u201a": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u2026": "...",
        "\u00a0": " ",
    }
)
"""Typographic punctuation folded to the ASCII the word pattern matches.

**A curly apostrophe cost four good sentences in one round.** The teacher
writes `stone\u2019s`, the pattern only knows `'`, so the word split into
`stone` and a bare `s`, and the line was rejected for a word outside the
level that was never a word. Folding is done once here and used by both
this module and the tokeniser, so the two cannot disagree about what a
word is.
"""


def fold_typography(text: str) -> str:
    """Replace typographic punctuation with its ASCII equivalent."""
    return text.translate(TYPOGRAPHIC)


def tokenise(text: str) -> list[str]:
    """Lowercased word forms. Punctuation and digits are handled separately."""
    return WORD_RE.findall(fold_typography(text).lower())


def unlicensed(
    vocabulary: Vocabulary, text: str, level: int, *, exact: bool = True
) -> list[str]:
    """Tokens in ``text`` that are not admissible at ``level``.

    Empty means the text sits inside the level's vocabulary ceiling. Used at
    the generation boundary, where teacher output is untrusted and a soft
    instruction to stay inside a word list has been measured as one the
    teacher does not reliably follow.

    **``exact`` is the default and it is the stricter reading.** Without it
    a token resolves through :meth:`Vocabulary.lookup`, which strips
    suffixes, so ``ended`` passes on the strength of ``end`` and reaches a
    book in a form the lexicon does not carry. The tokeniser then finds it,
    but only after it is written: ``rains``, ``stared``, ``warmed``,
    ``clearing``, ``facing``, ``cleared``, ``lighting``, ``thoughts``,
    ``ended``, ``lived`` and ``winding`` were each found that way, eleven
    real gaps discovered downstream of the check meant to prevent them.

    Exact matching asks the question the tokeniser asks: is this surface
    form carried by some sense admitted at this level. Pass ``exact=False``
    for the older, permissive reading, which remains right where the
    question is whether a reader would know the word rather than whether
    the corpus may contain it.
    """
    out: list[str] = []
    for token in tokenise(text):
        if vocabulary.is_free(token):
            continue
        if exact:
            if any(sense.level <= level for sense in vocabulary.senses(token)):
                continue
            out.append(token)
            continue
        term = vocabulary.lookup(token)
        if term is not None and term.level <= level:
            continue
        out.append(token)
    return out


def unlexicalised(
    vocabulary: Vocabulary, scheduled: Mapping[str, int]
) -> list[tuple[str, int]]:
    """Scheduled concepts with no word licensed at or before their level.

    **A concept with no word cannot be taught**, because the generator is
    constrained to the level's admissible vocabulary and nothing in that
    list names the concept.

    Nothing caught this before it was asked about. The other vocabulary
    rules run the opposite way, requiring that a word names a real concept
    and that a word does not precede its concept. **Neither fires when a
    concept has no word**, because an unlexicalised concept breaks no rule
    as written. It is simply unwritable.
    """
    licensed: dict[str, int] = {}
    for term in vocabulary.terms:
        current = licensed.get(term.concept)
        if current is None or term.level < current:
            licensed[term.concept] = term.level
    out: list[tuple[str, int]] = []
    for concept, level in scheduled.items():
        earliest = licensed.get(concept)
        if earliest is None or earliest > level:
            out.append((concept, level))
    return sorted(out)


def concept_levels(records: Sequence[Record]) -> dict[str, int]:
    """Earliest level at which each concept is taught."""
    out: dict[str, int] = {}
    for record in records:
        for concept in record.concepts:
            current = out.get(concept)
            if current is None or record.level < current:
                out[concept] = record.level
    return out


def term_levels(vocabulary: Vocabulary, records: Sequence[Record]) -> dict[str, int]:
    """Earliest authored level of each word. ``records`` is kept for callers.

    **A word is admissible as soon as any of its senses is**, which is the
    rule ``lookup`` already follows. A plain dict comprehension took
    whichever sense came last, so `set` read as level two on the strength
    of its noun sense while its verb sense sat at level one, and a
    level-one record using it failed the ceiling.
    """
    del records
    out: dict[str, int] = {}
    for term in vocabulary.terms:
        seen = out.get(term.word)
        if seen is None or term.level < seen:
            out[term.word] = term.level
    return out


def _check_lower_bound(
    vocabulary: Vocabulary,
    records: Sequence[Record],
    scheduled: Mapping[str, int] | None = None,
) -> list[Violation]:
    """A word may not be introduced before the concept it names is taught.

    ``scheduled`` is the curriculum's concept-to-level assignment. Where it
    is given it is authoritative, and records only fill in concepts the
    schedule has not placed.

    **A schedule states where a concept is taught. Records only show where
    it has been taught so far.** Testing a prescriptive lexicon against the
    second reports every word whose corpus is not yet written, which is the
    normal state and not a defect.
    """
    taught = dict(concept_levels(records))
    for concept, level in (scheduled or {}).items():
        current = taught.get(concept)
        if current is None or level < current:
            taught[concept] = level
    out: list[Violation] = []
    for term in vocabulary.terms:
        concept_level = taught.get(term.concept)
        if concept_level is None:
            out.append(
                Violation(
                    "term-never-introduced",
                    f"term {term.word!r} names concept {term.concept!r}, "
                    "which is never taught",
                )
            )
        elif term.level < concept_level:
            out.append(
                Violation(
                    "term-before-concept",
                    f"term {term.word!r} is admitted at level {term.level} but "
                    f"its concept {term.concept!r} is not taught until "
                    f"{concept_level}",
                )
            )
    return out


def validate_vocabulary(
    vocabulary: Vocabulary,
    records: Sequence[Record],
    known_concepts: Mapping[str, object],
    scheduled: Mapping[str, int] | None = None,
) -> list[Violation]:
    """Check licensing and the ceiling rule.

    ``scheduled`` maps a concept to the level a curriculum schedule places it
    at. Supplied, it is what the lower-bound rule tests against.

    **The lower bound is a claim about the curriculum, not about whichever
    records happen to exist.** Measured against records alone, a licensed
    word fails the moment its lexicon is authored ahead of its corpus, which
    is the order a prescriptive lexicon requires.
    """
    out: list[Violation] = []
    out.extend(_check_licensing(vocabulary, known_concepts))
    out.extend(_check_lower_bound(vocabulary, records, scheduled))
    out.extend(_check_lexicalisation(vocabulary, known_concepts, scheduled))
    out.extend(_check_inflections(vocabulary))
    out.extend(_check_doubling(vocabulary))
    out.extend(_check_plurals(vocabulary))
    out.extend(_check_comparison(vocabulary))
    out.extend(_check_ostensive(vocabulary))
    levels = term_levels(vocabulary, records)
    out.extend(_check_ceiling(vocabulary, records, levels))
    out.extend(_check_coverage(vocabulary, records, levels))
    return out


def _check_lexicalisation(
    vocabulary: Vocabulary,
    known_concepts: Mapping[str, object],
    scheduled: Mapping[str, int] | None,
) -> list[Violation]:
    """A concept in the graph and on the schedule must have a word.

    Restricted to concepts the graph holds, because a concept a schedule
    only plans cannot have a term at all. A term must name a graph concept,
    so planning one and lexicalising it are the same step and the rule
    would fire on every plan.
    """
    if not scheduled:
        return []
    in_graph = {c: lvl for c, lvl in scheduled.items() if c in known_concepts}
    return [
        Violation(
            "concept-unlexicalised",
            f"concept {concept!r} is scheduled at level {level} and no word "
            "is licensed for it there",
        )
        for concept, level in unlexicalised(vocabulary, in_graph)
    ]


def _check_licensing(
    vocabulary: Vocabulary, known_concepts: Mapping[str, object]
) -> list[Violation]:
    out: list[Violation] = []
    seen: dict[str, str] = {}
    pairs: set[tuple[str, str]] = set()
    for term in vocabulary.terms:
        if (term.word, term.concept) in pairs:
            out.append(
                Violation(
                    "duplicate-sense",
                    f"{term.word!r} is listed twice under {term.concept!r}",
                )
            )
        pairs.add((term.word, term.concept))
        if term.concept not in known_concepts:
            out.append(
                Violation(
                    "unlicensed-term",
                    f"term {term.word!r} names concept {term.concept!r}, "
                    "which is not in the graph",
                )
            )
        for form in term.surface_forms():
            # **A form shared by two senses of one word is ordinary.** `sets`
            # is the plural of the noun and the third person of the verb.
            # A form shared by two DIFFERENT words is not, because nothing
            # can then decide which concept the token carries.
            clash = seen.get(form)
            if clash is not None and clash != term.word:
                out.append(
                    Violation(
                        "duplicate-form",
                        f"form {form!r} belongs to {clash!r} and {term.word!r}",
                    )
                )
            seen[form] = term.word
            if form in vocabulary.core:
                out.append(
                    Violation(
                        "core-collision", f"form {form!r} is both core and licensed"
                    )
                )
    return out


def _check_ceiling(
    vocabulary: Vocabulary, records: Sequence[Record], levels: Mapping[str, int | None]
) -> list[Violation]:
    """No record may use a term admitted above its own level."""
    out: list[Violation] = []
    for record in records:
        for token in tokenise(record.content):
            if vocabulary.is_free(token):
                continue
            general = vocabulary.general_level(token)
            if general is not None:
                if general > record.level:
                    out.append(
                        Violation(
                            "vocabulary-ceiling",
                            f"record {record.id!r} at level {record.level} uses "
                            f"{token!r}, a general word admitted at level {general}",
                        )
                    )
                continue
            term = vocabulary.lookup(token)
            if term is None:
                out.append(
                    Violation(
                        "unknown-word",
                        f"record {record.id!r} uses {token!r}, "
                        "which is neither core, exempt, nor a licensed term",
                    )
                )
                continue
            level = levels.get(term.word)
            if level is not None and level > record.level:
                out.append(
                    Violation(
                        "vocabulary-ceiling",
                        f"record {record.id!r} at level {record.level} uses "
                        f"{token!r}, admitted at level {level}",
                    )
                )
    return out


def _check_coverage(
    vocabulary: Vocabulary, records: Sequence[Record], levels: Mapping[str, int | None]
) -> list[Violation]:
    """Retired 2026-09-24. Always returns nothing.

    It required every term admitted at level L to appear in some level-L
    record, on the reasoning that admitting a word is a commitment to teach
    it.

    **That reasoning held only while the vocabulary was descriptive.** It was
    derived to describe the words the sample corpus happened to use, so
    every admitted word was used by construction and the check could only
    ever fire on a mistake.

    The vocabulary is now prescriptive. It is authored ahead of the corpus
    to license what may be written, and a licensed word no record has
    reached yet is the expected state rather than an error. Enforcing the
    old rule would require the corpus to exhaust its lexicon before the
    lexicon could be written, which is the wrong way round.

    Utilisation is still worth knowing and is reported by
    :func:`utilisation` as a number rather than as a violation, because a
    corpus using very little of its lexicon means either a thin corpus or a
    padded lexicon and the number does not say which.
    """
    del vocabulary, records, levels
    return []


@dataclass(frozen=True, slots=True)
class Utilisation:
    """How much of the licensed lexicon a corpus actually reaches."""

    level: int
    admitted: int
    used: int

    @property
    def fraction(self) -> float:
        return self.used / self.admitted if self.admitted else 0.0


def utilisation(
    vocabulary: Vocabulary, records: Sequence[Record], level: int
) -> Utilisation:
    """Licensed terms at a level against those a corpus reaches there.

    Reported, never enforced. A low number means the corpus is thin or the
    lexicon is padded, and it does not distinguish them.
    """
    admitted = {t.word for t in vocabulary.terms if t.level <= level}
    used: set[str] = set()
    for record in records:
        if record.level != level:
            continue
        for token in tokenise(record.content):
            term = vocabulary.lookup(token)
            if term is not None and term.level <= level:
                used.add(term.word)
    return Utilisation(level=level, admitted=len(admitted), used=len(used))


def load_vocabulary(path: Path) -> Vocabulary:
    parsed: object = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(parsed, dict):
        raise ValueError("vocabulary must be a JSON object")
    body = cast(dict[object, object], parsed)
    return Vocabulary(
        core=frozenset(_str_list(body.get("core"), "core")),
        terms=tuple(_parse_terms(body.get("terms"))),
        general=_parse_general(body.get("general")),
        exempt=frozenset(_str_list(body.get("exempt"), "exempt")),
        substitutions=_parse_substitutions(body.get("substitutions")),
        ostensive=frozenset(_str_list(body.get("ostensive"), "ostensive")),
    )


def _check_plurals(vocabulary: Vocabulary) -> list[Violation]:
    """Every noun must have its plural admissible at the noun's level.

    The same rule as verb inflections, and it exists for the same reason.
    A noun admitted without its plural sends a generator reaching for a
    form that is not there.
    """
    out: list[Violation] = []
    for term in vocabulary.terms:
        if "noun" not in term.pos.split():
            continue
        form = plural(term.word)
        if form == term.word or form in vocabulary.core:
            continue
        if any(sense.level <= term.level for sense in vocabulary.senses(form)):
            continue
        out.append(
            Violation(
                "missing-plural",
                f"noun {term.word!r} is admitted at level {term.level} and its "
                f"plural {form!r} is not admissible there",
            )
        )
    return out


def _check_ostensive(vocabulary: Vocabulary) -> list[Violation]:
    """An ostensive word must still be a term the corpus teaches.

    The dictionary declining to define a word is a statement about the
    dictionary. It is not permission to leave the word out of the books.
    """
    return [
        Violation(
            "ostensive-unlicensed",
            f"{word!r} is ostensive and is not an admitted term",
        )
        for word in sorted(vocabulary.ostensive)
        if not vocabulary.senses(word)
    ]


def _check_inflections(vocabulary: Vocabulary) -> list[Violation]:
    """Every inflection of a verb must be admissible at the verb's level.

    **Standard procedure, not a repair.** Where the inflection lives does
    not matter. It may be a form of the same term, a term of its own, or a
    core function word. What matters is that a generator constrained to
    the level can reach it.
    """
    out: list[Violation] = []
    for term in vocabulary.terms:
        if "verb" not in term.pos.split():
            continue
        for form in verb_forms(term.word):
            reachable = any(
                sense.level <= term.level for sense in vocabulary.senses(form)
            )
            if form in vocabulary.core or reachable:
                continue
            out.append(
                Violation(
                    "missing-inflection",
                    f"verb {term.word!r} is admitted at level {term.level} and "
                    f"its form {form!r} is not admissible there",
                )
            )
    return out


def _check_comparison(vocabulary: Vocabulary) -> list[Violation]:
    """Every graded form of a declared adjective must be admissible.

    The same rule as verb inflections and noun plurals, for the same
    reason: a word admitted in one form sends a generator reaching for one
    that is not there. Declared rather than inferred, because gradability
    is not recoverable from spelling.
    """
    out: list[Violation] = []
    for term in vocabulary.terms:
        if "adjective" not in term.pos.split():
            continue
        for form in comparison(term.word):
            if form in vocabulary.core:
                continue
            if any(sense.level <= term.level for sense in vocabulary.senses(form)):
                continue
            out.append(
                Violation(
                    "missing-comparison",
                    f"adjective {term.word!r} is admitted at level {term.level} "
                    f"and its form {form!r} is not admissible there",
                )
            )
    return out


def _check_doubling(vocabulary: Vocabulary) -> list[Violation]:
    """A verb whose doubling cannot be derived must be classified by hand.

    **This is the narrow half of a gap the project has not closed.** No
    check compares a derived form against English, which is how ``rised``,
    ``choosed``, ``costed``, ``shined``, ``shrinked``, ``slided`` and
    ``winned`` stayed admissible for several commits. It does close the one
    class where spelling alone cannot decide: a longer verb ending
    consonant-vowel-consonant doubles when its final syllable is stressed
    and not otherwise, so ``admit`` gives admitted and ``visit`` gives
    visited. A verb of that shape must appear in ``IRREGULAR`` or in
    ``NO_DOUBLE_MULTISYLLABIC``, and the gate refuses it until it does.
    """
    return [
        Violation(
            "unclassified-doubling",
            f"verb {term.word!r} ends consonant-vowel-consonant and is not "
            "listed as doubling or as not doubling, so its past and present "
            "participle cannot be derived",
        )
        for term in vocabulary.terms
        if "verb" in term.pos.split() and doubling_is_ambiguous(term.word)
    ]


def _parse_substitutions(raw: object) -> dict[str, str]:
    if raw is None:
        return {}
    if not isinstance(raw, dict):
        raise ValueError("'substitutions' must be an object")
    out: dict[str, str] = {}
    for key, value in cast(dict[object, object], raw).items():
        if not isinstance(key, str) or not isinstance(value, str):
            raise ValueError("substitutions must map a string to a string")
        if not value.strip():
            raise ValueError(f"substitution for {key!r} is empty")
        out[key] = value
    return out


def _parse_general(raw: object) -> dict[int, frozenset[str]]:
    if raw is None:
        return {}
    if not isinstance(raw, dict):
        raise ValueError("'general' must be an object keyed by level")
    body = cast(dict[object, object], raw)
    out: dict[int, frozenset[str]] = {}
    for key, value in body.items():
        if not isinstance(key, str) or not key.isdigit():
            raise ValueError(f"general key {key!r} must be a level number")
        out[int(key)] = frozenset(_str_list(value, f"general[{key}]"))
    return out


def _str_list(raw: object, where: str) -> list[str]:
    if raw is None:
        return []
    if not isinstance(raw, list):
        raise ValueError(f"'{where}' must be a list")
    items = cast(list[object], raw)
    out: list[str] = []
    for index, item in enumerate(items):
        if not isinstance(item, str):
            raise ValueError(f"{where}[{index}]: expected a string")
        out.append(item.lower())
    return out


def _parse_terms(raw: object) -> list[Term]:
    if raw is None:
        return []
    if not isinstance(raw, list):
        raise ValueError("'terms' must be a list")
    items = cast(list[object], raw)
    out: list[Term] = []
    for index, item in enumerate(items):
        where = f"terms[{index}]"
        if not isinstance(item, dict):
            raise ValueError(f"{where}: expected an object")
        entry = cast(dict[object, object], item)
        word = entry.get("word")
        concept = entry.get("concept")
        level = entry.get("level")
        if not isinstance(word, str) or not isinstance(concept, str):
            raise ValueError(f"{where}: 'word' and 'concept' must be strings")
        if not isinstance(level, int) or isinstance(level, bool):
            raise ValueError(f"{where}: 'level' must be an integer")
        out.append(
            Term(
                word=word.lower(),
                concept=concept,
                level=level,
                forms=tuple(_str_list(entry.get("forms"), f"{where}.forms")),
                pos=_parse_pos(entry.get("pos"), where),
            )
        )
    return out


def _parse_pos(raw: object, where: str) -> str:
    if raw is None:
        return ""
    if not isinstance(raw, str):
        raise ValueError(f"{where}.pos: expected a string")
    parts = raw.split()
    for part in parts:
        if part not in ("verb", "noun", "adjective"):
            raise ValueError(
                f"{where}.pos: only 'verb', 'noun' and 'adjective' are "
                f"recognised, got {part!r}"
            )
    if len(set(parts)) != len(parts):
        raise ValueError(f"{where}.pos: repeated part of speech in {raw!r}")
    return " ".join(parts)
