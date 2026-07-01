import pygame
from settings import *


class Chest:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.opened = False

    def is_near_player(self, player):
        distance = abs(player.x - self.x) + abs(player.y - self.y)
        return distance <= 1

    def draw(self, screen):
        rect = pygame.Rect(
            self.x * TILE_SIZE,
            self.y * TILE_SIZE,
            TILE_SIZE,
            TILE_SIZE
        )

        if self.opened:
            color = (120, 80, 40)
        else:
            color = (180, 110, 40)

        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, (255, 220, 80), rect, 2)

        lock_rect = pygame.Rect(
            rect.x + 11,
            rect.y + 12,
            10,
            8
        )
        pygame.draw.rect(screen, (255, 230, 120), lock_rect)