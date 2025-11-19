"""
Intent summariser implementation.

This module defines the public API for summarising chunks of code or
text.  It should expose a function (e.g. `summarise`) that takes a
string and returns a concise sentence describing the purpose or
behaviour of that string.  Initially, you might simply truncate the
first non‑empty line; later you can integrate an AI model.
"""

def summarise(text: str) -> str:
    """Return a brief summary of *text*.

    TODO: Replace this stub with a more sophisticated summarisation
    algorithm.  For now, just return the first line (up to 80
    characters).
    """
    for line in text.splitlines():
        clean = line.strip()
        if clean:
            return clean[:80]
    return ""
