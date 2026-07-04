import math
import pygame


class SlimeNPC:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.timer = 0
        self.dialog_index = 0

        self.dialogs = [
            "すらいむのようなもの「ボーナスフロアだよ〜！ぷるぷる」",
            "すらいむのようなもの「僕は悪いスライムじゃないよ！」",
            "すらいむのようなもの「ミルク、つよくなってね〜！」",
        ]

    def update(self):
        self.timer += 1

    def is_near_player(self, player):
        return abs(self.x - player.x) + abs(self.y - player.y) <= 1

    def talk(self):
        text = self.dialogs[self.dialog_index]
        self.dialog_index = (self.dialog_index + 1) % len(self.dialogs)
        return text

    def draw(self, screen):
        tile_size = 32
        px = self.x * tile_size
        py = self.y * tile_size

        bounce = math.sin(self.timer * 0.12) * 4

        body_rect = pygame.Rect(px + 5, py + 8 + bounce, 22, 18)
        pygame.draw.ellipse(screen, (70, 190, 255), body_rect)
        pygame.draw.ellipse(screen, (160, 235, 255), body_rect, 2)

        pygame.draw.circle(screen, (20, 50, 80), (px + 12, int(py + 17 + bounce)), 2)
        pygame.draw.circle(screen, (20, 50, 80), (px + 21, int(py + 17 + bounce)), 2)

        pygame.draw.arc(
            screen,
            (20, 50, 80),
            pygame.Rect(px + 12, py + 17 + bounce, 9, 7),
            0,
            3.14,
            1,
        )

        shine_x = px + 10
        shine_y = int(py + 12 + bounce)
        pygame.draw.circle(screen, (230, 255, 255), (shine_x, shine_y), 3)

    def draw_talk_icon(self, screen):
        tile_size = 32
        px = self.x * tile_size + 16
        py = self.y * tile_size - 6

        pygame.draw.circle(screen, (255, 230, 80), (px, py), 8)
        font = pygame.font.SysFont(None, 18)
        text = font.render("!", True, (80, 50, 10))
        screen.blit(text, text.get_rect(center=(px, py + 1)))