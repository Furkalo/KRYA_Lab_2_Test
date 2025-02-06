import math
import pygame

class Gun:
    """
     The Gun class represents a gun in a 2D game that can rotate based on the mouse position
    and fire lasers of different colors based on the current level.

    """
    def __init__(self, width, height, gun_images):
        """
        Initialize the gun's properties such as width, height, and gun images for each level

        :param width: The width of the screen.
        :param height: The height of the screen.
        :param gun_images: A list of images representing the gun for each level
        """
        self.width = width
        self.height = height
        self.gun_images = gun_images
        self.lasers = ['red', 'purple', 'green']

    def calculate_rotation(self, mouse_pos):
        """
        Calculates the rotation angle required for the gun to point towards the mouse position.

        :param mouse_pos:  The current position of the mouse (x, y)
        :return: The rotation angle in degrees that the gun needs to rotate to aim at the mouse.
        """
        gun_point = (self.width / 2, self.height - 200)

        if mouse_pos[0] != gun_point[0]:
            slope = (mouse_pos[1] - gun_point[1]) / (mouse_pos[0] - gun_point[0])
        else:
            slope = -100000

        angle = math.atan(slope)
        return math.degrees(angle)


    def draw(self, screen, level, mouse_pos):
        """
        Draws the gun rotated according to the mouse position, and fires a laser if the mouse button is pressed.

        :param screen: The surface to draw the gun on.
        :param level: The current level of the game that determines the gun and laser color.
        :param mouse_pos: The current position of the mouse (x, y).
        :return: None
        """
        rotation = self.calculate_rotation(mouse_pos)
        gun_point = (self.width / 2, self.height - 200)

        if mouse_pos[0] < self.width / 2:
            gun = pygame.transform.flip(self.gun_images[level - 1], True, False)
            if mouse_pos[1] < 600:
                rotated_gun = pygame.transform.rotate(gun, 90 - rotation)
                screen.blit(rotated_gun, (self.width / 2 - 90, self.height - 250))

                clicks = pygame.mouse.get_pressed()
                if clicks[0]:
                    pygame.draw.circle(screen, self.lasers[level - 1], mouse_pos, 5)
        else:
            gun = self.gun_images[level - 1]
            if mouse_pos[1] < 600:
                rotated_gun = pygame.transform.rotate(gun, 270 - rotation)
                screen.blit(rotated_gun, (self.width / 2 - 30, self.height - 250))

                clicks = pygame.mouse.get_pressed()
                if clicks[0]:
                    pygame.draw.circle(screen, self.lasers[level - 1], mouse_pos, 5)

