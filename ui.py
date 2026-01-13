import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from weapons import WEAPON_NAMES

FONT_SIZE = 32
FONT_COLOR = (255, 255, 255)  # White


class UI:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.large_font = pygame.font.Font(None, 64)

    def draw(self, game_state, player=None):
        """Draw all HUD elements"""
        self._draw_score(game_state.score)
        self._draw_combo(game_state.combo_multiplier)
        self._draw_lives(game_state.lives)
        if player:
            self._draw_weapon(player.current_weapon)
            self._draw_bombs(player.bomb_count)

    def _draw_score(self, score):
        """Render score in top-left corner"""
        score_text = self.font.render(f"Score: {score}", True, FONT_COLOR)
        self.screen.blit(score_text, (10, 10))

    def _draw_combo(self, multiplier):
        """Render combo multiplier (only if > 1)"""
        if multiplier > 1:
            combo_text = self.font.render(f"Combo: x{multiplier}", True, (255, 200, 0))
            self.screen.blit(combo_text, (10, 45))

    def _draw_lives(self, lives):
        """Render lives indicator in top-right corner"""
        lives_text = self.font.render(f"Lives: {lives}", True, FONT_COLOR)
        text_rect = lives_text.get_rect()
        text_rect.topright = (SCREEN_WIDTH - 10, 10)
        self.screen.blit(lives_text, text_rect)

    def _draw_weapon(self, weapon_type):
        """Render current weapon at bottom-left"""
        weapon_name = WEAPON_NAMES.get(weapon_type, "Unknown")
        weapon_text = self.font.render(f"Weapon: {weapon_name} [Q]", True, (100, 200, 255))
        self.screen.blit(weapon_text, (10, SCREEN_HEIGHT - 40))

    def _draw_bombs(self, bomb_count):
        """Render bomb count at bottom-left"""
        bomb_text = self.font.render(f"Bombs: {bomb_count} [B]", True, (255, 165, 0))
        self.screen.blit(bomb_text, (10, SCREEN_HEIGHT - 75))

    def draw_game_over(self, final_score):
        """Render game over screen"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(180)
        self.screen.blit(overlay, (0, 0))

        # Game Over text
        game_over_text = self.large_font.render("GAME OVER", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 40))
        self.screen.blit(game_over_text, text_rect)

        # Final score
        score_text = self.font.render(f"Final Score: {final_score}", True, FONT_COLOR)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 20))
        self.screen.blit(score_text, score_rect)
