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
    # Table for storing raw source files
        cur.execute(
        """
            CREATE TABLE IF NOT EXISTS source_store (
            id INTEGER PRIMARY KEY,
        path TEXT NOT NULL,
        content BLOB,
    hash TEXT
    )
    """
    )
    
    # Table for storing semantic chunks from source files
    cur.execute(
    """
    CREATE TABLE IF NOT EXISTS semantic_chunks (
    id INTEGER PRIMARY KEY,
    file_id INTEGER NOT NULL,
    content TEXT,
    summary TEXT,
    FOREIGN KEY (file_id) REFERENCES source_store(id)
    )
    """
    )
    
    # Table for vector embeddings
    cur.execute(
    """
    CREATE TABLE IF NOT EXISTS embeddings (
    chunk_id INTEGER PRIMARY KEY,
    vector BLOB,
    FOREIGN KEY (chunk_id) REFERENCES semantic_chunks(id)
    )
    """
    )
    
    # Table for graph relations between chunks (call, import, etc)
    cur.execute(
    """
    CREATE TABLE IF NOT EXISTS relation_graph (
    from_id INTEGER NOT NULL,
    to_id INTEGER NOT NULL,
    type TEXT,
    FOREIGN KEY (from_id) REFERENCES semantic_chunks(id),
    FOREIGN KEY (to_id) REFERENCES semantic_chunks(id)
    )
    """
    )
    conn.commit()


