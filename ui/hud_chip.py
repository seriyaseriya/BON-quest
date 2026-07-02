import pygame

from settings import *


def draw_hud_chip(screen, font, icon, value, x, y, color, width=50):
    rect = pygame.Rect(x, y, width, 18)

    pygame.draw.rect(
        screen,
        (20, 18, 26),
        rect,
        border_radius=7,
    )
    pygame.draw.rect(
        screen,
        color,
        rect,
        1,
        border_radius=7,
    )

    icon_image = font.render(str(icon), True, color)
    value_image = font.render(str(value), True, WHITE)

    screen.blit(icon_image, (x + 5, y + 3))
    screen.blit(value_image, (x + 22, y + 3))