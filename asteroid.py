import pygame
from circleshape import CircleShape
from constants import LINE_WIDTH

# Base class for asteroids
class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.color = (255, 0, 0)  # Red color for asteroids

    def draw(self, screen):
        pygame.draw.circle(screen, "white", (int(self.position.x), int(self.position.y)), self.radius, LINE_WIDTH)
        
    def update(self, dt):
        self.position += self.velocity * dt