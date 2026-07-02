import pygame

from settings import *


ABILITY_ICONS = {
    "soccer_ball": "⚽",
    "mouse_bomb": "B",
    "cat_beam": "☄",
    "lullaby": "♪",
    "intimidate": "!",
    "scratch": "爪",
    "barrier": "盾",
    "purr": "♡",
}


RARITY_COLORS = {
    "common": (190, 190, 190),
    "uncommon": (90, 220, 120),
    "rare": (80, 150, 255),
    "legendary": (255, 190, 70),
}


def draw_ability_icon(screen, font, ability, x, y):
    rarity = ability["rarity"]
    color = RARITY_COLORS.get(rarity, (190, 190, 190))

    rect = pygame.Rect(x, y, 38, 38)

    surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    pygame.draw.rect(
        surface,
        (24, 20, 30, 155),
        (0, 0, rect.width, rect.height),
        border_radius=10,
    )
    screen.blit(surface, (rect.x, rect.y))

    pygame.draw.rect(screen, color, rect, 2, border_radius=10)

    icon = ABILITY_ICONS.get(ability["id"], "★")
    icon_text = font.render(icon, True, color)
    screen.blit(
        icon_text,
        (
            rect.centerx - icon_text.get_width() // 2,
            rect.y + 6,
        ),
    )

    lv_text = font.render(str(ability["level"]), True, WHITE)
    screen.blit(
        lv_text,
        (
            rect.right - lv_text.get_width() - 5,
            rect.bottom - lv_text.get_height() - 3,
        ),
    )


def draw_ability_ui(screen, ability_manager):
    abilities = ability_manager.get_ability_display_data()

    if not abilities:
        return

    font = pygame.font.SysFont(None, 20)

    start_x = INTERNAL_WIDTH - 178
    start_y = 10

    for index, ability in enumerate(abilities):
        col = index % 4
        row = index // 4

        x = start_x + col * 42
        y = start_y + row * 42

        draw_ability_icon(screen, font, ability, x, y)