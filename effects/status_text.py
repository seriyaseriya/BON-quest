import pygame

from settings import TILE_SIZE


class StatusText:
    def __init__(self, x, y, text, color=(255, 255, 255)):
        self.x = x * TILE_SIZE + TILE_SIZE // 2
        self.y = y * TILE_SIZE
        self.text = text
        self.color = color
        self.life = 45
        self.max_life = 45

        self.font = pygame.font.Font(None, 24)

    def update(self):
        self.y -= 0.6
        self.life -= 1

    def is_finished(self):
        return self.life <= 0

    def draw(self, screen):
        alpha = int(255 * (self.life / self.max_life))

        image = self.font.render(
            self.text,
            True,
            self.color,
        )

        image.set_alpha(alpha)

        rect = image.get_rect(
            center=(int(self.x), int(self.y)),
        )

        screen.blit(image, rect)