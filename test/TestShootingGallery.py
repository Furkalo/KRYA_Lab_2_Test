import unittest
import pygame
from unittest.mock import MagicMock, patch
from BackEnd.Gun import Gun
from BackEnd.ResourceManager import ResourceManager
from BackEnd.ScoreManager import ScoreManager
from BackEnd.SoundManager import SoundManager
from BackEnd.ShootingGallery import ShootingGallery
import os


class TestShootingGallery(unittest.TestCase):
    def setUp(self):
        pygame.init()
        pygame.mixer.init()
        os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

        # Mock necessary dependencies
        self.mock_resource_manager = MagicMock(spec=ResourceManager)
        self.mock_sound_manager = MagicMock(spec=SoundManager)
        self.mock_score_manager = MagicMock(spec=ScoreManager)
        self.mock_gun = MagicMock(spec=Gun)

        # Setup return values for mocked methods
        self.mock_resource_manager.load_image.return_value = pygame.Surface((1, 1))
        self.mock_score_manager.update_best_scores.return_value = False

        # Patch SoundManager and pygame.mixer.Sound to prevent file loading
        with patch("BackEnd.SoundManager.SoundManager", return_value=self.mock_sound_manager), \
                patch("pygame.mixer.Sound", return_value=MagicMock()):
            self.game = ShootingGallery()

        # Replace managers with mocks
        self.game.resource_manager = self.mock_resource_manager
        self.game.sound_manager = self.mock_sound_manager
        self.game.score_manager = self.mock_score_manager
        self.game.gun = self.mock_gun

        # Replace the screen with a mock surface
        self.game.screen = pygame.Surface((self.game.WIDTH, self.game.HEIGHT))

    def tearDown(self):
        pygame.quit()
        pygame.mixer.quit()

    def test_initialization(self):
        """Test game initialization"""
        self.assertEqual(self.game.WIDTH, 900)
        self.assertEqual(self.game.HEIGHT, 800)
        self.assertEqual(self.game.level, 0)
        self.assertEqual(self.game.mode, 0)
        self.assertEqual(self.game.points, 0)
        self.assertTrue(self.game.menu)
        self.assertFalse(self.game.game_over)
        self.assertEqual(self.game.fps, 60)

    @patch("pygame.mixer.Sound", return_value=MagicMock())
    def test_mode_select_free_play(self, mock_sound):
        """Test free play mode selection"""
        self.game.mode_select(0)
        self.assertEqual(self.game.mode, 0)
        self.assertEqual(self.game.level, 1)
        self.assertFalse(self.game.menu)
        self.assertEqual(self.game.ammo, 0)
        self.assertEqual(self.game.time_remaining, 0)

    @patch("pygame.mixer.Sound", return_value=MagicMock())
    def test_mode_select_ammo_mode(self, mock_sound):
        """Test ammo mode selection"""
        self.game.mode_select(1)
        self.assertEqual(self.game.mode, 1)
        self.assertEqual(self.game.level, 1)
        self.assertFalse(self.game.menu)
        self.assertEqual(self.game.ammo, 81)

    @patch("pygame.mixer.Sound", return_value=MagicMock())
    def test_mode_select_timed_mode(self, mock_sound):
        """Test timed mode selection"""
        self.game.mode_select(2)
        self.assertEqual(self.game.mode, 2)
        self.assertEqual(self.game.level, 1)
        self.assertFalse(self.game.menu)
        self.assertEqual(self.game.time_remaining, 30)

    def test_reset_game_state(self):
        """Test game state reset"""
        # Set non-default values
        self.game.level = 2
        self.game.points = 100
        self.game.ammo = 50
        self.game.menu = False
        self.game.game_over = True

        # Reset state
        self.game.reset_game_state()

        # Verify reset values
        self.assertEqual(self.game.level, 0)
        self.assertEqual(self.game.points, 0)
        self.assertEqual(self.game.ammo, 0)
        self.assertTrue(self.game.menu)
        self.assertFalse(self.game.game_over)
        self.assertTrue(self.game.new_coords)

    def test_handle_event_quit(self):
        """Test quit event handling"""
        event = MagicMock()
        event.type = pygame.QUIT
        result = self.game.handle_event(event)
        self.assertFalse(result)

    def test_handle_event_mouse_click(self):
        """Test mouse click event handling"""
        event = MagicMock()
        event.type = pygame.MOUSEBUTTONDOWN
        event.button = 1

        # Mock mouse position for shooting
        with patch('pygame.mouse.get_pos', return_value=(100, 100)):
            result = self.game.handle_event(event)
            self.assertTrue(result)
            self.assertTrue(self.game.shot)
            self.assertEqual(self.game.total_shots, 1)

    def test_pause_functionality(self):
        """Test pause functionality"""
        self.game.level = 2
        self.game.pause = True
        self.game.resume_level = 2

        self.game.resume_game()

        self.assertFalse(self.game.pause)
        self.assertEqual(self.game.level, 2)
        self.assertTrue(self.game.clicked)

    def test_return_to_menu(self):
        """Test return to menu functionality"""
        self.game.game_over = True
        self.game.pause = True

        self.game.return_to_menu()

        self.assertFalse(self.game.game_over)
        self.assertFalse(self.game.pause)
        self.assertTrue(self.game.menu)

    def test_initialize_targets(self):
        """Test target initialization"""
        # Test Level 1
        self.game.level = 1
        self.game.initialize_targets()
        self.assertEqual(len(self.game.target_coords), 3)
        self.assertEqual(len(self.game.target_coords[0]), 10)
        self.assertEqual(len(self.game.target_coords[1]), 5)
        self.assertEqual(len(self.game.target_coords[2]), 3)

        # Test Level 2
        self.game.level = 2
        self.game.initialize_targets()
        self.assertEqual(len(self.game.target_coords), 3)
        self.assertEqual(len(self.game.target_coords[0]), 12)
        self.assertEqual(len(self.game.target_coords[1]), 8)
        self.assertEqual(len(self.game.target_coords[2]), 5)

    def test_update_game_state(self):
        """Test game state update"""
        self.game.level = 1
        self.game.new_coords = True

        self.game.update_game_state()

        self.assertFalse(self.game.new_coords)
        self.assertFalse(self.game.game_over)

    def test_game_over_conditions(self):
        """Test game over conditions"""
        # Test ammo mode game over
        self.game.mode = 1
        self.game.level = 1
        self.game.ammo = 0
        self.game.check_level_completion()
        self.assertTrue(self.game.game_over)

        # Reset and test timed mode game over
        self.game.game_over = False
        self.game.mode = 2
        self.game.time_remaining = 0
        self.game.check_level_completion()
        self.assertTrue(self.game.game_over)


if __name__ == '__main__':
    unittest.main()