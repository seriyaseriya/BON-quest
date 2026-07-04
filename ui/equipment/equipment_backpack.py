import pygame

from ui.font_manager import get_menu_font, get_small_font
from ui.equipment.equipment_colors import get_rarity_color


def draw_equipment_backpack(screen, rect, inventory, selected_index=0):
    font = get_menu_font()
    small_font = get_small_font()

    panel = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    panel.fill((15, 17, 26, 230))

    pygame.draw.rect(panel, (120, 180, 255), panel.get_rect(), 2, border_radius=14)

    title = font.render("BACKPACK", True, (180, 220, 255))
    panel.blit(title, (18, 14))

    items = getattr(inventory, "equipment_items", [])

    if len(items) == 0:
        empty = small_font.render("No equipment", True, (150, 150, 150))
        panel.blit(empty, (20, 62))
    else:
        y = 60

        for i, item in enumerate(items[:8]):
            if i == selected_index:
                highlight = pygame.Rect(12, y - 4, rect.width - 24, 46)
                pygame.draw.rect(panel, (255, 220, 120, 55), highlight, border_radius=8)
            rarity = item.get("rarity", "Common")
            color = get_rarity_color(rarity)

            line = f"{i + 1}. {item.get('name', 'Unknown')}"
            text = small_font.render(line, True, color)
            panel.blit(text, (20, y))

            slot = item.get("slot", "-")
            stat = f"{slot}  ATK {item.get('attack', 0)} / DEF {item.get('defense', 0)}"
            stat_text = small_font.render(stat, True, (210, 210, 210))
            panel.blit(stat_text, (40, y + 22))

            y += 52

    help_text = small_font.render("1-8: Equip   E: Close", True, (230, 230, 230))
    panel.blit(help_text, (20, rect.height - 34))

    screen.blit(panel, rect)