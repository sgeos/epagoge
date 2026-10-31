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

from collections.abc import Mapping
from typing import Final

VOWELS: Final[frozenset[str]] = frozenset("aeiou")

SIBILANT_ENDINGS: Final[tuple[str, ...]] = ("s", "x", "z", "ch", "sh", "o")
"""Endings taking ``-es`` rather than ``-s``. ``o`` covers go and do."""

NO_DOUBLE: Final[frozenset[str]] = frozenset("wxy")
"""Never doubled, so ``show`` gives showing and not showwing."""

NO_DOUBLE_MULTISYLLABIC: Final[frozenset[str]] = frozenset(
    {
        # Admitted 2026-10-30 in evals/review/level_2_long_tail/.
        "blossom",
        "differ",
        "fasten",
        "interpret",
        "lessen",
        "recover",
        "shorten",
        "strengthen",
        "threaten",
        "answer",
        "cover",
        "discover",
        "enter",
        "happen",
        "listen",
        "monitor",
        "offer",
        "open",
        "order",
        "remember",
        "scatter",
        # The single-l spelling the modern sources use. British usage doubles.
        "travel",
        "uncover",
        "whisper",
        "wonder",
        # Final syllable unstressed. The regular forms do not double.
        "consider",
        "develop",
        "harbor",
        "inhibit",
        "maintain",
        "quarrel",
        "utter",
        "visit",
        # Admitted on 2026-10-29, final syllable unstressed.
        "flatten",
        "focus",
        "gather",
        "transit",
        # Admitted on 2026-10-30, final syllable unstressed.
        "abandon",
        "alter",
        "deliver",
        "inhabit",
        # Admitted on 2026-10-30 as a second sense, final syllable
        # unstressed. American spelling, as the noun is.
        "color",
    }
)
"""Longer verbs ending consonant-vowel-consonant whose final syllable is
unstressed, so the consonant does not double.

**Spelling does not say which way these go.** ``admit`` doubles and
``visit`` does not, and nothing in the letters distinguishes them. Every
such verb is therefore classified by hand, either here or in
:data:`IRREGULAR`, and :func:`doubling_is_ambiguous` reports any that are
classified in neither so the gate can refuse them. ``admit`` reached the
lexicon as ``admited`` before this list existed.
"""

