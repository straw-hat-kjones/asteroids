import pygame
import sys
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH} \nScreen height: {SCREEN_HEIGHT}")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)
    asteroid_field = AsteroidField()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)  # Placeholder for player object
    
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        
        # Game logic and rendering would go here
        
        log_state()
        screen.fill("black")
        for obj in updatable:
            obj.update(dt)
        for obj in asteroids:
            if player.collide_with(obj):
                log_event("player_hit", player_pos=[player.position.x, player.position.y], asteroid_pos=[obj.position.x, obj.position.y])
                # Handle collision (e.g., end game, reduce health, etc.)
                print("Game over!")
                sys.exit()
            for shot in shots:
                if shot.collide_with(obj):
                    log_event("asteroid_shot", asteroid_pos=[obj.position.x, obj.position.y], shot_pos=[shot.position.x, shot.position.y])
                    obj.split()
                    obj.kill()
                    shot.kill()
                    break
        #player.draw(screen)
        for obj in drawable:
            obj.draw(screen)
        #player.update(dt)
        pygame.display.flip()
        dt = clock.tick(60) / 1000  # Delta time in seconds
        #print(f"Frame Time: {dt:.4f} seconds")
    #print(f"Event logged: {event_type} with details {details}")
    import json
    


if __name__ == "__main__":
    main()