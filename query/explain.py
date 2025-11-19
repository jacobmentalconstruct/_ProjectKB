"""
Explanation utilities for Project KnowledgeBase.

This module should take the results of a search and produce human‑readable
responses.  For example, given a list of chunk IDs, fetch the
associated summaries and a few lines of code/text, then compose a
coherent answer for the user or agent.  This is also a good place to
implement formatting logic for citations or code snippets.
"""

from typing import List, Tuple


def explain_results(chunk_ids: List[int]) -> List[Tuple[str, str]]:
    """Turn a list of chunk IDs into (summary, excerpt) tuples."""
import sqlite3
    conn = sqlite3.connect("project_kb.sqlite")
    cur = conn.cursor()
    
    results = []
    for cid in chunk_ids:
cur.execute("SELECT summary, content FROM semantic_chunks WHERE id = ?", (cid,))
row = cur.fetchone()
if row:
summary, content = row
excerpt = content[:300].strip().replace("\n", " ")
results.append((summary, excerpt + ("..." if len(content) > 300 else "")))
return results


