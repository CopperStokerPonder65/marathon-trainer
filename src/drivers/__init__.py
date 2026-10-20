"""Output drivers - overlay, telemetry, hotkey listener."""
from __future__ import annotations

from src.bootstrap.attacher import MarathonSession
from src.bootstrap.config_loader import TrainerProfile
from src.drivers.overlay import OverlayDriver
from src.drivers.telemetry import TelemetryDriver
from src.drivers.hotkeys import HotkeyDriver


def build_drivers(session: MarathonSession, cfg: TrainerProfile) -> list:
    drivers = []
    for name, feat in cfg.features.items():
        if not feat.get("enabled"):
            continue
        driver = feat.get("driver")
        if driver == "overlay":
            drivers.append(OverlayDriver(session, feat))
        elif driver == "jsonl":
            drivers.append(TelemetryDriver(session, feat))
    drivers.append(HotkeyDriver(session, cfg.hotkeys))
    return drivers