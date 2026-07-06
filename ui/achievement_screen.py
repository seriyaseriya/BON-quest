import pygame
import math

from settings import *
from ui.achievement_card import AchievementCard


class AchievementScreen:
    def __init__(self):
        self.active = False
        self.scroll = 0
        self.target_scroll = 0
        self.animation_timer = 0
        self.card = AchievementCard()

    def open(self):
        self.active = True
        self.scroll = 0
        self.target_scroll = 0
        self.animation_timer = 0

    def close(self):
        self.active = False

    def update(self):
        if not self.active:
            return

        self.animation_timer += 1
        self.card.update()

        self.scroll += (self.target_scroll - self.scroll) * 0.25

    def handle_keydown(self, key, achievement_manager):
        if not self.active:
            return None

        if key == pygame.K_ESCAPE or key == pygame.K_RETURN or key == pygame.K_SPACE:
            self.close()
            return "close"

        if key == pygame.K_UP:
            self.move_scroll(-1, achievement_manager)
            return "handled"

        if key == pygame.K_DOWN:
            self.move_scroll(1, achievement_manager)
            return "handled"

        if key == pygame.K_PAGEUP:
            self.move_scroll(-4, achievement_manager)
            return "handled"

        if key == pygame.K_PAGEDOWN:
            self.move_scroll(4, achievement_manager)
            return "handled"

        return "handled"

    def handle_mouse_wheel(self, y, achievement_manager):
        if not self.active:
            return

        if y > 0:
            self.move_scroll(-1, achievement_manager)
        elif y < 0:
            self.move_scroll(1, achievement_manager)

    def move_scroll(self, amount, achievement_manager):
        achievements = achievement_manager.get_all()

        visible_count = 5
        max_scroll = max(0, len(achievements) - visible_count)

        self.target_scroll += amount
        self.target_scroll = max(0, min(self.target_scroll, max_scroll))

    def draw(self, screen, achievement_manager):
        if not self.active:
            return

        overlay = pygame.Surface((INTERNAL_WIDTH, INTERNAL_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 175))
        screen.blit(overlay, (0, 0))

        panel_w = 390
        panel_h = 325
        panel_x = (INTERNAL_WIDTH - panel_w) // 2
        panel_y = (INTERNAL_HEIGHT - panel_h) // 2

        pulse = int(math.sin(self.animation_timer * 0.06) * 8)

        shadow_rect = pygame.Rect(panel_x + 5, panel_y + 7, panel_w, panel_h)
        pygame.draw.rect(screen, (0, 0, 0), shadow_rect, border_radius=18)

        panel_rect = pygame.Rect(panel_x, panel_y, panel_w, panel_h)
        pygame.draw.rect(screen, (24, 22, 38), panel_rect, border_radius=18)
        pygame.draw.rect(screen, (255, 210 + pulse, 120), panel_rect, 3, border_radius=18)

        inner_rect = pygame.Rect(panel_x + 8, panel_y + 8, panel_w - 16, panel_h - 16)
        pygame.draw.rect(screen, (62, 48, 82), inner_rect, 2, border_radius=14)

        self.draw_header(screen, achievement_manager, panel_x, panel_y, panel_w)
        self.draw_cards(screen, achievement_manager, panel_x, panel_y, panel_w, panel_h)
        self.draw_footer(screen, panel_x, panel_y, panel_w, panel_h)
        self.draw_scrollbar(screen, achievement_manager, panel_x, panel_y, panel_w, panel_h)

    def draw_header(self, screen, achievement_manager, panel_x, panel_y, panel_w):
        title_font = pygame.font.SysFont("meiryo", 22, bold=True)
        sub_font = pygame.font.SysFont("meiryo", 12, bold=True)

        title = title_font.render("ACHIEVEMENTS", True, (255, 238, 170))

        screen.blit(
            title,
            (
                panel_x + (panel_w - title.get_width()) // 2,
                panel_y + 16,
            ),
        )

        unlocked = achievement_manager.get_unlocked_count()
        total = achievement_manager.get_total_count()
        rate = achievement_manager.get_unlock_rate()

        sub = sub_font.render(
            f"解除数 {unlocked}/{total}   達成率 {rate}%",
            True,
            (230, 220, 235),
        )

        screen.blit(
            sub,
            (
                panel_x + (panel_w - sub.get_width()) // 2,
                panel_y + 43,
            ),
        )

    def draw_cards(self, screen, achievement_manager, panel_x, panel_y, panel_w, panel_h):
        achievements = achievement_manager.get_all()

        card_x = panel_x + 22
        card_y = panel_y + 70
        card_w = panel_w - 54
        card_h = 54
        gap = 8

        first_index = int(self.scroll)
        offset_y = int((self.scroll - first_index) * (card_h + gap))

        for visible_i in range(5):
            index = first_index + visible_i

            if index < 0 or index >= len(achievements):
                continue

            achievement = achievements[index]

            y = card_y + visible_i * (card_h + gap) - offset_y

            if y < panel_y + 62 or y > panel_y + panel_h - 50:
                continue

            unlocked = achievement_manager.is_unlocked(
                achievement["id"]
            )

            self.card.draw(
                screen,
                achievement,
                card_x,
                y,
                card_w,
                card_h,
                unlocked,
                index,
            )

    def draw_footer(self, screen, panel_x, panel_y, panel_w, panel_h):
        guide_font = pygame.font.SysFont("meiryo", 10)

        guide = guide_font.render(
            "↑↓ / PageUp PageDown: スクロール   ESC / Enter: 戻る",
            True,
            (220, 215, 225),
        )

        screen.blit(
            guide,
            (
                panel_x + (panel_w - guide.get_width()) // 2,
                panel_y + panel_h - 24,
            ),
        )

    def draw_scrollbar(self, screen, achievement_manager, panel_x, panel_y, panel_w, panel_h):
        achievements = achievement_manager.get_all()

        visible_count = 5

        if len(achievements) <= visible_count:
            return

        bar_x = panel_x + panel_w - 17
        bar_y = panel_y + 70
        bar_h = panel_h - 122

        pygame.draw.rect(
            screen,
            (45, 42, 58),
            pygame.Rect(bar_x, bar_y, 6, bar_h),
            border_radius=4,
        )

        max_scroll = max(1, len(achievements) - visible_count)
        handle_h = max(26, int(bar_h * visible_count / len(achievements)))
        handle_y = bar_y + int((bar_h - handle_h) * self.scroll / max_scroll)

        pygame.draw.rect(
            screen,
            (255, 220, 130),
            pygame.Rect(bar_x, handle_y, 6, handle_h),
            border_radius=4,
        )