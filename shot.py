#file containing code for shooting gun 
#need to add poison grenades, laser gun, shotgun, homing rocket
from circleshape import CircleShape
from constants import SHOT_RADIUS, LINE_WIDTH, BIG_SHOT_RADIUS
import pygame
import random


class Shot(CircleShape):
    def __init__(self, x, y, color):
        super().__init__(x, y, SHOT_RADIUS)
        self.color = color
        self.counter = 0
     #old color is (255, 102, 153)
    def draw(self, screen):
            pygame.draw.circle(screen, self.color, self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
         self.position += self.velocity * dt
         self.counter += 1 
         if self.counter == 140:
              self.kill()

    def split(self):
         self.kill()
         

class Bigshot(CircleShape):
     def __init__(self, x, y, color):
        super().__init__(x, y, BIG_SHOT_RADIUS)
        self.color = color
        self.counter = 0 

     def draw(self, screen):
          pygame.draw.circle(screen, self.color, self.position, self.radius, LINE_WIDTH)
          
     def update(self, dt):
          self.position += self.velocity * dt
          self.counter += 1
          if self.counter == 110:
               self.kill()
    
     def split(self):
         self.kill()
         angle = random.uniform(20, 50)
         Shot_angle_1 = self.velocity.rotate(angle)
         Shot_angle_2 = self.velocity.rotate(-angle)
         shot_angle_3 = self.velocity.rotate(angle + angle)
         shot_angle_4 = self.velocity.rotate(-angle + -angle)
         shot_1 = Shot(self.position[0], self.position[1], self.color)
         shot_2 = Shot(self.position[0], self.position[1], self.color)
         shot_3 = Shot(self.position[0], self.position[1], self.color)
         shot_4 = Shot(self.position[0], self.position[1], self.color)
         shot_1.velocity =  Shot_angle_1 
         shot_2.velocity = Shot_angle_2 
         shot_3.velocity = shot_angle_3 
         shot_4.velocity = shot_angle_4

class Black_hole(CircleShape):
     def __init__(self, x, y, color):
          super().__init__(x, y, BIG_SHOT_RADIUS * 1.5)
          self.color = color

     def draw(self, screen):
            pygame.draw.circle(screen, self.color, self.position, self.radius, LINE_WIDTH)

     def update(self, dt):
          self.radius += 0.3

     def split(self):
          self.kill()