import pygame

from settings import *
from ui.font_manager import get_title_font, get_menu_font
from ui.reward_card import draw_reward_card
from ui.reward_animation import (
    get_reward_timer,
    get_title_float,
    get_card_slide_offset,
)
from ui.reward_effect import (
    draw_overlay,
    draw_chest_effect,
    draw_levelup_effect,
)


def is_chest_reward_screen(choices):
    for reward in choices:
        if reward.source == "chest":
            return True

    return False


def draw_reward_title(screen, title_font, font, timer, mode):
    title_float = get_title_float(timer)

    if mode == "chest":
        title_text = "Treasure Reward!"
        subtitle_text = "Choose one treasure from the chest"
        title_color = (255, 220, 120)
    elif mode == "level":
        title_text = "Level Up!"
        subtitle_text = "Choose one power for Milk"
        title_color = (160, 220, 255)
    else:
        title_text = "Choose Your Reward"
        subtitle_text = "Select one card with number keys"
        title_color = UI_TITLE

    title = title_font.render(title_text, True, title_color)
    title_x = WIDTH // 2 - title.get_width() // 2
    title_y = int(48 + title_float)
    screen.blit(title, (title_x, title_y))

    subtitle = font.render(subtitle_text, True, UI_HELP)
    subtitle_x = WIDTH // 2 - subtitle.get_width() // 2
    screen.blit(subtitle, (subtitle_x, title_y + 52))


def draw_reward_cards(screen, choices, font, timer, mode):
    card_width = 178
    card_height = 232
    gap = 24

    total_width = card_width * len(choices) + gap * (len(choices) - 1)
    start_x = WIDTH // 2 - total_width // 2
    base_y = 145

    for index, reward in enumerate(choices):
        x = start_x + index * (card_width + gap)
        y = base_y + get_card_slide_offset(timer, index)

        draw_reward_card(
            screen,
            reward,
            index,
            x,
            y,
            card_width,
            card_height,
            font,
            timer,
            mode,
        )


def draw_reward_screen(screen, choices, mode="reward"):
    if not choices:
        return

    timer = get_reward_timer(draw_reward_screen)

    title_font = get_title_font()
    font = get_menu_font()

    draw_overlay(screen, timer, mode)

    if mode == "chest":
        draw_chest_effect(screen, timer)
    elif mode == "level":
        draw_levelup_effect(screen, timer)

    draw_reward_title(screen, title_font, font, timer, mode)
    draw_reward_cards(screen, choices, font, timer, mode)


def draw_reward_choices(screen, choices):
    mode = "chest" if is_chest_reward_screen(choices) else "reward"
    draw_reward_screen(screen, choices, mode)