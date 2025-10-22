# utils.py
# Small utility helpers used across the project
import re
from typing import Any


def slugify(text: str) -> str:
    """Make a filesystem/test-friendly slug from text."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9_]+", "_", text)
    text = re.sub(r"_{2,}", "_", text)
    return text.strip("_")


def safe_repr(value: Any) -> str:
    """Return a short, code-safe representation of a value for embedding into templates."""
    try:
        # Use repr but keep it short for big lists/dicts
        r = repr(value)
        if len(r) > 400:
            return r[:400] + '...'
        return r
    except Exception:
        return str(value)
