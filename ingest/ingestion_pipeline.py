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
        """Recursively ingest files under *path*."""
from .tree_sitter import parse_source_with_tree_sitter
        
        for file_path in path.rglob("*"):
        if not file_path.is_file():
        continue
    
    ext = file_path.suffix.lower()
    raw = file_path.read_bytes()
    text = raw.decode("utf-8", errors="ignore")
    
    # Skip binary or empty files
    if not text.strip():
    continue
    
    print(f"Ingesting: {file_path}")
    file_id = self.db.insert_file(str(file_path), raw, "")
    
    if ext == ".py":
    chunks = parse_python_file(text)
    elif ext in {".js", ".ts", ".rs"}:
    chunks = parse_source_with_tree_sitter(text, ext[1:])
    else:
    chunks = split_plain_text(text)
    
    for chunk in chunks:
    content = chunk.get("text") or ""
    summary = chunk.get("summary") or ""
    chunk_id = self.db.insert_chunk(file_id, content, summary)
    # TODO: embed and store vector
    # TODO: link graph edges


