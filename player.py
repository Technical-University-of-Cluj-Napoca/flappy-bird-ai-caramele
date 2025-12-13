import random
import pygame
import config
import brain

class Player:
    def __init__(self):
        self.x , self.y = 50, 200
        self.color = random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)
        self.rect = pygame.Rect(self.x, self.y, 50, 50)

        self.img = pygame.image.load("assets/bird.png").convert_alpha()
        self.img = pygame.transform.scale(self.img, (50, 50))

        self.velocity = 0
        self.flap = False
        self.alive = True
        self.lifespan = 0
        self.fitness = 0

        #AI
        self.decision = None
        self.vision = [0.5, 1, 0.5]
        self.inputs = 3
        self.brain = brain.Brain(self.inputs)
        self.brain.generate_network()



    def draw(self, screen):
        #pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.img, self.rect)

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
            self.lifespan += 1
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

    def calculate_fitness(self):
        self.fitness = self.lifespan

    def clone(self):
        clone = Player()
        clone.fitness = self.fitness
        clone.brain = self.brain.clone()
        clone.brain.generate_network()
        return clone
    
class Bird:
    def __init__(self, x, y, width=50, height = 50):
        self.x = x
        self.y = y
        self.img = pygame.image.load("assets/bird.png").convert_alpha()
    
        self.img = pygame.transform.scale(self.img, (width, height))
        self.float_offset = 0  
        self.float_dir = 1    
        self.float_speed = 0.5 
        self.float_range = 10  

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y + self.float_offset))

    
    def flop(self):
        '''
        function for bird to float up and down during the tutorial
        '''
        self.float_offset += self.float_dir * self.float_speed
        if self.float_offset > self.float_range or self.float_offset < -self.float_range:
            self.float_dir *= -1


class ManualBird(Bird):
    def __init__(self, x, y, width=50, height = 50):
        super().__init__(x, y, width, height)

        self.vel = 0
        self.gravity = 0.2
        self.jump_strength = -5
        
        self.rect = pygame.Rect(self.x, self.y, width - 10, height - 20)
    
    def update(self):
        self.float_offset = 0

        #bird pulled down by gravity
        self.vel += self.gravity

        self.y += self.vel#move forward
        self.rect.y = self.y #update collision box

    def jump(self):
        self.vel = self.jump_strength
        self.y += self.vel
    
    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))

    #function to check for ground collision
    def hit_ground(self):
        return self.rect.bottom >= config.GROUND_Y - 1
    
    
    def hit_pipe(self):
        for pipe in config.pipes:
            if self.rect.colliderect(pipe.top_rect) or \
                self.rect.colliderect(pipe.bottom_rect):
                return True
        return False