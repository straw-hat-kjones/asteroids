import pygame
from circleshape import CircleShape
from constants import PLAYER_RADIUS, LINE_WIDTH, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN_SECONDS
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.color = (0, 255, 0)  # Green color for the player
        self.rotation = 0  # Initial rotation angle
        self.player_shot_cooldown = 0 

    # in the Player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    def rotate(self, dt):
        return PLAYER_TURN_SPEED * dt
    
    def update(self, dt):
        self.player_shot_cooldown -= dt
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            # ?
            self.rotation -= self.rotate(dt)
        if keys[pygame.K_d]:
            # ?
            self.rotation += self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            return self.shoot()
        
            
    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector
        
    def shoot(self):
        if self.player_shot_cooldown > 0:
            return None
        self.player_shot_cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS
        shot = Shot(self.position.x, self.position.y)
        shot_direction = pygame.Vector2(0, 1).rotate(self.rotation)
        shot.velocity = shot_direction * PLAYER_SHOOT_SPEED
        return shot