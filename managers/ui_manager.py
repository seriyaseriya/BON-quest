import pygame

from settings import *

from ui.hud import draw_hud
from ui.inventory_ui import draw_inventory
from ui.equipment_ui import draw_equipment
from ui.levelup_ui import draw_level_up
from ui.reward_ui import draw_reward_choices


class UIManager:
    def __init__(self):
        self.title_font = pygame.font.SysFont(None, 72)
        self.small_font = pygame.font.SysFont(None, 32)

    def draw_floor_intro(self, screen, floor_intro_timer, floor_intro_text):
        if floor_intro_timer <= 0:
            return

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(120)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        text = self.title_font.render(
            floor_intro_text,
            True,
            UI_TITLE,
        )

        x = WIDTH // 2 - text.get_width() // 2
        y = HEIGHT // 2 - text.get_height() // 2

        screen.blit(text, (x, y))

    def draw_game_over(self, screen, game_over):
        if not game_over:
            return

        text = self.title_font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(text, (140, 170))

        text = self.small_font.render("Press R to Restart", True, WHITE)
        screen.blit(text, (210, 260))

    def get_hud_message(self, player, chests, message):
        hud_message = message

        for chest in chests:
            if not chest.opened and chest.is_near_player(player):
                hud_message = "E : Open Chest"

        return hud_message

    def draw(
        self,
        screen,
        player,
        floor,
        enemy_count,
        inventory,
        message,
        boss,
        chests,
        floor_intro_timer,
        floor_intro_text,
        game_over,
        level_up,
        level_reward_choices,
        show_inventory,
        show_equipment,
        show_reward_choices,
        reward_choices,
    ):
        hud_message = self.get_hud_message(
            player,
            chests,
            message,
        )

        draw_hud(
            screen,
            player,
            floor,
            enemy_count,
            inventory,
            hud_message,
            boss,
        )

        self.draw_floor_intro(
            screen,
            floor_intro_timer,
            floor_intro_text,
        )

        self.draw_game_over(screen, game_over)

        if level_up:
            draw_level_up(
                screen,
                player,
                level_reward_choices,
            )

        if show_inventory:
            draw_inventory(screen, inventory, player)

        if show_equipment:
            draw_equipment(screen, player)

        if show_reward_choices:
            draw_reward_choices(screen, reward_choices)