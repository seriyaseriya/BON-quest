import pygame
import math

from settings import *


class BossCutin:
    def __init__(self):
        self.image_cache = {}

    def load_image(self, path):
        if path is None:
            return None

        if path in self.image_cache:
            return self.image_cache[path]

        try:
            image = pygame.image.load(path).convert_alpha()

            target_h = int(INTERNAL_HEIGHT * 0.72)
            ratio = target_h / image.get_height()
            target_w = int(image.get_width() * ratio)

            image = pygame.transform.smoothscale(
                image,
                (
                    target_w,
                    target_h,
                ),
            )

            self.image_cache[path] = image
            return image

        except Exception:
            return None

    def draw(
        self,
        screen,
        intro_data,
        timer,
        appear,
    ):
        self.draw_speed_lines(screen, timer, appear)
        self.draw_boss_image(screen, intro_data, timer, appear)

    def draw_speed_lines(self, screen, timer, appear):
        alpha = int(110 * appear)

        if alpha <= 0:
            return

        line_surface = pygame.Surface(
            (INTERNAL_WIDTH, INTERNAL_HEIGHT),
            pygame.SRCALPHA,
        )

        center_x = INTERNAL_WIDTH + 30
        center_y = INTERNAL_HEIGHT // 2

        for i in range(18):
            angle = -2.7 + i * 0.16 + math.sin(timer * 0.04) * 0.03

            x1 = center_x
            y1 = center_y

            x2 = int(center_x + math.cos(angle) * 360)
            y2 = int(center_y + math.sin(angle) * 260)

            pygame.draw.line(
                line_surface,
                (255, 80, 90, alpha),
                (x1, y1),
                (x2, y2),
                2,
            )

        screen.blit(line_surface, (0, 0))

    def draw_boss_image(self, screen, intro_data, timer, appear):
        image = self.load_image(
            intro_data.get("image")
        )

        if image is None:
            self.draw_placeholder(screen, timer, appear)
            return

        target_x = INTERNAL_WIDTH - image.get_width() - 18
        start_x = INTERNAL_WIDTH + 80

        overshoot = math.sin(min(1.0, appear) * math.pi) * 18
        x = int(start_x + (target_x - start_x) * appear + overshoot)
        y = INTERNAL_HEIGHT - image.get_height() - 8

        shake = 0

        if 0.25 < appear < 0.55:
            shake = int(math.sin(timer * 0.7) * 2)

        screen.blit(
            image,
            (
                x + shake,
                y,
            ),
        )

    def draw_placeholder(self, screen, timer, appear):
        w = 120
        h = 150

        target_x = INTERNAL_WIDTH - w - 28
        start_x = INTERNAL_WIDTH + 80

        x = int(start_x + (target_x - start_x) * appear)
        y = INTERNAL_HEIGHT - h - 18

        rect = pygame.Rect(x, y, w, h)

        pygame.draw.rect(
            screen,
            (45, 25, 40),
            rect,
            border_radius=18,
        )

        pygame.draw.rect(
            screen,
            (255, 80, 100),
            rect,
            3,
            border_radius=18,
        )

        font = pygame.font.SysFont("meiryo", 18, bold=True)
        text = font.render("BOSS", True, (255, 220, 220))

        screen.blit(
            text,
            (
                rect.centerx - text.get_width() // 2,
                rect.centery - text.get_height() // 2,
            ),
        )