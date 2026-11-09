"""Statistics for the current game."""
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion


class GameStats:
    """Tracks run statistics and session and all-time score records."""

    def __init__(self, game: "AlienInvasion") -> None:
        """Initialize statistics and score records."""
        self.game = game
        self.settings = game.settings
        self.path = self.settings.scores_file
        self.max_score = 0
        self.high_score = 0
        self.reset_stats()

    def reset_stats(self) -> None:
        """Restore run statistics without clearing score records."""
        self.ships_left = self.settings.starting_ship_count
        self.score = 0
        self.level = 1

    def update(self, collisions: dict) -> None:
        """Award points and update the score records."""
        self._update_score(collisions)
        self._update_max_score()
        self._update_high_score()

    def _update_score(self, collisions: dict) -> None:
        """Award one alien's points per collision dictionary key."""
        self.score += self.settings.alien_points * len(collisions)

    def _update_max_score(self) -> None:
        """Keep the highest score earned during this session."""
        if self.score > self.max_score:
            self.max_score = self.score

    def _update_high_score(self) -> None:
        """Keep the highest score earned across all runs."""
        if self.score > self.high_score:
            self.high_score = self.score

    def update_level(self) -> None:
        """Advance to the next fleet's level."""
        self.level += 1
