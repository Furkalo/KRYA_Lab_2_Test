import unittest
from unittest.mock import patch, mock_open, MagicMock

from BackEnd.ScoreManager import ScoreManager


class test_ScoreManager(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data="100\n200\n300\n")
    def test_load_best_scores(self, mock_file):
        """Тест успішного завантаження рекордів з файлу"""
        mock_font = MagicMock()
        sm = ScoreManager(mock_font)

        self.assertEqual(sm.best_freeplay, 100)
        self.assertEqual(sm.best_ammo, 200)
        self.assertEqual(sm.best_timed, 300)
        mock_file.assert_called_once_with("high_scores.txt", "r")

    def test_update_best_scores(self):
        """Тест оновлення рекордів"""
        mock_font = MagicMock()
        sm = ScoreManager(mock_font)

        self.assertTrue(sm.update_best_scores(0, 0, 50))  # Очікується оновлення Freeplay
        self.assertEqual(sm.best_freeplay, 50)

        self.assertTrue(sm.update_best_scores(1, 300, 0))  # Очікується оновлення Ammo
        self.assertEqual(sm.best_ammo, 300)

        self.assertTrue(sm.update_best_scores(2, 400, 0))  # Очікується оновлення Timed
        self.assertEqual(sm.best_timed, 400)

        self.assertFalse(sm.update_best_scores(1, 200, 0))  # Не повинно оновитись, бо 200 < 300

if __name__ == "__main__":
    unittest.main()