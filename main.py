#main code for asteroids
import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_state
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from logger import log_event
import sys
from shot import Shot, Bigshot, Black_hole



def main():
    sec_weapons = ("main cannon", "singularity",)
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    print(f"current secondary weapons: {sec_weapons}")
    weapon = input("choose your secondary weapon: ")
    print(f"selcted weapon is {weapon}")
    
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
    Black_hole.containers = (updatable, drawable, shots)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    player.secondary_weapon = player.sec_weapon(weapon)
    print(player.secondary_weapon)
    asteroid_field = AsteroidField()
    
    high_scores = _fetch_high_scores()

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
                if len(high_scores) < 10 or high_scores[-1]["score"] < int_score:
                    print(f"Congrats on the high score!")
                    name = input("Type your name for posterity:")
                    if len(name) > 20:
                        name = name[:20]
                    high_scores.append({"name": name, "score": int_score})
                    high_scores.sort(key=_sort_by_score, reverse= True)
                    _print_high_scores(high_scores)
                    _save_high_scores(high_scores)  
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


def _fetch_high_scores():
    high_scores = []
    try:
        with open("high_scores.txt") as list_of_scores:
            current_line = list_of_scores.readline()
            while len(current_line) > 20:
                high_player = current_line[:20].strip()
                high_score = int(current_line[20:])
                high_scores.append({"name": high_player, "score": high_score})
                current_line = list_of_scores.readline()
    except FileNotFoundError:
        pass  # this is fine :fire:
    return high_scores
        
def _print_high_scores(scores):
    counter = 1
    print("current high scores:")
    for entry in scores:
        print(f"{counter}: {entry["name"]:<20}{entry["score"]}")
        counter += 1

def _save_high_scores(scores):
     with open("high_scores.txt", "w") as list_of_scores:
         counter = 1
         for entry in scores:
             list_of_scores.write(f"{entry["name"]:<20}{entry["score"]}\n")
             counter += 1
             if counter > 10:
                 break 

def _sort_by_score(entry):
    return entry["score"]
         

    

if __name__ == "__main__":
    main()