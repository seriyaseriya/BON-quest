import pygame

from settings import *


def draw_hud_message(screen, font, message):
    if message == "":
        return

    box = pygame.Rect(368, 10, 250, 28)

    pygame.draw.rect(
        screen,
        (26, 22, 30),
        box,
        border_radius=9,
    )
    pygame.draw.rect(
        screen,
        (255, 230, 120),
        box,
        1,
        border_radius=9,
    )

    text = font.render(str(message), True, (255, 240, 150))
    screen.blit(text, (box.x + 10, box.y + 7))