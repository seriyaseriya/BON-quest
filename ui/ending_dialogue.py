import pygame
import math

from settings import *


class EndingDialogue:
    def __init__(self):
        self.lines = []
        self.visible_count = 0
        self.text_speed = 2
        self.timer = 0

    def set_lines(self, lines):
        self.lines = lines
        self.visible_count = 0
        self.timer = 0

    def get_full_text(self):
        return "\n".join(self.lines)

    def update(self):
        self.timer += 1

        if self.is_finished():
            return

        if self.timer % self.text_speed == 0:
            self.visible_count += 1

            full_text = self.get_full_text()

            if self.visible_count > len(full_text):
                self.visible_count = len(full_text)

    def is_finished(self):
        return self.visible_count >= len(self.get_full_text())

    def skip(self):
        self.visible_count = len(self.get_full_text())

    def draw(self, screen):
        box_w = INTERNAL_WIDTH - 70
        box_h = 82
        box_x = 35
        box_y = INTERNAL_HEIGHT - box_h - 22

        shadow_rect = pygame.Rect(box_x + 4, box_y + 5, box_w, box_h)
        pygame.draw.rect(screen, (0, 0, 0), shadow_rect, border_radius=14)

        box_rect = pygame.Rect(box_x, box_y, box_w, box_h)
        pygame.draw.rect(screen, (24, 20, 30), box_rect, border_radius=14)
        pygame.draw.rect(screen, (255, 220, 130), box_rect, 3, border_radius=14)

        font = pygame.font.SysFont("meiryo", 16, bold=True)

        visible_text = self.get_full_text()[:self.visible_count]
        visible_lines = visible_text.split("\n")

        for i, line in enumerate(visible_lines[:3]):
            rendered = font.render(line, True, (250, 242, 225))
            screen.blit(rendered, (box_x + 24, box_y + 16 + i * 22))

        if self.is_finished():
            self.draw_next_icon(screen, box_x + box_w - 28, box_y + box_h - 20)

    def draw_next_icon(self, screen, x, y):
        offset = int(math.sin(self.timer * 0.15) * 3)

        points = [
            (x, y + offset),
            (x + 10, y + offset),
            (x + 5, y + 7 + offset),
        ]

        pygame.draw.polygon(screen, (255, 220, 130), points)