"""
Tree‑sitter ingestion utilities.

Provides an interface for parsing files using the Tree‑sitter library.
Extracts symbols (functions, classes) AND their source text for embedding.
"""

def parse_source_with_tree_sitter(source: str, language: str) -> list:
    """
    Parse source text using Tree‑sitter and return a list of symbols.
    
    Returns:
        list[dict]: A list of dicts containing:
            - type: str (function, class, etc.)
            - name: str (identifier)
            - text: str (the full source code of the node)
            - docstring: str (empty for now, hard to generalize across languages)
            - start_line/end_line: int
    """
    from tree_sitter import Parser
    from tree_sitter_languages import get_language
    
    try:
        ts_lang = get_language(language)
    except Exception:
        # Return empty if language is not installed/supported
        print(f"Tree-sitter language '{language}' not found. Skipping structural parse.")
        return []

    parser = Parser()
    parser.set_language(ts_lang)
    
    # Tree-sitter works on bytes
    source_bytes = bytes(source, "utf8")
    tree = parser.parse(source_bytes)
    root_node = tree.root_node

    def extract_symbols(node):
        symbols = []
        
        # Iterate over children
        for child in node.children:
            # Broad set of node types to capture across JS, TS, Rust, Go, etc.
            relevant_types = (
                "function", "function_definition", "method_definition", 
                "class", "class_declaration", "impl_item"
            )
            
            if child.type in relevant_types:
                # Extract Name
                name_node = child.child_by_field_name("name")
                name = name_node.text.decode("utf8") if name_node else "<unknown>"
                
                # Extract Full Source Text (CRITICAL for Embeddings)
                # We slice the original source bytes using the node's byte range
                node_text = source_bytes[child.start_byte : child.end_byte].decode("utf8")

                symbols.append({
                    "type": child.type,
                    "name": name,
                    "text": node_text, # <--- Added this so the Embedder has something to read
                    "docstring": "",   # Placeholder; extracting comments varies wildly by language
                    "start_line": child.start_point[0] + 1,
                    "end_line": child.end_point[0] + 1
                })
            
            # Recursively check children (e.g. methods inside classes)
            symbols.extend(extract_symbols(child))
            
        return symbols

    return extract_symbols(root_node)