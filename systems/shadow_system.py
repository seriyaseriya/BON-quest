import pygame

from settings import TILE_SIZE


class ShadowSystem:
    def draw_shadow(self, screen, x, y, scale=1.0, alpha=95):
        px = x * TILE_SIZE
        py = y * TILE_SIZE

        width = int(24 * scale)
        height = int(8 * scale)

        shadow = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)

        rect = pygame.Rect(
            TILE_SIZE // 2 - width // 2,
            TILE_SIZE - 4,
            width,
            height,
        )

        pygame.draw.ellipse(shadow, (0, 0, 0, alpha), rect)
        screen.blit(shadow, (px, py))

    def draw_entity_shadows(self, screen, player, items, chests, enemy_manager):
        for item in items:
            self.draw_shadow(screen, item.x, item.y, scale=0.8, alpha=70)

        for chest in chests:
            self.draw_shadow(screen, chest.x, chest.y, scale=1.0, alpha=90)

        for enemy in enemy_manager.get_collision_targets():
            self.draw_shadow(screen, enemy.x, enemy.y, scale=1.1, alpha=90)

        self.draw_shadow(screen, player.x, player.y, scale=1.0, alpha=95)