"""Settings for Alien Invasion."""
from pathlib import Path


class Settings:
    """A class to store all settings for Alien Invasion."""

    def __init__(self) -> None:
        """Initialize the game's settings."""
        self.name: str = "Alien Invasion"
        self.screen_w = 1200
        self.screen_h = 800
        self.fps = 60

        self.images_dir = Path.cwd() / "Assets" / "images"
        self.sound_dir = Path.cwd() / "Assets" / "sound"
        self.fonts_dir = Path.cwd() / "Assets" / "Fonts"
        self.file_dir = Path.cwd() / "Assets" / "file"

        self.bg_file = self.images_dir / "Starbasesnow.png"
        self.ship_file = self.images_dir / "ship2(no bg).png"
        self.ship_w = 40
        self.ship_h = 60
        self.ship_speed = 5
