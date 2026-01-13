from constants import (SCORE_SMALL, SCORE_MEDIUM, SCORE_LARGE, COMBO_TIMEOUT,
                       COMBO_MAX, STARTING_LIVES, ASTEROID_MIN_RADIUS)


class GameState:
    def __init__(self):
        self.score = 0
        self.combo_multiplier = 1
        self.combo_timer = 0.0
        self.lives = STARTING_LIVES
        self.game_over = False

    def add_score(self, asteroid_radius):
        """Calculate and add score based on asteroid size with combo multiplier"""
        # Smaller asteroids = more points
        if asteroid_radius <= ASTEROID_MIN_RADIUS:
            base_score = SCORE_SMALL
        elif asteroid_radius <= ASTEROID_MIN_RADIUS * 2:
            base_score = SCORE_MEDIUM
        else:
            base_score = SCORE_LARGE

        self.score += base_score * self.combo_multiplier

    def increment_combo(self):
        """Increase combo multiplier and reset timer"""
        self.combo_timer = COMBO_TIMEOUT
        if self.combo_multiplier < COMBO_MAX:
            self.combo_multiplier += 1

    def reset_combo(self):
        """Reset combo to 1x"""
        self.combo_multiplier = 1
        self.combo_timer = 0.0

    def update(self, dt):
        """Update combo timer, reset if expired"""
        if self.combo_timer > 0:
            self.combo_timer -= dt
            if self.combo_timer <= 0:
                self.reset_combo()

    def lose_life(self):
        """Decrement lives, set game_over if 0"""
        self.lives -= 1
        if self.lives <= 0:
            self.game_over = True

    def reset(self):
        """Reset all state for new game"""
        self.score = 0
        self.combo_multiplier = 1
        self.combo_timer = 0.0
        self.lives = STARTING_LIVES
        self.game_over = False
