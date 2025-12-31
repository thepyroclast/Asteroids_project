#file containing code for shooting gun 
from circleshape import CircleShape
from constants import SHOT_RADIUS, LINE_WIDTH, BIG_SHOT_RADIUS
import pygame
import random


class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)
        self.color = (255, 102, 153)
    def draw(self, screen):
            pygame.draw.circle(screen, self.color, self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
         self.position += self.velocity * dt

    def split(self):
         self.kill()
         

class Bigshot(CircleShape):
     def __init__(self, x, y):
        super().__init__(x, y, BIG_SHOT_RADIUS)
        self.color = (225, 102, 153)

     def draw(self, screen):
          pygame.draw.circle(screen, self.color, self.position, self.radius, LINE_WIDTH)
          
     def update(self, dt):
          self.position += self.velocity * dt
    
     def split(self):
         self.kill()
         angle = random.uniform(20, 50)
         Shot_angle_1 = self.velocity.rotate(angle)
         Shot_angle_2 = self.velocity.rotate(-angle)
         shot_1 = Shot(self.position[0], self.position[1])
         shot_2 = Shot(self.position[0], self.position[1])
         shot_1.velocity =  Shot_angle_1 * 1.2
         shot_2.velocity = Shot_angle_2 * 1.2

