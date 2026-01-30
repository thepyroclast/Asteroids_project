#the file containing the asteroids
import pygame
from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS, ASTEROID_KINDS
from logger import log_event
import random

class Asteroid(CircleShape):
    def __init__(self, x, y, radius, color, size):
        super().__init__(x, y, radius)
        self.color = color
        self.health = size
        self.size = size 

    def make_points(self, position, radius, health):
         point1 = (position[0], position[1] - (radius))
         point2 = (position[0] - (radius * 0.1), position[1] - (radius * 0.7))
         point3 = (position[0] + (radius * 0.1), position[1] - (radius * 0.6))
         point4 = (position[0] + (radius * 0.3), position[1] - (radius * 0.2))
         point5 = (position[0], position[1] - (radius * 0.1))
         point6 = (position[0] + (radius * 0.1), position[1] + (radius * 0.1))
         if health <= 1:
              list_of_points = [point1, point2, point3, point4, point5, point6]
              return list_of_points
         if health == 2:
              list_of_points = [point1, point2, point3, point4]
              return list_of_points
         if health == 3: 
              list_of_points = [point1, point2, point3]
              return list_of_points
         else:
              raise Exception("incorrectly making points")

    
    def draw(self, screen):
            pygame.draw.circle(screen, self.color, self.position, self.radius, LINE_WIDTH)
            if self.health < self.size:
                 cracks = self.make_points(self.position, self.radius, self.health)
                 pygame.draw.lines(screen, self.color, False, cracks, 2)

    def update(self, dt):
         self.position += self.velocity * dt
              
    def split(self):
         self.kill()
         if self.color == (229, 72, 242):
              power_up = PowerUp(self.position[0], self.position[1], 15, (228, 0, 134))
         if self.radius <= ASTEROID_MIN_RADIUS:
              return
         log_event("asteroid_split")
         angle = random.uniform(20, 50)
         asteroid_angle_1 = self.velocity.rotate(angle)
         asteroid_angle_2 = self.velocity.rotate(-angle)
         new_radius = self.radius - ASTEROID_MIN_RADIUS
         asteroid_1 = Asteroid(self.position[0], self.position[1], new_radius, (222, 214, 173), self.size - 1)
         asteroid_2 = Asteroid(self.position[0], self.position[1], new_radius, (222, 214, 173), self.size - 1)
         asteroid_1.velocity = asteroid_angle_1 * 1.2
         asteroid_2.velocity = asteroid_angle_2 * 1.2

class PowerUp(CircleShape):
     def __init__(self, x, y, radius, color ):
          super().__init__(x, y, radius,)
          self.color = color 

     def draw(self, screen):
          pygame.draw.circle(screen, self.color, self.position, self.radius, LINE_WIDTH)

     def split(self):
          self.kill()
