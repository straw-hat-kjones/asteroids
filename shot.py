import pygame
from circleshape import CircleShape
from constants import SHOT_RADIUS, PLAYER_SHOOT_SPEED, SCREEN_WIDTH, SCREEN_HEIGHT

class Shot(CircleShape):
    def __init__(self, x, y, radius=None, color=None):
        super().__init__(x, y, radius if radius else SHOT_RADIUS)
        self.color = color if color else (255, 255, 255)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.position.x), int(self.position.y)), self.radius)

    def update(self, dt):
        self.position += self.velocity * dt
        # Remove shot if off-screen
        if (self.position.x < -self.radius or
            self.position.x > SCREEN_WIDTH + self.radius or
            self.position.y < -self.radius or
            self.position.y > SCREEN_HEIGHT + self.radius):
            self.kill()