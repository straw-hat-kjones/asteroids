import pygame
import sys
import random
from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from game_state import GameState
from ui import UI
from explosion import Explosion
from bomb import Bomb
from laser import Laser
from weapons import WeaponType
from powerup import PowerUp, ShieldPowerUp, SpeedPowerUp
from constants import POWERUP_DROP_CHANCE, POWERUP_SPAWN_RATE


def create_starfield(screen_size):
    """Create a procedural starfield background"""
    surface = pygame.Surface(screen_size)
    surface.fill((0, 0, 20))  # Very dark blue background

    # Add random stars
    for _ in range(150):
        x = random.randint(0, screen_size[0])
        y = random.randint(0, screen_size[1])
        brightness = random.randint(100, 255)
        color = (brightness, brightness, brightness)
        size = random.choice([1, 1, 1, 2])  # Most stars are small
        pygame.draw.circle(surface, color, (x, y), size)

    return surface


def spawn_random_powerup(x, y):
    """Spawn a random power-up at the given position"""
    powerup_types = [ShieldPowerUp, SpeedPowerUp]
    powerup_class = random.choice(powerup_types)
    return powerup_class(x, y)

def main():
    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print(f"Screen width: {SCREEN_WIDTH} \nScreen height: {SCREEN_HEIGHT}")
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    dt = 0
    background = create_starfield((SCREEN_WIDTH, SCREEN_HEIGHT))
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    explosions = pygame.sprite.Group()
    bombs = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)
    Explosion.containers = (explosions, updatable, drawable)
    Bomb.containers = (bombs, updatable, drawable)
    PowerUp.containers = (powerups, updatable, drawable)
    ShieldPowerUp.containers = (powerups, updatable, drawable)
    SpeedPowerUp.containers = (powerups, updatable, drawable)
    asteroid_field = AsteroidField()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    game_state = GameState()
    ui = UI(screen)
    player_laser = Laser(player)
    powerup_spawn_timer = 0.0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    player.switch_weapon()
                if event.key == pygame.K_b:
                    player.drop_bomb()
        
        log_state()
        screen.blit(background, (0, 0))

        # Update game state (combo timer)
        game_state.update(dt)

        for obj in updatable:
            obj.update(dt)

        for obj in asteroids:
            # Player-asteroid collision (using triangular hitbox)
            if not player.invincible and not player.is_shielded() and player.collide_with_circle(obj):
                log_event("player_hit", player_pos=[player.position.x, player.position.y], asteroid_pos=[obj.position.x, obj.position.y])
                game_state.lose_life()
                game_state.reset_combo()

                if game_state.game_over:
                    print(f"Game over! Final score: {game_state.score}")
                    # Draw game over screen
                    for draw_obj in drawable:
                        draw_obj.draw(screen)
                    ui.draw_game_over(game_state.score)
                    pygame.display.flip()
                    pygame.time.wait(3000)
                    pygame.quit()
                    return
                else:
                    # Respawn player
                    player.respawn(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                    log_event("player_respawn", lives=game_state.lives)
            # Shield destroys asteroids on contact (using triangular hitbox)
            elif player.is_shielded() and player.collide_with_circle(obj):
                game_state.add_score(obj.radius)
                Explosion(obj.position.x, obj.position.y, obj.radius)
                # Chance to spawn power-up
                if random.random() < POWERUP_DROP_CHANCE:
                    spawn_random_powerup(obj.position.x, obj.position.y)
                obj.split()
                obj.kill()

            # Shot-asteroid collision
            for shot in shots:
                if shot.collide_with(obj):
                    log_event("asteroid_shot", asteroid_pos=[obj.position.x, obj.position.y], shot_pos=[shot.position.x, shot.position.y])
                    game_state.add_score(obj.radius)
                    game_state.increment_combo()
                    # Create explosion at asteroid position
                    Explosion(obj.position.x, obj.position.y, obj.radius)
                    # Chance to spawn power-up
                    if random.random() < POWERUP_DROP_CHANCE:
                        spawn_random_powerup(obj.position.x, obj.position.y)
                    obj.split()
                    obj.kill()
                    shot.kill()
                    break

        # Handle bomb explosions
        for bomb in bombs:
            if bomb.exploded:
                pos, radius = bomb.get_explosion_area()
                # Create visual explosion
                Explosion(pos.x, pos.y, radius)
                # Destroy all asteroids in radius
                for asteroid in asteroids:
                    distance = pos.distance_to(asteroid.position)
                    if distance < radius + asteroid.radius:
                        game_state.add_score(asteroid.radius)
                        Explosion(asteroid.position.x, asteroid.position.y, asteroid.radius)
                        asteroid.split()
                        asteroid.kill()
                bomb.kill()

        # Handle laser weapon
        keys = pygame.key.get_pressed()
        if player.current_weapon == WeaponType.LASER and keys[pygame.K_SPACE]:
            player_laser.active = True
            player_laser.update(dt)
            # Check laser-asteroid collisions
            if player_laser.can_damage():
                for asteroid in asteroids:
                    if player_laser.check_collision(asteroid):
                        game_state.add_score(asteroid.radius)
                        game_state.increment_combo()
                        Explosion(asteroid.position.x, asteroid.position.y, asteroid.radius)
                        asteroid.split()
                        asteroid.kill()
                        player_laser.reset_damage_timer()
                        break  # Only hit one asteroid per damage tick
        else:
            player_laser.active = False

        # Handle power-up collection
        for powerup in powerups:
            if player.collide_with(powerup):
                powerup.apply(player)
                powerup.kill()
                log_event("powerup_collected", powerup_type=powerup.__class__.__name__)

        # Timed power-up spawning
        powerup_spawn_timer += dt
        if powerup_spawn_timer >= POWERUP_SPAWN_RATE:
            powerup_spawn_timer = 0
            x = random.uniform(100, SCREEN_WIDTH - 100)
            y = random.uniform(100, SCREEN_HEIGHT - 100)
            spawn_random_powerup(x, y)

        for obj in drawable:
            obj.draw(screen)

        # Draw laser (on top of other objects)
        player_laser.draw(screen)

        # Draw UI
        ui.draw(game_state, player)

        pygame.display.flip()
        dt = clock.tick(60) / 1000  # Delta time in seconds
        #print(f"Frame Time: {dt:.4f} seconds")
    #print(f"Event logged: {event_type} with details {details}")
    import json
    


if __name__ == "__main__":
    main()