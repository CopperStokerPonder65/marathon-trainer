"""Pygame overlay driver - draws HUD on top of the game window."""
from __future__ import annotations

import pygame

from src.bootstrap.attacher import MarathonSession


class OverlayDriver:
    name = "overlay"

    def __init__(self, session: MarathonSession, config: dict) -> None:
        self.session = session
        self.config = config
        self.fps = int(config.get("fps", 60))
        pygame.init()
        self.screen = pygame.display.set_mode((320, 120), pygame.NOFRAME | pygame.SRCALPHA)
        pygame.display.set_caption("Marathon Trainer Overlay")
        self.font = pygame.font.SysFont("consolas", 14)
        self.clock = pygame.time.Clock()
        self._last: dict = {}

    def render(self, state: dict) -> None:
        self._last = state
        self.screen.fill((0, 0, 0, 0))
        y = 6
        if self.config.get("show_health") and "health" in state:
            txt = f"HP {state['health']:>3}/{state.get('max_health', '?')}"
            self.screen.blit(self.font.render(txt, True, (0, 255, 128)), (8, y))
            y += 18
        if self.config.get("show_position") and "position" in state:
            px, py = state["position"]
            self.screen.blit(self.font.render(f"POS {px:.1f},{py:.1f}", True, (0, 200, 255)), (8, y))
        pygame.display.flip()
        self.clock.tick(self.fps)

    def close(self) -> None:
        pygame.quit()