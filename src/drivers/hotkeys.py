"""Global hotkey listener - uses the `keyboard` package."""
from __future__ import annotations

import keyboard

from src.bootstrap.attacher import MarathonSession


class HotkeyDriver:
    name = "hotkeys"

    def __init__(self, session: MarathonSession, hotkeys: dict[str, str]) -> None:
        self.session = session
        self.hotkeys = hotkeys
        self._handlers: list = []
        for action, key in hotkeys.items():
            handler = self._make_handler(action)
            keyboard.add_hotkey(key, handler)
            self._handlers.append(key)

    @staticmethod
    def _make_handler(action: str):
        def _h() -> None:
            if action == "panic_unload":
                raise KeyboardInterrupt
        return _h

    def render(self, state: dict) -> None:
        return None

    def close(self) -> None:
        for key in self._handlers:
            try:
                keyboard.remove_hotkey(key)
            except KeyError:
                pass