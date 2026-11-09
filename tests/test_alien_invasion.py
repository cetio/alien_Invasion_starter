"""Tests for the Play menu, input guards, and new-run reset."""
import unittest
from unittest.mock import patch

import pygame

from alien_invasion import AlienInvasion


class PlayMenuTests(unittest.TestCase):
    """Exercise game transitions with headless video and audio drivers."""

    def setUp(self) -> None:
        """Create a real game without a window, sound, or reset delay."""
        drivers = patch.dict("os.environ", {
            "SDL_VIDEODRIVER": "dummy",
            "SDL_AUDIODRIVER": "dummy",
        })
        drivers.start()
        self.addCleanup(drivers.stop)
        pause = patch("alien_invasion.sleep")
        pause.start()
        self.addCleanup(pause.stop)
        self.addCleanup(pygame.quit)
        self.game = AlienInvasion()
        pygame.event.clear()

    def _send_event(self, event_type, **attributes) -> None:
        """Process one event through the game's input handler."""
        pygame.event.post(pygame.event.Event(event_type, **attributes))
        self.game._check_input()

    def _click_play(self) -> None:
        """Left-click the button at its displayed position."""
        self._send_event(pygame.MOUSEBUTTONDOWN,
                         pos=self.game.play_button.rect.center, button=1)

    def test_game_opens_on_an_inactive_menu(self) -> None:
        self.assertTrue(self.game.running)
        self.assertFalse(self.game.active)
        self.assertNotIn(self.game.play_button, self.game.entities)

    def test_inactive_screen_draws_button_and_shows_cursor(self) -> None:
        pygame.mouse.set_visible(False)
        self.game._update_screen()
        self.assertTrue(pygame.mouse.get_visible())
        self.assertEqual(self.game.screen.get_at(
            self.game.play_button.rect.topleft)[:3],
            self.game.settings.button_color)

    def test_inactive_loop_keeps_input_and_drawing_but_not_simulation(self) -> None:
        def stop_after_frame():
            self.game.running = False

        with patch.object(self.game, "_check_input") as check_input, \
                patch.object(self.game, "_update_entities") as update, \
                patch.object(self.game, "_check_collisions") as collisions, \
                patch.object(self.game, "_update_screen",
                             side_effect=stop_after_frame) as draw:
            self.game.run_game()
        check_input.assert_called_once_with()
        draw.assert_called_once_with()
        update.assert_not_called()
        collisions.assert_not_called()

    def test_outside_click_does_not_start_game(self) -> None:
        self._send_event(pygame.MOUSEBUTTONDOWN, pos=(0, 0), button=1)
        self.assertFalse(self.game.active)

    def test_non_left_clicks_do_not_start_game(self) -> None:
        for button in (2, 3, 4, 5):
            with self.subTest(button=button):
                self._send_event(
                    pygame.MOUSEBUTTONDOWN,
                    pos=self.game.play_button.rect.center, button=button)
                self.assertFalse(self.game.active)

    def test_play_uses_click_coordinates_and_hides_cursor(self) -> None:
        with patch("pygame.mouse.get_pos", return_value=(0, 0)):
            self._click_play()
        self.assertTrue(self.game.active)
        self.assertFalse(pygame.mouse.get_visible())

    def test_active_screen_does_not_draw_button(self) -> None:
        self._click_play()
        with patch.object(self.game.play_button, "draw") as draw:
            self.game._update_screen()
        draw.assert_not_called()
        self.assertFalse(pygame.mouse.get_visible())

    def test_invisible_button_cannot_restart_active_game(self) -> None:
        self._click_play()
        self.game.game_stats.ships_left = 1
        self.game.ship.x = 100.0
        self.game.ship.fire()
        fleet = tuple(self.game.alien_fleet.fleet)
        bullets = tuple(self.game.arsenal.arsenal)
        self._click_play()
        self.assertEqual(self.game.game_stats.ships_left, 1)
        self.assertEqual(self.game.ship.x, 100.0)
        self.assertEqual(tuple(self.game.alien_fleet.fleet), fleet)
        self.assertEqual(tuple(self.game.arsenal.arsenal), bullets)

    def test_inactive_movement_keydowns_do_not_set_flags(self) -> None:
        for key, flag in ((pygame.K_LEFT, "moving_left"),
                          (pygame.K_RIGHT, "moving_right")):
            with self.subTest(key=key):
                self._send_event(pygame.KEYDOWN, key=key)
                self.assertFalse(getattr(self.game.ship, flag))

    def test_inactive_space_does_not_fire_or_play_sound(self) -> None:
        with patch.object(self.game, "laser_sound") as sound:
            self._send_event(pygame.KEYDOWN, key=pygame.K_SPACE)
        self.assertFalse(self.game.arsenal.arsenal)
        sound.play.assert_not_called()

    def test_inactive_keyups_clear_movement_flags(self) -> None:
        self.game.ship.moving_left = True
        self.game.ship.moving_right = True
        self._send_event(pygame.KEYUP, key=pygame.K_LEFT)
        self._send_event(pygame.KEYUP, key=pygame.K_RIGHT)
        self.assertFalse(self.game.ship.moving_left)
        self.assertFalse(self.game.ship.moving_right)

    def test_active_movement_keys_still_work(self) -> None:
        self._click_play()
        for key, flag in ((pygame.K_LEFT, "moving_left"),
                          (pygame.K_RIGHT, "moving_right")):
            with self.subTest(key=key):
                start_x = self.game.ship.x
                self._send_event(pygame.KEYDOWN, key=key)
                self.assertTrue(getattr(self.game.ship, flag))
                self.game._update_entities()
                self.assertNotEqual(self.game.ship.x, start_x)
                self._send_event(pygame.KEYUP, key=key)
                self.assertFalse(getattr(self.game.ship, flag))

    def test_active_space_still_fires_and_plays_sound(self) -> None:
        self._click_play()
        with patch.object(self.game, "laser_sound") as sound:
            self._send_event(pygame.KEYDOWN, key=pygame.K_SPACE)
        self.assertEqual(len(self.game.arsenal.arsenal), 1)
        sound.play.assert_called_once_with(fade_ms=250)

    def test_quit_key_and_window_close_work_while_inactive(self) -> None:
        for event_type, attributes in (
                (pygame.KEYDOWN, {"key": pygame.K_q}), (pygame.QUIT, {})):
            with self.subTest(event_type=event_type):
                self.game.running = True
                with patch("pygame.quit") as quit_game:
                    with self.assertRaises(SystemExit):
                        self._send_event(event_type, **attributes)
                self.assertFalse(self.game.running)
                quit_game.assert_called_once_with()

    def test_game_over_and_play_restore_a_fresh_run(self) -> None:
        self._click_play()
        self.game.ship.fire()
        old_fleet = tuple(self.game.alien_fleet.fleet)
        old_bullets = tuple(self.game.arsenal.arsenal)
        self.game.ship.x = 100.0
        self.game.ship.rect.x = 100
        self.game.ship.moving_left = True
        self.game.ship.moving_right = True
        self.game.game_stats.ships_left = 1
        self.game._check_game_status()
        self.assertEqual(self.game.game_stats.ships_left, 0)
        self.assertFalse(self.game.active)
        self.game._update_screen()
        self.assertTrue(pygame.mouse.get_visible())

        self._click_play()
        self.assertTrue(self.game.active)
        self.assertFalse(pygame.mouse.get_visible())
        self.assertEqual(self.game.game_stats.ships_left,
                         self.game.settings.starting_ship_count)
        self.assertTrue(old_bullets)
        self.assertFalse(self.game.arsenal.arsenal)
        self.assertEqual(len(self.game.alien_fleet.fleet), len(old_fleet))
        self.assertTrue(set(old_fleet).isdisjoint(self.game.alien_fleet.fleet))
        self.assertEqual(self.game.ship.rect.midbottom,
                         self.game.screen.get_rect().midbottom)
        self.assertEqual(self.game.ship.x, float(self.game.ship.rect.x))
        self.assertFalse(self.game.ship.moving_left)
        self.assertFalse(self.game.ship.moving_right)

    def test_losing_a_ship_does_not_restore_lives_or_show_menu(self) -> None:
        self._click_play()
        self.game._check_game_status()
        self.assertEqual(self.game.game_stats.ships_left,
                         self.game.settings.starting_ship_count - 1)
        self.assertTrue(self.game.active)
        self.assertFalse(pygame.mouse.get_visible())

    def test_clearing_fleet_does_not_restore_lives_or_show_menu(self) -> None:
        self._click_play()
        self.game.game_stats.ships_left = 1
        alien = next(iter(self.game.alien_fleet.fleet))
        self.game.alien_fleet.fleet.empty()
        self.game.alien_fleet.fleet.add(alien)
        self.game.ship.fire()
        bullet = next(iter(self.game.arsenal.arsenal))
        bullet.rect.center = alien.rect.center
        with patch.object(self.game, "impact_sound") as sound:
            self.game._check_collisions()
        sound.play.assert_called_once_with(fade_ms=250)
        self.assertEqual(self.game.game_stats.ships_left, 1)
        self.assertTrue(self.game.active)
        self.assertTrue(self.game.alien_fleet.fleet)
        self.assertFalse(self.game.arsenal.arsenal)
        self.assertFalse(pygame.mouse.get_visible())


if __name__ == '__main__':
    unittest.main()
