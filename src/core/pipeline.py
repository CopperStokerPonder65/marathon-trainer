"""Pipeline: ingest -> process -> drive."""
from __future__ import annotations

import time
from dataclasses import dataclass, field

from rich.console import Console

from src.bootstrap.attacher import MarathonSession
from src.bootstrap.config_loader import TrainerProfile
from src.processors import build_processors
from src.drivers import build_drivers

console = Console()


@dataclass
class TrainerPipeline:
    session: MarathonSession
    config: TrainerProfile
    dry_run: bool = False
    _processors: list = field(default_factory=list)
    _drivers: list = field(default_factory=list)
    _running: bool = False

    def __post_init__(self) -> None:
        self._processors = build_processors(self.session, self.config, dry_run=self.dry_run)
        self._drivers = build_drivers(self.session, self.config)

    def disable_driver(self, name: str) -> None:
        self._drivers = [d for d in self._drivers if d.name != name]

    def tick(self) -> None:
        state = {"ts": time.time(), "pid": self.session.pid}
        for proc in self._processors:
            if not proc.enabled:
                continue
            delta = proc.process()
            if delta:
                state.update(delta)
        for drv in self._drivers:
            drv.render(state)

    def run_forever(self) -> None:
        self._running = True
        interval = self.config.game.poll_interval_ms / 1000.0
        console.print(f"[dim]pipeline running every {interval:.2f}s[/]")
        while self._running:
            self.tick()
            time.sleep(interval)

    def shutdown(self) -> None:
        self._running = False
        for drv in self._drivers:
            drv.close()
        console.print("[dim]pipeline shutdown[/]")