import pygame
from settings import *
from ui.font_manager import get_title_font, get_menu_font


def draw_equipment(screen, player):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(UI_EQUIPMENT_ALPHA)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))

    title_font = get_title_font()
    font = get_menu_font()

    title = title_font.render(
        "Equipment",
        True,
        UI_TITLE
    )

    screen.blit(title, (210, 50))

    pygame.draw.rect(
        screen,
        UI_FRAME,
        MENU_PANEL_RECT,
        2
    )

    weapon = player.equipment.weapon
    armor = player.equipment.armor

    y = 140

    lines = [
        "=== CURRENT EQUIPMENT ===",
        "",
        f"Weapon : {weapon['name']}",
        f"ATK +{weapon['attack']}",
        "",
        f"Armor  : {armor['name']}",
        f"DEF +{armor['defense']}",
        "",
        "=== PLAYER STATUS ===",
        "",
        f"Level      : {player.level}",
        f"HP         : {player.hp}/{player.max_hp}",
        f"Attack     : {player.get_total_attack()}",
        f"Defense    : {player.equipment.get_defense_bonus()}",
    ]

    for line in lines:
        text = font.render(line, True, UI_TEXT)
        screen.blit(text, (150, y))
        y += 28

    help_text = font.render(
        "E : Close",
        True,
        UI_HELP
    )

    screen.blit(help_text, (260, 455))