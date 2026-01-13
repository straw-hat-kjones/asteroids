import pygame
from circleshape import CircleShape
from constants import SHOT_RADIUS, PLAYER_SHOOT_SPEED

class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)
        self.color = (255, 255, 0)  # Yellow color for shots

    def draw(self, screen):
        pygame.draw.circle(screen, "white", (int(self.position.x), int(self.position.y)), self.radius, SHOT_RADIUS)

    def update(self, dt):
        self.position += self.velocity * dt