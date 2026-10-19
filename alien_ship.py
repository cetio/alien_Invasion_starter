"""The player's ship."""
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class Ship:
    """The player ship entity class."""

    def __init__(self, game: "AlienInvasion") -> None:
        """Initialize the ship and set its starting position."""
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.layer = 1

        self.image = pygame.image.load(self.settings.ship_file)
        self.image = pygame.transform.scale(
            self.image, (self.settings.ship_w, self.settings.ship_h))

        self.rect = self.image.get_rect()
        self.screen_rect = game.screen.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom

    def draw(self) -> None:
        """Draw the ship at its current position."""
        self.screen.blit(self.image, self.rect)
