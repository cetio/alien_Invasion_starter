"""Buttons for the game's menus."""
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class Button:
    """A centered button with a rendered label."""

    def __init__(self, game: "AlienInvasion", message: str) -> None:
        """Create the button and prepare its label."""
        self.screen = game.screen
        self.boundaries = self.screen.get_rect()
        self.settings = game.settings

        self.font = pygame.font.Font(
            str(self.settings.font_file), self.settings.button_font_size)
        self.rect = pygame.Rect(
            0, 0, self.settings.button_w, self.settings.button_h)
        self.rect.center = self.boundaries.center
        self._prep_message(message)

    def _prep_message(self, message: str) -> None:
        """Render the label and center it within the button."""
        self.message_image = self.font.render(
            message, True, self.settings.text_color)
        self.message_rect = self.message_image.get_rect()
        self.message_rect.center = self.rect.center

    def draw(self) -> None:
        """Draw the button's rectangle and label."""
        self.screen.fill(self.settings.button_color, self.rect)
        self.screen.blit(self.message_image, self.message_rect)

    def check_clicked(self, mouse_position) -> bool:
        """Return whether the position falls inside the button."""
        return self.rect.collidepoint(mouse_position)
