import pygame

from settings import *

from ui.hud import draw_hud
from ui.inventory_ui import draw_inventory
from ui.equipment_ui import draw_equipment
from ui.levelup_ui import draw_level_up
from ui.reward_ui import draw_reward_choices
from ui.font_manager import get_hud_font


class UIManager:
    def __init__(self):
        self.title_font = pygame.font.SysFont(None, 52)
        self.small_font = get_hud_font()
        self.game_over_anim_timer = 0

    def draw_floor_intro(self, screen, floor_intro_timer, floor_intro_text):
        if floor_intro_timer <= 0:
            return

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(120)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))

        text = self.title_font.render(
            floor_intro_text,
            True,
            UI_TITLE,
        )

        x = WIDTH // 2 - text.get_width() // 2
        y = HEIGHT // 2 - text.get_height() // 2

        screen.blit(text, (x, y))

    def draw_game_over(self, screen, game_over, run_stats_manager=None):
        if not game_over:
            self.game_over_anim_timer = 0
            return

        self.game_over_anim_timer += 1
        t = self.game_over_anim_timer

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, min(230, 120 + t * 3)))
        screen.blit(overlay, (0, 0))

        font = get_hud_font()

        panel_w = 520
        panel_h = 405
        panel_x = WIDTH // 2 - panel_w // 2
        panel_y = 38

        glow_alpha = 90 + int(40 * abs((t % 60) - 30) / 30)

        glow = pygame.Surface((panel_w + 22, panel_h + 22), pygame.SRCALPHA)
        pygame.draw.rect(
            glow,
            (255, 210, 90, glow_alpha),
            (0, 0, panel_w + 22, panel_h + 22),
            4,
            border_radius=12,
        )
        screen.blit(glow, (panel_x - 11, panel_y - 11))

        panel = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        panel.fill((18, 18, 32, 235))
        screen.blit(panel, (panel_x, panel_y))

        pygame.draw.rect(
            screen,
            (255, 225, 120),
            (panel_x, panel_y, panel_w, panel_h),
            3,
            border_radius=10,
        )

        for i in range(18):
            sx = (i * 47 + t * 2) % WIDTH
            sy = (i * 83 + t) % HEIGHT
            size = 2 + (i % 3)

            pygame.draw.circle(
                screen,
                (255, 230, 130),
                (sx, sy),
                size,
            )

        title_y = panel_y + 18 + int(3 * abs((t % 50) - 25) / 25)

        title = self.title_font.render(
            "GAME OVER",
            True,
            (255, 85, 85),
        )

        screen.blit(
            title,
            (
                WIDTH // 2 - title.get_width() // 2,
                title_y,
            ),
        )

        if run_stats_manager is not None:
            rank = run_stats_manager.get_rank()
            comment = run_stats_manager.get_rank_comment()

            rank_offset = int(8 * abs((t % 70) - 35) / 35)

            rank_font = pygame.font.SysFont(None, 104)
            rank_shadow = rank_font.render(rank, True, (90, 55, 15))
            rank_text = rank_font.render(rank, True, (255, 235, 120))

            rank_label = font.render("評価", True, WHITE)

            screen.blit(rank_label, (panel_x + 55, panel_y + 92))

            screen.blit(
                rank_shadow,
                (
                    panel_x + 94,
                    panel_y + 74 - rank_offset + 4,
                ),
            )

            screen.blit(
                rank_text,
                (
                    panel_x + 90,
                    panel_y + 70 - rank_offset,
                ),
            )

            y = panel_y + 142

            final_score = run_stats_manager.calculate_score()
            final_points = run_stats_manager.calculate_points()

            count_rate = min(1.0, t / 90)

            shown_score = int(final_score * count_rate)
            shown_points = int(final_points * count_rate)

            lines = [
                f"到達階層：{run_stats_manager.max_floor_reached}F",
                f"倒した敵：{run_stats_manager.enemies_defeated}体",
                f"倒したボス：{run_stats_manager.bosses_defeated}体",
                f"獲得コイン：{run_stats_manager.coins_earned}枚",
                f"スコア：{shown_score}",
                f"持ち帰りポイント：{shown_points} pt",
            ]

            for line in lines:
                text = font.render(
                    line,
                    True,
                    WHITE,
                )

                screen.blit(
                    text,
                    (
                        panel_x + 220,
                        y,
                    ),
                )

                y += 28

            comment_alpha = 180 + int(60 * abs((t % 80) - 40) / 40)
            comment_surface = font.render(
                comment,
                True,
                (255, 235, 170),
            )
            comment_surface.set_alpha(comment_alpha)

            screen.blit(
                comment_surface,
                (
                    WIDTH // 2 - comment_surface.get_width() // 2,
                    panel_y + 318,
                ),
            )

        retry = font.render("R：リトライ", True, (220, 255, 220))
        title_back = font.render("T / ESC：タイトルへ戻る", True, (220, 220, 255))

        screen.blit(retry, (panel_x + 105, panel_y + 360))
        screen.blit(title_back, (panel_x + 285, panel_y + 360))

    def get_hud_message(self, player, chests, message):
        hud_message = message

        for chest in chests:
            if not chest.opened and chest.is_near_player(player):
                hud_message = "E : Open Chest"

        return hud_message

    def draw(
        self,
        screen,
        player,
        floor,
        enemy_count,
        inventory,
        message,
        boss,
        chests,
        floor_intro_timer,
        floor_intro_text,
        game_over,
        level_up,
        level_reward_choices,
        show_inventory,
        show_equipment,
        show_reward_choices,
        reward_choices,
        equipment_selected_index,
        run_stats_manager=None,
    ):
        hud_message = self.get_hud_message(
            player,
            chests,
            message,
        )

        draw_hud(
            screen,
            player,
            floor,
            enemy_count,
            inventory,
            hud_message,
            boss,
        )

        self.draw_floor_intro(
            screen,
            floor_intro_timer,
            floor_intro_text,
        )

        self.draw_game_over(
            screen,
            game_over,
            run_stats_manager,
        )

        if level_up:
            draw_level_up(
                screen,
                player,
                level_reward_choices,
            )

        if show_inventory:
            draw_inventory(screen, inventory, player)

        if show_equipment:
            draw_equipment(
                screen,
                player,
                inventory,
                equipment_selected_index,
            )

        if show_reward_choices:
            draw_reward_choices(screen, reward_choices)