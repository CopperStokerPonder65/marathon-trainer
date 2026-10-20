"""Infinite-health processor."""
from __future__ import annotations

from dataclasses import dataclass

from src.processors.base import Processor


@dataclass
class HealthProcessor(Processor):
    name: str = "health"
    offsets: dict[str, int] = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        self.offsets = {
            "player_health": 0x00B2C140,
            "player_max_health": 0x00B2C144,
        }

    def process(self) -> dict:
        hp = self.read_int(self.offsets["player_health"])
        max_hp = self.read_int(self.offsets["player_max_health"])
        target = int(self.config.get("value", max_hp))
        if 0 < hp < target:
            self.write_int(self.offsets["player_health"], target)
        return {"health": hp, "max_health": max_hp}