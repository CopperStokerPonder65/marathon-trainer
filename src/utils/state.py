"""Small persistent state store for last-seen build id."""
from __future__ import annotations

import json
from pathlib import Path

STATE_PATH = Path("trainer_state.json")


def read_state() -> dict:
    if not STATE_PATH.exists():
        return {}
    try:
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def write_state(data: dict) -> None:
    STATE_PATH.write_text(json.dumps(data, indent=2), encoding="utf-8")