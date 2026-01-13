import pygame
from constants import LASER_MAX_LENGTH, LASER_WIDTH, SCREEN_WIDTH, SCREEN_HEIGHT


class Laser(pygame.sprite.Sprite):
    """Continuous laser beam - not a CircleShape since it's a line"""

    def __init__(self, player):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.player = player
        self.color = (255, 0, 0)  # Red
        self.start_pos = None
        self.end_pos = None
        self.active = False
        self.damage_timer = 0

    def update(self, dt):
        if not self.active:
            self.damage_timer = 0
            return

        # Laser originates from player position
        self.start_pos = self.player.position.copy()

        # Calculate end point based on player rotation
        direction = pygame.Vector2(0, 1).rotate(self.player.rotation)
        self.end_pos = self.start_pos + direction * LASER_MAX_LENGTH

        # Update damage timer
        self.damage_timer += dt

    def draw(self, screen):
        if self.active and self.start_pos and self.end_pos:
            # Draw main laser beam
            pygame.draw.line(screen, self.color,
                           self.start_pos, self.end_pos, LASER_WIDTH)
            # Draw glow effect with wider semi-transparent line
            pygame.draw.line(screen, (255, 100, 100),
                           self.start_pos, self.end_pos, LASER_WIDTH + 2)

    def check_collision(self, asteroid):
        """Check if laser intersects with asteroid circle"""
        if not self.active or not self.start_pos or not self.end_pos:
            return False
        return self._line_circle_intersection(
            self.start_pos, self.end_pos,
            asteroid.position, asteroid.radius
        )

    def _line_circle_intersection(self, line_start, line_end, circle_center, radius):
        """Returns True if line segment intersects circle"""
        # Vector from line start to line end
        d = line_end - line_start
        # Vector from line start to circle center
        f = line_start - circle_center

        a = d.dot(d)
        b = 2 * f.dot(d)
        c = f.dot(f) - radius * radius

        discriminant = b * b - 4 * a * c
        if discriminant < 0:
            return False

        discriminant = discriminant ** 0.5
        t1 = (-b - discriminant) / (2 * a)
        t2 = (-b + discriminant) / (2 * a)

        # Check if intersection is within line segment (t between 0 and 1)
        return (0 <= t1 <= 1) or (0 <= t2 <= 1) or (t1 < 0 < t2)

    def can_damage(self):
        """Check if laser can deal damage based on damage timer"""
        from constants import LASER_DAMAGE_INTERVAL
        return self.damage_timer >= LASER_DAMAGE_INTERVAL

    def reset_damage_timer(self):
        """Reset damage timer after dealing damage"""
        self.damage_timer = 0
