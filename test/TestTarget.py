import pytest
import pygame
from unittest.mock import MagicMock
from BackEnd.Target import Target  # Припускаємо, що клас Target знаходиться в папці BackEnd

# Фікстура для ініціалізації pygame
@pytest.fixture(autouse=True)
def init_pygame():
    """Фікстура для ініціалізації та завершення роботи pygame для кожного тесту."""
    pygame.init()
    yield
    pygame.quit()

# Тест для перевірки ініціалізації класу Target
def test_target_initialization():
    """Тест перевіряє ініціалізацію об'єкта Target."""
    image = MagicMock()  # Мок для зображення
    target = Target(x=100, y=200, image=image, speed_multiplier=1.5)

    # Перевірка, чи правильно ініціалізовані атрибути
    assert target.x == 100
    assert target.y == 200
    assert target.image == image
    assert target.speed_multiplier == 1.5
    assert isinstance(target.rect, pygame.Rect)  # Перевірка, чи rect є прямокутником

# Тест для перевірки руху цілі (метод move)
def test_target_move():
    """Тест перевіряє рух цілі за допомогою методу move."""
    image = MagicMock()
    target = Target(x=100, y=200, image=image, speed_multiplier=1)

    # Збережемо початкове значення x для порівняння
    initial_x = target.x

    # Викликаємо метод move для оновлення позиції
    target.move(width=500)

    # Перевірка, чи змінилося значення x
    assert target.x == initial_x - 2  # Позиція повинна зменшитися на 2
    assert target.rect.x == target.x + 20  # Перевірка, чи змінився rect

# Тест для перевірки випадку, коли ціль виходить за межі екрана і з'являється з правої сторони
def test_target_move_off_screen():
    """Тест перевіряє, чи ціль з'являється з правої сторони після того, як виходить за межі екрану."""
    image = MagicMock()
    target = Target(x=-200, y=200, image=image, speed_multiplier=1)

    # Викликаємо метод move, щоб перевірити, чи ціль повернеться з правої сторони
    target.move(width=500)

    # Перевірка, чи x знову встановлено на праву сторону екрана
    assert target.x == 500  # Позиція має бути рівною ширині екрану

# Тест для перевірки малювання цілі на екрані
def test_target_draw():
    """Тест перевіряє, чи правильно малюється ціль на екрані."""
    image = MagicMock()
    target = Target(x=100, y=200, image=image, speed_multiplier=1)

    screen = MagicMock()  # Мок для екрану

    # Викликаємо метод draw для малювання цілі
    target.draw(screen)

    # Перевірка, чи був викликаний метод blit з правильними аргументами
    screen.blit.assert_called_once_with(image, (100, 200))

# Запуск тестів
if __name__ == '__main__':
    pytest.main()
