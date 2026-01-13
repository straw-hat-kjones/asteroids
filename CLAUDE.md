# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the Game

```bash
# Using uv (Python 3.13 required)
uv run python main.py
```

No tests or linting configured. The project uses pygame 2.6.1.

## Controls

- W/S: Thrust forward/backward
- A/D: Rotate left/right
- Space: Shoot (hold for laser)
- Q: Cycle weapons (Standard → Spread → Rapid → Laser)
- B: Drop bomb

## Architecture

### Entity System

All game entities inherit from `CircleShape` (extends `pygame.sprite.Sprite`), which provides:
- Position/velocity as `pygame.Vector2`
- Collision via `collide_with()` (circle-circle)
- Screen wrapping via `wrap_position()`

**Entity hierarchy:**
- `CircleShape` → `Player`, `Asteroid`, `Shot`, `Bomb`, `PowerUp` (and subclasses)
- `Player` uses triangular collision (`collide_with_circle()`) via `collision.py`

### Sprite Group Pattern

Entities auto-register to sprite groups via class-level `containers` attribute set in `main.py`:
```python
Player.containers = (updatable, drawable)
Asteroid.containers = (asteroids, updatable, drawable)
```

Groups used: `updatable`, `drawable`, `asteroids`, `shots`, `explosions`, `bombs`, `powerups`

### Key Modules

- **constants.py**: All game tuning values (speeds, sizes, timings, scoring)
- **weapons.py**: `WeaponType` enum + `WeaponConfig` dataclass defining weapon behaviors
- **game_state.py**: Score, combo system, lives tracking
- **powerup.py**: Base `PowerUp` class + `ShieldPowerUp`, `SpeedPowerUp` implementations
- **logger.py**: JSONL logging to `game_state.jsonl` and `game_events.jsonl`

### Game Loop (main.py)

1. Process pygame events
2. Update all sprites in `updatable` group
3. Handle collisions (player-asteroid, shot-asteroid, bomb explosions, laser, powerups)
4. Draw all sprites in `drawable` group + UI overlay
