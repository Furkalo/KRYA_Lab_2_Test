import unittest
from unittest.mock import patch, MagicMock

from BackEnd.ResourceManager import ResourceManager


class TestResourceManager(unittest.TestCase):

    @patch("pygame.image.load")
    def test_load_image_success(self, mock_load):
        """Тест успішного завантаження зображення"""
        mock_image = MagicMock()
        mock_load.return_value = mock_image

        result = ResourceManager.load_image("test_image.png")
        self.assertEqual(result, mock_image)
        mock_load.assert_called_once_with("test_image.png")

    @patch("pygame.font.Font")
    def test_load_font_success(self, mock_font):
        """Тест успішного завантаження шрифту"""
        mock_font_instance = MagicMock()
        mock_font.return_value = mock_font_instance

        result = ResourceManager.load_font("test_font.ttf", 20)
        self.assertEqual(result, mock_font_instance)
        mock_font.assert_called_once_with("test_font.ttf", 20)


if __name__ == "__main__":
    unittest.main()
