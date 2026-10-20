"""Attach to a running Marathon process and identify its build."""
from __future__ import annotations

from dataclasses import dataclass

import pymem
import pymem.process


@dataclass(frozen=True)
class MarathonSession:
    pid: int
    build_id: str
    module_base: int
    process_handle: object


def _read_build_id(pm: pymem.Pymem, module_base: int) -> str:
    # Build id is stored as a 16-byte ASCII string at module_base + 0x4A2C10.
    raw = pm.read_bytes(module_base + 0x4A2C10, 16)
    return raw.rstrip(b"\x00").decode("ascii", errors="replace")


def attach_to_marathon(process_name: str) -> MarathonSession:
    try:
        pm = pymem.Pymem(process_name)
    except pymem.exception.ProcessNotFound as exc:
        raise RuntimeError(f"process '{process_name}' not running") from exc

    module = pymem.process.module_from_name(pm.process_handle, process_name)
    if module is None:
        raise RuntimeError(f"module '{process_name}' not loaded")

    build_id = _read_build_id(pm, module.lpBaseOfDll)
    return MarathonSession(
        pid=pm.process_id,
        build_id=build_id,
        module_base=module.lpBaseOfDll,
        process_handle=pm,
    )