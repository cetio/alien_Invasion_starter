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
        """Create one centered row with a gap between aliens."""
        alien_w = self.settings.alien_w
        screen_w = self.settings.screen_w
        fleet_w = self._calculate_fleet_size(screen_w, alien_w)
        x_offset = self._calculate_offsets(screen_w, alien_w, fleet_w)

        for column in range(fleet_w):
            if column % 2 == 0:
                continue
            current_x = alien_w * column + x_offset
            self._create_alien(current_x, 10)

    def _calculate_fleet_size(self, screen_w, alien_w) -> int:
        """Return an odd number of slots with room for side margins."""
        fleet_w = screen_w // alien_w
        if fleet_w % 2 == 0:
            fleet_w -= 1
        else:
            fleet_w -= 2
        return fleet_w

    def _calculate_offsets(self, screen_w, alien_w, fleet_w) -> int:
        """Return the horizontal offset that centers the row."""
        return int((screen_w - fleet_w * alien_w) // 2)

    def _create_alien(self, current_x, current_y) -> None:
        """Add an alien at the given position."""
        self.fleet.add(Alien(self, current_x, current_y))

    def update(self) -> None:
        """Keep the fleet stationary while laying out the row."""
        pass

    def draw(self) -> None:
        """Draw each alien in the fleet."""
        alien: Alien
        for alien in self.fleet:
            alien.draw()
