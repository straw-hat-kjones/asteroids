import pygame
import math
from circleshape import CircleShape
from constants import (POWERUP_RADIUS, POWERUP_LIFETIME, SHIELD_DURATION,
                       SPEED_BOOST_DURATION, SPEED_BOOST_MULTIPLIER)


class PowerUp(CircleShape):
    """Base class for all power-ups"""

    def __init__(self, x, y):
        super().__init__(x, y, POWERUP_RADIUS)
        self.lifetime = POWERUP_LIFETIME
        self.bob_offset = 0  # For visual bobbing effect
        self.bob_speed = 3
        self.color = (255, 255, 255)  # Override in subclasses

    def update(self, dt):
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()
        # Bobbing animation
        self.bob_offset = math.sin(pygame.time.get_ticks() / 200) * 3

    def apply(self, player):
        """Override in subclasses to apply effect"""
        raise NotImplementedError

    def draw(self, screen):
        """Override in subclasses for specific visuals"""
        raise NotImplementedError


class ShieldPowerUp(PowerUp):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (0, 150, 255)  # Blue

    def draw(self, screen):
        center = (int(self.position.x), int(self.position.y + self.bob_offset))
        # Draw outer circle
        pygame.draw.circle(screen, self.color, center, self.radius, 2)
        # Draw inner circle (shield icon)
        pygame.draw.circle(screen, self.color, center, self.radius // 2, 1)
        # Fade effect when about to expire
        if self.lifetime < 3:
            alpha = int(255 * (self.lifetime / 3))
            # Drawing with alpha not easily supported, use brightness instead
            fade_color = tuple(int(c * (self.lifetime / 3)) for c in self.color)
            pygame.draw.circle(screen, fade_color, center, self.radius, 2)

    def apply(self, player):
        player.activate_shield(SHIELD_DURATION)


class SpeedPowerUp(PowerUp):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.color = (255, 255, 0)  # Yellow

    def draw(self, screen):
        center = (int(self.position.x), int(self.position.y + self.bob_offset))
        # Draw arrow pointing up (speed icon)
        points = [
            (center[0], center[1] - self.radius),
            (center[0] + self.radius // 2, center[1] + self.radius // 2),
            (center[0], center[1]),
            (center[0] - self.radius // 2, center[1] + self.radius // 2),
        ]
        pygame.draw.polygon(screen, self.color, points, 2)

    def apply(self, player):
        player.activate_speed_boost(SPEED_BOOST_DURATION, SPEED_BOOST_MULTIPLIER)
