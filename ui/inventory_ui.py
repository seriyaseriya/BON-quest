import pygame
from settings import *
from ui.font_manager import get_title_font, get_menu_font


def draw_inventory(screen, inventory, player):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(UI_OVERLAY_ALPHA)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))

    title_font = get_title_font()
    font = get_menu_font()

    title = title_font.render(
        "Inventory",
        True,
        UI_TITLE
    )

    screen.blit(title, (220, 60))

    pygame.draw.rect(
        screen,
        UI_FRAME,
        MENU_PANEL_RECT,
        2
    )

    y = 150

    potion = inventory.items.get("potion", 0)

    texts = [
        f"Potion : {potion}",
        f"Coins  : {inventory.coins} G",
        "",
        "Weapon",
        f"  {player.equipment.weapon['name']}",
        f"  ATK +{player.equipment.weapon['attack']}",
        "",
        "Armor",
        f"  {player.equipment.armor['name']}",
        f"  DEF +{player.equipment.armor['defense']}",
    ]

    for text in texts:
        image = font.render(text, True, UI_TEXT)
        screen.blit(image, (170, y))
        y += 24

    help_text = font.render(
        "1 : Potion     I : Close",
        True,
        UI_HELP
    )

    screen.blit(help_text, (170, 390))