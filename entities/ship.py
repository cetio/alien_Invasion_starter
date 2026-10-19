"""The player's ship."""
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from game import AlienInvasion


class Ship:
    """The player ship entity class."""

    def __init__(self, game: "AlienInvasion") -> None:
        """Initialize the ship and set its starting position."""
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.layer = 1
        self.priority = 1

        self.image = pygame.image.load(self.settings.ship_file)
        self.image = pygame.transform.scale(
            self.image, (self.settings.ship_w, self.settings.ship_h))

        self.rect = self.image.get_rect()
        self.boundaries = game.screen.get_rect()
        self.rect.midbottom = self.boundaries.midbottom

        self.moving_right = False
        self.moving_left = False
        self.x = float(self.rect.x)

    def update(self) -> None:
        """Update the ship's position based on the movement flags."""
        if self.moving_right and self.rect.right < self.boundaries.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > self.boundaries.left:
            self.x -= self.settings.ship_speed
        self.rect.x = self.x

    def draw(self) -> None:
        """Draw the ship at its current position."""
        self.screen.blit(self.image, self.rect)
