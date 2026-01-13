import pygame
from circleshape import CircleShape
from constants import BOMB_RADIUS, BOMB_EXPLOSION_RADIUS, BOMB_FUSE_TIME


class Bomb(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, BOMB_RADIUS)
        self.fuse_timer = BOMB_FUSE_TIME
        self.exploded = False
        self.explosion_radius = BOMB_EXPLOSION_RADIUS
        self.color = (255, 100, 0)  # Orange

    def draw(self, screen):
        if not self.exploded:
            # Draw bomb with pulsing effect based on fuse timer
            pulse = 1.0 + 0.3 * (1 - self.fuse_timer / BOMB_FUSE_TIME)
            draw_radius = int(self.radius * pulse)
            pygame.draw.circle(screen, self.color,
                             (int(self.position.x), int(self.position.y)),
                             draw_radius, 2)
            # Inner dot
            pygame.draw.circle(screen, (255, 255, 0),
                             (int(self.position.x), int(self.position.y)),
                             3)

    def update(self, dt):
        self.fuse_timer -= dt
        if self.fuse_timer <= 0:
            self.explode()

    def explode(self):
        """Mark bomb as exploded - actual destruction handled in main loop"""
        self.exploded = True

    def get_explosion_area(self):
        """Returns position and radius for explosion check"""
        return self.position, self.explosion_radius
