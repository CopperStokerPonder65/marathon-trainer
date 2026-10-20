"""Rich-based logging setup."""
from __future__ import annotations

import logging
from pathlib import Path

from rich.logging import RichHandler


def setup_logging(level: str = "INFO") -> None:
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(message)s",
        handlers=[
            RichHandler(rich_tracebacks=True, show_path=False),
            logging.FileHandler(log_dir / "session.log", encoding="utf-8"),
        ],
    )