import pygame

from settings import *
from data.abilities import ABILITY_DATA


def draw_ability_ui(screen, ability_manager):
    abilities = ability_manager.get_ability_display_data()

    if not abilities:
        return

    font = pygame.font.SysFont(None, 20)

    x = INTERNAL_WIDTH - 160
    y = 12

    title = font.render("Abilities", True, (255, 255, 255))
    screen.blit(title, (x, y))

    y += 22

    for ability in abilities:
        text = f"{ability['name']} Lv{ability['level']}"
        image = font.render(text, True, (255, 255, 255))
        screen.blit(image, (x, y))
        y += 20