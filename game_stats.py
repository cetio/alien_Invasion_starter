"""Statistics for the current game."""


class GameStats:
    """Tracks the ships remaining in the current run."""

    def __init__(self, ship_limit: int) -> None:
        """Initialize the number of ships available."""
        self.ships_left = ship_limit
