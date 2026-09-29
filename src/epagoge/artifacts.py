"""Exclusive output publication and deterministic run identifiers."""

from __future__ import annotations

import hashlib
import json
import os
import platform
import sys
import tempfile
from collections.abc import Generator
from contextlib import contextmanager
from importlib.metadata import distributions
from pathlib import Path
from typing import BinaryIO, cast


def digest(value: object) -> str:
    return hashlib.sha256(
        json.dumps(
            value, sort_keys=True, separators=(",", ":"), allow_nan=False
        ).encode()
    ).hexdigest()


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def environment() -> dict[str, str]:
    return dict(sorted((d.metadata["Name"], d.version) for d in distributions()))


def check_outputs(paths: list[Path], *, overwrite: bool = False) -> None:
    resolved = [p.resolve() for p in paths]
    if len(set(resolved)) != len(resolved):
        raise ValueError("output paths must be distinct")
    for path in paths:
        if path.is_symlink() or (
            path.exists() and (not overwrite or not path.is_file())
        ):
            raise FileExistsError(f"refusing to replace {path}")


@contextmanager
def atomic_output(
    path: Path, *, overwrite: bool = False
) -> Generator[BinaryIO, None, None]:
    """Publish only complete artifacts and refuse races with existing outputs."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=path.parent, delete=False) as handle:
        temporary = Path(handle.name)
        try:
            yield cast(BinaryIO, handle.file)
            handle.flush()
            os.fsync(handle.fileno())
            handle.close()
            if overwrite:
                if path.is_symlink():
                    raise FileExistsError(f"refusing to replace symlink {path}")
                temporary.replace(path)
            else:
                # Linking publishes atomically and fails if another writer won.
                os.link(temporary, path)
        finally:
            temporary.unlink(missing_ok=True)


def write_json(path: Path, value: object, *, overwrite: bool = False) -> None:
    with atomic_output(path, overwrite=overwrite) as handle:
        handle.write((json.dumps(value, indent=2, allow_nan=False) + "\n").encode())


def input_manifest(root: Path, level: int) -> dict[str, object]:
    """Hash the authored inputs and executable sources, excluding private files."""
    books = sorted((root / f"curriculum/books/level_{level}").glob("*.md"))
    code = sorted((root / "src").rglob("*.py")) + sorted((root / "tools").glob("*.py"))
    files = (
        books
        + code
        + [
            root / "curriculum/vocabulary.json",
            root / "curriculum/graph/concepts.json",
            root / f"curriculum/schedule/level_{level:02d}.json",
            root / "pyproject.toml",
            root / "uv.lock",
        ]
    )
    hashes = {str(p.relative_to(root)): file_digest(p) for p in files}
    return {
        "schema": 1,
        "inputs": hashes,
        "corpus_hash": digest(
            {str(p.relative_to(root)): hashes[str(p.relative_to(root))] for p in books}
        ),
        "graph_hash": hashes["curriculum/graph/concepts.json"],
        "environment": environment(),
        "python": sys.version,
        "platform": platform.platform(),
    }
