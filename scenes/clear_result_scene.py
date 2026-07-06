import pygame
import math

from settings import *


class ClearResultScene:
    def __init__(self, game):
        self.game = game
        self.screen = game.game_surface
        self.reset()

    def reset(self):
        self.timer = 0
        self.fade_alpha = 255
        self.fade_mode = "in"

    def handle_keydown(self, key):
        if key == pygame.K_RETURN or key == pygame.K_SPACE or key == pygame.K_ESCAPE:
            self.game.change_scene("title")

    def handle_mouse_button_down(self, button, pos):
        if button == 1:
            self.game.change_scene("title")

    def update(self):
        self.timer += 1

        if self.fade_mode == "in":
            self.fade_alpha -= 6

            if self.fade_alpha <= 0:
                self.fade_alpha = 0
                self.fade_mode = "none"

    def draw(self):
        self.draw_background()
        self.draw_panel()
        self.draw_fade()

    def draw_background(self):
        self.screen.fill((18, 15, 28))

        for i in range(36):
            x = (i * 37 + self.timer) % INTERNAL_WIDTH
            y = (i * 53) % INTERNAL_HEIGHT
            r = 1 + (i % 3)

            pygame.draw.circle(
                self.screen,
                (255, 225, 150),
                (x, y),
                r,
            )

    def draw_panel(self):
        panel_w = 330
        panel_h = 255
        panel_x = (INTERNAL_WIDTH - panel_w) // 2
        panel_y = (INTERNAL_HEIGHT - panel_h) // 2

        pygame.draw.rect(
            self.screen,
            (0, 0, 0),
            pygame.Rect(panel_x + 5, panel_y + 7, panel_w, panel_h),
            border_radius=18,
        )

        pygame.draw.rect(
            self.screen,
            (32, 26, 46),
            pygame.Rect(panel_x, panel_y, panel_w, panel_h),
            border_radius=18,
        )

        pygame.draw.rect(
            self.screen,
            (255, 220, 120),
            pygame.Rect(panel_x, panel_y, panel_w, panel_h),
            3,
            border_radius=18,
        )

        title_font = pygame.font.SysFont("arialblack", 30, bold=True)
        text_font = pygame.font.SysFont("meiryo", 15, bold=True)
        small_font = pygame.font.SysFont("meiryo", 11, bold=True)

        pulse = int(math.sin(self.timer * 0.08) * 10)

        title = title_font.render(
            "GAME CLEAR!",
            True,
            (255, 225 + pulse, 130),
        )

        self.screen.blit(
            title,
            (
                panel_x + (panel_w - title.get_width()) // 2,
                panel_y + 20,
            ),
        )

        save = self.game.save_manager

        clear_time = save.get_last_clear_time()
        best_time = save.get_best_clear_time()

        clear_time_text = self.format_time(clear_time)
        best_time_text = self.format_time(best_time)

        rows = [
            ("CLEAR TIME", clear_time_text),
            ("BEST TIME", best_time_text),
            ("TOTAL CLEARS", str(save.get_total_clears())),
            ("HIGHEST FLOOR", f"{save.data.get('highest_floor', 1)}F"),
        ]

        start_y = panel_y + 78

        for i, (label, value) in enumerate(rows):
            y = start_y + i * 29

            label_text = text_font.render(
                label,
                True,
                (220, 190, 230),
            )

            value_text = text_font.render(
                value,
                True,
                (255, 245, 220),
            )

            self.screen.blit(label_text, (panel_x + 38, y))
            self.screen.blit(
                value_text,
                (
                    panel_x + panel_w - value_text.get_width() - 38,
                    y,
                ),
            )

        note = small_font.render(
            "クリアタイムは今後オンラインランキングに対応予定",
            True,
            (210, 205, 220),
        )

        self.screen.blit(
            note,
            (
                panel_x + (panel_w - note.get_width()) // 2,
                panel_y + panel_h - 48,
            ),
        )

        guide = small_font.render(
            "Enter / Space / Click：タイトルへ",
            True,
            (245, 235, 210),
        )

        self.screen.blit(
            guide,
            (
                panel_x + (panel_w - guide.get_width()) // 2,
                panel_y + panel_h - 25,
            ),
        )

    def format_time(self, seconds):
        if seconds is None:
            return "--:--.---"

        total_seconds = int(seconds)
        minutes = total_seconds // 60
        sec = total_seconds % 60
        milli = int((seconds - total_seconds) * 1000)

        return f"{minutes:02d}:{sec:02d}.{milli:03d}"

    def draw_fade(self):
        if self.fade_alpha <= 0:
            return

        fade = pygame.Surface((INTERNAL_WIDTH, INTERNAL_HEIGHT))
        fade.fill((0, 0, 0))
        fade.set_alpha(self.fade_alpha)
        self.screen.blit(fade, (0, 0))