import pygame
import random


class Ground:
    ground_level = 539

    def __init__(self, win_width):
        self.x, self.y = 0, Ground.ground_level
        self.rect = pygame.Rect(self.x, self.y, win_width, 5)

    def draw(self, window):
        pygame.draw.rect(window, (255, 255, 255), self.rect)

class Pipes:
    width = 100
    opening = 150#bigger gap in the pipes

    pipe_img = pygame.image.load("assets/pipe.png")

    def __init__(self, screen_width):
        self.x = screen_width
        self.bottom_height = random.randint(10, 300)
        self.top_height = Ground.ground_level - self.bottom_height - self.opening
        self.bottom_rect = self.top_rect = pygame.Rect(0, 0, 0, 0), pygame.Rect(0, 0, 0, 0)
        self.passed = False
        self.off_screen = False
        self.counted = False

        self.move_gap = False
        self.gap_dir = random.choice([-1, 1])
        self.gap_speed = 0.6
        self.gap_range = 60
        self.gap_shift = 0
        self._base_bottom_height = self.bottom_height

        self.bottom_pipe_img = pygame.transform.scale(Pipes.pipe_img, (self.width, self.bottom_height))
        self.top_pipe_img = pygame.transform.scale(Pipes.pipe_img, (self.width, self.top_height))
        self.top_pipe_img = pygame.transform.flip(self.top_pipe_img, False,True)

    def draw(self, screen):
        self.bottom_rect = pygame.Rect(self.x, Ground.ground_level - self.bottom_height, self.width, self.bottom_height)
        self.top_rect = pygame.Rect(self.x, 0, self.width, self.top_height)
        screen.blit(self.bottom_pipe_img, self.bottom_rect)
        screen.blit(self.top_pipe_img, self.top_rect)

    def update(self):
        self.x -= 3
        self.update_moving_gap()
        if self.x + Pipes.width <= 30:
            self.passed = True
        if self.x <= -self.width:
            self.off_screen = True

    def update_moving_gap(self):
        if not self.move_gap:
            return

        self.gap_shift += self.gap_dir * self.gap_speed
        if abs(self.gap_shift) > self.gap_range:
            self.gap_dir *= -1

        new_bottom = int(self._base_bottom_height + self.gap_shift)

        min_h = 10
        max_bottom = Ground.ground_level - self.opening - min_h
        if new_bottom < min_h:
            new_bottom = min_h
        elif new_bottom > max_bottom:
            new_bottom = max_bottom

        self.bottom_height = new_bottom
        self.top_height = Ground.ground_level - self.bottom_height - self.opening

        self.bottom_pipe_img = pygame.transform.scale(Pipes.pipe_img, (self.width, self.bottom_height))
        self.top_pipe_img = pygame.transform.scale(Pipes.pipe_img, (self.width, self.top_height))
        self.top_pipe_img = pygame.transform.flip(self.top_pipe_img, False, True)

