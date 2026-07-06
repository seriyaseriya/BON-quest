import pygame
from settings import TILE_SIZE, MAP_WIDTH, MAP_HEIGHT


class LaserProjectile:
    def __init__(
        self,
        x,
        y,
        direction_x,
        direction_y,
        damage,
        duration=12,
        length_tiles=12,
        width=18,
        color=(120, 240, 255),
        owner="player",
    ):
        self.x = x
        self.y = y
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.damage = damage
        self.duration = duration
        self.max_duration = duration
        self.length_tiles = length_tiles
        self.width = width
        self.color = color
        self.owner = owner
        self.pierce = True
        self.alive = True
        self.hit_enemies = set()

    def update(self, game_map=None):
        self.duration -= 1
        if self.duration <= 0:
            self.alive = False

    @property
    def rect(self):
        end_x, end_y = self.get_end_position()

        left = min(self.x, end_x) - self.width
        top = min(self.y, end_y) - self.width
        width = abs(end_x - self.x) + self.width * 2
        height = abs(end_y - self.y) + self.width * 2

        return pygame.Rect(left, top, width, height)

    def get_end_position(self):
        length = self.length_tiles * TILE_SIZE

        end_x = self.x + self.direction_x * length
        end_y = self.y + self.direction_y * length

        end_x = max(0, min(end_x, MAP_WIDTH * TILE_SIZE))
        end_y = max(0, min(end_y, MAP_HEIGHT * TILE_SIZE))

        return end_x, end_y

    def draw(self, screen, camera_x=0, camera_y=0):
        if not self.alive:
            return

        end_x, end_y = self.get_end_position()

        start = (
            int(self.x - camera_x),
            int(self.y - camera_y),
        )
        end = (
            int(end_x - camera_x),
            int(end_y - camera_y),
        )

        alpha_rate = self.duration / self.max_duration

        glow_surface = pygame.Surface(
            screen.get_size(),
            pygame.SRCALPHA,
        )

        pygame.draw.line(
            glow_surface,
            (120, 240, 255, int(90 * alpha_rate)),
            start,
            end,
            self.width * 3,
        )

        pygame.draw.line(
            glow_surface,
            (160, 250, 255, int(160 * alpha_rate)),
            start,
            end,
            self.width * 2,
        )

        pygame.draw.line(
            glow_surface,
            (255, 255, 255, int(240 * alpha_rate)),
            start,
            end,
            self.width,
        )

        screen.blit(glow_surface, (0, 0))