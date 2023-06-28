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
