"""Books, and the definitions they carry.

A record teaches a concept. **A book is where a reader is told what the
words mean before they are used**, and where the material that uses them
follows in one thread rather than as unconnected assertions.

Specification in ``docs/spec/BOOKS.md``. Standard library only.

The shape is three parts in order. The subject is defined, then the words
are defined, then a story uses them. That ordering is the point. A
definition with nothing following it is a glossary, and a story with no
definitions in front of it assumes vocabulary the reader does not have.

**Every definition is written in the vocabulary of its own level.** At level
one that means seven hundred words defining themselves, which is a closure
property the lexicon was not authored for and may not have.
"""

from __future__ import annotations

import json
import random
import re
from collections.abc import Callable, Collection, Iterable, Mapping, Sequence
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Final, cast

from epagoge.concept_graph import Violation


class DefinitionKind(Enum):
    """What a definition is about."""

    WORD = "word"
    DOMAIN = "domain"
    TOPIC = "topic"
    """A schedule unit. The smallest thing a book can be about."""


@dataclass(frozen=True, slots=True)
class Definition:
    """A record's claim to say what something is.

    Carried on the record rather than on the book, because a book is an
    ordering of records and the definition belongs to the sentence that
    makes it.
    """

    kind: DefinitionKind
    target: str


@dataclass(frozen=True, slots=True)
class Book:
    """An ordered run of records with one subject.

    ``about`` and ``teaches`` are **written for a person, not for the
    corpus**, and are the one place in a book where the level's vocabulary
    ceiling does not apply.

    **The corpus is CC0 and is meant to be used.** A parent choosing books
    for a child, or anyone curating a training corpus, has to know what a
    book is about and what it is for, and cannot be asked to infer that
    from sixteen spreads written in eight hundred words. Neither field is
    part of the text a model trains on.
    """

    id: str
    level: int
    title: str
    subject_kind: DefinitionKind
    subject: str
    records: tuple[str, ...] = ()
    about: str = ""
    """What the book is about, in ordinary unrestricted English."""

    teaches: str = ""
    """What a reader is meant to come away with, in ordinary English."""

    form: str = ""
    """How the book is written: ``narrative``, ``question``, ``reference``.

    **A form is what a reader learns to do, not only what they learn.**
    Measured 2026-09-25, the level-one corpus held one question mark in
    4,419 records and no instance of a question being answered, so a model
    trained on it continued a question instead of answering. A corpus that
    only ever states cannot teach anything else.

    Empty where unrecorded, which is every book written before the field
    existed. Those are narrative and the field does not claim it for them.
    """

    author: str = ""
    """Who wrote it. A person, or the teacher model and its operator."""

    licence: str = ""
    """The licence this book is published under, by SPDX identifier.

    **Recorded per book rather than assumed from the repository.** The
    corpus is CC0, and the `exclude/` directories exist so that outside
    contributions can arrive, which means a book in this tree may not
    share the repository's licence. A book that does not say is a book
    nobody can safely reuse, which defeats publishing it.
    """

    first_published: str = ""
    """ISO date this book first existed, in any version."""

    published: str = ""
    """ISO date of this version.

    **Two dates because a book is edited.** A curator comparing two copies
    needs to know which is later, and a reader citing one needs to know
    when the text they read was fixed. One date cannot answer both.
    """


SPREADS_BY_LEVEL: Final[dict[int, int]] = {1: 16, 2: 64, 3: 112, 4: 160}
"""Spreads per book, by level, from the binding.

A book is bound in signatures of sixteen pages, so every level's page
count is a multiple of sixteen and a book that misses it cannot be
published without someone else padding or cutting it. Thirty-two pages at
level one, sixty-four at level two, two hundred and twenty-four at level
three, which is the operator's 225 landing almost exactly on fourteen
signatures. See `docs/decisions/BOOK_FORMATS.md`.
"""

