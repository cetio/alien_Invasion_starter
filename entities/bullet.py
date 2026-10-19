"""The player's laser bolts."""
from typing import TYPE_CHECKING

import pygame
from pygame.sprite import Sprite

from entity import Entity

if TYPE_CHECKING:
    from game import AlienInvasion


class Bullet(Sprite, Entity):
    """Laser (bullet) projectile entity class."""

    def __init__(self, game: "AlienInvasion") -> None:
        """Create a bullet at the ship's current position."""
        super().__init__()

        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        # TODO: We might want to support layer 0 (or possibly negative layers?) so the ship doesn't clip it.
        self.layer = 2
        self.priority = 2

        self.image = pygame.image.load(self.settings.bullet_file)
        self.image = pygame.transform.scale(
            self.image, (self.settings.bullet_w, self.settings.bullet_h))

        self.rect = self.image.get_rect()
        self.rect.midtop = game.ship.rect.midtop

        self.y = float(self.rect.y)

    def update(self) -> None:
        """Move the bullet up the screen."""
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw(self) -> None:
        """Draw the bullet at its current position."""
        self.screen.blit(self.image, self.rect)
