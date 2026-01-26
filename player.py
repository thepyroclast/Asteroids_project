#definition of the player class
from circleshape import CircleShape
from constants import PLAYER_RADIUS
from constants import LINE_WIDTH, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN_SECONDS
import pygame
from shot import Shot, Bigshot, Black_hole

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_cooldown_timer = 0
        self.shot_cooldown_timer_second = 0 
        self.color = (182, 241, 242)
        self.secondary_weapon = None
        self.shield = 0 

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, self.color, self.triangle(), LINE_WIDTH)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.shot_cooldown_timer -= dt
        self.shot_cooldown_timer_second -= dt 
        self.shield -= dt
        if self.shield > 0:
            self.color = (67, 70, 255)
        else:
            self.color = (182, 241, 242)

        if keys[pygame.K_a]:
            reverse_dt = -dt
            self.rotate(reverse_dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_LSHIFT]:
            if keys[pygame.K_SPACE]:
                return
            self.shoot()
        if keys[pygame.K_SPACE]:
            if keys[pygame.K_LSHIFT]:
                return
            self.secondary_weapon()

    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    def shoot(self):
        if self.shot_cooldown_timer > 0:
            return
        self.shot_cooldown_timer = PLAYER_SHOOT_COOLDOWN_SECONDS
        bullet = Shot(self.position[0], self.position[1])
        bullet.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED 

    def big_shoot(self):
        if self.shot_cooldown_timer_second > 0:
            return
        self.shot_cooldown_timer_second = PLAYER_SHOOT_COOLDOWN_SECONDS * 2
        bullet = Bigshot(self.position[0], self.position[1])
        bullet.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED 

    def black_hole(self):
        if self.shot_cooldown_timer_second > 0:
            return
        self.shot_cooldown_timer_second = PLAYER_SHOOT_COOLDOWN_SECONDS * 2
        singulartity =  Black_hole(self.position[0], self.position[1])
        singulartity.velocity = pygame.Vector2(0, 0).rotate(self.rotation)

    def sec_weapon(self, chosen_weapon):
        if chosen_weapon == "main cannon":
            current_weapon = self.big_shoot
            return current_weapon
        if chosen_weapon == "singularity":
            current_weapon = self.black_hole 
            return current_weapon
        else:
            raise Exception(f"{chosen_weapon} is not a weapon")
        

        



