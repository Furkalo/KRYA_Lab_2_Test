import pytest

from unittest.mock import patch, MagicMock

from BackEnd.SoundManager import SoundManager


@pytest.fixture
def sound_manager():
    with patch('pygame.mixer.init'), patch('pygame.mixer.Sound') as mock_sound:
        mock_sound.return_value = MagicMock()
        return SoundManager()

def test_load_sounds(sound_manager):
    assert len(sound_manager.sounds) == 4  # Переконуємось, що всі звуки завантажились
    for sound in sound_manager.sounds.values():
        assert isinstance(sound, MagicMock)  # Моки використовуються замість реальних звуків

def test_play_sound(sound_manager):
    sound_name = 'monster'
    sound_manager.play_sound(sound_name)

    sound_manager.sounds[sound_name].play.assert_called_once()  # Перевіряємо виклик play()

def test_play_sound_not_loaded(sound_manager):
    with patch('builtins.print') as mock_print:
        sound_manager.play_sound('non_existing_sound')
        mock_print.assert_not_called()  # Не повинно бути помилок або друку