SPREADS: Final[int] = 16
"""Records per book, one per spread, giving a 32-page picture book.

**Operator standard, 2026-09-25, and it is a publishing constraint rather
than a stylistic one.** A picture book is bound in a signature, so its
page count is a multiple of sixteen and thirty-two pages is the trade
standard. Sixteen spreads is what that leaves, and a book that does not
meet it cannot be physically published without being padded or cut by
someone else.

Before this, books ran from one story line to twelve and five of
forty-six had a single line, which is not a book. The count is exact
rather than a floor, because a signature does not accept a book that is
nearly the right length.

The subject statement takes one spread, each defined word takes one, and
the story takes the rest. A book defining eight words therefore has seven
spreads of story, which is why `MAX_DEFINED` is capped well below that.
"""

MAX_WORDS: Final[int] = 1000
"""Superseded 2026-09-25. The former hard cap on a level-one book.

Operator figure, 2026-09-24. A level-one book runs from about a hundred
words to about eight hundred, and does not pass a thousand. Below the
typical range is not an error, since a book about one narrow thing is
allowed to be short. Above the cap it is no longer a picture book.

**This is the level-one figure and :func:`max_words` is the general
one.** A level-two module is sixty-four spreads at about two hundred and
fifty words a spread, so sixteen thousand words, and the level-one cap
would refuse every one of them.
"""

WORDS_PER_SPREAD: Final[dict[int, tuple[int, int]]] = {
    1: (50, 30),
    2: (250, 50),
    3: (500, 100),
    4: (500, 100),
}
"""Words on a spread, by level, as a nominal figure and a tolerance.

**Operator figures, 2026-09-25.** Level one carries fifty words to the
spread, give or take thirty. Level two carries two hundred and fifty,
which is a page of a hundred and twenty-five twice over. **Levels three
and above carry five hundred**, which is two hundred and fifty to the
page and the standard English typesetting metric.

So a level-one book runs to about eight hundred words, a level-two module
to sixteen thousand, level three to fifty-six thousand, and level four to
eighty thousand.

**One table, in one unit.** Words per page and a separate typical-words
band both said this and would have drifted from it. Every band the project
had recorded falls out of this table exactly, which is the check that it
is the same quantity and not a new one.

**The jump from level one is still the largest in the scheme**, a factor
of twenty in the artifact. A spread stops being a sentence under a picture
and becomes a passage, which is a different thing to generate as well as a
different thing to read.
"""


def max_words(level: int) -> int | None:
    """The hard cap on a book at this level, or None where none is settled.

    Derived from the binding and the density where both are known, so
    changing either changes this. A quarter is allowed over the nominal
    figure, because the cap exists to catch a book that is the wrong kind
    of artifact rather than one that ran long.

    **None rather than the level-one figure.** Levels three and four have a
    page count and no words-to-the-page number, and applying a picture
    book's thousand-word cap to a two-hundred-and-twenty-four spread book
    would refuse every one of them. A cap nobody has set is reported as
    absent, not invented.
    """
    band = typical_words(level)
    if band is None:
        return None
    return band[1] * 5 // 4


TYPICAL_WORDS: Final[tuple[int, int]] = (100, 800)
"""Superseded 2026-09-25 by :data:`WORDS_PER_SPREAD`.

Kept because it is the figure the level-one corpus was written to, and
every book in it sits inside this band and below the new one. The operator
set fifty words a spread, give or take thirty, which makes a level-one
book three hundred and twenty to one thousand two hundred and eighty words
rather than one hundred to eight hundred.
"""


def normalise_definition(text: str) -> str:
    """Capitalise and terminate a definition, which is a fragment by design.

    **The dictionary's own style is a capitalised fragment**, as in
    "Checking that something is true.", so a teacher writing "a small
    number of something" has written an acceptable definition in the wrong
    case. Measured 2026-09-25 over a round's quarantine, twenty-four of the
    twenty-five lines rejected as not a sentence were definitions and every
    one was recoverable this way.

    **Confined to definitions.** A story line is prose, and its shape is
    evidence about whether the teacher wrote a sentence at all, which is
    the failure `well_formed` exists for. Normalising a story line would
    have let "breath lasted long" through, which is the line that caused
    the check to be written.
    """
    text = text.strip()
    if not text:
        return text
    if not text[0].isupper():
        text = text[0].upper() + text[1:]
    if text[-1] not in ".!?":
        text += "."
    return text


