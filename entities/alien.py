"""The alien enemies."""
from typing import TYPE_CHECKING

import pygame
from pygame.sprite import Sprite

from entity import Entity

if TYPE_CHECKING:
    from entities.alien_fleet import AlienFleet


class Alien(Sprite, Entity):
    """Alien enemy entity class."""

    def __init__(self, fleet: "AlienFleet", x, y) -> None:
        """Create an alien at the given position."""
        super().__init__()

        self.fleet = fleet
        self.game = fleet.game
        self.settings = self.game.settings
        self.screen = self.game.screen
        self.layer = 3
        self.priority = 3
        self.boundaries = self.game.screen.get_rect()

        self.image = pygame.image.load(self.settings.alien_file)
        self.image = pygame.transform.scale(
            self.image, (self.settings.alien_w, self.settings.alien_h))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self) -> None:
        """Move the alien sideways, reversing and dropping at an edge."""
        if self.check_edges():
            self.settings.fleet_direction *= -1
            self.y += self.settings.fleet_drop_speed
        self.x += self.settings.fleet_speed * self.settings.fleet_direction
        self.rect.x = self.x
        self.rect.y = self.y

    def check_edges(self) -> bool:
        """Return whether the alien has reached either screen edge."""
        return (self.rect.right >= self.boundaries.right
                or self.rect.left <= self.boundaries.left)

    def draw(self) -> None:
        """Draw the alien at its current position."""
        self.screen.blit(self.image, self.rect)
