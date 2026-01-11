import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_state

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH} \nScreen height: {SCREEN_HEIGHT}")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
        
        # Game logic and rendering would go here
        
        log_state()
        screen.fill("black")
        pygame.display.flip()
    print(f"Event logged: {event_type} with details {details}")
    import json
    


if __name__ == "__main__":
    main()