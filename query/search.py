"""
Search utilities for Project KnowledgeBase.

Implement functions here to perform vector similarity search over
embedded chunks.  You might reuse or wrap the embedder API and use
cosine similarity to rank results.  Results should be passed to the
explanation module for further processing.
"""

from typing import List


def search_embeddings(query: str, top_k: int = 5) -> List[int]:
    """Search the knowledge base for chunks relevant to *query*.

    TODO: Tokenise and embed the query, compute similarities against
    stored embeddings, and return a list of chunk IDs sorted by
    relevance.  Use a vector search algorithm such as brute‑force
    cosine similarity for now.
    """
    return []
