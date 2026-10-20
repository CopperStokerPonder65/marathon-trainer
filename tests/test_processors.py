"""Tests for the memory processors - uses a fake pymem handle."""
from __future__ import annotations

from dataclasses import dataclass

import pytest

from src.bootstrap.attacher import MarathonSession
from src.processors.health import HealthProcessor


class FakePymem:
    def __init__(self, initial: dict[int, int]) -> None:
        self.mem = dict(initial)
        self.writes: list[tuple[int, int]] = []

    def read_int(self, addr: int) -> int:
        return self.mem.get(addr, 0)

    def write_int(self, addr: int, value: int) -> None:
        self.writes.append((addr, value))
        self.mem[addr] = value


def make_session(mem: dict[int, int]) -> MarathonSession:
    return MarathonSession(
        pid=1337, build_id="2026.3.0", module_base=0x1000, process_handle=FakePymem(mem)
    )


def test_health_processor_heals_when_low():
    session = make_session({0x1000 + 0x00B2C140: 12, 0x1000 + 0x00B2C144: 100})
    proc = HealthProcessor(session, {"value": 100})
    out = proc.process()
    assert out["health"] == 12
    assert (0x1000 + 0x00B2C140, 100) in session.process_handle.writes


def test_health_processor_dry_run_does_not_write():
    session = make_session({0x1000 + 0x00B2C140: 12, 0x1000 + 0x00B2C144: 100})
    proc = HealthProcessor(session, {"value": 100}, dry_run=True)
    proc.process()
    assert session.process_handle.writes == []