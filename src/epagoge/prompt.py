"""Generation prompts.

Builds the prompt for one teaching target. Pure and dependency-free so that
what the teacher is asked can be tested without running the teacher.

The shape is set by a finding recorded in ``generators/TEACHER.md``. Asked
to teach that use wears things out, the model returned sentences about
things breaking, which is the adjacent concept the graph deliberately
separates. One negative constraint fixed it. **A prompt therefore carries
the concept, its grounding, and its nearest graph neighbours as explicit
exclusions**, and the graph already holds the neighbours so they are
derived rather than authored.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Final

from epagoge.concept_graph import ConceptGraph

MAX_EXCLUSIONS: Final[int] = 6
"""Cap on neighbours named as exclusions.

A long exclusion list dilutes each entry and lengthens the prompt for no
gain. Six is a guess, not a measurement, and is the number to vary first if
conflation reappears.
"""


@dataclass(frozen=True, slots=True)
class Target:
    """One concept to teach, with everything the prompt needs about it."""

    concept: str
    name: str
    domain: str
    form: str
    primitives: tuple[tuple[str, str], ...] = ()
    """Register id and its observation text, in citation order."""

    exclusions: tuple[str, ...] = ()
    """Neighbour names the content must not drift into."""


def neighbours(graph: ConceptGraph, concept: str) -> list[str]:
    """Concepts near enough to be confused with this one.

    **Prerequisites and siblings only. Not dependents.**

    The recorded conflation was between a concept and its own prerequisite,
    where a record aimed at wearing out taught things breaking instead, so
    prerequisites must be excluded. Siblings sharing a prerequisite are
    coordinate concepts and are confusable for the same reason.

    **Dependents were excluded too and that was wrong.** It was added on
    reasoning rather than on evidence, and the evidence arrived later. A
    dependent is built on the target, so using it to illustrate the target
    is correct teaching rather than drift. Excluding them starved the
    general concepts, because **a general concept is taught through its
    instances and its instances are exactly its dependents**. Material,
    change and sound produced nothing at all in a measured run, each
    carrying five or six exclusions, while concepts carrying one produced
    everything asked of them.

    Ordered nearest first, then alphabetically, so the prompt is stable.
    """
    direct = set(graph.prerequisites_of(concept))
    siblings: set[str] = set()
    for parent in direct:
        siblings.update(
            other
            for other in graph.nodes
            if other != concept and parent in graph.prerequisites_of(other)
        )
    node = graph.nodes.get(concept)
    domain = node.domain if node is not None else None
    ordered: list[str] = []
    for group in (direct, siblings):
        for other in sorted(group):
            candidate = graph.nodes.get(other)
            if candidate is None or candidate.domain != domain:
                continue
            if other not in ordered and other != concept:
                ordered.append(other)
    return ordered[:MAX_EXCLUSIONS]


def target_for(
    graph: ConceptGraph,
    concept: str,
    form: str,
    primitives: Mapping[str, str],
    cited: Sequence[str] = (),
) -> Target:
    """Assemble a target, deriving exclusions from the graph."""
    node = graph.nodes[concept]
    if node.domain is None:
        raise ValueError(f"{concept!r} is a formal structure, not a teachable concept")
    grounding = tuple((p, primitives[p]) for p in cited if p in primitives)
    return Target(
        concept=concept,
        name=node.name,
        domain=node.domain,
        form=form,
        primitives=grounding,
        exclusions=tuple(graph.nodes[n].name for n in neighbours(graph, concept)),
    )


def build(target: Target, level: int, words: Sequence[str], count: int = 3) -> str:
    """Render the prompt.

    ``words`` is the admissible vocabulary at this level. It is supplied in
    full rather than described, because a described constraint is one the
    teacher approximates and a listed one is a constraint it can satisfy.
    """
    if count < 1:
        raise ValueError("count must be at least one")
    if not words:
        raise ValueError("no admissible vocabulary supplied")

    lines = [
        f"Write {count} separate sentences for a reading level {level} corpus.",
        "",
        "THE HARDEST CONSTRAINT IS THE WORD LIST AT THE BOTTOM.",
        "Every word you write must appear in it. Measured on a first run,",
        "29 percent of words fell outside it and no sentence survived.",
        "",
        f"TEACH EXACTLY THIS ONE IDEA: {target.name}.",
        "",
        # The form belongs to the unit, which may cover several concepts, so
        # it can name an idea this target's exclusions forbid. Asking for the
        # voice rather than the content is what keeps the two compatible.
        "Match the voice and reading level of the next line. Do NOT copy its",
        "content, which covers more than the one idea above:",
        f"  {target.form}",
    ]
    if target.primitives:
        # The observations are written for an adult reader and use words the
        # level does not admit. Saying so stops them being read as a style to
        # copy, which is one source of the measured vocabulary drift.
        lines += [
            "",
            "Ground each sentence in one of these observations. They are",
            "written above the reading level on purpose. Take the idea and",
            "not the wording:",
        ]
        lines += [f"  - {text}" for _, text in target.primitives]
    if target.exclusions:
        lines += [
            "",
            "DO NOT write about any of the following. They are different",
            "ideas taught separately, and blurring them is the failure this",
            "prompt exists to prevent:",
        ]
        lines += [f"  - {name}" for name in target.exclusions]
    lines += [
        "",
        "Use ONLY these words, in any order and any inflection:",
        "  " + " ".join(sorted(words)),
        "",
        "Rules:",
        "  - One idea per sentence. No lists, no headings, no numbering.",
        "  - State what is so. Do not address the reader as a teacher would.",
        "  - No word outside the list above.",
        f"  - Output exactly {count} lines and nothing else.",
    ]
    return "\n".join(lines)


def retry(
    target: Target,
    level: int,
    words: Sequence[str],
    rejected: Sequence[str],
    offending: Sequence[str],
    count: int = 3,
) -> str:
    """Re-ask after a rejection, naming the words that caused it.

    A generic repeat of the constraint produces a generic repeat of the
    violation. Naming the specific words converts the instruction from one
    the teacher approximates into one it can act on.
    """
    lines = [
        "Your previous answer was rejected. These sentences were not used:",
    ]
    lines += [f"  {line}" for line in rejected]
    lines += [
        "",
        "They used these words, which are not in the allowed list:",
        "  " + " ".join(sorted(set(offending))),
        "",
        "Write them again using only allowed words. Say the same things more",
        "plainly rather than saying different things.",
        "",
    ]
    return "\n".join(lines) + build(target, level, words, count=count)


def definitions_retry(
    words: Sequence[tuple[str, str]],
    level: int,
    admissible: Sequence[str],
    rejected: Sequence[str],
    offending: Sequence[str],
    substitutions: Mapping[str, str] | None = None,
) -> str:
    """Re-ask for definitions, naming the words that caused the rejection.

    **The dictionary generator asked once and kept what survived.** Measured
    on 2026-09-24 that produced eight admissible definitions from ninety-six
    requests, and four of the last five batches produced none at all. Every
    rejection in the batch that was classified was the same cause, a
    definition reaching outside the level's lexicon.

    The project already measured the remedy on the record generator, where
    a word list gave zero admissible records of twelve and the same list
    with the offending words named gave ten of ten. The finding is that a
    constraint stated in a prompt is a suggestion until something checks it
    and says what failed.
    """
    lines = [
        "Your previous answer was rejected. These entries were not used:",
    ]
    lines += [f"  {line}" for line in rejected]
    lines += [
        "",
        "They used these words, which are NOT in the allowed list:",
        "  " + " ".join(sorted(set(offending))),
        "",
        "Write them again without those words. Say the same thing more",
        "plainly rather than saying a different thing. A shorter definition",
        "that stays inside the list beats an exact one that does not.",
        "",
    ]
    return "\n".join(lines) + definitions(words, level, admissible, substitutions)


BOOK_FORMAT: Final[str] = """SUBJECT: <one sentence saying what this book is about>
WORD <word>: <one sentence saying what that word means>
STORY: <one sentence>"""


def continue_story(
    title: str,
    existing: str,
    count: int,
    level: int,
    admissible: Sequence[str],
) -> str:
    """Ask for the spreads a short book is missing.

    **A book below the standard is unfinished, not wrong.** Regenerating
    it would discard lines that are already true and admissible, so the
    teacher is shown what exists and asked only for the rest.
    """
    if count < 1:
        raise ValueError(f"count must be positive, got {count}")
    if not admissible:
        raise ValueError("no admissible vocabulary supplied")
    lines = [
        f"Here is the start of a picture book for a reader at level {level}.",
        "",
        f"TITLE: {title}",
        "",
        existing,
        "",
        f"Write {count} more sentences that carry the same story forward.",
        "One sentence per line, nothing else. No numbering.",
        "",
        "Use ONLY these words, in any order and any inflection:",
        "  " + " ".join(sorted(admissible)),
        "",
        "Rules:",
        "  - Each sentence is one page of the book, so it must stand alone",
        "    and also follow from the one before.",
        "  - Say what happens. Do not explain what a word means.",
        "  - Do not repeat a sentence that is already above.",
        "  - Every line ends with a full stop.",
    ]
    return "\n".join(lines)


def book(
    subject: str,
    subject_form: str,
    words: Mapping[str, str],
    level: int,
    admissible: Sequence[str],
    sentences: int = 10,
) -> str:
    """Prompt for a whole book in one completion.

    **Sentence-at-a-time prompting produced true, admissible, lifeless
    records**, among them three near-identical lines for one concept.
    Nothing connected one sentence to the next, so the teacher had no reason
    to vary them. Asking for the whole book is what supplies that reason.

    ``words`` maps each word to be defined to the concept that licenses it,
    so the teacher is told what the word is for and not only that it exists.
    """
    if not admissible:
        raise ValueError("no admissible vocabulary supplied")
    if sentences < 1:
        raise ValueError("a book needs at least one story sentence")

    lines = [
        f"Write a short book for a reading level {level} corpus.",
        "",
        "THE HARDEST CONSTRAINT IS THE WORD LIST AT THE BOTTOM.",
        "Every word you write must appear in it.",
        "",
        f"The book is about: {subject_form}",
        "",
        "Write these lines, in this order and in this exact format:",
        "",
        BOOK_FORMAT,
        "",
        "One SUBJECT line. Then one WORD line for each of these words:",
    ]
    lines += [f"  {word}" for word in sorted(words)]
    lines += [
        "",
        f"Then {sentences} STORY lines that tell one story, in order, using",
        "those words. **The story must be one thing happening, not a list of",
        "separate facts.** Each sentence follows from the one before it.",
        "",
        "Use ONLY these words, in any order and any inflection:",
        "  " + " ".join(sorted(admissible)),
        "",
        "Rules:",
        "  - One idea per line. No headings, no numbering, no blank lines.",
        "  - State what is so. Do not address the reader as a teacher would.",
        "  - A definition says what the word means, using the other words.",
        "  - No word outside the list above.",
    ]
    return "\n".join(lines)


def question_book(
    subject: str,
    subject_form: str,
    words: Mapping[str, str],
    level: int,
    admissible: Sequence[str],
    pairs: int = 10,
) -> str:
    """Prompt for a picture book that asks and answers.

    **The corpus could not teach a model to answer because it never showed
    one being answered.** One question mark in 4,419 level-one records and
    no question with an answer after it. A model reproduces the forms it
    was shown, so a corpus that only ever states produces a model that
    only ever continues.

    Operator direction 2026-09-25: the question-and-answer picture book is
    a real form and a rich one for reinforcing a concept, because the
    question names the thing and the answer says it again in other words.

    Each spread is one exchange, because a spread is a page turn and the
    turn is where the answer lands.
    """
    if not admissible:
        raise ValueError("no admissible vocabulary supplied")
    if pairs < 1:
        raise ValueError("a question book needs at least one exchange")

    lines = [
        f"Write a question-and-answer picture book for a reading level {level} corpus.",
        "",
        "THE HARDEST CONSTRAINT IS THE WORD LIST AT THE BOTTOM.",
        "Every word you write must appear in it.",
        "",
        f"The book is about: {subject_form}",
        "",
        "Write these lines, in this order and in this exact format:",
        "",
        "SUBJECT: <one sentence saying what the book is about>",
        "WORD <word>: <what that word means>",
        "ASK: <a question> | <its answer>",
        "",
        "One SUBJECT line. Then one WORD line for each of these words:",
    ]
    lines += [f"  {word}" for word in sorted(words)]
    lines += [
        "",
        f"Then {pairs} ASK lines. Each is a question, then a vertical bar,",
        "then the answer to that question.",
        "",
        "Rules for the ASK lines:",
        "  - The question ends with a question mark.",
        "  - The answer is a full sentence ending with a full stop, and it",
        "    answers the question rather than changing the subject.",
        "  - The answer says the thing again in other words, because that",
        "    is what makes the book teach rather than test.",
        "  - Later questions build on earlier answers.",
        "  - No word outside the list below.",
        "",
        "Use ONLY these words, in any order and any inflection:",
        "  " + " ".join(sorted(admissible)),
    ]
    return "\n".join(lines)


def fill_spread(
    subject_form: str,
    before: str,
    text: str,
    after: str,
    level: int,
    admissible: Sequence[str],
    words: int,
) -> str:
    """Ask for more of one spread, without rewriting what is there.

    **A level-one spread was ten words where the standard is fifty.**
    Measured 2026-09-25 over 227 books: median 164 words a book against a
    band of 320 to 1,280, and every book below it. Filling the spreads
    that exist multiplies the corpus by five without a new book, and
    without the repetition that more books about the same units produces.

    The spreads either side are shown so the addition belongs where it
    lands. The existing sentence is shown and is not to be repeated,
    because the cheapest wrong answer is to say it again slightly
    differently.
    """
    if not admissible:
        raise ValueError("no admissible vocabulary supplied")
    if words < 1:
        raise ValueError("a spread needs at least one word")

    lines = [
        f"Add to one page of a book for a reading level {level} corpus.",
        "",
        "THE HARDEST CONSTRAINT IS THE WORD LIST AT THE BOTTOM.",
        "Every word you write must appear in it.",
        "",
        f"The book is about: {subject_form}",
        "",
    ]
    if before.strip():
        lines += ["The page before says:", f"  {before.strip()}", ""]
    lines += ["This page says:", f"  {text.strip()}", ""]
    if after.strip():
        lines += ["The page after says:", f"  {after.strip()}", ""]
    lines += [
        f"Write about {words} more words for THIS page, carrying on from",
        "what it already says. Do not repeat it and do not write the page",
        "after.",
        "",
        "Use ONLY these words, in any order and any inflection:",
        "  " + " ".join(sorted(admissible)),
        "",
        "Rules:",
        "  - One sentence per line. No headings, no numbering.",
        "  - State what is so. Do not address the reader as a teacher would.",
        "  - Every sentence ends with a full stop and starts with a capital.",
        "  - No word outside the list above.",
    ]
    return "\n".join(lines)


def module_spread(
    topic: str,
    topic_form: str,
    heading: str,
    preceding: str,
    level: int,
    admissible: Sequence[str],
    words: int = 250,
) -> str:
    """Prompt for one spread of a textbook module.

    **A level-two spread is a passage, not a sentence under a picture.** A
    level-one book runs to about two hundred and twenty words in total and
    a level-two module to about sixteen thousand, so one module is seventy
    picture books of text and the unit of generation has to change with it.
    Asking for a whole module in one completion is not available: the
    teacher timed out at twenty-eight sentences.

    So a module is asked for a spread at a time, and ``preceding`` carries
    what came before, because the failure that sentence-at-a-time prompting
    produced at level one was disconnection, and a passage that does not
    follow from the last one is the same failure at a larger size.
    """
    if not admissible:
        raise ValueError("no admissible vocabulary supplied")
    if words < 1:
        raise ValueError("a spread needs at least one word")

    lines = [
        f"Write one spread of a textbook module for a reading level {level}",
        "corpus. The reader is entering fourth grade.",
        "",
        "THE HARDEST CONSTRAINT IS THE WORD LIST AT THE BOTTOM.",
        "Every word you write must appear in it.",
        "",
        f"The module is about: {topic_form}",
        f"This spread is about: {heading}",
        "",
    ]
    if preceding.strip():
        lines += [
            "The spread before this one said:",
            "",
            preceding.strip(),
            "",
            "Carry on from there. Do not repeat it.",
            "",
        ]
    lines += [
        f"Write about {words} words of connected prose, in several",
        "sentences. It is a passage a child reads, not a list and not a",
        "lesson plan.",
        "",
        "Use ONLY these words, in any order and any inflection:",
        "  " + " ".join(sorted(admissible)),
        "",
        "Rules:",
        "  - No headings, no numbering, no bullet points, no blank lines.",
        "  - State what is so. Do not address the reader as a teacher would.",
        "  - Every sentence ends with a full stop and starts with a capital.",
        "  - No word outside the list above.",
        f"  - Output the passage for {topic} and nothing else.",
    ]
    return "\n".join(lines)


def reword(text: str, offending: Sequence[str], admissible: Sequence[str]) -> str:
    """Ask for one sentence again, saying which words cannot be used.

    **A rejected line is not waste.** It is a sentence the teacher wanted to
    write and could not, so either the words belong in the lexicon or the
    sentence needs different words. Rewording is the second of those, and
    naming the offending words is what makes it actionable rather than a
    generic repeat of the constraint.
    """
    if not admissible:
        raise ValueError("no admissible vocabulary supplied")
    return "\n".join(
        [
            "Write this sentence again using different words.",
            "",
            f"  {text}",
            "",
            "These words are not allowed and must not appear:",
            "  " + " ".join(sorted(set(offending))),
            "",
            "Use ONLY these words, in any order and any inflection:",
            "  " + " ".join(sorted(admissible)),
            "",
            "Say the same thing more plainly. Output the one sentence and",
            "nothing else. It must end with a full stop.",
        ]
    )


def definitions(
    words: Sequence[tuple[str, str]],
    level: int,
    admissible: Sequence[str],
    substitutions: Mapping[str, str] | None = None,
) -> str:
    """Prompt for a batch of dictionary entries.

    **This is the self-hosting case.** Each definition must be written in
    the same vocabulary it belongs to, so the level's lexicon has to define
    itself the way a compiler written in its own language has to compile
    itself.

    Batched because related words define each other more consistently when
    the teacher sees them together, and because one call per word would
    spend the whole budget on prompt overhead.
    """
    if not words:
        raise ValueError("no words to define")
    if not admissible:
        raise ValueError("no admissible vocabulary supplied")
    lines = [
        f"Write a dictionary entry for each of these words, at reading level {level}.",
        "",
        "THE HARDEST CONSTRAINT IS THE WORD LIST AT THE BOTTOM.",
        "Every word you write must appear in it. **This is a dictionary that",
        "explains its own words using its own words**, so a definition that",
        "reaches outside the list defeats the purpose of writing it.",
        "",
        "Write one line per word, in this exact format:",
        "",
        "WORD <word>: <one sentence saying what that word means>",
        "",
        "The words, with the idea each one names:",
    ]
    # **One line per sense, not per word.** A word with two senses needs
    # two entries, as any dictionary has, and collapsing them to a mapping
    # silently dropped one.
    lines += [
        f"  {word}  ({concept.replace('_', ' ')})" for word, concept in sorted(words)
    ]
    lines += [
        "",
        "Use ONLY these words, in any order and any inflection:",
        "  " + " ".join(sorted(admissible)),
    ]
    if substitutions:
        # **Naming a banned word is not supplying the replacement.** The
        # retry named every offending word and the teacher reached for it
        # again, and those words overwhelmingly had an ordinary substitute
        # already admitted. An instruction to avoid something is harder to
        # act on than one that says what to write instead.
        lines += [
            "",
            "These words are NOT allowed. Write the replacement instead:",
        ]
        lines += [
            f'  {banned}  ->  write "{instead}"'
            for banned, instead in sorted(substitutions.items())
        ]
    lines += [
        "",
        "Rules:",
        "  - Say what the word means. Do not give an example instead.",
        "  - A word may appear in its own definition, as in a dictionary.",
        "  - Prefer simpler words even where a longer one would be exact.",
        "  - Every line ends with a full stop. No other output.",
    ]
    return "\n".join(lines)
