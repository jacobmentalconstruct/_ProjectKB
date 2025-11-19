"""
Central ingestion pipeline for Project KnowledgeBase.

Orchestrates scanning, parsing, embedding, and storage.
Implements a fallback hierarchy: 
1. Surgical AST (Python)
2. Tree-sitter CST (Other Code)
3. Text Heuristics (Docs/Fallback)
"""

from pathlib import Path
import logging

from ..db.interface import KnowledgeBaseDB
from ..embedding.encoder import OllamaEmbedder
# from ..graph.link_builder import build_links # (Optional: use if you want post-processing)
from .python_ast import parse_python_file
from .heuristics import split_plain_text
from .tree_sitter import parse_source_with_tree_sitter

class IngestionPipeline:
    def __init__(self, db: KnowledgeBaseDB) -> None:
        self.db = db
        self.embedder = OllamaEmbedder() # Now uses the real Ollama wrapper
        self.logger = logging.getLogger("ingest")

    def ingest_directory(self, path: Path) -> None:
        """Recursively ingest files under *path*."""
        path_obj = Path(path)
        
        if not path_obj.exists():
            print(f"Error: Path {path} does not exist.")
            return

        for file_path in path_obj.rglob("*"):
            if not file_path.is_file():
                continue
            
            # Basic exclusion of hidden files/directories
            if any(part.startswith('.') for part in file_path.parts):
                continue

            ext = file_path.suffix.lower()
            
            try:
                raw = file_path.read_bytes()
                text = raw.decode("utf-8", errors="ignore")
            except Exception as e:
                print(f"Skipping binary/unreadable: {file_path.name}")
                continue
            
            # Skip empty files
            if not text.strip():
                continue
            
            print(f"Ingesting: {file_path.relative_to(path_obj)}")
            
            # 1. Insert File Record
            file_id = self.db.insert_file(str(file_path), raw, "")
            
            chunks = []
            
            # ---------------------------------------------------------
            # PARSING HIERARCHY
            # ---------------------------------------------------------
            
            # TIER 1: Surgical Python AST
            if ext == ".py":
                try:
                    chunks = parse_python_file(text)
                    if not chunks:
                        # If AST yields nothing (e.g. empty __init__), strictly no error, just empty
                        pass
                except Exception as e:
                    print(f"⚠️  AST Error in {file_path.name}: {e}. Falling back to text.")
                    chunks = split_plain_text(text)

            # TIER 2: Tree-sitter (CST)
            elif ext in {".js", ".ts", ".rs", ".go", ".cpp", ".java"}:
                try:
                    # Remove the dot from extension for language code
                    chunks = parse_source_with_tree_sitter(text, ext[1:])
                except Exception:
                    # Silently fall back if tree-sitter isn't configured
                    chunks = split_plain_text(text)

            # TIER 3: Heuristics (Docs, configs, fallback)
            else:
                chunks = split_plain_text(text)
            
            # ---------------------------------------------------------
            # PROCESSING LOOP
            # ---------------------------------------------------------
            
            for chunk in chunks:
                # Determine content for embedding (Docs > Code Body > Summary)
                # We prioritize the actual code or docstring for the vector.
                content = chunk.get("text") or chunk.get("docstring") or ""
                
                # If a chunk is just metadata (like our 'module_context'), ensure it has text
                if not content and "summary" in chunk:
                    content = chunk["summary"]

                # Create a readable summary for the Agent's UI
                # Format: "[Function] my_func | Calls: a, b"
                name = chunk.get("name", "unnamed")
                kind = chunk.get("type", "text")
                meta_summary = f"[{kind}] {name}"
                
                if "calls" in chunk and chunk["calls"]:
                    meta_summary += f" | Calls: {', '.join(chunk['calls'][:3])}..."

                # INSERT CHUNK
                chunk_id = self.db.insert_chunk(file_id, content, meta_summary)
                
                # GENERATE & INSERT EMBEDDING
                if content.strip():
                    vector = self.embedder.transform(content)
                    if vector:
                        self.db.insert_embedding(chunk_id, vector)

                # INSERT RELATIONS (GRAPH EDGES)
                # This populates the 'Connective Tissue' of your RAG
                if "calls" in chunk:
                    for target_function in chunk["calls"]:
                        # We store the edge: (CurrentChunk) --calls--> (TargetName)
                        # Note: target_name is a string string right now. 
                        # Post-processing (Link Builder) usually resolves this to an ID, 
                        # but storing the raw string relation allows fuzzy matching later.
                        self.db.insert_relation(chunk_id, target_function, "calls")