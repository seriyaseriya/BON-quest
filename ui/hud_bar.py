import pygame


def draw_round_rect(screen, color, rect, radius=6, width=0):
    pygame.draw.rect(
        screen,
        color,
        rect,
        width,
        border_radius=radius,
    )


def draw_hud_bar(
    screen,
    x,
    y,
    width,
    height,
    ratio,
    fill_color,
    back_color,
    border_color,
):
    ratio = max(0, min(1, ratio))

    back_rect = pygame.Rect(x, y, width, height)
    fill_width = max(0, int(width * ratio))

    draw_round_rect(screen, back_color, back_rect, height // 2)

    if fill_width > 0:
        fill_rect = pygame.Rect(x, y, fill_width, height)
        draw_round_rect(screen, fill_color, fill_rect, height // 2)

    draw_round_rect(screen, border_color, back_rect, height // 2, 1)