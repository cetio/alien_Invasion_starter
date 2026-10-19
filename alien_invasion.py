#!/usr/bin/env python3.12
"""Alien Invasion — main game module."""
import sys

import pygame

from settings import Settings


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self) -> None:
        """Initialize the game, and create game resources."""
        pygame.init()

        self.clock = pygame.time.Clock()
        self.settings = Settings()

        self.screen = pygame.display.set_mode(
            (self.settings.screen_w, self.settings.screen_h))
        pygame.display.set_caption(self.settings.name)

        self.bg = pygame.image.load(self.settings.bg_file)
        self.bg = pygame.transform.scale(
            self.bg, (self.settings.screen_w, self.settings.screen_h))

        self.running = True

    def run_game(self) -> None:
        """Start the main loop for the game."""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()

            self.screen.blit(self.bg, (0, 0))
            pygame.display.flip()
            # TODO: This seems like a horrible idea. Time delta is superior, as FPS can be tricked.
            self.clock.tick(self.settings.fps)


if __name__ == '__main__':
    window = AlienInvasion()
    window.run_game()
