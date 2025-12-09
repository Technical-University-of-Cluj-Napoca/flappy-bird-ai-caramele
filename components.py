import pygame
import random

class Ground:
    ground_level = 500

    def __init__(self, win_width):
        self.x, self.y = 0, Ground.ground_level
        self.rect = pygame.Rect(self.x, self.y, win_width, 5)

    def draw(self, window):
        pygame.draw.rect(window, (255, 255, 255), self.rect)

class Pipes:
    width = 100
    opening = 100

    pipe_img = pygame.image.load("assets/pipe.png")

    def __init__(self, screen_width):
        self.x = screen_width
        self.bottom_height = random.randint(10, 300)
        self.top_height = Ground.ground_level - self.bottom_height - self.opening
        self.bottom_rect = self.top_rect = pygame.Rect(0, 0, 0, 0), pygame.Rect(0, 0, 0, 0)
        self.passed = False
        self.off_screen = False

        self.bottom_pipe_img = pygame.transform.scale(Pipes.pipe_img, (self.width, self.bottom_height))
        self.top_pipe_img = pygame.transform.scale(Pipes.pipe_img, (self.width, self.top_height))
        self.top_pipe_img = pygame.transform.flip(self.top_pipe_img, False,True)

    def draw(self, screen):
        self.bottom_rect = pygame.Rect(self.x, Ground.ground_level - self.bottom_height, self.width, self.bottom_height)
        self.top_rect = pygame.Rect(self.x, 0, self.width, self.top_height)
        screen.blit(self.bottom_pipe_img, self.bottom_rect)
        screen.blit(self.top_pipe_img, self.top_rect)

    def update(self):
        self.x -= 1
        if self.x + Pipes.width <= 30:
            self.passed = True
        if self.x <= -self.width:
            self.off_screen = True

