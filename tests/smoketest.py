"""
Placeholder test module.

This file demonstrates how to write a basic test.  Replace this test
with real tests as you implement functionality.  Running the test
suite should help ensure that individual units of the application
behave as expected.
"""

def test_placeholder() -> None:
    """Smoke test that instantiates DB and inserts a test file."""
    from interface import KnowledgeBaseDB
import tempfile

with tempfile.NamedTemporaryFile(suffix=".sqlite") as tmp:
db = KnowledgeBaseDB(tmp.name)
file_id = db.insert_file("foo.py", b"print('hello')", "abc123")
chunk_id = db.insert_chunk(file_id, "print('hello')", "hello call")
results = db.search_chunks_by_keyword("hello")
assert any("hello" in r for r in results)


