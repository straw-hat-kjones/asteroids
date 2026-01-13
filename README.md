# Asteroids

A classic Asteroids arcade game clone built with Python and pygame.

## Requirements

- Python 3.13+
- pygame 2.6.1

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd asteroids

# Install dependencies with uv
uv sync
```

## Running the Game

```bash
uv run python main.py
```

## Controls

| Key | Action |
|-----|--------|
| W | Thrust forward |
| S | Thrust backward |
| A | Rotate left |
| D | Rotate right |
| Space | Shoot |
| Q | Cycle weapons |
| B | Drop bomb |

## Features

- **Multiple Weapons**: Cycle through Standard, Spread, Rapid, and Laser weapons
- **Combo System**: Chain asteroid kills for score multipliers (up to 10x)
- **Power-ups**: Collect shields and speed boosts from destroyed asteroids
- **Bombs**: Limited-use area-of-effect explosions
- **Lives System**: 3 lives with temporary invincibility on respawn

## Scoring

| Asteroid Size | Base Points |
|---------------|-------------|
| Small | 100 |
| Medium | 50 |
| Large | 20 |

Points are multiplied by your current combo multiplier.
