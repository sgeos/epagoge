"""English verb inflection, so that admitting a verb admits all of it.

**A verb admitted in one form is a trap.** The core list held ``have``,
``has`` and ``had`` and not ``having``, and ``say``, ``says`` and ``said``
and not ``saying``. Forty such gaps were found on 2026-09-25 by reading
the words a generator was blocked by, which is an expensive way to
discover a missing plural.

Operator direction the same day. Every verb carries every inflection, as
standard procedure rather than as a repair. This module supplies the
forms and ``vocabulary`` enforces their presence, so the next gap is a
gate failure rather than a wasted batch.

Standard library only, matching the rest of the package.
"""

from __future__ import annotations

from typing import Final

VOWELS: Final[frozenset[str]] = frozenset("aeiou")

SIBILANT_ENDINGS: Final[tuple[str, ...]] = ("s", "x", "z", "ch", "sh", "o")
"""Endings taking ``-es`` rather than ``-s``. ``o`` covers go and do."""

NO_DOUBLE: Final[frozenset[str]] = frozenset("wxy")
"""Never doubled, so ``show`` gives showing and not showwing."""

IRREGULAR: Final[dict[str, tuple[str, str, str]]] = {
    # base: (past, past participle, present participle when not regular)
    "be": ("was", "been", "being"),
    "become": ("became", "become", "becoming"),
    "begin": ("began", "begun", "beginning"),
    "blow": ("blew", "blown", "blowing"),
    "break": ("broke", "broken", "breaking"),
    "bring": ("brought", "brought", "bringing"),
    "build": ("built", "built", "building"),
    "buy": ("bought", "bought", "buying"),
    "catch": ("caught", "caught", "catching"),
    "come": ("came", "come", "coming"),
    "cut": ("cut", "cut", "cutting"),
    "dig": ("dug", "dug", "digging"),
    "do": ("did", "done", "doing"),
    "draw": ("drew", "drawn", "drawing"),
    "drink": ("drank", "drunk", "drinking"),
    "eat": ("ate", "eaten", "eating"),
    "fall": ("fell", "fallen", "falling"),
    "feed": ("fed", "fed", "feeding"),
    "feel": ("felt", "felt", "feeling"),
    "find": ("found", "found", "finding"),
    "fly": ("flew", "flown", "flying"),
    "forget": ("forgot", "forgotten", "forgetting"),
    "freeze": ("froze", "frozen", "freezing"),
    "get": ("got", "got", "getting"),
    "give": ("gave", "given", "giving"),
    "go": ("went", "gone", "going"),
    "grow": ("grew", "grown", "growing"),
    "have": ("had", "had", "having"),
    "hear": ("heard", "heard", "hearing"),
    "hide": ("hid", "hidden", "hiding"),
    "hit": ("hit", "hit", "hitting"),
    "hold": ("held", "held", "holding"),
    "hurt": ("hurt", "hurt", "hurting"),
    "keep": ("kept", "kept", "keeping"),
    "know": ("knew", "known", "knowing"),
    "lead": ("led", "led", "leading"),
    "learn": ("learned", "learned", "learning"),
    "leave": ("left", "left", "leaving"),
    "let": ("let", "let", "letting"),
    "lie": ("lied", "lied", "lying"),
    "lose": ("lost", "lost", "losing"),
    "make": ("made", "made", "making"),
    "mean": ("meant", "meant", "meaning"),
    "meet": ("met", "met", "meeting"),
    "pay": ("paid", "paid", "paying"),
    "put": ("put", "put", "putting"),
    "read": ("read", "read", "reading"),
    "ring": ("rang", "rung", "ringing"),
    "run": ("ran", "run", "running"),
    "say": ("said", "said", "saying"),
    "see": ("saw", "seen", "seeing"),
    "sell": ("sold", "sold", "selling"),
    "set": ("set", "set", "setting"),
    "shake": ("shook", "shaken", "shaking"),
    "show": ("showed", "shown", "showing"),
    "shut": ("shut", "shut", "shutting"),
    "sing": ("sang", "sung", "singing"),
    "sink": ("sank", "sunk", "sinking"),
    "sleep": ("slept", "slept", "sleeping"),
    "speak": ("spoke", "spoken", "speaking"),
    "spell": ("spelled", "spelled", "spelling"),
    "spill": ("spilled", "spilled", "spilling"),
    "stand": ("stood", "stood", "standing"),
    "steal": ("stole", "stolen", "stealing"),
    "stick": ("stuck", "stuck", "sticking"),
    "swim": ("swam", "swum", "swimming"),
    "take": ("took", "taken", "taking"),
    "teach": ("taught", "taught", "teaching"),
    "tear": ("tore", "torn", "tearing"),
    "tell": ("told", "told", "telling"),
    "think": ("thought", "thought", "thinking"),
    "throw": ("threw", "thrown", "throwing"),
    "understand": ("understood", "understood", "understanding"),
    "wake": ("woke", "woken", "waking"),
    "wear": ("wore", "worn", "wearing"),
    "write": ("wrote", "written", "writing"),
}
"""Verbs whose past forms are not derivable. The present participle is
listed too so that one lookup answers the whole question."""


