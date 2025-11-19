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
    """Split plain text into paragraphs with start/end lines and summaries."""
lines = text.splitlines()
    chunks = []
    buffer = []
    start = 0
    
    def summarize(paragraph):
words = paragraph.split()
return " ".join(words[:12]) + ("..." if len(words) > 12 else "")

for idx, line in enumerate(lines + [""]):
if line.strip():
buffer.append(line)
elif buffer:
para = "\n".join(buffer)
chunks.append({
"type": "paragraph",
"start_line": start + 1,
"end_line": idx,
"text": para,
"summary": summarize(para)
})
buffer = []
start = idx + 1

return chunks


