import pygame

from settings import TILE_SIZE


class HealText:
    def __init__(self, x, y, amount):
        self.x = x * TILE_SIZE + TILE_SIZE // 2
        self.y = y * TILE_SIZE
        self.amount = amount
        self.life = 45
        self.max_life = 45

        self.font = pygame.font.Font(None, 24)

    def update(self):
        self.y -= 0.7
        self.life -= 1

    def is_finished(self):
        return self.life <= 0

    def draw(self, screen):
        alpha = int(255 * (self.life / self.max_life))

        text = self.font.render(
            f"+{self.amount}",
            True,
            (120, 255, 160),
        )

        text.set_alpha(alpha)

        rect = text.get_rect(
            center=(int(self.x), int(self.y)),
        )

        screen.blit(text, rect)