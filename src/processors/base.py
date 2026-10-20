"""Base class for all memory processors."""
from __future__ import annotations

from dataclasses import dataclass

from src.bootstrap.attacher import MarathonSession


@dataclass
class Processor:
    session: MarathonSession
    config: dict
    dry_run: bool = False

    name: str = "base"
    enabled: bool = True

    # Offsets are documented per-processor and MUST match the supported builds.
    offsets: dict[str, int] = {}

    def read_int(self, offset: int) -> int:
        pm = self.session.process_handle
        return pm.read_int(self.session.module_base + offset)

    def write_int(self, offset: int, value: int) -> None:
        if self.dry_run:
            return
        pm = self.session.process_handle
        pm.write_int(self.session.module_base + offset, value)

    def process(self) -> dict:
        raise NotImplementedError