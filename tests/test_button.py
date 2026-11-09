"""Tests for button layout, rendering, and hit testing."""
from types import SimpleNamespace
import unittest

import pygame

from button import Button
from settings import Settings


class ButtonTests(unittest.TestCase):
    """Check the button without opening a game window."""

    def setUp(self) -> None:
        """Create a button on an off-screen surface."""
        pygame.font.init()
        self.addCleanup(pygame.font.quit)
        self.screen = pygame.Surface((1200, 800))
        self.settings = Settings()
        self.button = Button(SimpleNamespace(
            screen=self.screen, settings=self.settings), "Play")

    def test_button_and_label_are_centered(self) -> None:
        self.assertEqual(self.button.rect.size, (200, 50))
        self.assertEqual(self.button.rect.center, self.screen.get_rect().center)
        self.assertEqual(self.button.message_rect.center, self.button.rect.center)

    def test_label_uses_a_transparent_background(self) -> None:
        self.assertEqual(self.button.message_image.get_at((0, 0)).a, 0)

    def test_hit_test_includes_only_points_inside_rectangle(self) -> None:
        rect = self.button.rect
        self.assertTrue(self.button.check_clicked(rect.center))
        self.assertTrue(self.button.check_clicked(rect.topleft))
        self.assertFalse(self.button.check_clicked(rect.bottomright))
        self.assertFalse(self.button.check_clicked((0, 0)))

    def test_drawing_preserves_the_surrounding_background(self) -> None:
        background_color = (12, 23, 34)
        self.screen.fill(background_color)
        self.button.draw()
        self.assertEqual(self.screen.get_at((0, 0))[:3], background_color)
        self.assertEqual(self.screen.get_at(self.button.rect.topleft)[:3],
                         self.settings.button_color)


if __name__ == '__main__':
    unittest.main()
