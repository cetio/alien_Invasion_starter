"""The alien enemies."""
from typing import TYPE_CHECKING

import pygame
from pygame.sprite import Sprite

from entity import Entity

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class Alien(Sprite, Entity):
    """Alien enemy entity class."""

    def __init__(self, game: "AlienInvasion", x, y) -> None:
        """Create an alien at the given position."""
        super().__init__()

        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.layer = 3
        self.priority = 3
        self.boundaries = game.screen.get_rect()

        self.image = pygame.image.load(self.settings.alien_file)
        self.image = pygame.transform.scale(
            self.image, (self.settings.alien_w, self.settings.alien_h))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self) -> None:
        """Keep the alien stationary."""
        pass

    def draw(self) -> None:
        """Draw the alien at its current position."""
        self.screen.blit(self.image, self.rect)
