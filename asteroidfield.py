import pygame
import random
from asteroid import Asteroid
from constants import *
class AsteroidField(pygame.sprite.Sprite):
    edges = [
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
            ),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
            ),
        ],
    ]

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0
        self.power_up_chance = 0.0
        self.phase = 1
        self.phase_progress = 0
        self.spw_mult = 1
        self.spd_mult = 1
        self.asteroid_kinds = ASTEROID_KINDS

    def spawn(self, radius, position, velocity, size):
        if random.uniform(0, 100) < self.power_up_chance:
            asteroid = Asteroid(position.x, position.y, radius, (229, 72, 242), size)
            asteroid.velocity = velocity
            self.power_up_chance = 0.0
        else:
            asteroid = Asteroid(position.x, position.y, radius, (222, 214, 173), size)
            asteroid.velocity = velocity
            self.power_up_chance += 1.0

    def update(self, dt):
        self.phase_progress += dt
        if self.phase_progress >= 30:
            self.phase_progress = 0
            self.phase += 1
            print(f"phase {self.phase} started")
            print(f"you have survived for {pygame.time.get_ticks() // 1000} seconds")
        self.get_phase_mult(self.phase)
        self.spawn_timer += dt * self.spw_mult
        if self.spawn_timer > ASTEROID_SPAWN_RATE_SECONDS:
            self.spawn_timer = 0

            # spawn a new asteroid at a random edge
            edge = random.choice(self.edges)
            speed = random.randint(40, 100)
            velocity = edge[0] * speed * self.spd_mult
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            kind = random.randint(1, self.asteroid_kinds)
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity, kind + 1)


    def get_phase_mult(self, phase):
        if phase >= 10:
            self.asteroid_kinds = 5
            return
        if phase >= 9:
            self.spw_mult = 2.75
            self.spd_mult = 2.25
            return
        if phase >= 8:
            self.spd_mult = 2
            return
        if phase >= 7:
            self.spd_mult = 1.75
            return
        if phase >= 6:
            self.spw_mult = 2.5
            return
        if phase >= 5:
            self.asteroid_kinds = 4
            self.spd_mult = 1.5
            return
        if phase >= 4:
            self.spw_mult = 2
            return
        if phase >= 3:
            self.spd_mult = 1.25
            return
        if phase >= 2:
            self.spw_mult = 1.5
            return
        if phase >= 1:
            return