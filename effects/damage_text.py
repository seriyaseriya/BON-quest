import pygame
from settings import *

class DamageText:
    def __init__(self, x, y, damage):
        self.x = x
        self.y = y
        self.damage = damage

        self.timer = 40

        self.font = pygame.font.SysFont(None, 28)

    def update(self):
        self.timer -= 1
        self.y -= 0.03

    def draw(self, screen):
        if self.timer <= 0:
            return

        alpha = int(255 * self.timer / 40)

        text = self.font.render(
            f"-{self.damage}",
            True,
            (255, 60, 60)
        )

        text.set_alpha(alpha)

        screen.blit(
            text,
            (
                self.x * TILE_SIZE + 8,
                self.y * TILE_SIZE - 10,
            )
        )

    def is_finished(self):
        return self.timer <= 0