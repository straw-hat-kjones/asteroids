import pygame
import random
from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS
from logger import log_event

# Base class for asteroids
class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.color = (255, 0, 0)  # Red color for asteroids

    def draw(self, screen):
        pygame.draw.circle(screen, "white", (int(self.position.x), int(self.position.y)), self.radius, LINE_WIDTH)
        
    def update(self, dt):
        self.position += self.velocity * dt
        
    def split(self):
        if self.radius > ASTEROID_MIN_RADIUS:
            log_event("asteroid_split", position=(self.position.x, self.position.y), radius=self.radius)
            new_radius = self.radius / 2
            offset = pygame.Vector2(random.uniform(-new_radius, new_radius), random.uniform(-new_radius, new_radius))
            asteroid1 = Asteroid(self.position.x + offset.x, self.position.y + offset.y, new_radius)
            asteroid1.velocity = self.velocity.rotate(random.uniform(20, 50)) * 1.2
            asteroid2 = Asteroid(self.position.x - offset.x, self.position.y - offset.y, new_radius)
            asteroid2.velocity = self.velocity.rotate(random.uniform(-50, -20)) * 1.2
            return [asteroid1, asteroid2]
        else:
            return []