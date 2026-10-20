"""Infinite-ammo processor."""
from __future__ import annotations

from dataclasses import dataclass

from src.processors.base import Processor


@dataclass
class AmmoProcessor(Processor):
    name: str = "ammo"
    offsets: dict[str, int] = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        # Ammo reserve is a 6-int array (one slot per weapon).
        self.offsets = {"reserve_array": 0x00B2C2A0}
        self.slot_count = 6

    def process(self) -> dict:
        reserve = int(self.config.get("reserve_value", 999))
        pm = self.session.process_handle
        base = self.session.module_base + self.offsets["reserve_array"]
        current = [pm.read_int(base + i * 4) for i in range(self.slot_count)]
        if not self.dry_run:
            for i, v in enumerate(current):
                if 0 < v < reserve:
                    pm.write_int(base + i * 4, reserve)
        return {"ammo_reserve": current}