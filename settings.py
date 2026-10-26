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

        self.bullet_file = self.images_dir / "laserBlast.png"
        self.laser_sound = self.sound_dir / "laser.mp3"
        self.bullet_w = 25
        self.bullet_h = 80
        self.bullet_speed = 7
        self.bullet_amount = 5

        self.alien_file = self.images_dir / "enemy_4.png"
        self.alien_w = 40
        self.alien_h = 40
        self.fleet_speed = 2
        self.fleet_direction = 1
        self.fleet_drop_speed = 10
