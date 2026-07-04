import pygame

from ui.font_manager import get_menu_font, get_small_font
from ui.equipment.equipment_colors import get_rarity_color


def draw_equipment_card(screen, rect, slot_name, item):
    font = get_menu_font()
    small_font = get_small_font()

    rarity = item.get("rarity", "Common")
    color = get_rarity_color(rarity)

    card = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    card.fill((18, 20, 32, 235))

    pygame.draw.rect(card, color, card.get_rect(), 2, border_radius=12)
    pygame.draw.rect(card, (255, 255, 255, 35), card.get_rect(), 1, border_radius=12)

    slot_text = small_font.render(slot_name, True, (220, 220, 220))
    card.blit(slot_text, (10, 6))

    name = item.get("name", "None")
    if len(name) > 13:
        name = name[:12] + "..."

    name_text = font.render(name, True, (255, 255, 255))
    card.blit(name_text, (10, 28))

    stats = []

    if item.get("attack", 0) > 0:
        stats.append(f"ATK+{item['attack']}")

    if item.get("defense", 0) > 0:
        stats.append(f"DEF+{item['defense']}")

    if item.get("max_hp", 0) > 0:
        stats.append(f"HP+{item['max_hp']}")

    if item.get("crit", 0) > 0:
        stats.append(f"CRIT+{item['crit']}")

    if item.get("coin_bonus", 0) > 0:
        stats.append(f"COIN+{item['coin_bonus']}")

    stat_text = " / ".join(stats[:2])
    if stat_text == "":
        stat_text = rarity

    stat = small_font.render(stat_text, True, color)
    card.blit(stat, (10, 58))

    screen.blit(card, rect)