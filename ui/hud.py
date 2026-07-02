from ui.boss_bar import draw_boss_bar
from ui.font_manager import get_hud_font
from ui.hud_panel import draw_hud_panel
from ui.message_log import draw_message_log


def draw_hud(screen, player, floor, enemy_count, inventory, message="", boss=None):
    font = get_hud_font()

    draw_hud_panel(
        screen,
        font,
        player,
        floor,
        enemy_count,
        inventory,
    )

    draw_message_log(screen, font, message)

    draw_boss_bar(screen, boss)