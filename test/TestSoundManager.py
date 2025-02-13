import pytest
import pygame
from unittest.mock import patch, MagicMock
from BackEnd.SoundManager import SoundManager

# Фікстура для ініціалізації та завершення роботи pygame перед кожним тестом
@pytest.fixture(autouse=True)
def init_pygame():
    """Фікстура для ініціалізації та завершення роботи pygame для кожного тесту."""
    pygame.init()  # Ініціалізація pygame
    yield  # Виконання тесту
    pygame.quit()  # Завершення роботи pygame після тесту

# Тест для перевірки завантаження звуків
@patch('pygame.mixer.Sound')
def test_load_sounds(mock_sound):
    """Тест перевіряє завантаження звуків у менеджер звуків."""
    # Arrange: Підготовка мок-об'єкта для pygame.mixer.Sound
    mock_sound.return_value = MagicMock()
    sound_manager = SoundManager()  # Створення об'єкта менеджера звуків

    # Act: Завантаження всіх звуків
    sound_manager.load_sounds()

    # Assert: Перевірка, що звуки були завантажені
    assert len(sound_manager.sounds) == 4  # Має бути 4 звуки
    assert 'monster' in sound_manager.sounds  # Перевірка, чи є звук 'monster'
    assert 'plate' in sound_manager.sounds  # Перевірка, чи є звук 'plate'
    assert 'bird' in sound_manager.sounds  # Перевірка, чи є звук 'bird'
    assert 'laser' in sound_manager.sounds  # Перевірка, чи є звук 'laser'

    # Перевірка, що метод Sound був викликаний 8 разів (для кожного звуку)
    assert mock_sound.call_count == 8

# Тест для перевірки відтворення звуку
@patch('pygame.mixer.Sound')
def test_play_sound(mock_sound):
    """Тест перевіряє відтворення звуку за запитом."""
    # Arrange: Підготовка мок-об'єкта для pygame.mixer.Sound
    mock_sound_instance = MagicMock()
    mock_sound.return_value = mock_sound_instance
    sound_manager = SoundManager()  # Створення об'єкта менеджера звуків
    sound_manager.load_sounds()  # Завантаження всіх звуків

    # Act: Виконання відтворення звуку 'monster'
    sound_manager.play_sound('monster')

    # Assert: Перевірка, що метод play був викликаний один раз
    mock_sound_instance.play.assert_called_once()

# Тест для перевірки поведінки при спробі відтворити неіснуючий звук
@patch('pygame.mixer.Sound')
def test_play_nonexistent_sound(mock_sound):
    """Тест перевіряє, що метод play не викликається для неіснуючого звуку."""
    # Arrange: Створення об'єкта менеджера звуків
    sound_manager = SoundManager()
    sound_manager.load_sounds()  # Завантаження всіх звуків

    # Act: Виконання спроби відтворити неіснуючий звук 'nonexistent'
    sound_manager.play_sound('nonexistent')

    # Assert: Перевірка, що метод play не був викликаний
    mock_sound.return_value.play.assert_not_called()

# Запуск тестів, якщо файл виконується безпосередньо
if __name__ == '__main__':
    pytest.main()