def typical_words(level: int) -> tuple[int, int] | None:
    """The word count a book at this level is expected to land in.

    Derived from the binding and the density rather than stated, so that
    changing either changes this. Reported and never enforced, like the
    band it generalises, because a book about one narrow thing is allowed
    to be short.

    **None where the density is not settled.** Levels five and above are
    papers rather than books, so a spread count measures nothing and
    reporting the level-one band for them would be a made-up number
    presented as a standard.

    Derived from one table rather than two. An earlier version kept words
    per page beside words per spread, which is the same quantity in two
    units, and they would have drifted.
    """
    spreads = SPREADS_BY_LEVEL.get(level)
    band = WORDS_PER_SPREAD.get(level)
    if spreads is None or band is None:
        return None
    nominal, tolerance = band
    return (spreads * (nominal - tolerance), spreads * (nominal + tolerance))


@dataclass(frozen=True, slots=True)
class Coverage:
    """What has a definition and what does not."""

    defined: frozenset[str]
    undefined: tuple[str, ...]

    @property
    def fraction(self) -> float:
        total = len(self.defined) + len(self.undefined)
        return len(self.defined) / total if total else 1.0


def definition_coverage(
    definitions: Mapping[str, Definition], kind: DefinitionKind, expected: Iterable[str]
) -> Coverage:
    """Which of ``expected`` carry a definition of ``kind``.

    Reported rather than enforced while the corpus is being written. A word
    with no definition is not a defect in an unfinished corpus and is one in
    a finished level.
    """
    defined = {d.target for d in definitions.values() if d.kind is kind}
    wanted = set(expected)
    return Coverage(
        defined=frozenset(defined & wanted),
        undefined=tuple(sorted(wanted - defined)),
    )


def book_prerequisites(
    books: Sequence[Book],
    teaches: Mapping[str, Collection[str]],
    prerequisites: Mapping[str, Collection[str]],
) -> dict[str, set[str]]:
    """Which books must precede which.

    Book B depends on book A when B teaches a concept whose prerequisite is
    taught in A and not in B. **The ordering ablation orders books**, so the
    topological constraint lives here rather than between concepts, and a
    control arm that ignores it is not a curriculum at all.

    ``teaches`` maps a book to the concepts its records cover.
    ``prerequisites`` is the concept graph's own relation.
    """
    owner: dict[str, str] = {}
    for book in books:
        for concept in teaches.get(book.id, ()):
            owner.setdefault(concept, book.id)

    out: dict[str, set[str]] = {b.id: set() for b in books}
    for book in books:
        covered = set(teaches.get(book.id, ()))
        for concept in covered:
            for need in prerequisites.get(concept, ()):
                if need in covered:
                    continue
                source = owner.get(need)
                if source is not None and source != book.id:
                    out[book.id].add(source)
    return out


def topological_orders_exist(deps: Mapping[str, Collection[str]]) -> bool:
    """Whether the book dependency graph is acyclic."""
    return len(linear_extension(deps, lambda ready: min(ready))) == len(deps)


def linear_extension(
    deps: Mapping[str, Collection[str]],
    pick: Callable[[set[str]], str],
) -> list[str]:
    """One ordering respecting every dependency. ``pick`` chooses among ties.

    Returns a short list when the graph is cyclic, which the caller checks
    rather than this raising, so a cycle is reported with the rest of the
    violations instead of stopping the run.
    """
    remaining = {node: set(parents) for node, parents in deps.items()}
    dependents: dict[str, set[str]] = {node: set() for node in deps}
    for node, parents in remaining.items():
        for parent in parents:
            dependents.setdefault(parent, set()).add(node)
    ready = {node for node, parents in remaining.items() if not parents}
    order: list[str] = []
    while ready:
        chosen = pick(ready)
        ready.discard(chosen)
        order.append(chosen)
        for child in sorted(dependents.get(chosen, ())):
            remaining[child].discard(chosen)
            if not remaining[child]:
                ready.add(child)
    return order


def random_linear_extension(
    deps: Mapping[str, Collection[str]], rng: random.Random
) -> list[str]:
    """A uniformly random choice among ready books at each step.

    **Not a random permutation.** A permutation can put a book teaching
    counting before the book teaching same and different, which is not a
    curriculum in any ordering and would make the control arm weaker than
    the design asks for rather than merely different.
    """
    return linear_extension(deps, lambda ready: rng.choice(sorted(ready)))


