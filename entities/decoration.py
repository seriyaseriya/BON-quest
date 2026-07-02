import pygame
import math

from settings import TILE_SIZE


class Decoration:
    def __init__(self, x, y, image, animated=False):
        self.x = x
        self.y = y
        self.image = image
        self.animated = animated
        self.timer = 0

    def update(self):
        self.timer += 1

    def draw(self, screen):
        px = self.x * TILE_SIZE
        py = self.y * TILE_SIZE

        offset_y = 0
        if self.animated:
            offset_y = int(math.sin(self.timer * 0.08) * 1)

        screen.blit(self.image, (px, py + offset_y))