"""Typed config loader for YAML profiles."""
from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel, Field


class GameConfig(BaseModel):
    process_name: str = "Marathon.exe"
    supported_builds: list[str] = Field(default_factory=list)
    poll_interval_ms: int = 250


class TrainerConfig(BaseModel):
    dry_run: bool = False
    log_level: str = "INFO"
    safety_lock: bool = True


class FeatureConfig(BaseModel):
    enabled: bool = False
    processor: str
    driver: str | None = None
    **extra: object


class TrainerProfile(BaseModel):
    game: GameConfig
    trainer: TrainerConfig
    features: dict[str, dict] = Field(default_factory=dict)
    hotkeys: dict[str, str] = Field(default_factory=dict)


def load_config(path: Path) -> TrainerProfile:
    if not path.exists():
        raise FileNotFoundError(f"config not found: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    return TrainerProfile(**data)