"""
Text embedding utilities using Ollama.
"""
import requests
from typing import List

class OllamaEmbedder:
    def __init__(self, model: str = "nomic-embed-text"):
        self.model = model
        self.api_url = "http://localhost:11434/api/embeddings"

    def transform(self, document: str) -> List[float]:
        """Generate embeddings via Ollama API."""
        try:
            response = requests.post(self.api_url, json={
                "model": self.model,
                "prompt": document
            })
            response.raise_for_status()
            return response.json()["embedding"]
        except Exception as e:
            print(f"Error embedding chunk: {e}")
            return []

    def fit(self, documents: List[str]) -> None:
        # Stateless models don't need fitting
        pass