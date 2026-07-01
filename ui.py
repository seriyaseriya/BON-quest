import pygame
from settings import *

def draw_ui(screen, player):
    font = pygame.font.SysFont(None, 28)

    hp_text = font.render(f"HP: {player.hp}/{player.max_hp}", True, WHITE)
    screen.blit(hp_text, (10, 10))

    pygame.draw.rect(screen, (80, 80, 80), (120, 12, 120, 18))

    hp_ratio = player.hp / player.max_hp
    hp_width = int(120 * hp_ratio)

    pygame.draw.rect(screen, (255, 80, 80), (120, 12, hp_width, 18))

    level_text = font.render(
        f"Lv:{player.level}  EXP:{player.exp}/{player.exp_to_next}  ATK:{player.get_total_attack()}",
        True,
        WHITE
    )
    screen.blit(level_text, (10, 90))


def draw_inventory(screen, inventory, player):
    title_font = pygame.font.SysFont(None, 48)
    font = pygame.font.SysFont(None, 30)

    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(225)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    title = title_font.render("Inventory", True, (255, 255, 0))
    screen.blit(title, (220, 70))

    y = 140

    potion_text = font.render(
        f"Potion        x {inventory.items.get('potion', 0)}",
        True,
        WHITE
    )
    screen.blit(potion_text, (170, y))

    y += 40

    coin_text = font.render(
        f"Coins         {inventory.coins}G",
        True,
        (255, 220, 80)
    )
    screen.blit(coin_text, (170, y))

    y += 60

    weapon = player.equipment.weapon
    armor = player.equipment.armor

    weapon_text = font.render(
        f"Weapon        {weapon['name']}  ATK +{weapon['attack']}",
        True,
        WHITE
    )
    screen.blit(weapon_text, (170, y))

    y += 40

    armor_text = font.render(
        f"Armor         {armor['name']}  DEF +{armor['defense']}",
        True,
        WHITE
    )
    screen.blit(armor_text, (170, y))

    y += 70

    help1 = font.render("1: Use Potion", True, (200, 200, 200))
    help2 = font.render("I: Close Inventory", True, (200, 200, 200))

    screen.blit(help1, (190, y))
    screen.blit(help2, (190, y + 35))


def draw_level_up(screen, player):
    title_font = pygame.font.SysFont(None, 56)
    font = pygame.font.SysFont(None, 32)

    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(220)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    title = title_font.render("LEVEL UP!", True, (255, 255, 0))
    screen.blit(title, (190, 90))

    info = font.render(f"Milk reached Level {player.level}", True, WHITE)
    screen.blit(info, (180, 150))

    choice1 = font.render("1: Max HP +3", True, WHITE)
    choice2 = font.render("2: Attack +1", True, WHITE)
    choice3 = font.render("3: Heal +5", True, WHITE)

    screen.blit(choice1, (220, 220))
    screen.blit(choice2, (220, 260))
    screen.blit(choice3, (220, 300))


def draw_equipment(screen, player):
    title_font = pygame.font.SysFont(None, 48)
    font = pygame.font.SysFont(None, 32)

    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(220)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    title = title_font.render("Equipment", True, (255, 255, 0))
    screen.blit(title, (210, 90))

    weapon = player.equipment.weapon
    armor = player.equipment.armor

    weapon_text = font.render(
        f"Weapon: {weapon['name']}  ATK +{weapon['attack']}",
        True,
        WHITE
    )

    armor_text = font.render(
        f"Armor: {armor['name']}  DEF +{armor['defense']}",
        True,
        WHITE
    )

    total_attack = font.render(
        f"Total ATK: {player.get_total_attack()}",
        True,
        WHITE
    )

    help_text = font.render("Press E to close", True, (200, 200, 200))

    screen.blit(weapon_text, (160, 180))
    screen.blit(armor_text, (160, 230))
    screen.blit(total_attack, (160, 280))
    screen.blit(help_text, (200, 340))