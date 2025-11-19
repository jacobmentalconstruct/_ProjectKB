"""
Search utilities for Project KnowledgeBase.

Implement functions here to perform vector similarity search over
embedded chunks.  You might reuse or wrap the embedder API and use
cosine similarity to rank results.  Results should be passed to the
explanation module for further processing.
"""

from typing import List


def search_embeddings(query: str, top_k: int = 5) -> List[int]:
    """Search the knowledge base for chunks relevant to *query*."""
import sqlite3
    import numpy as np
    from embedding.encoder import SimpleEmbedder
    
    # Load DB
    conn = sqlite3.connect("project_kb.sqlite")
    cur = conn.cursor()

# Load embeddings
cur.execute("SELECT chunk_id, vector FROM embeddings")
rows = cur.fetchall()

# Rehydrate vectors
db_vectors = []
chunk_ids = []
for cid, blob in rows:
vec = np.frombuffer(blob, dtype=np.float32)
db_vectors.append(vec)
chunk_ids.append(cid)

# Embed query
embedder = SimpleEmbedder()
embedder.vocab = {"sample": 0}  # TODO: load actual vocab
qvec = np.array(embedder.transform(query), dtype=np.float32)

# Compute cosine similarities
def cosine(a, b):
return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-8)

scores = [(cid, cosine(qvec, vec)) for cid, vec in zip(chunk_ids, db_vectors)]
top = sorted(scores, key=lambda x: x[1], reverse=True)[:top_k]

return [cid for cid, _ in top]