@dataclass(frozen=True, slots=True)
class Closure:
    """Whether a level's dictionary actually defines itself.

    **This is the self-hosting problem.** A dictionary in which every word
    is defined in terms of other words can still be vacuous, if those words
    are defined in terms of the first. A compiler written in its own
    language needs a seed compiler written in something else, and a level's
    lexicon needs words that are shown rather than said.

    The seed here is the function words, which name nothing, and the
    exemptions. Everything else has to reduce to them.
    """

    grounded: frozenset[str]
    undefined: tuple[str, ...]
    """Used in some definition and never defined."""

    blocked: tuple[str, ...]
    """Defined, but resting on something that is not grounded."""

    cycles: tuple[tuple[str, ...], ...]
    """Groups that genuinely define each other and reduce to nothing else.

    Distinguished from merely blocked, which an earlier version conflated
    with a cycle and so reported three cycles where there were none. A word
    waiting on a word that is waiting on an undefined word is stuck, not
    circular, and the two need different fixes.
    """

    @property
    def fraction(self) -> float:
        total = (
            len(self.grounded) + len(self.undefined) + sum(len(c) for c in self.cycles)
        )
        return len(self.grounded) / total if total else 1.0


def word_definitions(
    books: Sequence[Book], records: Sequence[Mapping[str, object]]
) -> dict[str, str]:
    """The canonical definition of each word, preferring the dictionary.

    **Fifty-two words carried two or more different definitions** on
    2026-09-25, because a book defines its words in context and the
    dictionary defines them again. That is the design and the paraphrase
    is useful to a reader.

    What was not the design is that every caller built the map by
    assignment in record order, so **which definition reached the training
    stream depended on which file was read last**. A dictionary book is the
    canonical source and wins; among ordinary books the first is kept, so
    the result does not move when an unrelated book is added.
    """
    canonical: dict[str, str] = {}
    ordinary: dict[str, str] = {}
    by_book = {
        book.id: [r for r in records if str(r["id"]) in set(book.records)]
        for book in books
    }
    for book in books:
        target = canonical if book.id.startswith("bk.dictionary.") else ordinary
        for record in by_book[book.id]:
            defines = record.get("defines")
            if not isinstance(defines, Mapping):
                continue
            entry = cast(Mapping[str, object], defines)
            if entry.get("kind") != "word":
                continue
            word = str(entry["target"])
            if word not in target:
                target[word] = str(record["content"])
    return {**ordinary, **canonical}


def dictionary_closure(
    definitions: Mapping[str, str],
    seed: Collection[str],
    tokenise: Callable[[str], list[str]],
    resolve: Callable[[str], str | None],
) -> Closure:
    """Which defined words reduce to the seed, and which do not.

    ``resolve`` maps a surface form to its headword, so that a definition
    using "cups" grounds on "cup". ``seed`` is the set of words available
    without definition.

    A word grounds when every content word in its definition is either in
    the seed, is the word itself, or is already grounded. Iterated to a
    fixed point, and whatever remains is either undefined or in a cycle.
    """
    known = set(seed)
    uses: dict[str, set[str]] = {}
    for word, text in definitions.items():
        needed: set[str] = set()
        for token in tokenise(text):
            head = resolve(token) or token
            # **Resolve before testing the seed.** `arms` is not itself in
            # the seed and `arm` is, so testing the surface form alone put
            # every inflection of a seed word on the frontier. Found on
            # 2026-09-25 with `arm` reported as undefined while sitting in
            # the ostensive set.
            if token in known or head in known:
                continue
            if head != word:
                needed.add(head)
        uses[word] = needed

    # **A seed word reduces to the seed trivially**, whether or not a
    # definition has also been written for it. Without this a defined seed
    # word was evaluated as though it still had to earn its ground.
    grounded: set[str] = {word for word in uses if word in known}
    changed = True
    while changed:
        changed = False
        for word, needed in uses.items():
            if word not in grounded and needed <= grounded:
                grounded.add(word)
                changed = True

    stuck = {w: n - grounded for w, n in uses.items() if w not in grounded}
    undefined = sorted({n for needs in stuck.values() for n in needs if n not in uses})

    # A word is cyclic only when every path out of it returns to the group.
    # A word waiting on a word that is waiting on something undefined is
    # blocked instead, and conflating the two reported cycles that were not.
    reaches_undefined: set[str] = set()
    changed = True
    while changed:
        changed = False
        for word, needs in stuck.items():
            if word in reaches_undefined:
                continue
            if any(n not in uses or n in reaches_undefined for n in needs):
                reaches_undefined.add(word)
                changed = True

    cycles: list[tuple[str, ...]] = []
    remaining = set(stuck) - reaches_undefined
    while remaining:
        start = min(remaining)
        component = {start}
        frontier = [start]
        while frontier:
            current = frontier.pop()
            for nxt in stuck.get(current, ()):
                if nxt in remaining and nxt not in component:
                    component.add(nxt)
                    frontier.append(nxt)
        cycles.append(tuple(sorted(component)))
        remaining -= component

    return Closure(
        grounded=frozenset(grounded),
        undefined=tuple(undefined),
        blocked=tuple(sorted(reaches_undefined)),
        cycles=tuple(cycles),
    )


