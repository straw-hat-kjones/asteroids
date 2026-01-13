import pygame
from circleshape import CircleShape
from constants import (PLAYER_RADIUS, LINE_WIDTH, PLAYER_TURN_SPEED, PLAYER_ACCELERATION,
                       PLAYER_MAX_SPEED, PLAYER_FRICTION, RESPAWN_INVINCIBILITY, RESPAWN_BLINK_RATE,
                       BOMB_STARTING_COUNT)
from shot import Shot
from weapons import WeaponType, WEAPON_CONFIGS
from bomb import Bomb
from collision import circle_intersects_triangle

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.color = (0, 255, 0)  # Green color for the player
        self.rotation = 0  # Initial rotation angle
        self.player_shot_cooldown = 0
        # Invincibility state
        self.invincible = False
        self.invincibility_timer = 0.0
        self.visible = True
        self.blink_timer = 0.0
        # Weapon system
        self.current_weapon = WeaponType.STANDARD
        self.available_weapons = [WeaponType.STANDARD, WeaponType.SPREAD, WeaponType.RAPID, WeaponType.LASER]
        self.weapon_index = 0
        # Laser state (handled separately)
        self.laser_active = False
        # Bomb inventory
        self.bomb_count = BOMB_STARTING_COUNT
        # Shield power-up state
        self.shield_active = False
        self.shield_timer = 0.0
        # Speed boost state
        self.speed_multiplier = 1.0
        self.speed_boost_timer = 0.0 

    # in the Player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def collide_with_circle(self, other):
        """Check if player triangle collides with a circle (asteroid/powerup)"""
        return circle_intersects_triangle(
            other.position,
            other.radius,
            self.triangle()
        )

    def draw(self, screen):
        if self.visible:
            # Draw shield if active
            if self.shield_active:
                shield_radius = self.radius + 10
                pygame.draw.circle(screen, (0, 150, 255),
                                 (int(self.position.x), int(self.position.y)),
                                 int(shield_radius), 2)
            # Draw player triangle
            pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    def rotate(self, dt):
        return PLAYER_TURN_SPEED * dt
    
    def update(self, dt):
        self.player_shot_cooldown -= dt

        # Handle invincibility timer and blinking
        if self.invincible:
            self.invincibility_timer -= dt
            self.blink_timer -= dt
            if self.blink_timer <= 0:
                self.visible = not self.visible
                self.blink_timer = RESPAWN_BLINK_RATE
            if self.invincibility_timer <= 0:
                self.invincible = False
                self.visible = True

        # Handle shield timer
        if self.shield_active:
            self.shield_timer -= dt
            if self.shield_timer <= 0:
                self.shield_active = False

        # Handle speed boost timer
        if self.speed_boost_timer > 0:
            self.speed_boost_timer -= dt
            if self.speed_boost_timer <= 0:
                self.speed_multiplier = 1.0

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotation -= self.rotate(dt)
        if keys[pygame.K_d]:
            self.rotation += self.rotate(dt)
        if keys[pygame.K_w]:
            self.thrust(dt)
        if keys[pygame.K_s]:
            self.thrust(-dt)
        if keys[pygame.K_SPACE]:
            return self.shoot()

        # Apply friction and update position
        self.velocity *= PLAYER_FRICTION
        self.position += self.velocity * dt
        self.wrap_position()

    def thrust(self, dt):
        """Apply thrust in the direction the ship is facing"""
        thrust_direction = pygame.Vector2(0, 1).rotate(self.rotation)
        # Apply speed multiplier from power-ups
        self.velocity += thrust_direction * PLAYER_ACCELERATION * self.speed_multiplier * dt
        # Clamp to max speed (also affected by multiplier)
        max_speed = PLAYER_MAX_SPEED * self.speed_multiplier
        if self.velocity.length() > max_speed:
            self.velocity.scale_to_length(max_speed)

    def activate_shield(self, duration):
        """Activate shield power-up"""
        self.shield_active = True
        self.shield_timer = duration

    def activate_speed_boost(self, duration, multiplier):
        """Activate speed boost power-up"""
        self.speed_multiplier = multiplier
        self.speed_boost_timer = duration

    def is_shielded(self):
        """Check if player has shield active"""
        return self.shield_active

    def respawn(self, x, y):
        """Reset position and enable invincibility"""
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.rotation = 0
        self.invincible = True
        self.invincibility_timer = RESPAWN_INVINCIBILITY
        self.visible = True
        self.blink_timer = RESPAWN_BLINK_RATE

    def get_weapon_config(self):
        """Get the current weapon configuration"""
        return WEAPON_CONFIGS[self.current_weapon]

    def switch_weapon(self):
        """Cycle to next available weapon"""
        self.weapon_index = (self.weapon_index + 1) % len(self.available_weapons)
        self.current_weapon = self.available_weapons[self.weapon_index]
        self.laser_active = False  # Reset laser when switching

    def drop_bomb(self):
        """Drop a bomb at current position"""
        if self.bomb_count <= 0:
            return None
        self.bomb_count -= 1
        return Bomb(self.position.x, self.position.y)

    def shoot(self):
        config = self.get_weapon_config()

        # Handle continuous weapons (laser) differently - laser handled in main loop
        if config.is_continuous:
            return None

        # Cooldown check for non-continuous weapons
        if self.player_shot_cooldown > 0:
            return None

        self.player_shot_cooldown = config.cooldown

        shots = []
        base_direction = pygame.Vector2(0, 1).rotate(self.rotation)

        if config.shot_count == 1:
            # Single shot
            shot = Shot(self.position.x, self.position.y, config.shot_radius, config.color)
            shot.velocity = base_direction * config.shot_speed
            shots.append(shot)
        else:
            # Spread shot
            angle_step = config.spread_angle / (config.shot_count - 1)
            start_angle = -config.spread_angle / 2

            for i in range(config.shot_count):
                angle_offset = start_angle + (angle_step * i)
                shot_direction = base_direction.rotate(angle_offset)
                shot = Shot(self.position.x, self.position.y, config.shot_radius, config.color)
                shot.velocity = shot_direction * config.shot_speed
                shots.append(shot)

        return shots if len(shots) > 1 else (shots[0] if shots else None)