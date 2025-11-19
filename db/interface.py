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
        """Insert a file into the source_store table.

        TODO: implement and return the new file's ID.
        """
        raise NotImplementedError

    # Additional methods to be defined...