def validate_books(
    books: Sequence[Book],
    record_levels: Mapping[str, int],
    definitions: Mapping[str, Definition],
    known_words: Collection[str],
    known_domains: Collection[str],
    known_topics: Collection[str],
    word_counts: Mapping[str, int] | None = None,
    spreads: int | None = None,
    describe: bool = False,
) -> list[Violation]:
    """Return every breach. Empty means the books are sound.

    ``describe`` requires every book to say what it is about and what it
    teaches, for the curator rather than the reader. Off by default because
    every book in the corpus predates the fields.

    ``spreads`` enforces the page standard when given. It is a parameter
    rather than a constant because a board book and a picture book bind to
    different signatures, so the number is a property of the edition and
    not of the validator.
    """
    out: list[Violation] = []
    seen: dict[str, str] = {}
    for book in books:
        # **A dictionary is reference material, not a picture book.** It is
        # as long as the lexicon is, so binding it to a signature would
        # mean cutting definitions to fit a page count.
        if book.id.startswith("bk.dictionary."):
            continue
        if spreads is not None and len(book.records) != spreads:
            out.append(
                Violation(
                    "wrong-length",
                    f"book {book.id!r} has {len(book.records)} spreads and a "
                    f"publishable book has {spreads}",
                )
            )
    targets = {
        DefinitionKind.WORD: set(known_words),
        DefinitionKind.DOMAIN: set(known_domains),
        DefinitionKind.TOPIC: set(known_topics),
    }

    for record_id, definition in sorted(definitions.items()):
        if definition.target not in targets[definition.kind]:
            out.append(
                Violation(
                    "definition-unknown-target",
                    f"record {record_id!r} defines {definition.kind.value}"
                    f" {definition.target!r}, which does not exist",
                )
            )

    for book in books:
        # **Reported, not enforced, until the corpus carries them.** Every
        # book predates these fields, so refusing a book without them would
        # refuse the whole corpus. The count is what makes the gap visible.
        if describe and not (book.about.strip() and book.teaches.strip()):
            out.append(
                Violation(
                    "undescribed-book",
                    f"book {book.id!r} does not say what it is about or what"
                    " it teaches, which a curator needs and a reader of the"
                    " text cannot recover",
                )
            )
        if describe and not book.licence.strip():
            out.append(
                Violation(
                    "unlicensed-book",
                    f"book {book.id!r} names no licence, so nobody can safely"
                    " reuse it, and the repository's licence cannot be assumed"
                    " for a book that may have come from elsewhere",
                )
            )
    for book in books:
        if not book.records:
            out.append(Violation("empty-book", f"book {book.id!r} holds no record"))
        for record_id in book.records:
            if record_id not in record_levels:
                out.append(
                    Violation(
                        "unknown-record",
                        f"book {book.id!r} names absent record {record_id!r}",
                    )
                )
                continue
            if record_levels[record_id] != book.level:
                out.append(
                    Violation(
                        "book-level-mismatch",
                        f"book {book.id!r} at level {book.level} holds record"
                        f" {record_id!r} at level {record_levels[record_id]}",
                    )
                )
            if record_id in seen:
                out.append(
                    Violation(
                        "record-in-two-books",
                        f"record {record_id!r} is in {seen[record_id]!r}"
                        f" and {book.id!r}",
                    )
                )
            seen[record_id] = book.id

        # The subject must be defined inside the book that is about it. A
        # book about a thing that never says what the thing is leaves the
        # reader to infer it, which is the failure this shape exists to fix.
        defined_here = {
            (d.kind, d.target)
            for r in book.records
            if (d := definitions.get(r)) is not None
        }
        if (book.subject_kind, book.subject) not in defined_here:
            out.append(
                Violation(
                    "subject-undefined",
                    f"book {book.id!r} is about {book.subject_kind.value}"
                    f" {book.subject!r} and no record in it defines that",
                )
            )

        if word_counts is not None:
            total = sum(word_counts.get(r, 0) for r in book.records)
            cap = max_words(book.level)
            if cap is not None and total > cap:
                out.append(
                    Violation(
                        "book-too-long",
                        f"book {book.id!r} runs to {total} words, over the"
                        f" {cap} cap for level {book.level}",
                    )
                )

        # Definition before use. A word defined after the story that uses it
        # is a glossary at the back, which is not what this ordering is for.
        first_story = next(
            (i for i, r in enumerate(book.records) if r not in definitions),
            len(book.records),
        )
        for index, record_id in enumerate(book.records):
            if index > first_story and record_id in definitions:
                out.append(
                    Violation(
                        "definition-after-use",
                        f"book {book.id!r} defines in {record_id!r} after the"
                        " material that uses it has begun",
                    )
                )
    return out


