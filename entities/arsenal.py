"""The ship's weapon loadout."""
from typing import TYPE_CHECKING

import pygame

from entities.bullet import Bullet

if TYPE_CHECKING:
    from game import AlienInvasion


class ShipArsenal:
    """Manages the ship's live bullets."""

    def __init__(self, game: "AlienInvasion") -> None:
        """Create an empty arsenal."""
        self.game = game
        self.settings = game.settings
        self.arsenal = pygame.sprite.Group()

    def fire_bullet(self) -> bool:
        """Fire a bullet if the arsenal isn't full."""
        if len(self.arsenal) < self.settings.bullet_amount:
            self.arsenal.add(Bullet(self.game))
            return True
        return False

    def update_arsenal(self) -> None:
        """Update the bullets, then cull any that left the screen."""
        self.arsenal.update()
        self._remove_bullets_off_screen()

    def _remove_bullets_off_screen(self) -> None:
        """Remove bullets that have gone off the top of the screen."""
        for bullet in self.arsenal.copy():
            if bullet.rect.bottom <= 0:
                self.arsenal.remove(bullet)

    def draw(self) -> None:
        """Draw each bullet in the arsenal."""
        for bullet in self.arsenal:
            bullet.draw()