IRREGULAR: Final[dict[str, tuple[str, str, str]]] = {
    # base: (past, past participle, present participle when not regular)
    "be": ("was", "been", "being"),
    "become": ("became", "become", "becoming"),
    "begin": ("began", "begun", "beginning"),
    "break": ("broke", "broken", "breaking"),
    "build": ("built", "built", "building"),
    "come": ("came", "come", "coming"),
    "do": ("did", "done", "doing"),
    "drink": ("drank", "drunk", "drinking"),
    "eat": ("ate", "eaten", "eating"),
    "fall": ("fell", "fallen", "falling"),
    "feed": ("fed", "fed", "feeding"),
    "find": ("found", "found", "finding"),
    "forget": ("forgot", "forgotten", "forgetting"),
    "freeze": ("froze", "frozen", "freezing"),
    "get": ("got", "got", "getting"),
    "give": ("gave", "given", "giving"),
    "go": ("went", "gone", "going"),
    "have": ("had", "had", "having"),
    "hang": ("hung", "hung", "hanging"),
    "hear": ("heard", "heard", "hearing"),
    "hide": ("hid", "hidden", "hiding"),
    "keep": ("kept", "kept", "keeping"),
    "know": ("knew", "known", "knowing"),
    "lead": ("led", "led", "leading"),
    "learn": ("learned", "learned", "learning"),
    "leave": ("left", "left", "leaving"),
    "lie": ("lied", "lied", "lying"),
    "make": ("made", "made", "making"),
    "mean": ("meant", "meant", "meaning"),
    "meet": ("met", "met", "meeting"),
    "pay": ("paid", "paid", "paying"),
    "read": ("read", "read", "reading"),
    "ring": ("rang", "rung", "ringing"),
    "run": ("ran", "run", "running"),
    "say": ("said", "said", "saying"),
    "see": ("saw", "seen", "seeing"),
    "shake": ("shook", "shaken", "shaking"),
    "show": ("showed", "shown", "showing"),
    "sit": ("sat", "sat", "sitting"),
    "choose": ("chose", "chosen", "choosing"),
    "cost": ("cost", "cost", "costing"),
    "rise": ("rose", "risen", "rising"),
    "shine": ("shone", "shone", "shining"),
    "shrink": ("shrank", "shrunk", "shrinking"),
    "slide": ("slid", "slid", "sliding"),
    "win": ("won", "won", "winning"),
    "lose": ("lost", "lost", "losing"),
    "fly": ("flew", "flown", "flying"),
    "draw": ("drew", "drawn", "drawing"),
    "grow": ("grew", "grown", "growing"),
    "blow": ("blew", "blown", "blowing"),
    "hold": ("held", "held", "holding"),
    "feel": ("felt", "felt", "feeling"),
    "sell": ("sold", "sold", "selling"),
    "buy": ("bought", "bought", "buying"),
    "bend": ("bent", "bent", "bending"),
    "bring": ("brought", "brought", "bringing"),
    "catch": ("caught", "caught", "catching"),
    "dig": ("dug", "dug", "digging"),
    "cut": ("cut", "cut", "cutting"),
    "hit": ("hit", "hit", "hitting"),
    "hurt": ("hurt", "hurt", "hurting"),
    "let": ("let", "let", "letting"),
    "put": ("put", "put", "putting"),
    "set": ("set", "set", "setting"),
    "shut": ("shut", "shut", "shutting"),
    "sing": ("sang", "sung", "singing"),
    # Admitted at level two on 2026-10-07. The rule gave `layed`, `rided`,
    # `sended` and `occured`. Occur doubles, so it is classified here.
    "lay": ("laid", "laid", "laying"),
    "lend": ("lent", "lent", "lending"),
    "occur": ("occurred", "occurred", "occurring"),
    "ride": ("rode", "ridden", "riding"),
    "send": ("sent", "sent", "sending"),
    # Admitted at level two on 2026-10-07. The rule gave `striked`.
    "strike": ("struck", "struck", "striking"),
    # `lit` is the past and participle a kindergarten reader meets. The
    # regular `lighted` is correct English and archaic beside it, and the
    # operator's rule is that a verb's inflections are all admitted while
    # its archaic ones need not be. Added 2026-09-26.
    "light": ("lit", "lit", "lighting"),
    "sink": ("sank", "sunk", "sinking"),
    "sleep": ("slept", "slept", "sleeping"),
    "speak": ("spoke", "spoken", "speaking"),
    "spell": ("spelled", "spelled", "spelling"),
    "spill": ("spilled", "spilled", "spilling"),
    "spread": ("spread", "spread", "spreading"),
    "stand": ("stood", "stood", "standing"),
    "steal": ("stole", "stolen", "stealing"),
    "stick": ("stuck", "stuck", "sticking"),
    "swim": ("swam", "swum", "swimming"),
    "swing": ("swung", "swung", "swinging"),
    "take": ("took", "taken", "taking"),
    "teach": ("taught", "taught", "teaching"),
    "tear": ("tore", "torn", "tearing"),
    "tell": ("told", "told", "telling"),
    "think": ("thought", "thought", "thinking"),
    "throw": ("threw", "thrown", "throwing"),
    "undo": ("undid", "undone", "undoing"),
    "understand": ("understood", "understood", "understanding"),
    "wake": ("woke", "woken", "waking"),
    "wear": ("wore", "worn", "wearing"),
    "write": ("wrote", "written", "writing"),
    # Final syllable stressed, so the consonant doubles. Listed rather than
    # derived, because stress is not recoverable from spelling.
    "admit": ("admitted", "admitted", "admitting"),
    "permit": ("permitted", "permitted", "permitting"),
    "prefer": ("preferred", "preferred", "preferring"),
    "quit": ("quit", "quit", "quitting"),
    "refer": ("referred", "referred", "referring"),
    "spend": ("spent", "spent", "spending"),
    # Admitted on 2026-10-28. The rule gave controled, transfered and
    # offseted. Offset also keeps its past unchanged.
    "control": ("controlled", "controlled", "controlling"),
    "offset": ("offset", "offset", "offsetting"),
    "transfer": ("transferred", "transferred", "transferring"),
    # Admitted on 2026-10-28. The rule gave spinned.
    "spin": ("spun", "spun", "spinning"),
    # Admitted on 2026-10-29. The rule gave drived.
    "drive": ("drove", "driven", "driving"),
    # Admitted on 2026-10-30. The rule gave binded, clinged, ridded,
    # transmited and withdrawed.
    "bind": ("bound", "bound", "binding"),
    # Admitted 2026-10-30 in evals/review/level_2_long_tail/.
    "fight": ("fought", "fought", "fighting"),
    "flee": ("fled", "fled", "fleeing"),
    "overcome": ("overcame", "overcome", "overcoming"),
    "submit": ("submitted", "submitted", "submitting"),
    "underlie": ("underlay", "underlain", "underlying"),
    "cling": ("clung", "clung", "clinging"),
    "rid": ("rid", "rid", "ridding"),
    "transmit": ("transmitted", "transmitted", "transmitting"),
    "withdraw": ("withdrew", "withdrawn", "withdrawing"),
    # The regular rule gave beated, broadcasted, bursted, seeked,
    # shooted, splitted and sweared.
    "behold": ("beheld", "beheld", "beholding"),
    "beat": ("beat", "beaten", "beating"),
    "broadcast": ("broadcast", "broadcast", "broadcasting"),
    "burst": ("burst", "burst", "bursting"),
    "seek": ("sought", "sought", "seeking"),
    "shoot": ("shot", "shot", "shooting"),
    "split": ("split", "split", "splitting"),
    "swear": ("swore", "sworn", "swearing"),
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


def doubling_is_ambiguous(word: str) -> bool:
    """True when the word is one whose doubling must be stated, not derived.

    Fires for a verb of more than one syllable ending consonant-vowel-
    consonant. ``_doubles_final`` answers no for every such word, which is
    right for ``visit`` and wrong for ``admit``, so a word this reports must
    appear in :data:`IRREGULAR` or in :data:`NO_DOUBLE_MULTISYLLABIC`.
    """
    if len(word) < 3 or sum(1 for c in word if c in VOWELS) < 2:
        return False
    if not (
        _is_consonant(word[-1])
        and word[-1] not in NO_DOUBLE
        and word[-2] in VOWELS
        and _is_consonant(word[-3])
    ):
        return False
    return word not in IRREGULAR and word not in NO_DOUBLE_MULTISYLLABIC


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


IRREGULAR_COMPARISON: Final[dict[str, tuple[str, str]]] = {
    "good": ("better", "best"),
    "bad": ("worse", "worst"),
    "far": ("further", "furthest"),
    "little": ("less", "least"),
    "many": ("more", "most"),
    "much": ("more", "most"),
    # Adverbs. The compared forms are already headwords of the matching
    # adjectives, so declaring the adverb does not take those surfaces over.
    "well": ("better", "best"),
    "badly": ("worse", "worst"),
}
"""Adjectives and adverbs whose comparison is not derivable from the spelling."""


def comparative(word: str) -> str:
    """The ``-er`` form of a gradable adjective.

    **Adjectives had no mechanism at all until 2026-09-25.** A verb takes
    every inflection from :func:`verb_forms` and a noun its plural from
    :func:`plural`, both enforced, while ``kinder`` and ``kindest`` were
    listed by hand. 299 of the 351 level-one terms carrying no part of
    speech had no comparative, and the teacher was blocked on ``tighter``
    and ``larger`` in a single round.

    **Only declared adjectives get this.** Whether a word is gradable is
    not recoverable from spelling: ``dead`` and ``wooden`` are not, and
    ``beautiful`` compares with more and most rather than a suffix. The
    part of speech says which, exactly as it does for a noun's plural.
    """
    listed = IRREGULAR_COMPARISON.get(word)
    if listed is not None:
        return listed[0]
    return _graded(word, "er", "r")


def superlative(word: str) -> str:
    """The ``-est`` form of a gradable adjective."""
    listed = IRREGULAR_COMPARISON.get(word)
    if listed is not None:
        return listed[1]
    return _graded(word, "est", "st")


def _graded(word: str, suffix: str, after_e: str) -> str:
    if word.endswith("e"):
        return word + after_e
    if word.endswith("y") and len(word) > 1 and _is_consonant(word[-2]):
        return word[:-1] + "i" + suffix
    if _doubles_final(word):
        return word + word[-1] + suffix
    return word + suffix


def comparison(word: str) -> tuple[str, ...]:
    """Both graded forms, without repeats. Empty where both equal the base."""
    out: list[str] = []
    for form in (comparative(word), superlative(word)):
        if form != word and form not in out:
            out.append(form)
    return tuple(out)


INFLECTION_SLOTS: Final[tuple[str, ...]] = (
    "singular",
    "plural",
    "third",
    "past",
    "past_participle",
    "present_participle",
    "comparative",
    "superlative",
)
"""Every slot a registration may name, in a stable order.

A noun has number. A verb has person, tense and the two participles. An
adjective or an adverb has comparison. A slot that does not exist for the
sense is recorded as an empty string, not invented by the spelling rules.
"""


def describe_inflections(
    word: str,
    pos: str,
    registered: Mapping[str, str] | None = None,
) -> tuple[tuple[str, str, str], ...]:
    """Each applicable slot as ``(name, form, origin)``.

    ``form`` is empty when the sense has no such alternate. ``origin`` is
    ``citation``, ``derived``, ``registered`` or ``absent``.

    A registered slot replaces the derived one. An empty registered value
    says the alternate does not exist. ``mass`` is a singular citation form
    with no plural. ``plural-only`` is a plural citation form with no
    singular. ``periphrastic`` compares with more and most. ``ungraded``
    does not compare. A plural equal to the citation form is an invariable
    noun, one spelling for both numbers, and it is not a separate flag.
    """
    recorded = dict(registered or {})
    parts = set(pos.split())
    rows: list[tuple[str, str, str]] = []

    def slot(name: str, derived: str | None, *, citation: bool = False) -> None:
        if name in recorded:
            value = recorded[name]
            if value == "":
                rows.append((name, "", "absent"))
            else:
                rows.append((name, value, "registered"))
            return
        if derived is None:
            rows.append((name, "", "absent"))
            return
        if citation and derived == word:
            rows.append((name, word, "citation"))
            return
        rows.append((name, derived, "derived"))

    if "noun" in parts:
        if "plural-only" in parts:
            slot("singular", None)
            slot("plural", word, citation=True)
        elif "mass" in parts:
            slot("singular", word, citation=True)
            slot("plural", None)
        else:
            slot("singular", word, citation=True)
            slot("plural", plural(word))
    if "verb" in parts:
        slot("third", third_person(word))
        slot("past", past(word))
        slot("past_participle", past_participle(word))
        slot("present_participle", present_participle(word))
    if "adjective" in parts or "adverb" in parts:
        if "periphrastic" in parts or "ungraded" in parts:
            slot("comparative", None)
            slot("superlative", None)
        else:
            slot("comparative", comparative(word))
            slot("superlative", superlative(word))
    return tuple(rows)


def owed_forms(
    word: str,
    pos: str,
    registered: Mapping[str, str] | None = None,
) -> tuple[str, ...]:
    """Distinct alternates that must be admissible, excluding the citation form."""
    out: list[str] = []
    for _name, form, _origin in describe_inflections(word, pos, registered):
        if form and form != word and form not in out:
            out.append(form)
    return tuple(out)


IRREGULAR_PLURAL: Final[dict[str, str]] = {
    "child": "children",
    "foot": "feet",
    "tooth": "teeth",
    # Admitted 2026-10-30 in evals/review/level_2_long_tail/.
    "salmon": "salmon",
    "snowman": "snowmen",
    "tomato": "tomatoes",
    "workman": "workmen",
    "man": "men",
    "woman": "women",
    "mouse": "mice",
    "goose": "geese",
    "person": "people",
    "leaf": "leaves",
    "shelf": "shelves",
    "knife": "knives",
    "life": "lives",
    "wife": "wives",
    "loaf": "loaves",
    "half": "halves",
    "self": "selves",
    # Missing until 2026-09-26, so the lexicon carried `thiefs`. Found by
    # judging the unused surface forms one at a time.
    "thief": "thieves",
    "fish": "fish",
    "sheep": "sheep",
    "deer": "deer",
    "species": "species",
    # Admitted at level two on 2026-10-07. The rule gave `potatos`.
    "potato": "potatoes",
    "axis": "axes",
    # The regular rule gave aircrafts, analysises and gentlemans.
    "aircraft": "aircraft",
    "analysis": "analyses",
    "gentleman": "gentlemen",
    "wolf": "wolves",
    # The regular rule gave nucleuses and phenomenons.
    "nucleus": "nuclei",
    "phenomenon": "phenomena",
    # Admitted at level two on 2026-10-28. The rule gave `volcanos`.
    "volcano": "volcanoes",
    # Admitted at level two on 2026-10-29. The rule gave `hypothesises`.
    "hypothesis": "hypotheses",
    # Admitted at level two on 2026-10-30. The rule gave `basises`,
    # `catfishes` and `shellfishes`.
    "basis": "bases",
    "catfish": "catfish",
    "shellfish": "shellfish",
}
"""Plurals not derivable from spelling. A word mapping to itself has no
distinct plural, which is a fact about the word and not a gap."""


def plural(word: str) -> str:
    """The plural of a noun.

    **A noun admitted without its plural is the same trap as a verb
    admitted without its participle.** Twelve plurals the corpus was
    already using were missing from the lexicon on 2026-09-25 and only
    exact tokenisation found them, because the corpus validator accepts a
    word by stripping suffixes and so never noticed.
    """
    listed = IRREGULAR_PLURAL.get(word)
    if listed is not None:
        return listed
    if word.endswith("y") and len(word) > 1 and _is_consonant(word[-2]):
        return word[:-1] + "ies"
    if word.endswith(("s", "x", "z", "ch", "sh")):
        return word + "es"
    return word + "s"
