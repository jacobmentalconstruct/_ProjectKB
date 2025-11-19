"""
Tree‑sitter ingestion utilities.

This module should provide an interface for parsing files using the
Tree‑sitter library.  Tree‑sitter produces concrete syntax trees for
many languages and can be used to extract similar information to what
`python_ast` provides for Python.  You will need to install and
configure Tree‑sitter languages separately.
"""

def parse_source_with_tree_sitter(source: str, language: str) -> list:
    """Parse source text using Tree‑sitter and return a list of symbols."""
from tree_sitter import Parser
    from tree_sitter_languages import get_language
    
    try:
    ts_lang = get_language(language)
except Exception:
raise ValueError(f"Unsupported language for Tree-sitter: {language}")

parser = Parser()
parser.set_language(ts_lang)
tree = parser.parse(bytes(source, "utf8"))
root_node = tree.root_node

def extract_symbols(node):
symbols = []
for child in node.children:
if child.type in ("function", "function_definition", "method_definition", "class", "class_declaration"):
symbols.append({
"type": child.type,
"name": child.child_by_field_name("name").text.decode("utf8") if child.child_by_field_name("name") else "<unknown>",
"start_line": child.start_point[0] + 1,
"end_line": child.end_point[0] + 1
})
symbols.extend(extract_symbols(child))
return symbols

return extract_symbols(root_node)


