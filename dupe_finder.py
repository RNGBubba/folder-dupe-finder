"""Find duplicate regular files by content hash."""

from __future__ import annotations

import argparse
import hashlib
from collections import defaultdict
from pathlib import Path
from typing import Iterable

_CHUNK_SIZE = 1024 * 1024


def _iter_files(root: Path) -> Iterable[Path]:
    """Yield regular files below root in deterministic relative-path order."""
    if root.is_file():
        yield root
        return
    if not root.is_dir():
        raise ValueError(f"not a directory or file: {root}")
    yield from sorted(
        (path for path in root.rglob("*") if path.is_file() and not path.is_symlink()),
        key=lambda path: path.relative_to(root).as_posix(),
    )


def _file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(_CHUNK_SIZE), b""):
            digest.update(chunk)
    return digest.hexdigest()


def find_duplicates(root: Path | str) -> list[list[Path]]:
    """Return groups of files sharing identical contents.

    Groups contain at least two paths and, like the paths within each group,
    are sorted by their first path. Files are streamed in chunks so large files
    do not need to fit in memory.
    """
    root = Path(root)
    by_size: dict[int, list[Path]] = defaultdict(list)
    for path in _iter_files(root):
        by_size[path.stat().st_size].append(path)

    groups: list[list[Path]] = []
    for candidates in by_size.values():
        by_hash: dict[str, list[Path]] = defaultdict(list)
        if len(candidates) > 1:
            for path in candidates:
                by_hash[_file_hash(path)].append(path)
        groups.extend(
            sorted((sorted(paths) for paths in by_hash.values() if len(paths) > 1), key=lambda paths: paths[0])
        )
    return sorted(groups, key=lambda paths: paths[0])


def main() -> int:
    parser = argparse.ArgumentParser(description="Find duplicate files by content hash.")
    parser.add_argument("directory", type=Path, help="directory to scan recursively")
    args = parser.parse_args()
    try:
        groups = find_duplicates(args.directory)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    for group in groups:
        print("\n".join(str(path) for path in group))
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
