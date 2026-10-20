"""JSONL telemetry driver - one event per line, easy to diff & replay."""
from __future__ import annotations

import json
from pathlib import Path

from src.bootstrap.attacher import MarathonSession


class TelemetryDriver:
    name = "telemetry"

    def __init__(self, session: MarathonSession, config: dict) -> None:
        self.session = session
        self.path = Path(config.get("path", "logs/telemetry.jsonl"))
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._fh = self.path.open("a", encoding="utf-8")

    def render(self, state: dict) -> None:
        if not state:
            return
        self._fh.write(json.dumps(state, default=str) + "\n")
        self._fh.flush()

    def close(self) -> None:
        self._fh.close()