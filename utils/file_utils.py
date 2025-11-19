"""
File utilities for Project KnowledgeBase.

Provide functions to recursively discover files, compute file hashes,
read file contents, and handle inclusion/exclusion patterns.  These
helpers should be used by the ingestion pipeline to determine which
files to process.
"""

from pathlib import Path
from typing import Iterable, List


def discover_files(root: Path, extensions: Iterable[str]) -> List[Path]:
    """Return a list of files under *root* matching the given extensions.

    TODO: Implement recursive traversal that skips excluded directories
    and files.  Use `Path.rglob` or similar functions to find
    candidate files.
    """
    return []
