"""
Database schema definitions for Project KnowledgeBase.

This module should create the tables needed to store source files,
semantic chunks, embeddings, and graph relationships.  The schema
should mirror the design described in the white paper.  Use SQL
commands within Python to create tables only if they do not already
exist.  Expose a function like `init_db(conn)` that accepts a
`sqlite3.Connection` and creates the schema.
"""

import sqlite3


def init_db(conn: sqlite3.Connection) -> None:
    """Initialise the database schema.

    TODO: Execute SQL statements to create the `source_store`,
    `semantic_chunks`, `relation_graph`, and any other required
    tables.  Commit the changes when done.
    """
    cur = conn.cursor()
    # Example table: adjust columns to suit your needs
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS example (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
        """
    )
    conn.commit()
