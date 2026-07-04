import pygame

from settings import WIDTH, HEIGHT
from ui.font_manager import get_title_font, get_small_font
from ui.equipment.equipment_card import draw_equipment_card
from ui.equipment.equipment_status import draw_equipment_status
from ui.equipment.equipment_backpack import draw_equipment_backpack


def draw_equipment_screen(screen, player, inventory, selected_index=0):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 195))
    screen.blit(overlay, (0, 0))

    title_font = get_title_font()
    small_font = get_small_font()

    title = title_font.render("EQUIPMENT", True, (255, 230, 150))
    screen.blit(title, title.get_rect(center=(WIDTH // 2, 38)))

    if not hasattr(player, "equipment"):
        warning = small_font.render("EquipmentSystem not found", True, (255, 120, 120))
        screen.blit(warning, warning.get_rect(center=(WIDTH // 2, HEIGHT // 2)))
        return

    # 左側：装備スロット 2列配置
    left_x = 24
    top_y = 72
    card_w = 155
    card_h = 86
    gap_x = 12
    gap_y = 10

    slots = [
        ("WEAPON", "weapon", 0, 0),
        ("ARMOR", "armor", 1, 0),
        ("ACCESSORY", "accessory", 0, 1),
        ("RELIC", "relic", 1, 1),
    ]

    for label, key, col, row in slots:
        x = left_x + col * (card_w + gap_x)
        y = top_y + row * (card_h + gap_y)
        rect = pygame.Rect(x, y, card_w, card_h)
        item = player.equipment.get_display_item(key)
        draw_equipment_card(screen, rect, label, item)

    # 左下：ステータス
    status_rect = pygame.Rect(24, 258, 322, 180)
    draw_equipment_status(screen, status_rect, player)

    # 右側：バックパック
    backpack_rect = pygame.Rect(370, 76, WIDTH - 395, HEIGHT - 130)
    draw_equipment_backpack(
        screen,
        backpack_rect,
        inventory,
        selected_index,
    )

    # 下部ガイド
    guide = small_font.render(
        "↑↓ 選択   Enter 装備   1-5 外す   E 閉じる",
        True,
        (235, 235, 235),
    )
    screen.blit(guide, guide.get_rect(center=(WIDTH // 2, HEIGHT - 28)))