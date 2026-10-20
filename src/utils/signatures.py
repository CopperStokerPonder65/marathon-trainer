"""Signature scanning helpers - locate offsets dynamically when builds shift."""
from __future__ import annotations

import re


def pattern_to_regex(pattern: str) -> re.Pattern[bytes]:
    parts = []
    for tok in pattern.split():
        if tok in ("??", "?"):
            parts.append(b".")
        else:
            parts.append(re.escape(bytes([int(tok, 16)])))
    return re.compile(b"".join(parts), re.DOTALL)


def find_pattern(haystack: bytes, pattern: str) -> int:
    m = pattern_to_regex(pattern).search(haystack)
    return m.start() if m else -1