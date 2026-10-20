"""Memory processors - one per trainer feature."""
from __future__ import annotations

from src.bootstrap.attacher import MarathonSession
from src.bootstrap.config_loader import TrainerProfile
from src.processors.health import HealthProcessor
from src.processors.ammo import AmmoProcessor
from src.processors.movement import MovementProcessor


def build_processors(session: MarathonSession, cfg: TrainerProfile, *, dry_run: bool) -> list:
    registry = {
        "health": HealthProcessor,
        "ammo": AmmoProcessor,
        "movement": MovementProcessor,
    }
    out = []
    for name, feat in cfg.features.items():
        if not feat.get("enabled"):
            continue
        proc_name = feat.get("processor", name)
        cls = registry.get(proc_name)
        if cls is None:
            continue
        out.append(cls(session, feat, dry_run=dry_run))
    return out