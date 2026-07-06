import pygame
import math
import random

from settings import *
from ui.boss_cutin import BossCutin


class BossIntro:
    def __init__(self):
        self.active = False
        self.timer = 0

        self.boss_name = ""
        self.subtitle = ""

        self.duration = 240

        self.shake_x = 0
        self.shake_y = 0

        self.flash_alpha = 0

        self.intro_data = None
        self.cutin = BossCutin()

    def start(self, boss_name, subtitle="", intro_data=None):
        self.active = True
        self.timer = 0

        self.boss_name = boss_name
        self.subtitle = subtitle

        self.intro_data = intro_data

        if self.intro_data is not None:
            self.boss_name = self.intro_data.get("name", boss_name)
            self.subtitle = self.intro_data.get("title", subtitle)

        self.shake_x = 0
        self.shake_y = 0

        self.flash_alpha = 0

    def reset(self):
        self.active = False
        self.timer = 0

        self.boss_name = ""
        self.subtitle = ""

        self.shake_x = 0
        self.shake_y = 0

        self.flash_alpha = 0

    def is_active(self):
        return self.active

    def update(self):
        if not self.active:
            return

        self.timer += 1

        # WARNING登場時の画面振動
        if 45 <= self.timer <= 85:
            power = 2

            self.shake_x = random.randint(-power, power)
            self.shake_y = random.randint(-power, power)
        else:
            self.shake_x = 0
            self.shake_y = 0

        # 白フラッシュ
        if self.timer == 105:
            self.flash_alpha = 210

        if self.flash_alpha > 0:
            self.flash_alpha = max(
                0,
                self.flash_alpha - 14,
            )

        if self.timer >= self.duration:
            self.active = False

    def draw(self, screen):
        if not self.active:
            return

        self.draw_dark_overlay(screen)
        self.draw_warning_lines(screen)

        if self.timer < 100:
            self.draw_warning(screen)
        else:
            self.draw_cutin_phase(screen)

        self.draw_flash(screen)

    def draw_dark_overlay(self, screen):
        alpha = 155

        if self.timer < 25:
            alpha = int(
                155 * self.timer / 25
            )

        if self.timer > self.duration - 30:
            alpha = int(
                155
                * (self.duration - self.timer)
                / 30
            )

        alpha = max(0, min(155, alpha))

        overlay = pygame.Surface(
            (INTERNAL_WIDTH, INTERNAL_HEIGHT),
            pygame.SRCALPHA,
        )

        overlay.fill(
            (
                8,
                0,
                5,
                alpha,
            )
        )

        screen.blit(
            overlay,
            (
                self.shake_x,
                self.shake_y,
            ),
        )

    def draw_warning_lines(self, screen):
        line_h = 24

        top_y = 30
        bottom_y = INTERNAL_HEIGHT - 54

        offset = int(
            (self.timer * 3) % 32
        )

        for y in (top_y, bottom_y):
            pygame.draw.rect(
                screen,
                (80, 8, 12),
                (
                    0,
                    y,
                    INTERNAL_WIDTH,
                    line_h,
                ),
            )

            for x in range(
                -32 + offset,
                INTERNAL_WIDTH + 32,
                32,
            ):
                pygame.draw.polygon(
                    screen,
                    (220, 35, 45),
                    [
                        (x, y),
                        (x + 16, y),
                        (x, y + line_h),
                        (x - 16, y + line_h),
                    ],
                )

    def draw_warning(self, screen):
        if self.timer < 25:
            return

        pulse = (
            math.sin(self.timer * 0.22)
            + 1
        ) / 2

        alpha = int(
            150 + pulse * 105
        )

        font = pygame.font.SysFont(
            "arialblack",
            46,
            bold=True,
        )

        text = font.render(
            "WARNING",
            True,
            (
                255,
                45,
                55,
            ),
        )

        text.set_alpha(alpha)

        x = (
            INTERNAL_WIDTH
            - text.get_width()
        ) // 2

        y = (
            INTERNAL_HEIGHT
            - text.get_height()
        ) // 2 - 6

        shadow = font.render(
            "WARNING",
            True,
            (20, 0, 0),
        )

        screen.blit(
            shadow,
            (
                x + 4 + self.shake_x,
                y + 5 + self.shake_y,
            ),
        )

        screen.blit(
            text,
            (
                x + self.shake_x,
                y + self.shake_y,
            ),
        )

        small_font = pygame.font.SysFont(
            "meiryo",
            12,
            bold=True,
        )

        message = small_font.render(
            "強大な気配が近づいている……",
            True,
            (255, 210, 210),
        )

        screen.blit(
            message,
            (
                (
                    INTERNAL_WIDTH
                    - message.get_width()
                ) // 2,
                y + 58,
            ),
        )

    def draw_boss_name(self, screen):
        appear = min(
            1.0,
            (self.timer - 105) / 35,
        )

        name_font = pygame.font.SysFont(
            "meiryo",
            30,
            bold=True,
        )

        sub_font = pygame.font.SysFont(
            "meiryo",
            13,
            bold=True,
        )

        name_text = name_font.render(
            self.boss_name,
            True,
            (255, 235, 215),
        )

        name_text.set_alpha(
            int(255 * appear)
        )

        x = (
            INTERNAL_WIDTH
            - name_text.get_width()
        ) // 2

        y = (
            INTERNAL_HEIGHT
            - name_text.get_height()
        ) // 2

        # 左右から伸びるライン
        line_width = int(
            105 * appear
        )

        center_y = y - 10

        pygame.draw.line(
            screen,
            (255, 70, 75),
            (
                INTERNAL_WIDTH // 2
                - line_width,
                center_y,
            ),
            (
                INTERNAL_WIDTH // 2
                - 20,
                center_y,
            ),
            2,
        )

        pygame.draw.line(
            screen,
            (255, 70, 75),
            (
                INTERNAL_WIDTH // 2
                + 20,
                center_y,
            ),
            (
                INTERNAL_WIDTH // 2
                + line_width,
                center_y,
            ),
            2,
        )

        screen.blit(
            name_text,
            (x, y),
        )

        if self.subtitle:
            subtitle_text = sub_font.render(
                self.subtitle,
                True,
                (255, 150, 155),
            )

            subtitle_text.set_alpha(
                int(255 * appear)
            )

            screen.blit(
                subtitle_text,
                (
                    (
                        INTERNAL_WIDTH
                        - subtitle_text.get_width()
                    ) // 2,
                    y + 43,
                ),
            )

    def draw_flash(self, screen):
        if self.flash_alpha <= 0:
            return

        flash = pygame.Surface(
            (INTERNAL_WIDTH, INTERNAL_HEIGHT),
            pygame.SRCALPHA,
        )

        flash.fill(
            (
                255,
                240,
                230,
                self.flash_alpha,
            )
        )

        screen.blit(
            flash,
            (0, 0),
        )

    def draw_cutin_phase(self, screen):
        appear = min(
            1.0,
            (self.timer - 100) / 35,
        )

        if self.intro_data is not None:
            self.cutin.draw(
                screen,
                self.intro_data,
                self.timer,
                appear,
            )

        self.draw_boss_name(screen)
        self.draw_dialogue(screen, appear)

    def draw_dialogue(self, screen, appear):
        if self.intro_data is None:
            return

        dialogue = self.intro_data.get("dialogue", "")

        if dialogue == "":
            return

        box_w = INTERNAL_WIDTH - 38
        box_h = 68
        box_x = 19
        box_y = INTERNAL_HEIGHT - box_h - 18

        box_alpha = int(230 * appear)

        box_surface = pygame.Surface(
            (box_w, box_h),
            pygame.SRCALPHA,
        )

        pygame.draw.rect(
            box_surface,
            (24, 15, 24, box_alpha),
            box_surface.get_rect(),
            border_radius=14,
        )

        pygame.draw.rect(
            box_surface,
            (255, 100, 110, box_alpha),
            box_surface.get_rect(),
            3,
            border_radius=14,
        )

        screen.blit(
            box_surface,
            (
                box_x,
                box_y,
            ),
        )

        font = pygame.font.SysFont("meiryo", 14, bold=True)

        chars = max(
            0,
            int((self.timer - 130) / 2),
        )

        visible_text = dialogue[:chars]
        lines = visible_text.split("\n")

        for i, line in enumerate(lines[:2]):
            rendered = font.render(
                line,
                True,
                (255, 235, 230),
            )

            rendered.set_alpha(
                int(255 * appear)
            )

            screen.blit(
                rendered,
                (
                    box_x + 18,
                    box_y + 16 + i * 24,
                ),
            )