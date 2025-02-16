import pytest
from unittest.mock import patch, MagicMock
from BackEnd.SoundManager import SoundManager

@pytest.fixture(autouse=True)
def mock_pygame_mixer():
    """Фікстура для мокування pygame.mixer"""
    with patch('pygame.mixer.init'), \
            patch('pygame.mixer.Sound'), \
            patch('pygame.mixer.Channel'):
        yield

@pytest.fixture(autouse=True)
def init_pygame():
    """Фікстура для ініціалізації та завершення роботи pygame для кожного тесту"""
    with patch('pygame.init'), \
            patch('pygame.quit'):
        yield

def test_load_sounds():
    """Тест перевіряє завантаження звуків у менеджер звуків"""
    with patch('pygame.mixer.Sound') as mock_sound:
        # Arrange
        mock_sound.return_value = MagicMock()
        sound_manager = SoundManager()

        # Act
        sound_manager.load_sounds()

        # Assert
        assert len(sound_manager.sounds) == 4
        assert all(sound in sound_manager.sounds for sound in ['monster', 'plate', 'bird', 'laser'])
        assert mock_sound.call_count == 8

def test_play_sound():
    """Тест перевіряє відтворення звуку за запитом"""
    with patch('pygame.mixer.Sound') as mock_sound:
        # Arrange
        mock_sound_instance = MagicMock()
        mock_sound.return_value = mock_sound_instance
        sound_manager = SoundManager()
        sound_manager.load_sounds()

        # Act
        sound_manager.play_sound('monster')

        # Assert
        mock_sound_instance.play.assert_called_once()

def test_play_nonexistent_sound():
    """Тест перевіряє, що метод play не викликається для неіснуючого звуку"""
    with patch('pygame.mixer.Sound') as mock_sound:
        # Arrange
        sound_manager = SoundManager()
        sound_manager.load_sounds()

        # Act
        sound_manager.play_sound('nonexistent')

        # Assert
        mock_sound.return_value.play.assert_not_called()

if __name__ == '__main__':
    pytest.main(['-v'])