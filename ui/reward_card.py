import math
import pygame

from settings import *
from ui.reward_animation import get_card_float
from ui.reward_effect import draw_card_special_effect


RARITY_COLORS = {
    "common": RARITY_COMMON,
    "uncommon": (90, 220, 120),
    "rare": RARITY_RARE,
    "epic": RARITY_EPIC,
    "legendary": RARITY_LEGENDARY,
    "mythic": (255, 80, 120),
}

RARITY_GLOW_COLORS = {
    "common": (80, 80, 80),
    "uncommon": (40, 120, 70),
    "rare": (40, 90, 180),
    "epic": (110, 60, 170),
    "legendary": (210, 130, 30),
    "mythic": (210, 40, 90),
}


def get_rarity_color(reward):
    return RARITY_COLORS.get(reward.rarity.lower(), RARITY_COMMON)


def get_rarity_glow_color(reward):
    return RARITY_GLOW_COLORS.get(reward.rarity.lower(), (80, 80, 80))


def get_card_gradient(reward, mode):
    rarity = reward.rarity.lower()

    if mode == "chest":
        return (68, 48, 24), (24, 18, 12)

    if rarity == "uncommon":
        return (34, 58, 42), (18, 28, 22)

    if rarity == "rare":
        return (34, 46, 72), (18, 24, 38)

    if rarity == "epic":
        return (58, 38, 76), (28, 18, 38)

    if rarity == "legendary":
        return (76, 54, 24), (36, 24, 12)

    if rarity == "mythic":
        return (76, 30, 42), (38, 14, 22)

    return (48, 42, 58), (22, 20, 28)


def draw_panel_gradient(screen, rect, top_color, bottom_color):
    for i in range(rect.height):
        ratio = i / max(1, rect.height)
        r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
        g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
        b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)

        pygame.draw.line(
            screen,
            (r, g, b),
            (rect.x, rect.y + i),
            (rect.x + rect.width, rect.y + i),
        )


def draw_text_center(screen, font, text, color, center_x, y):
    image = font.render(str(text), True, color)
    x = center_x - image.get_width() // 2
    screen.blit(image, (x, y))


def wrap_text(text, max_chars):
    words = str(text).split(" ")
    lines = []
    current = ""

    for word in words:
        test = word if current == "" else current + " " + word

        if len(test) > max_chars:
            if current:
                lines.append(current)
            current = word
        else:
            current = test

    if current:
        lines.append(current)

    return lines


def draw_sparkles(screen, reward, rect, timer):
    rarity = reward.rarity.lower()

    if rarity not in ["rare", "epic", "legendary", "mythic"]:
        return

    color = get_rarity_color(reward)

    for i in range(7):
        sx = rect.x + 16 + ((timer * 2 + i * 37) % max(1, rect.width - 32))
        sy = rect.y + 16 + ((timer + i * 53) % max(1, rect.height - 32))
        size = 1 + int(abs(math.sin(timer * 0.12 + i)) * 2)

        pygame.draw.circle(screen, color, (sx, sy), size)

        if rarity in ["legendary", "mythic"]:
            pygame.draw.line(screen, color, (sx - size * 2, sy), (sx + size * 2, sy))
            pygame.draw.line(screen, color, (sx, sy - size * 2), (sx, sy + size * 2))


def draw_reward_card(
    screen,
    reward,
    index,
    x,
    y,
    width,
    height,
    font,
    timer,
    mode="reward",
):
    frame_color = get_rarity_color(reward)
    glow_color = get_rarity_glow_color(reward)

    y = int(y + get_card_float(timer, index))

    glow_rect = pygame.Rect(x - 6, y - 6, width + 12, height + 12)
    pygame.draw.rect(screen, glow_color, glow_rect, border_radius=16)

    shadow_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    shadow_surface.fill((0, 0, 0, 90))
    screen.blit(shadow_surface, (x + 5, y + 7))

    card_rect = pygame.Rect(x, y, width, height)

    top_color, bottom_color = get_card_gradient(reward, mode)
    draw_panel_gradient(screen, card_rect, top_color, bottom_color)

    pygame.draw.rect(screen, frame_color, card_rect, 3, border_radius=14)

    inner_rect = pygame.Rect(x + 8, y + 8, width - 16, height - 16)
    pygame.draw.rect(screen, (255, 255, 255), inner_rect, 1, border_radius=10)

    number_box = pygame.Rect(x + 10, y + 10, 30, 28)
    pygame.draw.rect(screen, (20, 18, 24), number_box, border_radius=7)
    pygame.draw.rect(screen, frame_color, number_box, 2, border_radius=7)

    if getattr(reward, "chest_limited", False):
        limited_box = pygame.Rect(x + width - 62, y + 10, 50, 24)
        pygame.draw.rect(screen, (255, 210, 80), limited_box, border_radius=8)
        pygame.draw.rect(screen, (90, 55, 10), limited_box, 2, border_radius=8)

        limited_text = font.render("限定!", True, (60, 35, 5))
        limited_x = limited_box.centerx - limited_text.get_width() // 2
        limited_y = limited_box.centery - limited_text.get_height() // 2
        screen.blit(limited_text, (limited_x, limited_y))

    draw_text_center(screen, font, str(index + 1), UI_TITLE, number_box.centerx, number_box.y + 5)

    icon_box = pygame.Rect(x + width // 2 - 38, y + 34, 76, 62)
    pygame.draw.rect(screen, (18, 16, 22), icon_box, border_radius=12)
    pygame.draw.rect(screen, frame_color, icon_box, 3, border_radius=12)

    icon_text = font.render(str(reward.icon), True, frame_color)
    screen.blit(
        icon_text,
        (
            icon_box.centerx - icon_text.get_width() // 2,
            icon_box.centery - icon_text.get_height() // 2,
        ),
    )

    draw_text_center(screen, font, reward.name, UI_TEXT, x + width // 2, y + 108)
    draw_text_center(screen, font, reward.rarity.upper(), frame_color, x + width // 2, y + 134)

    desc_y = y + 160
    for line in wrap_text(reward.description, 19)[:3]:
        draw_text_center(screen, font, line, UI_HELP, x + width // 2, desc_y)
        desc_y += 20

    help_box = pygame.Rect(x + 42, y + height - 34, width - 84, 24)
    pygame.draw.rect(screen, (20, 18, 24), help_box, border_radius=8)
    pygame.draw.rect(screen, frame_color, help_box, 1, border_radius=8)

    draw_text_center(screen, font, f"Press {index + 1}", UI_TITLE, help_box.centerx, help_box.y + 4)

    draw_card_special_effect(screen, card_rect, timer, mode)
    draw_sparkles(screen, reward, card_rect, timer)