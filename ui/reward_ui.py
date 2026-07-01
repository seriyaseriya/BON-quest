import pygame

from settings import *
from ui.font_manager import get_title_font, get_menu_font


def get_rarity_color(reward):
    if reward.rarity == "rare":
        return RARITY_RARE

    if reward.rarity == "epic":
        return RARITY_EPIC

    if reward.rarity == "legendary":
        return RARITY_LEGENDARY

    return RARITY_COMMON


def draw_reward_card(screen, reward, index, x, y, width, height, font):
    frame_color = get_rarity_color(reward)

    pygame.draw.rect(screen, UI_PANEL_DARK, (x, y, width, height))
    pygame.draw.rect(screen, frame_color, (x, y, width, height), 3)

    number_text = font.render(str(index + 1), True, UI_TITLE)
    screen.blit(number_text, (x + 12, y + 10))

    icon_text = font.render(reward.icon, True, frame_color)
    icon_x = x + width - icon_text.get_width() - 12
    screen.blit(icon_text, (icon_x, y + 10))

    name_text = font.render(reward.name, True, UI_TEXT)
    name_x = x + width // 2 - name_text.get_width() // 2
    screen.blit(name_text, (name_x, y + 58))

    desc_text = font.render(reward.description, True, UI_HELP)
    desc_x = x + width // 2 - desc_text.get_width() // 2
    screen.blit(desc_text, (desc_x, y + 95))

    rarity_text = font.render(reward.rarity.upper(), True, frame_color)
    rarity_x = x + width // 2 - rarity_text.get_width() // 2
    screen.blit(rarity_text, (rarity_x, y + 130))

    help_text = font.render(f"Press {index + 1}", True, UI_TITLE)
    help_x = x + width // 2 - help_text.get_width() // 2
    screen.blit(help_text, (help_x, y + 165))


def draw_reward_choices(screen, choices):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(UI_OVERLAY_ALPHA)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))

    title_font = get_title_font()
    font = get_menu_font()

    title = title_font.render("Choose Your Reward", True, UI_TITLE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 55))

    card_width = 170
    card_height = 205
    gap = 22

    total_width = card_width * len(choices) + gap * (len(choices) - 1)
    start_x = WIDTH // 2 - total_width // 2
    y = 150

    for index, reward in enumerate(choices):
        x = start_x + index * (card_width + gap)
        draw_reward_card(screen, reward, index, x, y, card_width, card_height, font)