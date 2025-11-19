"""
Central ingestion pipeline for Project KnowledgeBase.

This module orchestrates the scanning of directories, determination of
file types, and delegation to the appropriate ingestion routines.  It
should handle deduplication, call the summariser and embedder, and
write results to the database via the interface layer.  The pipeline
should also record relationships discovered during parsing.
"""

from pathlib import Path
from typing import Iterable

from ..db.interface import KnowledgeBaseDB
from .python_ast import parse_python_file
from .heuristics import split_plain_text


class IngestionPipeline:
    """High‑level ingestion workflow.

    TODO: Walk through all files in a project, determine which parser
    to invoke based on file extension, collect the output, call a
    summariser, generate embeddings, and write everything to the
    knowledge base via the `KnowledgeBaseDB` instance provided.
    """

    def __init__(self, db: KnowledgeBaseDB) -> None:
        self.db = db

    def ingest_directory(self, path: Path) -> None:
        """Recursively ingest files under *path*.

        TODO: Use `Path.rglob` to find files, apply the correct parser,
        summarise each chunk, generate an embedding, and store results.
        """
        pass
