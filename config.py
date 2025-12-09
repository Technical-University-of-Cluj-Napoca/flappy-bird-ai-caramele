import pygame
import components

pygame.init()
SCREEN_WIDTH = 550
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
ground = components.Ground(SCREEN_WIDTH)

pygame.display.set_caption("Flappy Bird")

pipes = []

BACKROUND_IMG = pygame.image.load("assets/sky.png").convert()
BACKROUND_IMG = pygame.transform.scale(BACKROUND_IMG, (SCREEN_WIDTH, SCREEN_HEIGHT))

GROUND_IMG = pygame.image.load("assets/ground.png").convert_alpha()
scale_factor = SCREEN_WIDTH / GROUND_IMG.get_width()
GROUND_HEIGHT = int(GROUND_IMG.get_height() * scale_factor)
GROUND_IMG = pygame.transform.scale(GROUND_IMG, (SCREEN_WIDTH, GROUND_HEIGHT))
GROUND_Y = SCREEN_HEIGHT - GROUND_HEIGHT
GROUND_SPEED = 1

TITLE_FONT = pygame.font.SysFont("Arial", 64, bold=True)