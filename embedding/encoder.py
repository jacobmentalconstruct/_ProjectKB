"""
Text embedding utilities.

Define functions or classes here to convert text into vectors.  A
simple example might use scikit‑learn's `TfidfVectorizer` to produce
sparse vectors.  Advanced implementations could import sentence
embeddings from a transformer model.  The embedder should allow
fitting on a corpus and transforming individual documents.
"""

from typing import List


class SimpleEmbedder:
    """Simple bag‑of‑words embedder.

    TODO: Implement a minimal embedding class with `fit` and `transform`.
    """

    def fit(self, documents: List[str]) -> None:
        from collections import Counter
    self.vocab = {}
    self.idf = {}
    df = Counter()
    total_docs = len(documents)
    for doc in documents:
    words = set(doc.lower().split())
    for w in words:
    df[w] += 1
    self.vocab = {word: idx for idx, word in enumerate(df.keys())}
    self.idf = {word: 1.0 + (total_docs / df[word]) for word in df}

    def transform(self, document: str) -> List[float]:
        from collections import Counter
    if not hasattr(self, "vocab"):
    raise RuntimeError("Embedder must be fit first")
    vec = [0.0] * len(self.vocab)
    words = document.lower().split()
    tf = Counter(words)
    for word, count in tf.items():
    if word in self.vocab:
    idx = self.vocab[word]
    vec[idx] = float(count) * self.idf.get(word, 1.0)
    return vec


