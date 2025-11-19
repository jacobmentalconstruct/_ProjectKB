"""
Fallback heuristics for ingestion.

When no specialised parser exists for a given file type, use simple
heuristic methods to split the file into chunks.  For example,
markdown files can be split by headings, while plain text might be
split on paragraphs.  These functions should produce a list of
dictionaries or objects describing each chunk, similar to the output
of the structured parsers.
"""

def split_plain_text(text: str) -> list:
    """Split plain text into paragraphs.

    TODO: Implement a simple algorithm to divide the input into
    meaningful chunks.  Each chunk should include its text, start and
    end positions, and a brief summary.
    """
    return []