def _optional(fields: Mapping[object, object], key: str, where: str) -> str:
    """A string field that may be absent, but may not be the wrong type.

    Absent is allowed because the corpus predates these fields. A number
    or a list where prose belongs is a mistake and is refused.
    """
    value = fields.get(key)
    if value is None:
        return ""
    if not isinstance(value, str):
        raise ValueError(f"{where}.{key}: expected a string")
    return value


def _require(fields: Mapping[object, object], key: str, where: str) -> str:
    value = fields.get(key)
    if not isinstance(value, str):
        raise ValueError(f"{where}.{key}: expected a string")
    return value


def definition_from_json(raw: object, where: str) -> Definition | None:
    if raw is None:
        return None
    if not isinstance(raw, dict):
        raise ValueError(f"{where}: 'defines' must be an object")
    fields = cast(dict[object, object], raw)
    return Definition(
        kind=DefinitionKind(_require(fields, "kind", where)),
        target=_require(fields, "target", where),
    )


def book_from_json(payload: object, where: str = "book") -> tuple[Book, list[object]]:
    """One book and its records, from a single file.

    **A book is one file.** Splitting the ordering from the records made a
    book something a reviewer had to assemble from two places before they
    could read it, and reading it is the step that decides whether it enters
    the corpus.
    """
    if not isinstance(payload, dict):
        raise ValueError(f"{where}: expected an object")
    fields = cast(dict[object, object], payload)
    level = fields.get("level")
    if not isinstance(level, int):
        raise ValueError(f"{where}.level: expected an integer")
    raw_subject = fields.get("subject")
    if not isinstance(raw_subject, dict):
        raise ValueError(f"{where}.subject: expected an object")
    subject = cast(dict[object, object], raw_subject)
    raw_records = fields.get("records")
    if not isinstance(raw_records, list):
        raise ValueError(f"{where}.records: expected a list")
    records = cast(list[object], raw_records)
    ids: list[str] = []
    for position, record in enumerate(records):
        if not isinstance(record, dict):
            raise ValueError(f"{where}.records[{position}]: expected an object")
        identifier = cast(dict[object, object], record).get("id")
        if not isinstance(identifier, str):
            raise ValueError(f"{where}.records[{position}].id: expected a string")
        ids.append(identifier)
    book = Book(
        id=_require(fields, "id", where),
        level=level,
        title=_require(fields, "title", where),
        subject_kind=DefinitionKind(_require(subject, "kind", where)),
        subject=_require(subject, "target", where),
        records=tuple(ids),
        about=_optional(fields, "about", where),
        teaches=_optional(fields, "teaches", where),
        form=_optional(fields, "form", where),
        author=_optional(fields, "author", where),
        licence=_optional(fields, "licence", where),
        first_published=_optional(fields, "first_published", where),
        published=_optional(fields, "published", where),
    )
    return book, records


