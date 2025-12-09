import random
import pygame
import config
import brain

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
        self.vision = [0.5, 1, 0.5]
        self.inputs = 3
        self.brain = brain.Brain(self.inputs)
        self.brain.generate_network()



    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def ground_collide(self, ground):
        return pygame.Rect.colliderect(self.rect, ground)
    def sky_collide(self):
        return self.rect.y < 30
    def pipe_collide(self):
        for p in config.pipes:
            if pygame.Rect.colliderect(self.rect, p.top_rect) or pygame.Rect.colliderect(self.rect, p.bottom_rect):
                return True
        return False
    def update(self, ground):
        if not (self.ground_collide(ground) or self.pipe_collide()):
            self.velocity += 0.25
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
        if self.velocity >= 0:
            self.flap = False
    def look(self):
        if config.pipes:
            # Line to top pipe
            self.vision[0] = max(0, self.rect.center[1] - self.closest_pipe().top_rect.bottom) / 500
            pygame.draw.line(config.screen, self.color, self.rect.center,
                             (self.rect.center[0], self.closest_pipe().top_rect.bottom))

            # Line to mid pipe
            self.vision[1] = max(0, self.closest_pipe().x - self.rect.center[0]) / 500
            pygame.draw.line(config.screen, self.color, self.rect.center,
                             (self.closest_pipe().x, self.rect.center[1]))

            # Line to bottom pipe
            self.vision[2] = max(0, self.closest_pipe().bottom_rect.top - self.rect.center[1]) / 500
            pygame.draw.line(config.screen, self.color, self.rect.center,
                             (self.rect.center[0], self.closest_pipe().bottom_rect.top))



    def think(self):
       self.decision = self.brain.feedforward(self.vision)
       if self.decision >= 0.73:
           self.bird_flap()

    @staticmethod
    def closest_pipe():
        for p in config.pipes:
            if not p.passed:
                return p

