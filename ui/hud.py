import pygame
from settings import *
from ui.font_manager import get_hud_font
from ui.boss_bar import draw_boss_bar


def draw_hud(screen, player, floor, enemy_count, inventory, message="", boss=None):
    font = get_hud_font()

    hp_text = font.render(
        f"HP {player.hp}/{player.max_hp}",
        True,
        WHITE,
    )
    screen.blit(hp_text, (HUD_MARGIN_X, HUD_MARGIN_Y))

    pygame.draw.rect(
        screen,
        HP_BACK,
        (HP_BAR_X, HP_BAR_Y, HP_BAR_WIDTH, HP_BAR_HEIGHT)
    )

    hp_ratio = player.hp / player.max_hp
    hp_ratio = max(0, min(1, hp_ratio))

    pygame.draw.rect(
        screen,
        HP_RED,
        (
            HP_BAR_X,
            HP_BAR_Y,
            int(HP_BAR_WIDTH * hp_ratio),
            HP_BAR_HEIGHT,
        ),
    )

    exp_text = font.render(
        f"Lv {player.level}   EXP {player.exp}/{player.exp_to_next}",
        True,
        WHITE,
    )
    screen.blit(exp_text, (10, 42))

    floor_text = font.render(
        f"Floor {floor}",
        True,
        WHITE,
    )
    screen.blit(floor_text, (10, 74))

    enemy_text = font.render(
        f"Enemy {enemy_count}",
        True,
        WHITE,
    )
    screen.blit(enemy_text, (10, 106))

    coin_text = font.render(
        f"{inventory.coins} G",
        True,
        COIN_GOLD,
    )
    screen.blit(coin_text, (10, 138))

    weapon = player.equipment.weapon

    weapon_text = font.render(
        f"ATK {player.get_total_attack()} ({weapon['name']})",
        True,
        WHITE,
    )
    screen.blit(weapon_text, (10, 170))

    if message != "":
        text = font.render(
            message,
            True,
            (255, 255, 0),
        )
        screen.blit(text, (240, 10))

    draw_boss_bar(screen, boss)