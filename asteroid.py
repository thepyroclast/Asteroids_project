#the file containing the asteroids
import pygame
from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS
from logger import log_event
import random

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
    
    def draw(self, screen):
            pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
         self.position += self.velocity * dt
         
    def split(self):
         self.kill()
         if self.radius <= ASTEROID_MIN_RADIUS:
              return
         log_event("asteroid_split")
         angle = random.uniform(20, 50)
         asteroid_angle_1 = self.velocity.rotate(angle)
         asteroid_angle_2 = self.velocity.rotate(-angle)
         new_radius = self.radius - ASTEROID_MIN_RADIUS
         asteroid_1 = Asteroid(self.position[0], self.position[1], new_radius)
         asteroid_2 = Asteroid(self.position[0], self.position[1], new_radius)
         asteroid_1.velocity = asteroid_angle_1 * 1.2
         asteroid_2.velocity = asteroid_angle_2 * 1.2


