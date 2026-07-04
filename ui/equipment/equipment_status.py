import pygame

from ui.font_manager import get_menu_font, get_small_font


def draw_equipment_status(screen, rect, player):
    font = get_menu_font()
    small_font = get_small_font()

    panel = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    panel.fill((15, 17, 26, 235))

    pygame.draw.rect(panel, (255, 220, 120), panel.get_rect(), 2, border_radius=14)

    title = font.render("STATUS", True, (255, 230, 150))
    panel.blit(title, (16, 10))

    attack = player.get_total_attack() if hasattr(player, "get_total_attack") else player.attack
    defense = player.equipment.get_defense_bonus() if hasattr(player, "equipment") else 0
    max_hp_bonus = player.equipment.get_max_hp_bonus() if hasattr(player, "equipment") else 0
    crit = player.equipment.get_crit_bonus() if hasattr(player, "equipment") else 0
    coin = player.equipment.get_coin_bonus() if hasattr(player, "equipment") else 0

    lines = [
        f"Lv {player.level}",
        f"HP {player.hp}/{player.max_hp}",
        f"ATK {attack}",
        f"DEF {defense}",
        f"HP Bonus +{max_hp_bonus}",
        f"CRIT {crit}%",
        f"COIN {coin}%",
    ]

    x1 = 18
    x2 = rect.width // 2 + 8
    y = 48

    for i, line in enumerate(lines):
        x = x1 if i < 4 else x2
        yy = y + (i % 4) * 28
        text = small_font.render(line, True, (235, 235, 235))
        panel.blit(text, (x, yy))

    screen.blit(panel, rect)