BLOCK_RE: Final[re.Pattern[str]] = re.compile(r"^\[([^\]\n]+)\]\s*$", re.MULTILINE)
FRONT_MATTER = "---"


def records_in(
    book: Book, records: Sequence[Mapping[str, object]]
) -> list[Mapping[str, object]]:
    """The records belonging to one book, in the book's own order.

    ``load_book_dir`` returns every record in the directory flat, so a
    caller rewriting a single book has to select its own back out.
    """
    by_id = {str(r["id"]): r for r in records}
    return [by_id[i] for i in book.records if i in by_id]


def extend_records(
    existing: Sequence[Mapping[str, object]], new: Sequence[Mapping[str, object]]
) -> list[Mapping[str, object]]:
    """Existing records, then the new ones whose id is not already present.

    **A generator that re-renders a book from its own run alone destroys
    what earlier runs put there.** ``generate_dictionary.py`` filtered its
    new records against the ids already in the book and then wrote the file
    from that filtered list, which would have replaced twenty-two
    accumulated definitions with whatever the next run happened to produce.

    Found by reading the write path before running it rather than by losing
    the definitions, so the failure is recorded as latent rather than as an
    incident. The accumulate-and-deduplicate rule lives here so a test can
    reach it, since the generators are outside the coverage source.
    """
    out = list(existing)
    have = {str(r["id"]) for r in out}
    for record in new:
        identifier = str(record["id"])
        if identifier in have:
            continue
        have.add(identifier)
        out.append(record)
    return out


def book_head(book: Book) -> dict[str, object]:
    """The front matter of a book, for handing back to :func:`render_book`.

    **Every tool that rewrites a book was rebuilding this by hand**, and
    each hand-built copy listed the fields that existed when it was
    written. Adding `about` and `teaches` would therefore have erased them
    from any book a rewriter touched, silently, which is the shape of
    failure this project has found four times in other places.

    One function, so a new field reaches every writer at once.
    """
    head: dict[str, object] = {
        "id": book.id,
        "level": book.level,
        "title": book.title,
        "subject": {"kind": book.subject_kind.value, "target": book.subject},
    }
    # Omitted rather than written empty, so a book that has never been
    # described does not carry two blank fields pretending otherwise.
    for key, value in (
        ("form", book.form),
        ("author", book.author),
        ("licence", book.licence),
        ("first_published", book.first_published),
        ("published", book.published),
        ("about", book.about),
        ("teaches", book.teaches),
    ):
        if value:
            head[key] = value
    return head


def render_book(
    payload: Mapping[str, object], records: Sequence[Mapping[str, object]]
) -> str:
    """A book as prose with its annotation above it.

    **JSON was the wrong format and the ratio said so.** A level-one book of
    173 words occupied 260 lines of structure, and the project's own
    sequence makes reading the corpus the step that decides whether
    generation continues. A format that obstructs reading obstructs the one
    check nothing automates.

    It gets worse with level. A level-five record is a paragraph and a
    level-seven one draws on real literature, neither of which survives
    being escaped into a string field.
    """
    # One line per record annotation. Pretty-printing the whole block put
    # 190 lines of structure above 137 words of prose, which is the problem
    # this format exists to fix rather than a smaller version of it.
    head = {k: v for k, v in payload.items() if k != "records"}
    annotations = ",\n".join(
        "    "
        + json.dumps(str(r["id"]))
        + ": "
        + json.dumps(
            {k: v for k, v in r.items() if k not in ("id", "content", "level")}
        )
        for r in records
    )
    front = (
        json.dumps(head, indent=2)[:-2].rstrip().rstrip(",")
        + ',\n  "records": {\n'
        + annotations
        + "\n  }\n}"
    )
    body = "\n\n".join(f"[{r['id']}]\n{r['content']}" for r in records)
    return f"{FRONT_MATTER}\n{front}\n{FRONT_MATTER}\n\n{body}\n"


