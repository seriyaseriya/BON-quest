import pygame

from settings import *
from ui.hud_bar import draw_hud_bar
from ui.hud_chip import draw_hud_chip
from ui.hud_face import get_milk_face


def draw_round_rect(screen, color, rect, radius=10, width=0):
    pygame.draw.rect(
        screen,
        color,
        rect,
        width,
        border_radius=radius,
    )


def draw_text(screen, font, text, color, x, y):
    image = font.render(str(text), True, color)
    screen.blit(image, (x, y))


def draw_hud_panel(screen, font, player, floor, enemy_count, inventory):
    panel = pygame.Rect(8, 8, 342, 84)

    shadow = pygame.Surface((panel.width, panel.height), pygame.SRCALPHA)
    shadow.fill((0, 0, 0, 70))
    screen.blit(shadow, (panel.x + 4, panel.y + 5))

    panel_surface = pygame.Surface((panel.width, panel.height), pygame.SRCALPHA)
    pygame.draw.rect(
        panel_surface,
        (42, 38, 52, 145),
        (0, 0, panel.width, panel.height),
        border_radius=14,
    )
    screen.blit(panel_surface, (panel.x, panel.y))

    draw_round_rect(screen, (255, 220, 170), panel, 14, 2)

    face = get_milk_face(player)
    draw_text(screen, font, face, (255, 245, 220), panel.x + 12, panel.y + 10)

    hp_ratio = player.hp / max(1, player.max_hp)
    hp_text = f"{player.hp}/{player.max_hp}"
    draw_text(screen, font, hp_text, WHITE, panel.x + 42, panel.y + 10)

    draw_hud_bar(
        screen,
        panel.x + 116,
        panel.y + 15,
        210,
        10,
        hp_ratio,
        HP_RED,
        HP_BACK,
        (255, 180, 180),
    )

    exp_ratio = player.exp / max(1, player.exp_to_next)

    draw_text(
        screen,
        font,
        f"Lv{player.level}",
        (170, 220, 255),
        panel.x + 14,
        panel.y + 42,
    )

    draw_hud_bar(
        screen,
        panel.x + 58,
        panel.y + 47,
        100,
        8,
        exp_ratio,
        (90, 170, 255),
        (26, 34, 48),
        (150, 210, 255),
    )

    draw_hud_chip(
        screen,
        font,
        "F",
        floor,
        panel.x + 170,
        panel.y + 38,
        (170, 220, 255),
        42,
    )

    draw_hud_chip(
        screen,
        font,
        "E",
        enemy_count,
        panel.x + 216,
        panel.y + 38,
        (255, 150, 150),
        50,
    )

    draw_hud_chip(
        screen,
        font,
        "G",
        inventory.coins,
        panel.x + 270,
        panel.y + 38,
        COIN_GOLD,
        58,
    )

    draw_hud_chip(
        screen,
        font,
        "ATK",
        player.get_total_attack(),
        panel.x + 14,
        panel.y + 60,
        (255, 210, 160),
        70,
    )