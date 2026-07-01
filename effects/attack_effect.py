import pygame
from settings import *

class AttackEffect:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.timer = 15
        self.font = pygame.font.SysFont(None, 36)

    def update(self):
        self.timer -= 1

    def draw(self, screen):
        if self.timer <= 0:
            return

        text = self.font.render("✦", True, (255, 255, 80))
        screen.blit(
            text,
            (
                self.x * TILE_SIZE + 8,
                self.y * TILE_SIZE + 2
            )
        )

    def is_finished(self):
        return self.timer <= 0