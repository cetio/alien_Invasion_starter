#!/usr/bin/env python3.12
"""Alien Invasion — main game module."""
import sys
from time import sleep

import pygame

from entities.alien_fleet import AlienFleet
from entities.ship_arsenal import ShipArsenal
from entities.ship import Ship
from game_stats import GameStats
from settings import Settings


class AlienInvasion:
    """Overall class to manage game assets and behavior."""

    def __init__(self) -> None:
        """Initialize the game, and create game resources."""
        pygame.init()

        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.game_stats = GameStats(self.settings.starting_ship_count)

        self.screen = pygame.display.set_mode(
            (self.settings.screen_w, self.settings.screen_h))
        pygame.display.set_caption(self.settings.name)

        self.bg = pygame.image.load(self.settings.bg_file)
        self.bg = pygame.transform.scale(
            self.bg, (self.settings.screen_w, self.settings.screen_h))

        self.arsenal = ShipArsenal(self)
        self.ship = Ship(self, self.arsenal)
        self.entities = [self.ship]
        self.alien_fleet = AlienFleet(self)
        self.alien_fleet.create_fleet()
        self.entities.append(self.alien_fleet)

        pygame.mixer.init()
        self.laser_sound = pygame.mixer.Sound(self.settings.laser_sound)
        self.laser_sound.set_volume(0.7)
        self.impact_sound = pygame.mixer.Sound(self.settings.impact_sound)
        self.impact_sound.set_volume(0.7)

        self.running = True
        self.active = True

    def run_game(self) -> None:
        """Start the main loop for the game."""
        while self.running:
            self._check_input()
            if self.active:
                self._update_entities()
                self._check_collisions()
            self._update_screen()
            # TODO: This seems like a horrible idea. Time delta is superior, as FPS can be tricked.
            self.clock.tick(self.settings.fps)

    def _update_entities(self) -> None:
        """Update each entity in priority order."""
        for entity in sorted(self.entities, key=lambda entity: entity.priority):
            entity.update()

    def _check_collisions(self) -> None:
        """Check ship, bottom-edge, and projectile collisions."""
        if self.ship.check_collisions(self.alien_fleet.fleet):
            self._check_game_status()
            return
        if self.alien_fleet.check_fleet_bottom():
            self._check_game_status()
            return
        collisions = self.alien_fleet.check_collisions(self.ship.arsenal.arsenal)
        if collisions:
            self.impact_sound.play(fade_ms=250)
            if self.alien_fleet.check_destroyed_status():
                self._reset_level()

    def _reset_level(self) -> None:
        """Clear projectiles, rebuild the fleet, and re-center the ship."""
        self.ship.arsenal.arsenal.empty()
        self.alien_fleet.fleet.empty()
        self.alien_fleet.create_fleet()
        self.ship._center_ship()
        sleep(0.5)

    def _check_game_status(self) -> None:
        """Spend a ship and stop gameplay when none remain."""
        if self.game_stats.ships_left > 0:
            self.game_stats.ships_left -= 1
        if self.game_stats.ships_left > 0:
            self._reset_level()
        else:
            self.active = False

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
        elif event.key == pygame.K_SPACE:
            if self.active and self.ship.fire():
                self.laser_sound.play(fade_ms=250)
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
