import pygame
import components
SCREEN_WIDTH = 550
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
ground = components.Ground(SCREEN_WIDTH)

pipes = []