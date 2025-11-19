"""
Logging utilities for Project KnowledgeBase.

Define functions or classes here to provide consistent logging across
the application.  Consider using Python's built‑in `logging` module
with customised formatters to include timestamps, log levels, and
module names.
"""

import logging

def get_logger(name: str) -> logging.Logger:
    """Return a logger configured with timestamps and module names."""
logger = logging.getLogger(name)
    if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
    fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
return logger


