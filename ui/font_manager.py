import pygame
from settings import *


_font_cache = {}


def get_font(size, name=FONT_NAME):
    key = (name, size)

    if key not in _font_cache:
        _font_cache[key] = pygame.font.SysFont(name, size)

    return _font_cache[key]


def get_hud_font():
    return get_font(HUD_FONT_SIZE)


def get_menu_font():
    return get_font(MENU_FONT_SIZE)


def get_small_font():
    return get_font(SMALL_FONT_SIZE)


def get_title_font():
    return get_font(TITLE_FONT_SIZE)


def get_levelup_title_font():
    return get_font(LEVELUP_TITLE_FONT_SIZE)


def get_levelup_font():
    return get_font(LEVELUP_FONT_SIZE)