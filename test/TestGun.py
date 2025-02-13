import pytest
import pygame
from BackEnd.Gun import Gun  # Assuming your Gun class is in the gun.py file

@pytest.fixture
def setup_gun():
    """Fixture to set up the Gun object and related properties."""
    pygame.init()
    width = 800
    height = 600
    gun_images = [pygame.Surface((50, 50)) for _ in range(3)]  # Mocks for images
    gun = Gun(width, height, gun_images)
    return gun, width, height

def test_calculate_rotation(setup_gun):
    """Tests the correct calculation of the rotation angle of the gun."""
    gun, width, height = setup_gun
    mouse_pos = (width // 2 + 1, height - 250)  # Slight shift to the right to avoid division by 0
    angle = gun.calculate_rotation(mouse_pos)
    assert -90 <= angle <= 90, f"Expected angle to be between -90 and 90, but got {angle}"

def test_lasers_colors(setup_gun):
    """Tests that the laser color list is correct."""
    gun, _, _ = setup_gun
    assert gun.lasers == ['red', 'purple', 'green'], f"Expected laser colors to be ['red', 'purple', 'green'], but got {gun.lasers}"

def test_draw(setup_gun):
    """Tests that the draw method doesn't throw errors when drawing."""
    gun, width, height = setup_gun
    screen = pygame.Surface((width, height))
    mouse_pos = (width // 2, height // 2)
    try:
        gun.draw(screen, level=1, mouse_pos=mouse_pos)
    except Exception as e:
        pytest.fail(f"draw method raised an exception: {e}")


if __name__ == "__main__":
    pytest.main()
