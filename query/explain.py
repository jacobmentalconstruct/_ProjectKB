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
    """Turn a list of chunk IDs into explanations.

    TODO: Look up each chunk's summary and snippet and return a list
    of tuples `(summary, excerpt)`.  Format these in a way that is
    useful for consumption by agents or end users.
    """
    return []
