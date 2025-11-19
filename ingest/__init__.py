"""
Ingestion package for Project KnowledgeBase.

This package contains modules responsible for parsing and extracting
information from various file types.  Each submodule implements a
parser for a specific language or format.  For example, `python_ast`
handles Python files by walking the AST, while `tree_sitter` could
support multiple languages via the Tree‑sitter library.  Fallback
parsers live in `heuristics` for handling plain text or unknown
formats.
"""
