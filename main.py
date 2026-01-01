#main code for asteroids
import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_state
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from logger import log_event
import sys
from shot import Shot, Bigshot



def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    score = 0 
    kill_count = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (updatable, drawable, shots)
    Bigshot.containers = (updatable, drawable, shots)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()
    
    highest_score = 0
    highest_player = ""
    with open("highest_score.txt") as highest_file:
        first_line = highest_file.readline()
        if len(first_line) <= 20:
            print("bad highest file")
        else:
            highest_player = first_line[:20]
            highest_player = highest_player.strip()
            score_string = first_line[20:]
            highest_score = int(score_string)
    dt = 0
    while True:
        log_state()
        for event in pygame.event.get():
             if event.type == pygame.QUIT:
                return
        screen.fill("black")
        for asteroid in asteroids:
            if asteroid.collides_with(player) == True:
                log_event("player_hit")
                score = score / 60 + kill_count
                int_score = int(score)
                print("Game over!")
                print(f"Kill count: {kill_count}!")
                print(f"Current score: {int_score}!")
                if int_score > highest_score:
                    print(f"Congrats on the highest score!")
                    name = input("Type your name for posterity:")
                    if len(name) > 20:
                        name = name[:20]
                    print(f"Congrats on the highest score! You beat {highest_player}'s old score of {highest_score}.")
                    with open("highest_score.txt", "w") as highest_file:
                        highest_file.write(f"{name:<20}{int_score}\n")
                sys.exit()
        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot) == True:
                    log_event("asteroid_shot")
                    asteroid.split()
                    shot.split()
                    kill_count += 1
        updatable.update(dt)
        for item in drawable:
            item.draw(screen)
        pygame.display.flip()
        score += 1 
        fps = clock.tick(60)
        dt = fps / 1000
        

if __name__ == "__main__":
    main()
