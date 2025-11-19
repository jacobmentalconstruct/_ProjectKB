"""
Graph link builder.

This module contains logic for constructing relationships between
symbols based on parsing output.  For example, given a list of
function definitions and call information, create edges representing
`calls` relationships.  You can extend this to include other edge
types such as `imports` or `inherits`.  The output should be
compatible with the `relation_graph` table in the database.
"""

from typing import Iterable


def build_links(symbols: Iterable[dict]) -> Iterable[tuple]:
    """Generate graph edges from parsed symbol definitions."""
edges = []
    for sym in symbols:
    from_name = sym.get("name")
    for callee in sym.get("calls", []):
    edges.append((from_name, callee, "calls"))
return edges


