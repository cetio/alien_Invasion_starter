"""The player's ship."""
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    from entities.ship_arsenal import ShipArsenal


class Ship:
    """The player ship entity class."""

    def __init__(self, game: "AlienInvasion", arsenal: "ShipArsenal") -> None:
        """Initialize the ship and set its starting position."""
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.arsenal = arsenal
        self.layer = 1
        self.priority = 1

        self.image = pygame.image.load(self.settings.ship_file)
        self.image = pygame.transform.scale(
            self.image, (self.settings.ship_w, self.settings.ship_h))

        self.rect = self.image.get_rect()
        self.boundaries = game.screen.get_rect()
        self._center_ship()

        self.moving_right = False
        self.moving_left = False

    def _center_ship(self) -> None:
        """Center the ship at the bottom and reset its float position."""
        self.rect.midbottom = self.boundaries.midbottom
        self.x = float(self.rect.x)

    def update(self) -> None:
        """Update the ship's position and its arsenal."""
        self._update_ship_movement()
        self.arsenal.update_arsenal()

    def _update_ship_movement(self) -> None:
        """Update the ship's position based on the movement flags."""
        if self.moving_right and self.rect.right < self.boundaries.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > self.boundaries.left:
            self.x -= self.settings.ship_speed
        self.rect.x = self.x

    def fire(self) -> bool:
        """Fire a bullet through the arsenal."""
        return self.arsenal.fire_bullet()

    def check_collisions(self, other_group) -> bool:
        """Re-center the ship if it collides with another sprite."""
        if pygame.sprite.spritecollideany(self, other_group):
            self._center_ship()
            return True
        return False

    def draw(self) -> None:
        """Draw the ship and its arsenal."""
        self.arsenal.draw()
        self.screen.blit(self.image, self.rect)
