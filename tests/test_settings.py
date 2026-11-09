"""Tests for resettable settings and difficulty scaling."""
import unittest

from settings import Settings


class SettingsTests(unittest.TestCase):
    """Check gameplay defaults without creating game resources."""

    def setUp(self) -> None:
        """Create settings and record the expected gameplay defaults."""
        self.settings = Settings()
        self.defaults = {
            "ship_speed": 5,
            "starting_ship_count": 3,
            "bullet_w": 25,
            "bullet_h": 80,
            "bullet_speed": 7,
            "bullet_amount": 5,
            "alien_w": 40,
            "alien_h": 40,
            "fleet_speed": 2,
            "fleet_drop_speed": 10,
        }

    def test_constructor_initializes_dynamic_defaults(self) -> None:
        for name, value in self.defaults.items():
            with self.subTest(setting=name):
                self.assertEqual(getattr(self.settings, name), value)
        self.assertEqual(self.settings.difficulty_scale, 1.1)
        self.assertEqual(self.settings.fleet_direction, 1)

    def test_initialization_restores_all_dynamic_defaults(self) -> None:
        for name in self.defaults:
            setattr(self.settings, name, -1)
        self.settings.initialize_dynamic_settings()
        for name, value in self.defaults.items():
            with self.subTest(setting=name):
                self.assertEqual(getattr(self.settings, name), value)

    def test_initialization_preserves_static_configuration(self) -> None:
        self.settings.screen_w = 1000
        self.settings.difficulty_scale = 1.25
        before = vars(self.settings).copy()
        self.settings.initialize_dynamic_settings()
        self.assertEqual(vars(self.settings), before)

    def test_difficulty_scales_only_movement_speeds(self) -> None:
        expected = vars(self.settings).copy()
        for name in ("ship_speed", "bullet_speed", "fleet_speed"):
            expected[name] *= self.settings.difficulty_scale
        self.settings.increase_difficulty()
        self.assertEqual(vars(self.settings), expected)

    def test_repeated_increases_compound(self) -> None:
        for increases in range(1, 4):
            self.settings.increase_difficulty()
            for name in ("ship_speed", "bullet_speed", "fleet_speed"):
                with self.subTest(increases=increases, setting=name):
                    self.assertAlmostEqual(
                        getattr(self.settings, name),
                        self.defaults[name] * 1.1 ** increases)


if __name__ == '__main__':
    unittest.main()
