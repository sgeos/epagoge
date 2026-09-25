"""Check that documents do not name files which no longer exist.

The reference repository gates on markdown links resolving. This project
almost never writes one. It cross-references by backticked path instead,
429 times against 4 markdown links, so a link checker would have gated on
one percent of the references and reported success over the rest. That is
the silent-partial-coverage shape this project keeps finding in its own
tools, so the check is written against what the documents actually do.

WHAT COUNTS AS A REFERENCE. A backticked token that looks like a path,
meaning it ends in a known extension or a slash. Tokens holding a glob or
a space are skipped, because they are patterns rather than paths.

HOW A REFERENCE RESOLVES, in order. Relative to the directory of the
document naming it, then relative to the repository root, then against the
basename of any tracked file. The third fallback is deliberate and it is
what keeps this check honest rather than noisy: prose says
`validate_graph.py` where the file is `tools/validate_graph.py`, and a
reader follows that without difficulty. What the check is for is a file
that has been renamed or deleted while a document still names it, and a
basename that matches nothing anywhere is exactly that case.

A PATH THE REPOSITORY HAS DECIDED NOT TO TRACK RESOLVES TOO. A document
may name a file that is produced at runtime and deliberately ignored, and
`git check-ignore` answers that question without this file keeping a list
of such paths. A by-name exception list is correct on the day it is
written and silently wrong once the set grows, which is the defect class
this project has now met five times.

CHANGELOG.md IS EXEMPT, and this is a decision rather than an oversight. A
changelog records what was true at a past commit. A file named in an entry
and deleted afterwards makes the entry historical, not wrong, and editing
it to satisfy a checker would falsify the record. The project's rule is
that corrections are kept in place.
"""

from __future__ import annotations

import pathlib
import re
import subprocess  # noqa: S404
import sys
from collections import defaultdict

TOKEN = re.compile(r"`([^`\n]+)`")
LOOKS_LIKE_PATH = re.compile(
    r"^[A-Za-z0-9_][A-Za-z0-9_./-]*(/|\.(md|py|sh|json|jsonl|toml|txt|cff|yml|yaml|pt))$"
)
EXEMPT = frozenset({"CHANGELOG.md"})


def tracked_files() -> list[str]:
    out = subprocess.run(  # noqa: S603
        ["git", "ls-files"],  # noqa: S607
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    return out.split()


def ignored(tokens: list[str]) -> set[str]:
    """The subset of the given paths that the repository ignores.

    Asked in one call rather than one per path, because a subprocess per
    reference would dominate the runtime of the whole check.
    """
    if not tokens:
        return set()
    result = subprocess.run(  # noqa: S603
        ["git", "check-ignore", "--stdin"],  # noqa: S607
        input="\n".join(tokens),
        capture_output=True,
        text=True,
    )
    # Exit 0 means some path matched, 1 means none did, anything else is an
    # error and must not read as "nothing is ignored".
    if result.returncode not in (0, 1):
        raise RuntimeError(f"git check-ignore failed: {result.stderr.strip()}")
    return {line.strip() for line in result.stdout.splitlines() if line.strip()}


def resolves(
    token: str, here: pathlib.Path, root: pathlib.Path, by_base: dict[str, list[str]]
) -> bool:
    """True when the token names something that exists or is tracked.

    A token ending in a slash names a directory, and a directory resolves
    when anything tracked lives under it, which is what makes an empty
    placeholder directory resolve through its own marker file.
    """
    for base in (here, root):
        candidate = base / token
        if candidate.exists():
            return True
    name = pathlib.PurePosixPath(token.rstrip("/")).name
    return bool(by_base.get(name))


def main() -> int:
    root = pathlib.Path()
    tracked = tracked_files()
    by_base: dict[str, list[str]] = defaultdict(list)
    for path in tracked:
        by_base[pathlib.PurePosixPath(path).name].append(path)
        for parent in pathlib.PurePosixPath(path).parents:
            if str(parent) != ".":
                by_base[parent.name].append(path)

    documents = [f for f in tracked if f.endswith(".md") and f not in EXEMPT]
    dead: dict[str, list[str]] = defaultdict(list)
    seen = 0

    for document in documents:
        here = pathlib.Path(document).parent
        text = pathlib.Path(document).read_text(encoding="utf-8")
        for match in TOKEN.finditer(text):
            token = match.group(1).strip()
            if any(c in token for c in "*? ") or not LOOKS_LIKE_PATH.match(token):
                continue
            seen += 1
            if not resolves(token, here, root, by_base):
                dead[token].append(document)

    if dead:
        candidates = [
            str(pathlib.Path(document).parent / token)
            for token, documents_naming in dead.items()
            for document in documents_naming
        ] + list(dead)
        deliberately_ignored = ignored(candidates)
        for token in list(dead):
            paths = {str(pathlib.Path(d).parent / token) for d in dead[token]} | {token}
            if paths & deliberately_ignored:
                del dead[token]

    print(f"  references checked  {seen} over {len(documents)} documents")
    print(f"  exempt              {len(EXEMPT)} ({', '.join(sorted(EXEMPT))})")
    if not dead:
        print("  unresolved          none")
        return 0

    print(f"  unresolved          {sum(len(v) for v in dead.values())}")
    for token in sorted(dead):
        print(f"    {token}")
        for document in sorted(set(dead[token])):
            print(f"        named in {document}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
