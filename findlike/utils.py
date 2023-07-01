from __future__ import annotations

from typing import Iterable, Any
from pathlib import Path


def try_read_file(filename: Path) -> str | None:
    with filename.open() as f:
        try:
            document = f.read()
        except UnicodeDecodeError:
            document = None
    return document


def compress(data: Iterable[Any], selectors: Iterable[Any]) -> list[Any]:
    return [d for d, s in zip(data, selectors) if s]


def collect_paths(
    directory: Path, extensions: list[str], recursive: bool = False
) -> list[Path]:
    """ Collects file paths in a directory that match the given extensions.

    Args:
        directory (Path): The directory to search in.
        extensions (list[str]): A list of file extensions to search for. The
            extensions should not contain asterisks nor dots. Example: "txt"
        recursive (bool, optional): Whether to search for files in
            subdirectories as well. Defaults to False.

    Returns:
        list[Path]: A list of paths to the matching files.
    """
    glob_func = directory.rglob if recursive else directory.glob
    paths = [
        x for ext in extensions for x in glob_func(ext) if x.is_file()
    ]
    return paths

