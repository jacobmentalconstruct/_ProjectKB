"""
Python AST ingestion utilities.

This module should define functions or classes that parse Python files
using the built‑in `ast` module.  The goal is to extract structural
information such as functions, classes, variables, and their
relationships.  Use visitors or node walkers to traverse the AST
selectively and produce a concise representation suitable for
storage in the knowledge base.  Avoid dumping the entire AST; only
capture what is necessary for understanding the code.
"""

import ast
from typing import Iterable, List


def parse_python_file(source: str) -> List[dict]:
    """Parse a Python source file and return a list of symbol definitions."""
tree = ast.parse(source)
    symbols = []
    
    class SymbolVisitor(ast.NodeVisitor):
    def visit_FunctionDef(self, node: ast.FunctionDef):
    symbols.append({
    "type": "function",
    "name": node.name,
    "start_line": node.lineno,
"end_line": getattr(node, "end_lineno", node.lineno),
"docstring": ast.get_docstring(node) or ""
})
self.generic_visit(node)

def visit_ClassDef(self, node: ast.ClassDef):
symbols.append({
"type": "class",
"name": node.name,
"start_line": node.lineno,
"end_line": getattr(node, "end_lineno", node.lineno),
"docstring": ast.get_docstring(node) or ""
})
self.generic_visit(node)

SymbolVisitor().visit(tree)
return symbols


