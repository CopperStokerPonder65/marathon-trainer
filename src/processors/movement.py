"""Movement tweaks: gravity scale, jump height."""
from __future__ import annotations

from dataclasses import dataclass

from src.processors.base import Processor


@dataclass
class MovementProcessor(Processor):
    name: str = "movement"
    offsets: dict[str, int] = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        self.offsets = {
            "gravity_scale": 0x00B2C310,
            "jump_impulse": 0x00B2C318,
        }

    def process(self) -> dict:
        gravity = float(self.config.get("gravity_scale", 1.0))
        jump = float(self.config.get("jump_height", 1.0))
        pm = self.session.process_handle
        if not self.dry_run:
            pm.write_float(self.session.module_base + self.offsets["gravity_scale"], gravity)
            pm.write_float(self.session.module_base + self.offsets["jump_impulse"], jump)
        return {"gravity_scale": gravity, "jump_height": jump}