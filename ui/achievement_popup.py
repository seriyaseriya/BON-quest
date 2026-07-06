import pygame
import math
import random

from settings import *


class AchievementPopup:
    def __init__(self):
        self.queue = []
        self.current = None
        self.timer = 0
        self.duration = 210
        self.particles = []

    def add(self, achievement):
        self.queue.append(achievement)

    def update(self):
        if self.current is None:
            if len(self.queue) > 0:
                self.current = self.queue.pop(0)
                self.timer = 0
                self.particles = []
            else:
                return

        self.timer += 1

        if self.timer % 5 == 0:
            self.spawn_sparkles()

        for p in self.particles:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["life"] -= 1

        self.particles = [
            p for p in self.particles if p["life"] > 0
        ]

        if self.timer >= self.duration:
            self.current = None
            self.timer = 0
            self.particles = []

    def spawn_sparkles(self):
        for _ in range(2):
            self.particles.append(
                {
                    "x": INTERNAL_WIDTH - random.randint(40, 150),
                    "y": random.randint(22, 82),
                    "vx": random.uniform(-0.4, 0.2),
                    "vy": random.uniform(-0.5, 0.4),
                    "life": random.randint(18, 35),
                    "size": random.randint(2, 4),
                }
            )

    def draw(self, screen):
        if self.current is None:
            return

        progress = min(1.0, self.timer / 25)

        if self.timer > self.duration - 35:
            progress = max(0.0, (self.duration - self.timer) / 35)

        ease = 1 - (1 - progress) * (1 - progress)

        popup_w = 250
        popup_h = 72
        target_x = INTERNAL_WIDTH - popup_w - 12
        hidden_x = INTERNAL_WIDTH + 10
        x = int(hidden_x + (target_x - hidden_x) * ease)
        y = 18

        achievement = self.current
        rarity = achievement.get("rarity", "bronze")

        border_color = self.get_rarity_color(rarity)
        pulse = int(math.sin(self.timer * 0.2) * 10)

        shadow_rect = pygame.Rect(x + 4, y + 5, popup_w, popup_h)
        pygame.draw.rect(screen, (0, 0, 0), shadow_rect, border_radius=15)

        rect = pygame.Rect(x, y, popup_w, popup_h)
        pygame.draw.rect(screen, (32, 28, 44), rect, border_radius=15)
        pygame.draw.rect(
            screen,
            (
                min(255, border_color[0] + pulse),
                min(255, border_color[1] + pulse),
                min(255, border_color[2] + pulse),
            ),
            rect,
            3,
            border_radius=15,
        )

        icon_rect = pygame.Rect(x + 10, y + 13, 46, 46)
        pygame.draw.rect(screen, (20, 18, 28), icon_rect, border_radius=12)
        pygame.draw.rect(screen, border_color, icon_rect, 2, border_radius=12)

        icon_font = pygame.font.SysFont("segoeuiemoji", 25)
        small_font = pygame.font.SysFont("meiryo", 11, bold=True)
        name_font = pygame.font.SysFont("meiryo", 14, bold=True)

        icon_text = icon_font.render(
            achievement.get("icon", "★"),
            True,
            border_color,
        )

        screen.blit(
            icon_text,
            (
                icon_rect.centerx - icon_text.get_width() // 2,
                icon_rect.centery - icon_text.get_height() // 2,
            ),
        )

        label = small_font.render(
            "実績解除！",
            True,
            (255, 245, 190),
        )

        name = name_font.render(
            achievement.get("name", ""),
            True,
            (245, 240, 250),
        )

        desc = small_font.render(
            achievement.get("description", ""),
            True,
            (210, 205, 220),
        )

        screen.blit(label, (x + 66, y + 12))
        screen.blit(name, (x + 66, y + 29))
        screen.blit(desc, (x + 66, y + 49))

        self.draw_sparkles(screen)

    def draw_sparkles(self, screen):
        for p in self.particles:
            alpha = max(0, min(255, p["life"] * 8))
            size = p["size"]

            sparkle = pygame.Surface((size * 2 + 2, size * 2 + 2), pygame.SRCALPHA)

            pygame.draw.circle(
                sparkle,
                (255, 245, 160, alpha),
                (size + 1, size + 1),
                size,
            )

            screen.blit(
                sparkle,
                (
                    int(p["x"]),
                    int(p["y"]),
                ),
            )

    def get_rarity_color(self, rarity):
        if rarity == "bronze":
            return (235, 170, 100)

        if rarity == "silver":
            return (230, 235, 255)

        if rarity == "gold":
            return (255, 220, 90)

        if rarity == "rainbow":
            return (210, 160, 255)

        return (255, 230, 150)