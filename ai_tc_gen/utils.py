"""Small utility helpers used across the project."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


_REPLACEMENT_PATTERN = re.compile(r"[^a-z0-9_]+")


def slugify(text: str, fallback: str = "untitled") -> str:
    """Make a filesystem/test-friendly slug from arbitrary text."""
    slug = _REPLACEMENT_PATTERN.sub("_", text.lower())
    slug = re.sub(r"_{2,}", "_", slug).strip("_")
    return slug or fallback


def safe_repr(value: Any, max_length: int = 400) -> str:
    """Return a short representation that is safe to embed in comments."""
    try:
        rendered = repr(value)
    except Exception:
        rendered = str(value)

    if len(rendered) > max_length:
        return f"{rendered[:max_length]}..."
    return rendered


def ensure_parent_dir(path: str | Path) -> None:
    """Create a file path's parent directory when it does not already exist."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)


def dump_json(data: Any) -> str:
    """Render deterministic, human-readable JSON."""
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True)
