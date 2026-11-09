"""The game's statistics overlay."""
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class HUD:
    """Render cached score images over the game world."""

    def __init__(self, game: "AlienInvasion") -> None:
        """Create the font and prepare the score images."""
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.boundaries = self.screen.get_rect()
        self.game_stats = game.game_stats
        self.padding = 20

        self.font = pygame.font.Font(
            str(self.settings.font_file), self.settings.hud_font_size)
        self.update_scores()

    def update_scores(self) -> None:
        """Refresh the score images from the current statistics."""
        self._update_max_score()
        self._update_score()
        self._update_high_score()

    def _update_max_score(self) -> None:
        """Render the session maximum at the top right."""
        message = f"Max Score: {self.game_stats.max_score:.0f}"
        self.max_score_image = self.font.render(
            message, True, self.settings.text_color)
        self.max_score_rect = self.max_score_image.get_rect()
        self.max_score_rect.right = self.boundaries.right - self.padding
        self.max_score_rect.top = self.padding

    def _update_score(self) -> None:
        """Render the run score below the session maximum."""
        message = f"Score: {self.game_stats.score:.0f}"
        self.score_image = self.font.render(
            message, True, self.settings.text_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.boundaries.right - self.padding
        self.score_rect.top = self.max_score_rect.bottom + self.padding

    def _update_high_score(self) -> None:
        """Render the persistent high score at the top center."""
        message = f"High Score: {self.game_stats.high_score:.0f}"
        self.high_score_image = self.font.render(
            message, True, self.settings.text_color)
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.midtop = (
            self.boundaries.centerx, self.padding)

    def draw(self) -> None:
        """Draw the cached score images."""
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.max_score_image, self.max_score_rect)
        self.screen.blit(self.score_image, self.score_rect)
