import math
import pygame

from settings import TILE_SIZE


class MerchantCat:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.name = "商人ネコ"
        self.anim_timer = 0
        self.bob_offset = 0

        self.lines = [
            "商人ネコ「いいものあるにゃ。見ていくにゃ？」",
            "商人ネコ「冒険には準備が大事にゃ！」",
            "商人ネコ「コインがあれば強くなれるにゃ！」",
        ]

    def update(self):
        self.anim_timer += 1
        self.bob_offset = math.sin(self.anim_timer * 0.08) * 3

    def is_near_player(self, player):
        dx = abs(self.x - player.x)
        dy = abs(self.y - player.y)
        return dx + dy <= 1

    def talk(self):
        index = (self.anim_timer // 90) % len(self.lines)
        return self.lines[index]

    def draw(self, screen):
        px = self.x * TILE_SIZE
        py = self.y * TILE_SIZE + self.bob_offset

        body = pygame.Rect(px + 8, py + 10, TILE_SIZE - 16, TILE_SIZE - 12)
        head = pygame.Rect(px + 10, py + 2, TILE_SIZE - 20, TILE_SIZE - 18)

        pygame.draw.ellipse(screen, (210, 150, 80), body)
        pygame.draw.ellipse(screen, (235, 185, 110), head)

        left_ear = [
            (px + 13, py + 8),
            (px + 19, py - 3),
            (px + 25, py + 8),
        ]
        right_ear = [
            (px + TILE_SIZE - 25, py + 8),
            (px + TILE_SIZE - 19, py - 3),
            (px + TILE_SIZE - 13, py + 8),
        ]

        pygame.draw.polygon(screen, (235, 185, 110), left_ear)
        pygame.draw.polygon(screen, (235, 185, 110), right_ear)

        pygame.draw.circle(screen, (30, 25, 20), (px + 21, py + 18), 2)
        pygame.draw.circle(screen, (30, 25, 20), (px + TILE_SIZE - 21, py + 18), 2)
        pygame.draw.circle(screen, (80, 45, 35), (px + TILE_SIZE // 2, py + 23), 2)

        bag = pygame.Rect(px + TILE_SIZE - 15, py + 24, 13, 15)
        pygame.draw.rect(screen, (120, 75, 35), bag, border_radius=3)
        pygame.draw.rect(screen, (80, 45, 25), bag, 2, border_radius=3)

    def draw_talk_icon(self, screen):
        px = self.x * TILE_SIZE + TILE_SIZE // 2
        py = self.y * TILE_SIZE - 14 + self.bob_offset

        pygame.draw.circle(screen, (255, 245, 180), (px, py), 10)
        pygame.draw.circle(screen, (80, 55, 25), (px, py), 10, 2)

        font = pygame.font.SysFont(None, 18)
        text = font.render("E", True, (60, 40, 20))
        rect = text.get_rect(center=(px, py))
        screen.blit(text, rect)