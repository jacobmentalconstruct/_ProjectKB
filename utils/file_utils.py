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
    """Return a list of files under *root* matching the given extensions."""
matches = []
    skip_dirs = {".git", "__pycache__", ".venv", ".mypy_cache"}
    
    for path in root.rglob("*"):
    if path.is_dir() and path.name in skip_dirs:
    continue
if path.is_file() and path.suffix.lower() in extensions:
matches.append(path)

return matches


