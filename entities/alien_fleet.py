"""The alien fleet."""
from typing import TYPE_CHECKING

import pygame

from entities.alien import Alien
from entity import Entity

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class AlienFleet(Entity):
    """Manages the fleet's aliens and layout."""

    def __init__(self, game: "AlienInvasion") -> None:
        """Create an empty fleet."""
        self.game = game
        self.settings = game.settings
        self.layer = 3
        self.priority = 3
        self.fleet = pygame.sprite.Group()
        self.fleet_direction = self.settings.fleet_direction
        self.drop_speed = self.settings.fleet_drop_speed

    def create_fleet(self) -> None:
        """Create a centered rectangular fleet in the screen's top half."""
        alien_w = self.settings.alien_w
        alien_h = self.settings.alien_h
        screen_w = self.settings.screen_w
        screen_h = self.settings.screen_h
        fleet_w, fleet_h = self._calculate_fleet_size(
            screen_w, screen_h, alien_w, alien_h)
        x_offset, y_offset = self._calculate_offsets(
            screen_w, screen_h, alien_w, alien_h, fleet_w, fleet_h)
        self._create_rectangle_fleet(
            alien_w, alien_h, fleet_w, fleet_h, x_offset, y_offset)

    def _calculate_fleet_size(
            self, screen_w, screen_h, alien_w, alien_h) -> tuple[int, int]:
        """Return odd slot counts with room for margins in the top half."""
        fleet_w = screen_w // alien_w
        fleet_h = (screen_h // 2) // alien_h
        if fleet_w % 2 == 0:
            fleet_w -= 1
        else:
            fleet_w -= 2
        if fleet_h % 2 == 0:
            fleet_h -= 1
        else:
            fleet_h -= 2
        return int(fleet_w), int(fleet_h)

    def _calculate_offsets(
            self, screen_w, screen_h, alien_w, alien_h,
            fleet_w, fleet_h) -> tuple[int, int]:
        """Return offsets that center the fleet in the screen's top half."""
        x_offset = int((screen_w - fleet_w * alien_w) // 2)
        half_screen = screen_h // 2
        y_offset = int((half_screen - fleet_h * alien_h) // 2)
        return x_offset, y_offset

    def _create_rectangle_fleet(
            self, alien_w, alien_h, fleet_w, fleet_h,
            x_offset, y_offset) -> None:
        """Create spaced rows and columns of aliens."""
        for row in range(fleet_h):
            for column in range(fleet_w):
                if column % 2 == 0 or row % 2 == 0:
                    continue
                current_x = alien_w * column + x_offset
                current_y = alien_h * row + y_offset
                self._create_alien(current_x, current_y)

    def _create_alien(self, current_x, current_y) -> None:
        """Add an alien at the given position."""
        self.fleet.add(Alien(self, current_x, current_y))

    def update(self) -> None:
        """Keep the fleet stationary while laying out the rows."""
        pass

    def draw(self) -> None:
        """Draw each alien in the fleet."""
        alien: Alien
        for alien in self.fleet:
            alien.draw()
