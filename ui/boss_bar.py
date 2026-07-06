import pygame
from settings import *
from ui.font_manager import get_menu_font


def draw_boss_bar(screen, boss):
    if boss is None:
        return

    if boss.hp <= 0:
        return

    font = get_menu_font()

    bar_width = 340
    bar_height = 14
    bar_x = 24
    bar_y = HEIGHT - 75

    hp_ratio = boss.hp / boss.max_hp
    hp_ratio = max(0, min(1, hp_ratio))

    name = getattr(boss, "name", "KING RAT")

    name_text = font.render(name, True, UI_TITLE)
    screen.blit(name_text, (bar_x, bar_y - 22))

    pygame.draw.rect(
        screen,
        HP_BACK,
        (bar_x, bar_y, bar_width, bar_height)
    )

    pygame.draw.rect(
        screen,
        HP_RED,
        (bar_x, bar_y, int(bar_width * hp_ratio), bar_height)
    )

    pygame.draw.rect(
        screen,
        UI_FRAME,
        (bar_x, bar_y, bar_width, bar_height),
        2
    )

    hp_text = font.render(
        f"{boss.hp}/{boss.max_hp}",
        True,
        WHITE
    )

    text_x = bar_x + bar_width // 2 - hp_text.get_width() // 2
    text_y = bar_y + bar_height // 2 - hp_text.get_height() // 2

    screen.blit(hp_text, (text_x, text_y))