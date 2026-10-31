"""Compare a generated JSON file in the working tree with a git revision, by key.

The worker line asked for this after the sixth trial, where regenerating
provenance silently rewrote three existing records. Dict entries are compared
by key, and lists of records by a key built from the named fields, so that a
reordering is not reported as a change. Only added, removed and changed keys
are printed, each with its old and new value truncated to one line.

    python3 tmp/dromon-trial-8/keydiff.py curriculum/provenance.json words senses
    python3 tmp/dromon-trial-8/keydiff.py curriculum/vocabulary.json terms=word,concept
    python3 tmp/dromon-trial-8/keydiff.py FILE SECTION --rev aae4abe --changed-only

Exit status is 0 whatever the differences, and 2 on a usage or git error.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

WIDTH = 160


def one_line(value: object) -> str:
    text = json.dumps(value, sort_keys=True, ensure_ascii=False)
    return text if len(text) <= WIDTH else text[: WIDTH - 3] + "..."


def keyed(section: object, fields: list[str]) -> dict[str, object]:
    if isinstance(section, dict):
        return {str(k): v for k, v in section.items()}
    if isinstance(section, list):
        if not fields:
            raise SystemExit("a list section needs key fields, as terms=word,concept")
        out: dict[str, object] = {}
        for record in section:
            key = ".".join(str(record.get(f)) for f in fields)
            if key in out:
                key = f"{key}#dup{sum(1 for k in out if k.startswith(key))}"
            out[key] = record
        return out
    return {"(value)": section}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    parser.add_argument(
        "sections", nargs="+", help="NAME or NAME=field,field for a list"
    )
    parser.add_argument("--rev", default="HEAD")
    parser.add_argument("--changed-only", action="store_true")
    args = parser.parse_args()
    try:
        old_text = subprocess.run(  # noqa: S603
            ["git", "show", f"{args.rev}:{args.file}"],  # noqa: S607
            check=True,
            capture_output=True,
            text=True,
        ).stdout
    except subprocess.CalledProcessError as err:
        print(err.stderr.strip(), file=sys.stderr)
        return 2
    old_doc = json.loads(old_text)
    with Path(args.file).open(encoding="utf-8") as handle:
        new_doc = json.load(handle)
    for spec in args.sections:
        name, _, field_text = spec.partition("=")
        fields = [f for f in field_text.split(",") if f]
        old = keyed(old_doc.get(name, {}), fields)
        new = keyed(new_doc.get(name, {}), fields)
        added = sorted(set(new) - set(old))
        removed = sorted(set(old) - set(new))
        changed = sorted(k for k in set(old) & set(new) if old[k] != new[k])
        print(
            f"== {args.file} {name} against {args.rev}: "
            f"{len(added)} added, {len(removed)} removed, {len(changed)} changed"
        )
        for key in changed:
            print(
                f"~ {key}\n    old {one_line(old[key])}\n    new {one_line(new[key])}"
            )
        for key in removed:
            print(f"- {key} {one_line(old[key])}")
        if not args.changed_only:
            for key in added:
                print(f"+ {key} {one_line(new[key])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
