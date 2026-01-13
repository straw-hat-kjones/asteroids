from enum import Enum, auto
from dataclasses import dataclass


class WeaponType(Enum):
    STANDARD = auto()
    SPREAD = auto()
    RAPID = auto()
    LASER = auto()


@dataclass
class WeaponConfig:
    cooldown: float          # Seconds between shots
    shot_speed: float        # Projectile speed
    shot_radius: float       # Projectile size
    shot_count: int          # Number of projectiles per shot
    spread_angle: float      # Angle spread for multi-shot (degrees)
    color: tuple             # RGB color for projectile
    is_continuous: bool      # For laser: continuous fire while held


WEAPON_CONFIGS = {
    WeaponType.STANDARD: WeaponConfig(
        cooldown=0.3,
        shot_speed=500,
        shot_radius=5,
        shot_count=1,
        spread_angle=0,
        color=(255, 255, 255),  # White
        is_continuous=False
    ),
    WeaponType.SPREAD: WeaponConfig(
        cooldown=0.5,
        shot_speed=450,
        shot_radius=4,
        shot_count=5,
        spread_angle=30,  # Total spread: -15 to +15 degrees
        color=(255, 165, 0),  # Orange
        is_continuous=False
    ),
    WeaponType.RAPID: WeaponConfig(
        cooldown=0.1,
        shot_speed=600,
        shot_radius=3,
        shot_count=1,
        spread_angle=0,
        color=(0, 255, 255),  # Cyan
        is_continuous=False
    ),
    WeaponType.LASER: WeaponConfig(
        cooldown=0.0,  # Continuous
        shot_speed=0,  # Instant (raycast)
        shot_radius=2,
        shot_count=1,
        spread_angle=0,
        color=(255, 0, 0),  # Red
        is_continuous=True
    ),
}

# Weapon names for display
WEAPON_NAMES = {
    WeaponType.STANDARD: "Standard",
    WeaponType.SPREAD: "Spread",
    WeaponType.RAPID: "Rapid",
    WeaponType.LASER: "Laser"
}
