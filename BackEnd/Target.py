import pygame

#class
class Target:
    """
    A class to represent a moving target in a game.

    Attributes:
        x (int): The x-coordinate of the target.
        y (int): The y-coordinate of the target.
        image (pygame.Surface): The image of the target.
        speed_multiplier (float): The multiplier for the target's speed.
        rect (pygame.Rect): The rectangular area for collision detection.
    """
    def __init__(self, x, y, image, speed_multiplier=1):
        self.x = x
        self.y = y
        self.image = image
        self.speed_multiplier = speed_multiplier
        self.rect = pygame.Rect(x + 20, y, 60, 60)

    def move(self, width):
        """
        Updates the position of the target by moving it to the left.
        If the target moves off the screen (beyond the left boundary),
        it reappears on the right side of the screen.

        :param width: The width of the screen, used to reset the position when the target goes off-screen.
        :return: None
        """
        self.x -= 2 ** self.speed_multiplier
        if self.x < -150:
            self.x = width
        self.rect.x = self.x + 20

    def draw(self, screen):
        """
        Draws the target image on the screen at its current position.

        :param screen: The game screen where the target is drawn.
        :return: None
        """
        screen.blit(self.image, (self.x, self.y))

