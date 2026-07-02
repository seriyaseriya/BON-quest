import pygame
import math

from settings import *


SHINE_DURATION = 45


def clamp_alpha(value):
    return max(0, min(255, int(value)))


def draw_overlay(screen, timer, mode):
    alpha = clamp_alpha(min(UI_OVERLAY_ALPHA + 50, timer * 12))

    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    if mode == "chest":
        overlay.fill((12, 8, 0, alpha))
    elif mode == "level":
        overlay.fill((8, 8, 18, alpha))
    else:
        overlay.fill((0, 0, 0, alpha))

    screen.blit(overlay, (0, 0))


def draw_chest_effect(screen, timer):
    aura = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    for i in range(5):
        radius = 90 + i * 34 + (timer % 30)
        alpha = clamp_alpha(55 - i * 8)

        pygame.draw.circle(
            aura,
            (255, 190, 70, alpha),
            (WIDTH // 2, HEIGHT // 2 + 18),
            radius,
            3,
        )

    screen.blit(aura, (0, 0))

    for i in range(34):
        x = (timer * 3 + i * 47) % WIDTH
        y = 90 + ((timer * 2 + i * 61) % 300)
        size = 1 + ((timer + i) % 3)
        pygame.draw.circle(screen, (255, 225, 120), (x, y), size)


def draw_levelup_effect(screen, timer):
    aura = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    for i in range(4):
        radius = 80 + i * 40 + (timer % 25)
        alpha = clamp_alpha(45 - i * 7)

        pygame.draw.circle(
            aura,
            (120, 180, 255, alpha),
            (WIDTH // 2, HEIGHT // 2 + 12),
            radius,
            3,
        )

    screen.blit(aura, (0, 0))

    for i in range(28):
        x = (timer * 2 + i * 53) % WIDTH
        y = 95 + ((timer * 3 + i * 41) % 280)
        size = 1 + int(abs(math.sin(timer * 0.08 + i)) * 2)
        pygame.draw.circle(screen, (160, 210, 255), (x, y), size)


def draw_card_special_effect(screen, rect, timer, mode):
    if timer > SHINE_DURATION:
        return

    if mode == "chest":
        color = (255, 220, 110)
    elif mode == "level":
        color = (150, 210, 255)
    else:
        return

    progress = timer / SHINE_DURATION
    shine_x = rect.x - 60 + int((rect.width + 120) * progress)

    pygame.draw.line(
        screen,
        color,
        (shine_x, rect.y + 8),
        (shine_x - 44, rect.y + rect.height - 8),
        3,
    )

    pygame.draw.rect(screen, color, rect, 1, border_radius=14)