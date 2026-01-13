import pygame
import random
import math


class Particle:
    """Individual explosion particle"""
    def __init__(self, x, y, angle, speed, lifetime):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(
            math.cos(angle) * speed,
            math.sin(angle) * speed
        )
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = random.randint(2, 5)

    def update(self, dt):
        self.position += self.velocity * dt
        self.velocity *= 0.95  # Friction/slowdown
        self.lifetime -= dt
        return self.lifetime > 0

    def draw(self, screen):
        # Fade out as lifetime decreases
        alpha_ratio = self.lifetime / self.max_lifetime
        color = (
            int(255 * alpha_ratio),
            int(200 * alpha_ratio),
            int(100 * alpha_ratio)
        )
        pygame.draw.circle(screen, color,
                          (int(self.position.x), int(self.position.y)),
                          max(1, int(self.size * alpha_ratio)))


class Explosion(pygame.sprite.Sprite):
    """Particle explosion effect"""

    def __init__(self, x, y, radius):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.particles = []
        self.expanding_ring_radius = 0
        self.ring_max_radius = radius * 1.5
        self.ring_speed = radius * 3  # Expands faster for bigger asteroids
        self.lifetime = 0.5  # Total explosion duration

        # Create particles
        num_particles = int(radius / 3) + 5
        for _ in range(num_particles):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(50, 150)
            particle_lifetime = random.uniform(0.3, 0.6)
            self.particles.append(
                Particle(x, y, angle, speed, particle_lifetime)
            )

    def update(self, dt):
        self.lifetime -= dt

        # Expand ring
        self.expanding_ring_radius += self.ring_speed * dt

        # Update particles
        self.particles = [p for p in self.particles if p.update(dt)]

        # Remove when done
        if self.lifetime <= 0 and len(self.particles) == 0:
            self.kill()

    def draw(self, screen):
        # Draw expanding ring (fades out)
        if self.expanding_ring_radius < self.ring_max_radius:
            alpha_ratio = 1 - (self.expanding_ring_radius / self.ring_max_radius)
            ring_color = (
                int(255 * alpha_ratio),
                int(150 * alpha_ratio),
                int(50 * alpha_ratio)
            )
            pygame.draw.circle(screen, ring_color,
                             (int(self.position.x), int(self.position.y)),
                             int(self.expanding_ring_radius), 2)

        # Draw particles
        for particle in self.particles:
            particle.draw(screen)
