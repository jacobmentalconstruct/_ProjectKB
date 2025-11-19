"""
Python AST ingestion utilities.
Extracts high-level structure (imports, globals, functions, classes) 
and call graphs without dumping low-level syntax trees.
"""
import ast
from typing import List, Dict, Any

def parse_python_file(source: str) -> List[dict]:
    """
    Parse Python source into a list of 'Symbol' dictionaries.
    Each symbol represents a chunk of code (Function, Class, or Module-level summary).
    """
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []

    visitor = SurgicalVisitor()
    visitor.visit(tree)
    return visitor.symbols

class SurgicalVisitor(ast.NodeVisitor):
    def __init__(self):
        self.symbols = []
        # Track imports and globals to add to the "Module" summary later
        self.imports = []
        self.globals = []

    def visit_Import(self, node):
        for alias in node.names:
            self.imports.append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        module = node.module or ""
        for alias in node.names:
            self.imports.append(f"{module}.{alias.name}")
        self.generic_visit(node)

    def visit_Assign(self, node):
        # Only capture top-level (Global) assignments
        # If it's inside a function/class, we ignore it to reduce noise.
        if getattr(node, 'col_offset', 0) == 0: 
            for target in node.targets:
                if isinstance(target, ast.Name):
                    self.globals.append(target.id)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        self._handle_func_or_method(node, "function")

    def visit_AsyncFunctionDef(self, node):
        self._handle_func_or_method(node, "async_function")

    def visit_ClassDef(self, node):
        # 1. Capture the Class itself
        self.symbols.append({
            "type": "class",
            "name": node.name,
            "start_line": node.lineno,
            "end_line": getattr(node, "end_lineno", node.lineno),
            "docstring": ast.get_docstring(node) or "",
            "bases": [b.id for b in node.bases if isinstance(b, ast.Name)]
        })
        # 2. Continue visiting children to catch methods
        self.generic_visit(node)

    def _handle_func_or_method(self, node, type_name):
        # EXTRACT CALLS: Scan the body of this function to see who it talks to.
        # This creates the "Graph" edges.
        calls = []
        for child in ast.walk(node):
            if isinstance(child, ast.Call):
                if isinstance(child.func, ast.Name):
                    calls.append(child.func.id)
                elif isinstance(child.func, ast.Attribute):
                    calls.append(child.func.attr)
        
        # Deduplicate calls
        calls = list(set(calls))

        self.symbols.append({
            "type": type_name,
            "name": node.name,
            "start_line": node.lineno,
            "end_line": getattr(node, "end_lineno", node.lineno),
            "docstring": ast.get_docstring(node) or "",
            "calls": calls,  # <--- The Agent uses this to know "Who does X connect to?"
            "args": [a.arg for a in node.args.args] # Useful to see inputs
        })

    def visit_Module(self, node):
        # Visit all children first to populate imports/globals/symbols
        self.generic_visit(node)
        
        # Add a "File Summary" symbol at the very start of the list
        # This helps the agent understand the file's context before reading functions
        if self.imports or self.globals:
            self.symbols.insert(0, {
                "type": "module_context",
                "name": "__file_context__",
                "start_line": 1,
                "end_line": 1,
                "text": f"Imports: {', '.join(self.imports)}\nGlobals: {', '.join(self.globals)}",
                "summary": "Module imports and global variables"
            })