def _is_consonant(letter: str) -> bool:
    return letter.isalpha() and letter not in VOWELS


def _doubles_final(word: str) -> bool:
    """Consonant-vowel-consonant in a single syllable doubles.

    Approximated by syllable count rather than by stress, which is not
    recoverable from spelling. ``stop`` doubles, ``visit`` does not, and
    the approximation is stated rather than hidden because it is wrong for
    stressed final syllables in longer words such as ``begin``, which is
    why those are listed as irregular.
    """
    if len(word) < 3 or sum(1 for c in word if c in VOWELS) != 1:
        return False
    return (
        _is_consonant(word[-1])
        and word[-1] not in NO_DOUBLE
        and word[-2] in VOWELS
        and _is_consonant(word[-3])
    )


def third_person(word: str) -> str:
    """The ``-s`` form. Regular for every English verb but ``be``."""
    if word == "be":
        return "is"
    if word == "have":
        return "has"
    if word.endswith("y") and len(word) > 1 and _is_consonant(word[-2]):
        return word[:-1] + "ies"
    if word.endswith(SIBILANT_ENDINGS):
        return word + "es"
    return word + "s"


def present_participle(word: str) -> str:
    """The ``-ing`` form."""
    listed = IRREGULAR.get(word)
    if listed is not None:
        return listed[2]
    if word.endswith("ie"):
        return word[:-2] + "ying"
    if word.endswith("ee") or word.endswith("ye") or word.endswith("oe"):
        return word + "ing"
    if word.endswith("e"):
        return word[:-1] + "ing"
    if _doubles_final(word):
        return word + word[-1] + "ing"
    return word + "ing"


def past(word: str) -> str:
    listed = IRREGULAR.get(word)
    if listed is not None:
        return listed[0]
    return _regular_past(word)


def past_participle(word: str) -> str:
    listed = IRREGULAR.get(word)
    if listed is not None:
        return listed[1]
    return _regular_past(word)


def _regular_past(word: str) -> str:
    if word.endswith("e"):
        return word + "d"
    if word.endswith("y") and len(word) > 1 and _is_consonant(word[-2]):
        return word[:-1] + "ied"
    if _doubles_final(word):
        return word + word[-1] + "ed"
    return word + "ed"


def verb_forms(word: str) -> tuple[str, ...]:
    """Every inflection of ``word``, excluding the base, without repeats.

    Order is stable so that a generated lexicon diff is readable.
    """
    out: list[str] = []
    for form in (
        third_person(word),
        past(word),
        past_participle(word),
        present_participle(word),
    ):
        if form != word and form not in out:
            out.append(form)
    return tuple(out)
