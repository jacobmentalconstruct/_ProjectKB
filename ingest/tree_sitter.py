"""
Tree‑sitter ingestion utilities.

This module should provide an interface for parsing files using the
Tree‑sitter library.  Tree‑sitter produces concrete syntax trees for
many languages and can be used to extract similar information to what
`python_ast` provides for Python.  You will need to install and
configure Tree‑sitter languages separately.
"""

def parse_source_with_tree_sitter(source: str, language: str) -> list:
    """Parse source text using Tree‑sitter.

    TODO: Use the appropriate Tree‑sitter parser for the given
    language and return a representation of the file's structure.
    """
    raise NotImplementedError
