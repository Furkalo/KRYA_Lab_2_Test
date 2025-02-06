import pygame
from BackEnd.ShootingGallery import ShootingGallery

pygame.init()

if __name__ == "__main__":
    game = ShootingGallery()
    game.run()