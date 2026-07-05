import pygame

from settings import *


class Projectile:
    def __init__(
        self,
        x,
        y,
        vx,
        vy,
        radius=6,
        damage=1,
        duration=120,
        color=(255, 255, 255),
        owner="player",
        bounce=False,
        pierce=False,
        freeze_duration=0,
    ):
        self.x = float(x)
        self.y = float(y)
        self.vx = float(vx)
        self.vy = float(vy)

        self.radius = radius
        self.damage = damage
        self.duration = duration
        self.color = color
        self.owner = owner

        self.bounce = bounce
        self.pierce = pierce
        self.freeze_duration = freeze_duration

        self.alive = True

    @property
    def rect(self):
        return pygame.Rect(
            int(self.x - self.radius),
            int(self.y - self.radius),
            self.radius * 2,
            self.radius * 2,
        )

    def update(self, game_map=None):
        if not self.alive:
            return

        self.x += self.vx
        self.y += self.vy

        if game_map is not None:
            self.handle_wall_collision(game_map)

        self.duration -= 1

        if self.duration <= 0:
            self.alive = False

    def handle_wall_collision(self, game_map):
        tile_x = int(self.x // TILE_SIZE)
        tile_y = int(self.y // TILE_SIZE)

        if tile_x < 0 or tile_x >= MAP_WIDTH:
            self.alive = False
            return

        if tile_y < 0 or tile_y >= MAP_HEIGHT:
            self.alive = False
            return

        if game_map[tile_y][tile_x] in ["#", "~"]:
            if self.bounce:
                self.vx *= -1
                self.vy *= -1

                self.x += self.vx
                self.y += self.vy
            else:
                self.alive = False

    def draw(self, screen, camera_x=0, camera_y=0):
        if not self.alive:
            return

        pygame.draw.circle(
            screen,
            self.color,
            (
                int(self.x - camera_x),
                int(self.y - camera_y),
            ),
            self.radius,
        )