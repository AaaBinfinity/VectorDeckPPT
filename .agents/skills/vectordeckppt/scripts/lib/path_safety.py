from __future__ import annotations

import os
from collections.abc import Iterable, Mapping
from itertools import combinations
from pathlib import Path

type PathLike = str | os.PathLike[str]


class PathSafetyError(ValueError):
    """Raised when an output path could overwrite an input or uses the wrong file type."""


def require_suffix(
    path: PathLike,
    suffixes: str | Iterable[str],
    *,
    label: str,
) -> Path:
    """Resolve *path* and require one of *suffixes* for a writable file target."""

    candidate = Path(path).expanduser()
    normalized = _normalize_suffixes(suffixes)
    if candidate.suffix.lower() not in normalized:
        expected = ", ".join(sorted(normalized))
        raise PathSafetyError(f"{label} must use one of these extensions: {expected}")

    resolved = candidate.resolve()
    if resolved.exists() and resolved.is_dir():
        raise PathSafetyError(f"{label} must be a file path, not a directory: {resolved}")
    return resolved


def paths_refer_to_same_file(first: PathLike, second: PathLike) -> bool:
    """Return whether two paths resolve to, or already identify, the same file."""

    first_path = Path(first).expanduser().resolve()
    second_path = Path(second).expanduser().resolve()
    if first_path == second_path:
        return True
    if not first_path.exists() or not second_path.exists():
        return False
    try:
        return os.path.samefile(first_path, second_path)
    except OSError:
        return False


def ensure_distinct_paths(paths: Mapping[str, PathLike]) -> dict[str, Path]:
    """Resolve named paths and reject any pair that identifies the same file."""

    resolved = {name: Path(path).expanduser().resolve() for name, path in paths.items()}
    for (first_name, first_path), (second_name, second_path) in combinations(
        resolved.items(), 2
    ):
        if paths_refer_to_same_file(first_path, second_path):
            raise PathSafetyError(
                f"{first_name} and {second_name} must refer to different files: {first_path}"
            )
    return resolved


def _normalize_suffixes(suffixes: str | Iterable[str]) -> set[str]:
    values = [suffixes] if isinstance(suffixes, str) else list(suffixes)
    normalized = {
        value.lower() if value.startswith(".") else f".{value.lower()}" for value in values
    }
    if not normalized:
        raise ValueError("At least one output extension is required")
    return normalized
