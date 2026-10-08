#!/usr/bin/env python3
"""Verify the installed environment against uv.lock without running uv.

**Why this exists.** `tools/check.sh` begins with `uv sync --locked`. Inside
an agent sandbox that confines writes to the workspace, uv 0.9.5 fails before
it does anything: it writes a marker under its cache in the home directory,
and with a cache moved into the workspace it panics reading the macOS proxy
configuration. Both were observed on 2026-10-07 under the Codex and Claude
Code sandboxes. The gate then stopped before any check ran.

This is the fallback the gate uses when, and only when, uv fails in one of
those two ways. It runs on the project interpreter, reads files only, and
needs neither the network nor the uv cache.

**What it checks.**

1. **The lock is current.** The pinned optional and development requirements
   in `pyproject.toml` equal the requirements the lock recorded for the
   project. This is the property `--locked` exists to enforce.
2. **Every installed distribution is locked.** Each one other than the
   project appears in the lock at exactly the installed version.
3. **Every direct requirement is installed** at its pinned version.

**What it does not check.** It does not walk the lock's dependency graph, so
a missing transitive dependency is not reported here. It would fail the
tests on import instead. Continuous integration runs the real `uv sync`, so
the published revision is always checked the strict way.

    .venv/bin/python tools/check_environment.py
"""

from __future__ import annotations

import re
import tomllib
from importlib import metadata
from pathlib import Path
from typing import cast

ROOT = Path(__file__).resolve().parent.parent

PIN_RE = re.compile(r"^\s*([A-Za-z0-9][A-Za-z0-9._-]*)\s*==\s*([^\s;]+)\s*$")


def normalise(name: str) -> str:
    """The PEP 503 normal form, so `Jinja2` and `jinja2` compare equal."""
    return re.sub(r"[-_.]+", "-", name).lower()


def _pins(requirements: list[str], where: str) -> dict[str, str]:
    """Exact pins from requirement strings. Anything else is refused."""
    pins: dict[str, str] = {}
    for requirement in requirements:
        match = PIN_RE.match(requirement)
        if match is None:
            raise ValueError(f"{where}: {requirement!r} is not an exact pin")
        pins[normalise(match[1])] = match[2]
    return pins


def declared(pyproject_text: str) -> dict[str, str]:
    """Every exact pin the project declares, runtime, extras and groups."""
    raw = cast(dict[str, object], tomllib.loads(pyproject_text))
    project = cast(dict[str, object], raw["project"])
    requirements = list(cast(list[str], project.get("dependencies", [])))
    extras = cast(dict[str, list[str]], project.get("optional-dependencies", {}))
    groups = cast(dict[str, list[str]], raw.get("dependency-groups", {}))
    for listed in [*extras.values(), *groups.values()]:
        requirements.extend(listed)
    return _pins(requirements, "pyproject.toml")


def locked(lock_text: str, project: str) -> tuple[dict[str, str], dict[str, str]]:
    """The lock's package versions, and the pins it recorded for the project."""
    raw = cast(dict[str, object], tomllib.loads(lock_text))
    packages = cast(list[dict[str, object]], raw.get("package", []))
    versions: dict[str, str] = {}
    recorded: dict[str, str] = {}
    for package in packages:
        name = normalise(str(package["name"]))
        if name == normalise(project):
            meta = cast(dict[str, object], package.get("metadata", {}))
            entries = list(cast(list[dict[str, str]], meta.get("requires-dist", [])))
            dev = cast(dict[str, list[dict[str, str]]], meta.get("requires-dev", {}))
            for listed in dev.values():
                entries.extend(listed)
            for entry in entries:
                recorded[normalise(entry["name"])] = entry["specifier"].removeprefix(
                    "=="
                )
            continue
        versions[name] = str(package["version"])
    return versions, recorded


def problems(
    pyproject_text: str, lock_text: str, installed: dict[str, str]
) -> list[str]:
    """Every disagreement between the declaration, the lock and the install."""
    raw = cast(dict[str, object], tomllib.loads(pyproject_text))
    project = str(cast(dict[str, object], raw["project"])["name"])
    pins = declared(pyproject_text)
    versions, recorded = locked(lock_text, project)
    found: list[str] = []
    if pins != recorded:
        found.append(
            f"uv.lock is stale: pyproject.toml pins {sorted(pins.items())} "
            f"and the lock recorded {sorted(recorded.items())}"
        )
    for name, version in sorted(installed.items()):
        if name == normalise(project):
            continue
        if name not in versions:
            found.append(f"{name} {version} is installed and not in uv.lock")
        elif versions[name] != version:
            found.append(f"{name} is {version}, uv.lock has {versions[name]}")
    for name, version in sorted(pins.items()):
        if installed.get(name) != version:
            found.append(
                f"{name}=={version} is required and {installed.get(name)} is installed"
            )
    return found


def main() -> int:
    installed = {
        normalise(dist.metadata["Name"]): dist.version
        for dist in metadata.distributions()
    }
    found = problems(
        (ROOT / "pyproject.toml").read_text(encoding="utf-8"),
        (ROOT / "uv.lock").read_text(encoding="utf-8"),
        installed,
    )
    if found:
        print(f"environment differs from uv.lock in {len(found)} way(s):")
        for line in found:
            print(f"  {line}")
        return 1
    print(
        f"environment matches uv.lock: {len(installed)} installed distributions checked"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
