"""
Intent summariser implementation.

This module defines the public API for summarising chunks of code or
text.  It should expose a function (e.g. `summarise`) that takes a
string and returns a concise sentence describing the purpose or
behaviour of that string.  Initially, you might simply truncate the
first non‑empty line; later you can integrate an AI model.
"""

def summarise(text: str) -> str:
    """Return a brief summary of *text* (first non-empty line, max 80 chars)."""
for line in text.splitlines():
    clean = line.strip()
    if clean:
    return clean[:77] + "..." if len(clean) > 80 else clean
    return ""


