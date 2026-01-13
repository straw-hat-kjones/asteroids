import pygame
import random
import math
from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS
from logger import log_event

# Base class for asteroids
class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.color = (255, 0, 0)  # Red color for asteroids
        self.vertices = self._generate_lumpy_shape()
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-50, 50)  # Degrees per second

    def _generate_lumpy_shape(self):
        """Generate irregular polygon vertices based on radius"""
        vertices = []
        # More vertices for larger asteroids
        num_vertices = random.randint(7, 12)

        for i in range(num_vertices):
            # Angle for this vertex
            angle = (2 * math.pi * i) / num_vertices
            # Random variation in radius (70% to 100% of base radius)
            vertex_radius = self.radius * random.uniform(0.7, 1.0)
            # Calculate vertex position relative to center (0, 0)
            x = math.cos(angle) * vertex_radius
            y = math.sin(angle) * vertex_radius
            vertices.append(pygame.Vector2(x, y))

        return vertices

    def get_world_vertices(self):
        """Get vertices transformed to world position with rotation"""
        world_verts = []
        for v in self.vertices:
            # Rotate vertex
            rotated = v.rotate(self.rotation)
            # Translate to world position
            world_verts.append(self.position + rotated)
        return world_verts

    def draw(self, screen):
        # Draw lumpy polygon
        world_verts = self.get_world_vertices()
        points = [(int(v.x), int(v.y)) for v in world_verts]
        pygame.draw.polygon(screen, "white", points, LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt
        self.rotation += self.rotation_speed * dt
        self.wrap_position()
        
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