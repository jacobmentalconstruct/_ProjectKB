"""
Logging utilities for Project KnowledgeBase.

Define functions or classes here to provide consistent logging across
the application.  Consider using Python's built‑in `logging` module
with customised formatters to include timestamps, log levels, and
module names.
"""

import logging

def get_logger(name: str) -> logging.Logger:
    """Return a logger configured for the given module name.

    TODO: Configure the logger with handlers and formatters as
    appropriate for your application.  For now, return the default
    logger.
    """
    return logging.getLogger(name)
