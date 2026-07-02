import pygame
import random

from settings import *
from boss_skills.base_boss_skill import BaseBossSkill


class IceFloorSkill(BaseBossSkill):
    def __init__(
        self,
        cooldown=130,
        duration=120,
        warning_time=20,
        damage_interval=45,
    ):
        super().__init__(cooldown)

        self.duration = duration
        self.warning_time = warning_time
        self.damage_interval = damage_interval

        self.is_warning = False
        self.warning_timer = 0

        self.active_timer = 0
        self.damage_timer = 0

        self.tiles = []

    def update(self, boss, game_map, player):
        self.update_timer()

        if self.is_warning:
            self.update_warning(boss)
            return

        if self.active_timer > 0:
            self.update_active(boss, player)
            return

        if not self.can_use():
            return

        self.start_warning(boss, player)

    def start_warning(self, boss, player):
        self.tiles = self.create_tiles(boss, player)

        if len(self.tiles) == 0:
            self.reset_timer()
            return

        self.is_warning = True
        self.warning_timer = self.warning_time
        self.reset_timer()

    def update_warning(self, boss):
        self.warning_timer -= 1

        if self.warning_timer <= 0:
            self.is_warning = False
            self.active_timer = self.duration
            self.damage_timer = 0

    def update_active(self, boss, player):
        self.active_timer -= 1

        if self.damage_timer > 0:
            self.damage_timer -= 1

        if self.damage_timer <= 0:
            for tile_x, tile_y in self.tiles:
                if player.x == tile_x and player.y == tile_y:
                    boss.damage_player(
                        player,
                        max(1, boss.attack - 2),
                    )
                    self.damage_timer = self.damage_interval
                    break

        if self.active_timer <= 0:
            self.tiles = []

    def create_tiles(self, boss, player):
        tiles = []

        base_tiles = [
            (player.x, player.y),
            (player.x + 1, player.y),
            (player.x - 1, player.y),
            (player.x, player.y + 1),
            (player.x, player.y - 1),
        ]

        if boss.phase >= 2:
            base_tiles.extend([
                (player.x + 1, player.y + 1),
                (player.x - 1, player.y - 1),
            ])

        if boss.phase >= 3:
            base_tiles.extend([
                (player.x - 1, player.y + 1),
                (player.x + 1, player.y - 1),
            ])

        for tile_x, tile_y in base_tiles:
            if not self.is_valid_tile(boss, tile_x, tile_y):
                continue

            tiles.append((tile_x, tile_y))

        return tiles

    def is_valid_tile(self, boss, x, y):
        return (
            x >= boss.arena_left
            and y >= boss.arena_top
            and x <= boss.arena_right
            and y <= boss.arena_bottom
        )

    def draw(self, screen, boss, camera_x=0, camera_y=0):
        if self.is_warning:
            self.draw_warning(screen, camera_x, camera_y)
            return

        if self.active_timer > 0:
            self.draw_active(screen, camera_x, camera_y)

    def draw_warning(self, screen, camera_x=0, camera_y=0):
        for tile_x, tile_y in self.tiles:
            rect = pygame.Rect(
                tile_x * TILE_SIZE - camera_x,
                tile_y * TILE_SIZE - camera_y,
                TILE_SIZE,
                TILE_SIZE,
            )

            pygame.draw.rect(
                screen,
                (180, 240, 255),
                rect,
                2,
            )

    def draw_active(self, screen, camera_x=0, camera_y=0):
        for tile_x, tile_y in self.tiles:
            rect = pygame.Rect(
                tile_x * TILE_SIZE - camera_x,
                tile_y * TILE_SIZE - camera_y,
                TILE_SIZE,
                TILE_SIZE,
            )

            pygame.draw.rect(
                screen,
                (120, 220, 255),
                rect,
            )

            pygame.draw.rect(
                screen,
                (230, 255, 255),
                rect,
                2,
            )