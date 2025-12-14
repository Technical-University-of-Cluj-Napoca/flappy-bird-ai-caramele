import pygame
import components

pygame.init()
SCREEN_WIDTH = 550
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
ground = components.Ground(SCREEN_WIDTH)

pygame.display.set_caption("Flappy Bird")

pipes = []

BACKGROUND_IMG = pygame.image.load("assets/sky.png").convert()
BACKGROUND_IMG = pygame.transform.scale(BACKGROUND_IMG, (SCREEN_WIDTH, SCREEN_HEIGHT))

BACKGROUND_IMG_NIGHT = pygame.image.load("assets/night_sky.png").convert()
BACKGROUND_IMG_NIGHT = pygame.transform.scale(BACKGROUND_IMG_NIGHT, (SCREEN_WIDTH, SCREEN_HEIGHT))

GROUND_IMG = pygame.image.load("assets/ground.png").convert_alpha()
scale_factor = SCREEN_WIDTH / GROUND_IMG.get_width()
GROUND_HEIGHT = int(GROUND_IMG.get_height() * scale_factor)
GROUND_IMG = pygame.transform.scale(GROUND_IMG, (SCREEN_WIDTH, GROUND_HEIGHT))
GROUND_Y = SCREEN_HEIGHT - GROUND_HEIGHT
GROUND_SPEED = 1

# TITLE_FONT = pygame.font.SysFont("Arial", 64, bold=True)
TITLE_FONT = pygame.font.Font("assets/fonts/LuckiestGuy-Regular.ttf", 64)
def load_score(file):
    try:
        with open(file, "r") as f:
            return int(f.read())
    except:
        return 0

def save_score(score, file):
    with open(file, "w") as f:
        f.write(str(score))

HIGH_SCORE = load_score("score.txt")
HIGH_SCORE_AUTO = load_score("score_auto.txt")