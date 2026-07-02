import pygame
import random

from settings import *
from boss_skills.base_boss_skill import BaseBossSkill


class TreatThrowSkill(BaseBossSkill):
    def __init__(
        self,
        cooldown=95,
        warning_time=25,
        damage_bonus=2,
    ):
        super().__init__(cooldown)

        self.warning_time = warning_time
        self.damage_bonus = damage_bonus

        self.is_warning = False
        self.warning_timer = 0

        self.target_tiles = []

    def update(self, boss, game_map, player):
        self.update_timer()

        if self.is_warning:
            self.update_warning(boss, player)
            return

        if not self.can_use():
            return

        self.start_warning(boss, player)

    def start_warning(self, boss, player):
        self.target_tiles = self.create_target_tiles(boss, player)

        if len(self.target_tiles) == 0:
            self.reset_timer()
            return

        self.is_warning = True
        self.warning_timer = self.warning_time
        self.reset_timer()

    def create_target_tiles(self, boss, player):
        tiles = [
            (player.x, player.y),
            (player.x + 1, player.y),
            (player.x - 1, player.y),
            (player.x, player.y + 1),
            (player.x, player.y - 1),
        ]

        if boss.phase >= 2:
            tiles.extend([
                (player.x + 1, player.y + 1),
                (player.x - 1, player.y - 1),
            ])

        if boss.phase >= 3:
            tiles.extend([
                (player.x + 2, player.y),
                (player.x - 2, player.y),
            ])

        valid_tiles = []

        for x, y in tiles:
            if x < boss.arena_left or x > boss.arena_right:
                continue

            if y < boss.arena_top or y > boss.arena_bottom:
                continue

            valid_tiles.append((x, y))

        return valid_tiles

    def update_warning(self, boss, player):
        self.warning_timer -= 1

        if self.warning_timer <= 0:
            self.apply_damage(boss, player)
            self.is_warning = False

    def apply_damage(self, boss, player):
        for tile_x, tile_y in self.target_tiles:
            if player.x == tile_x and player.y == tile_y:
                boss.damage_player(
                    player,
                    boss.attack + self.damage_bonus,
                )
                return

    def draw(self, screen, boss, camera_x=0, camera_y=0):
        if not self.is_warning:
            return

        for tile_x, tile_y in self.target_tiles:
            rect = pygame.Rect(
                tile_x * TILE_SIZE - camera_x,
                tile_y * TILE_SIZE - camera_y,
                TILE_SIZE,
                TILE_SIZE,
            )

            pygame.draw.rect(
                screen,
                (255, 210, 120),
                rect,
                2,
            )

            inner_rect = pygame.Rect(
                rect.x + 8,
                rect.y + 8,
                rect.width - 16,
                rect.height - 16,
            )

            pygame.draw.rect(
                screen,
                (180, 110, 40),
                inner_rect,
            )