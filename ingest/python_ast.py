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
    """Parse a Python source file and return a list of symbol definitions.

    TODO: Walk the AST and return dictionaries containing details about
    functions, classes, variables, and their relations.  Each dict
    should include the name, start/end lines, docstring summary, and
    any discovered relationships (e.g. calls, modifies).
    """
    tree = ast.parse(source)
    # TODO: visit nodes and build symbol info
    return []
