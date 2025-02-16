import pytest
import pygame
from unittest.mock import patch, MagicMock

from BackEnd.ResourceManager import ResourceManager

@pytest.fixture(scope="module")
def pygame_init():
    pygame.init()
    yield
    pygame.quit()

class TestResourceManager:
    def setup_method(self):
        # Create test image and font paths
        self.test_image_path = "test_image.png"
        self.test_font_path = "test_font.ttf"
        self.invalid_path = "nonexistent_file.xyz"

    def test_load_image_success(self, pygame_init):
        # Create a mock surface
        mock_surface = pygame.Surface((100, 100))

        with patch('pygame.image.load') as mock_load:
            mock_load.return_value = mock_surface

            # Test loading without scaling
            result = ResourceManager.load_image(self.test_image_path)
            assert result is not None
            assert isinstance(result, pygame.Surface)
            mock_load.assert_called_once_with(self.test_image_path)

    def test_load_image_with_scale(self, pygame_init):
        mock_surface = pygame.Surface((100, 100))
        scale = (50, 50)

        with patch('pygame.image.load') as mock_load:
            mock_load.return_value = mock_surface

            result = ResourceManager.load_image(self.test_image_path, scale)
            assert result is not None
            assert isinstance(result, pygame.Surface)
            assert result.get_size() == scale

    def test_load_image_failure(self, pygame_init):
        with patch('pygame.image.load') as mock_load:
            mock_load.side_effect = pygame.error("Test error")

            result = ResourceManager.load_image(self.invalid_path)
            assert result is None

    def test_load_font_success(self, pygame_init):
        mock_font = MagicMock()
        font_size = 24

        with patch('pygame.font.Font') as mock_font_load:
            mock_font_load.return_value = mock_font

            result = ResourceManager.load_font(self.test_font_path, font_size)
            assert result is not None
            mock_font_load.assert_called_once_with(self.test_font_path, font_size)

    def test_load_font_failure_with_fallback(self, pygame_init):
        font_size = 24
        mock_font = MagicMock()

        with patch('pygame.font.Font') as mock_font_load:

            mock_font_load.side_effect = [pygame.error("Test error"), mock_font]

            result = ResourceManager.load_font(self.invalid_path, font_size)
            assert result is not None

            assert mock_font_load.call_count == 2
            mock_font_load.assert_called_with(None, font_size)


