"""
Database interface for Project KnowledgeBase.

This module should provide a convenient API for working with the
knowledge base.  Examples include inserting files, chunks, and
relations; querying for chunks; and wrapping SQL queries behind
friendly function calls.  The goal is to abstract away raw SQL so
other parts of the application can remain agnostic of the database
backend.
"""

import sqlite3
from typing import Any, Iterable, Optional


class KnowledgeBaseDB:
    """High‑level interface for interacting with the knowledge base.

    TODO: implement methods such as `insert_file`, `insert_chunk`,
    `insert_relation`, `search_chunks`, etc.  These methods should
    call SQL statements on a provided `sqlite3.Connection`.
    """

    def __init__(self, conn: sqlite3.Connection) -> None:
        self.conn = conn
        # Perhaps initialise the schema here

    def insert_file(self, path: str, content: bytes, hash_value: str) -> int:
        """Insert a file into the source_store table."""
cur = self.conn.cursor()
        cur.execute(
        """
        INSERT INTO source_store (path, content, hash)
    VALUES (?, ?, ?)
    """,
    (path, content, hash_value)
    )
    self.conn.commit()
    return cur.lastrowid

    def insert_chunk(self, file_id: int, content: str, summary: str) -> int:
    """Insert a semantic chunk and return its ID."""
    cur = self.conn.cursor()
    cur.execute(
    """
    INSERT INTO semantic_chunks (file_id, content, summary)
    VALUES (?, ?, ?)
    """,
    (file_id, content, summary)
    )
    self.conn.commit()
    return cur.lastrowid
    
    def search_chunks_by_keyword(self, keyword: str) -> Iterable[str]:
    """Search chunks that contain a keyword."""
    cur = self.conn.cursor()
    cur.execute(
    """
    SELECT summary FROM semantic_chunks
    WHERE content LIKE ?
    """,
    (f"%{keyword}%",)
    )
    return [row[0] for row in cur.fetchall()]

    def insert_embedding(self, chunk_id: int, vector: list[float]) -> None:
            import struct
            # Pack list of floats into binary data
            blob = struct.pack(f'{len(vector)}f', *vector)
            
            cur = self.conn.cursor()
            cur.execute(
                "INSERT OR REPLACE INTO embeddings (chunk_id, vector) VALUES (?, ?)",
                (chunk_id, blob)
            )
            self.conn.commit()


