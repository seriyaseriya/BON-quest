import pygame
from settings import *

class TitleScene:
    def __init__(self, game):
        self.game = game

        self.title_font = pygame.font.SysFont(None, 72)
        self.middle_font = pygame.font.SysFont(None, 44)
        self.small_font = pygame.font.SysFont(None, 32)

    def handle_keydown(self, key):
        if key == pygame.K_SPACE:
            self.game.start_game()

    def update(self):
        pass

    def draw(self):
        screen = self.game.screen

        screen.fill((20, 20, 30))

        title = self.title_font.render("BON QUEST", True, (255, 255, 120))
        screen.blit(title, (150, 110))

        subtitle = self.middle_font.render("Milk's Dungeon Adventure", True, WHITE)
        screen.blit(subtitle, (120, 180))

        start = self.small_font.render("Press SPACE to Start", True, WHITE)
        screen.blit(start, (210, 270))

        help_text = self.small_font.render(
            "WASD: Move   I: Inventory   R: Restart",
            True,
            (200, 200, 200)
        )
        screen.blit(help_text, (120, 330))