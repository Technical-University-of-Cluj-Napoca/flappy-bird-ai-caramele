import random
import pygame
import config

class Player:
    def __init__(self):
        self.x , self.y = 50, 200
        self.color = random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)
        self.rect = pygame.Rect(self.x, self.y, 20, 20)
        self.velocity = 0
        self.flap = False
        self.alive = True

        #AI
        self.decision = None


    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def ground_collide(self, ground):
        return pygame.Rect.colliderect(self.rect, ground)
    def sky_collide(self):
        return self.rect.y < 30
    def pipe_collide(self):
        for p in config.pipes:
            return pygame.Rect.colliderect(self.rect, p.top_rect) or pygame.Rect.colliderect(self.rect, p.bottom_rect)
    def update(self, ground):
        if not (self.ground_collide(ground) or self.pipe_collide()):
            self.velocity += 0.06
            self.rect.y += self.velocity
            if self.velocity > 5:
                self.velocity = 5
        else:
            self.alive = False
            self.velocity = 0
            self.flap = False
    def bird_flap(self):
        if not self.flap and not self.sky_collide():
            self.flap = True
            self.velocity -= 5
        if self.velocity >= 3:
            self.flap = False

    def think(self):
       self.decision = random.uniform(0, 1)
       if self.decision >= 0.73:
           self.bird_flap()




