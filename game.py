#!/usr/bin/env python3.12
"""Alien Invasion — main game module."""
import sys

import pygame

from entities.ship import Ship
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

        self.ship = Ship(self)
        self.entities = [self.ship]

        self.running = True

    def run_game(self) -> None:
        """Start the main loop for the game."""
        while self.running:
            self._check_input()
            self._update_entities()
            self._update_screen()
            # TODO: This seems like a horrible idea. Time delta is superior, as FPS can be tricked.
            self.clock.tick(self.settings.fps)

    def _update_entities(self) -> None:
        """Update each entity in priority order."""
        for entity in sorted(self.entities, key=lambda entity: entity.priority):
            entity.update()

    def _update_screen(self) -> None:
        """Draw the background and entities in layer order, then flip."""
        # Background is always layer 0 and other entities can't be below or equal to it.
        self.screen.blit(self.bg, (0, 0))

        for entity in sorted(self.entities, key=lambda entity: entity.layer):
            entity.draw()

        pygame.display.flip()

    def _check_input(self) -> None:
        """Respond to keypresses and window events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event: pygame.event.Event) -> None:
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            self.running = False
            pygame.quit()
            sys.exit()

    def _check_keyup_events(self, event: pygame.event.Event) -> None:
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False


if __name__ == '__main__':
    window = AlienInvasion()
    window.run_game()
