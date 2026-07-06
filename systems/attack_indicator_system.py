import pygame
import math

from settings import TILE_SIZE


class AttackIndicator:
    def __init__(
        self,
        x,
        y,
        radius,
        duration,
        color=(255, 255, 255),
    ):
        self.x = x
        self.y = y
        self.radius = radius
        self.duration = duration
        self.max_duration = duration
        self.color = color

    def update(self):
        self.duration -= 1

    def is_finished(self):
        return self.duration <= 0

    def draw(self, screen):
        t = self.duration / self.max_duration
        alpha = int(45 * (t ** 2))

        surface_size = self.radius * 2 + 8
        surface = pygame.Surface(
            (surface_size, surface_size),
            pygame.SRCALPHA,
        )

        center = surface_size // 2

        pygame.draw.circle(
            surface,
            (
                self.color[0],
                self.color[1],
                self.color[2],
                alpha,
            ),
            (center, center),
            self.radius,
            2,
        )

        pygame.draw.circle(
            surface,
            (
                self.color[0],
                self.color[1],
                self.color[2],
                alpha // 8,
            ),
            (center, center),
            self.radius,
        )

        screen.blit(
            surface,
            (
                int(self.x - center),
                int(self.y - center),
            ),
        )


class AttackIndicatorSystem:
    def __init__(self):
        self.indicators = []

    def clear(self):
        self.indicators.clear()

    def show_circle(
        self,
        tile_x,
        tile_y,
        radius_pixels,
        duration=10,
        color=(255, 255, 255),
    ):
        center_x = tile_x * TILE_SIZE + TILE_SIZE // 2
        center_y = tile_y * TILE_SIZE + TILE_SIZE // 2

        self.indicators.append(
            AttackIndicator(
                center_x,
                center_y,
                radius_pixels,
                duration,
                color,
            )
        )

    def update(self):
        for indicator in self.indicators[:]:
            indicator.update()

            if indicator.is_finished():
                self.indicators.remove(indicator)

    def draw(self, screen):
        for indicator in self.indicators:
            indicator.draw(screen)