import pygame
import math

from settings import *


class OpeningDialogue:
    def __init__(self):
        self.text = ""
        self.visible_count = 0
        self.text_speed = 2
        self.timer = 0

    def set_text(self, text):
        self.text = text
        self.visible_count = 0
        self.timer = 0

    def update(self):
        self.timer += 1

        if self.is_finished():
            return

        if self.timer % self.text_speed == 0:
            self.visible_count += 1

            if self.visible_count > len(self.text):
                self.visible_count = len(self.text)

    def is_finished(self):
        return self.visible_count >= len(self.text)

    def skip(self):
        self.visible_count = len(self.text)

    def draw(self, screen):
        box_w = INTERNAL_WIDTH - 70
        box_h = 78
        box_x = 35
        box_y = INTERNAL_HEIGHT - box_h - 22

        shadow_rect = pygame.Rect(
            box_x + 4,
            box_y + 5,
            box_w,
            box_h,
        )

        pygame.draw.rect(
            screen,
            (0, 0, 0),
            shadow_rect,
            border_radius=14,
        )

        box_rect = pygame.Rect(
            box_x,
            box_y,
            box_w,
            box_h,
        )

        pygame.draw.rect(
            screen,
            (22, 20, 32),
            box_rect,
            border_radius=14,
        )

        pygame.draw.rect(
            screen,
            (255, 220, 120),
            box_rect,
            3,
            border_radius=14,
        )

        inner_rect = pygame.Rect(
            box_x + 8,
            box_y + 8,
            box_w - 16,
            box_h - 16,
        )

        pygame.draw.rect(
            screen,
            (65, 50, 75),
            inner_rect,
            1,
            border_radius=10,
        )

        self.draw_paw(
            screen,
            box_x + 18,
            box_y + 17,
        )

        self.draw_paw(
            screen,
            box_x + box_w - 18,
            box_y + 17,
        )

        font = pygame.font.SysFont(
            "meiryo",
            15,
            bold=True,
        )

        visible_text = self.text[:self.visible_count]
        lines = self.wrap_text(visible_text, font, box_w - 52)

        start_y = box_y + 20

        for i, line in enumerate(lines[:2]):
            rendered = font.render(
                line,
                True,
                (245, 240, 230),
            )

            screen.blit(
                rendered,
                (
                    box_x + 34,
                    start_y + i * 25,
                ),
            )

        if self.is_finished():
            self.draw_next_icon(screen, box_x + box_w - 28, box_y + box_h - 20)

    def wrap_text(self, text, font, max_width):
        lines = []
        current = ""

        for char in text:
            test = current + char

            if font.size(test)[0] <= max_width:
                current = test
            else:
                lines.append(current)
                current = char

        if current:
            lines.append(current)

        return lines

    def draw_next_icon(self, screen, x, y):
        offset = int(math.sin(self.timer * 0.15) * 3)

        points = [
            (x, y + offset),
            (x + 10, y + offset),
            (x + 5, y + 7 + offset),
        ]

        pygame.draw.polygon(
            screen,
            (255, 220, 120),
            points,
        )

    def draw_paw(self, screen, x, y):
        color = (255, 220, 120)

        pygame.draw.circle(screen, color, (x, y + 5), 4)
        pygame.draw.circle(screen, color, (x - 5, y), 2)
        pygame.draw.circle(screen, color, (x, y - 2), 2)
        pygame.draw.circle(screen, color, (x + 5, y), 2)