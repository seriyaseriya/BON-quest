import pygame

from settings import *
from ui.boss_bar import draw_boss_bar
from ui.font_manager import get_hud_font
from ui.hud_panel import draw_hud_panel
from ui.message_log import draw_message_log


def draw_control_guide(screen, font, inventory, floor):
    potion_count = inventory.items.get("potion", 0)

    lines = [
        f"{floor}F  |  Potion x{potion_count}",
        "WASD Move  Q Potion",
        "Enter / Click Attack",
        "E Interact  I Inventory",
    ]

    small_font = pygame.font.SysFont(
        None,
        18,
    )

    padding = 7
    line_height = 16

    text_surfaces = []

    for line in lines:
        text = small_font.render(
            line,
            True,
            WHITE,
        )
        text_surfaces.append(text)

    panel_width = max(
        text.get_width()
        for text in text_surfaces
    ) + padding * 2

    panel_height = (
        len(lines) * line_height
        + padding * 2
    )

    margin = 8

    x = WIDTH - panel_width - margin
    y = HEIGHT - panel_height - margin

    panel = pygame.Surface(
        (
            panel_width,
            panel_height,
        ),
        pygame.SRCALPHA,
    )

    panel.fill((20, 20, 30, 155))

    screen.blit(
        panel,
        (
            x,
            y,
        ),
    )

    for index, text in enumerate(text_surfaces):
        screen.blit(
            text,
            (
                x + padding,
                y + padding + index * line_height,
            ),
        )


def draw_hud(screen, player, floor, enemy_count, inventory, message="", boss=None):
    font = get_hud_font()

    draw_hud_panel(
        screen,
        font,
        player,
        floor,
        enemy_count,
        inventory,
    )

    draw_control_guide(
        screen,
        font,
        inventory,
        floor,
    )

    draw_message_log(screen, font, message)

    draw_boss_bar(screen, boss)