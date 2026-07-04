import pygame

from ui.font_manager import get_menu_font, get_small_font
from ui.equipment.equipment_colors import get_rarity_color


def draw_equipment_compare(screen, rect, player, preview_item):
    font = get_menu_font()
    small_font = get_small_font()

    panel = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
    panel.fill((15, 17, 26, 230))

    pygame.draw.rect(panel, (255, 220, 120), panel.get_rect(), 2, border_radius=14)

    title = font.render("COMPARE", True, (255, 230, 150))
    panel.blit(title, (18, 14))

    if preview_item is None:
        text = small_font.render("装備を選ぶと比較できます", True, (170, 170, 170))
        panel.blit(text, (18, 64))
        screen.blit(panel, rect)
        return

    slot = preview_item.get("slot", "-")

    if slot == "accessory":
        current = player.equipment.get_display_item("accessory1")
    else:
        current = player.equipment.get_display_item(slot)

    color = get_rarity_color(preview_item.get("rarity", "Common"))

    name = font.render(preview_item.get("name", "Unknown"), True, color)
    panel.blit(name, (18, 58))

    rarity = small_font.render(preview_item.get("rarity", "Common"), True, color)
    panel.blit(rarity, (18, 92))

    lines = [
        ("ATK", preview_item.get("attack", 0), current.get("attack", 0)),
        ("DEF", preview_item.get("defense", 0), current.get("defense", 0)),
        ("HP", preview_item.get("max_hp", 0), current.get("max_hp", 0)),
        ("CRIT", preview_item.get("crit", 0), current.get("crit", 0)),
        ("COIN", preview_item.get("coin_bonus", 0), current.get("coin_bonus", 0)),
    ]

    y = 135
    for label, new_value, old_value in lines:
        diff = new_value - old_value

        if diff > 0:
            diff_text = f"+{diff}"
            diff_color = (120, 255, 160)
        elif diff < 0:
            diff_text = str(diff)
            diff_color = (255, 120, 120)
        else:
            diff_text = "±0"
            diff_color = (180, 180, 180)

        line = small_font.render(
            f"{label:<5} {old_value} → {new_value}",
            True,
            (235, 235, 235),
        )
        panel.blit(line, (18, y))

        diff_img = small_font.render(diff_text, True, diff_color)
        panel.blit(diff_img, (190, y))

        y += 28

    desc = preview_item.get("description", "")
    desc_text = small_font.render(desc[:24], True, (220, 220, 220))
    panel.blit(desc_text, (18, rect.height - 46))

    screen.blit(panel, rect)