def parse_book(text: str, where: str = "book") -> tuple[Book, list[object]]:
    """Read a book file back. Front matter, then id-marked blocks.

    Blocks are marked rather than positional. Positional matching is silent
    when an insertion shifts everything by one, which is the failure shape
    this project keeps finding in its own checks.
    """
    if not text.startswith(FRONT_MATTER):
        raise ValueError(f"{where}: no front matter")
    _, _, rest = text.partition(FRONT_MATTER)
    raw_head, sep, raw_body = rest.partition(f"\n{FRONT_MATTER}")
    if not sep:
        raise ValueError(f"{where}: front matter is not closed")
    head = json.loads(raw_head)
    if not isinstance(head, dict):
        raise ValueError(f"{where}: front matter must be an object")
    fields = cast(dict[str, object], head)
    annotations = fields.pop("records", {})
    if not isinstance(annotations, dict):
        raise ValueError(f"{where}.records: expected an object")
    notes = cast(dict[str, object], annotations)

    blocks: dict[str, str] = {}
    order: list[str] = []
    matches = list(BLOCK_RE.finditer(raw_body))
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(raw_body)
        identifier = match.group(1).strip()
        if identifier in blocks:
            raise ValueError(f"{where}: block {identifier!r} repeats")
        blocks[identifier] = raw_body[match.end() : end].strip()
        order.append(identifier)

    missing = sorted(set(notes) - set(blocks))
    extra = sorted(set(blocks) - set(notes))
    if missing:
        raise ValueError(f"{where}: annotated but no block: {' '.join(missing)}")
    if extra:
        raise ValueError(f"{where}: block but no annotation: {' '.join(extra)}")

    level = fields.get("level")
    if not isinstance(level, int):
        raise ValueError(f"{where}.level: expected an integer")
    records: list[object] = [
        {
            "id": identifier,
            "level": level,
            "content": blocks[identifier],
            **cast(dict[str, object], notes[identifier]),
        }
        for identifier in order
    ]
    fields["records"] = records
    return book_from_json(fields, where)


def load_book_dir(path: Path) -> tuple[list[Book], list[object]]:
    """Every book in a directory, newest ordering last.

    Sorted by filename so a run is reproducible and a diff is readable.
    """
    books: list[Book] = []
    payloads: list[object] = []
    for file in sorted(path.glob("*.md")):
        book, records = parse_book(file.read_text(encoding="utf-8"), file.name)
        books.append(book)
        payloads.extend(records)
    return books, payloads


def books_from_json(payload: object) -> list[Book]:
    if not isinstance(payload, list):
        raise ValueError("books payload must be a JSON list")
    out: list[Book] = []
    for index, entry in enumerate(cast(list[object], payload)):
        where = f"books[{index}]"
        if not isinstance(entry, dict):
            raise ValueError(f"{where}: expected an object")
        fields = cast(dict[object, object], entry)
        level = fields.get("level")
        if not isinstance(level, int):
            raise ValueError(f"{where}.level: expected an integer")
        raw_subject = fields.get("subject")
        if not isinstance(raw_subject, dict):
            raise ValueError(f"{where}.subject: expected an object")
        subject = cast(dict[object, object], raw_subject)
        raw_records = fields.get("records")
        if not isinstance(raw_records, list):
            raise ValueError(f"{where}.records: expected a list")
        records = cast(list[object], raw_records)
        for position, record in enumerate(records):
            if not isinstance(record, str):
                raise ValueError(f"{where}.records[{position}]: expected a string")
        # **The optional fields are read here too.** This listed six of
        # twelve, so every consumer of `load_books` saw a book whose form
        # and metadata were absent rather than empty and could not tell
        # the difference. The markdown reader had them and the JSON reader
        # did not, which is the same divergence in two directions.
        out.append(
            Book(
                id=_require(fields, "id", where),
                level=level,
                title=_require(fields, "title", where),
                subject_kind=DefinitionKind(_require(subject, "kind", where)),
                subject=_require(subject, "target", where),
                records=tuple(cast(list[str], records)),
                about=_optional(fields, "about", where),
                teaches=_optional(fields, "teaches", where),
                form=_optional(fields, "form", where),
                author=_optional(fields, "author", where),
                licence=_optional(fields, "licence", where),
                first_published=_optional(fields, "first_published", where),
                published=_optional(fields, "published", where),
            )
        )
    return out


def load_books(path: Path) -> list[Book]:
    return books_from_json(json.loads(path.read_text(encoding="utf-8")))
