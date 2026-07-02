import pygame

from settings import *
from boss_skills.base_boss_skill import BaseBossSkill


class IceShotSkill(BaseBossSkill):
    def __init__(
        self,
        cooldown=95,
        warning_time=20,
        damage_bonus=1,
    ):
        super().__init__(cooldown)

        self.warning_time = warning_time
        self.damage_bonus = damage_bonus

        self.is_warning = False
        self.warning_timer = 0

        self.target_x = 0
        self.target_y = 0

    def update(self, boss, game_map, player):
        self.update_timer()

        if self.is_warning:
            self.update_warning(boss, player)
            return

        if not self.can_use():
            return

        self.start_warning(player)

    def start_warning(self, player):
        self.is_warning = True
        self.warning_timer = self.warning_time
        self.target_x = player.x
        self.target_y = player.y
        self.reset_timer()

    def update_warning(self, boss, player):
        self.warning_timer -= 1

        if self.warning_timer <= 0:
            self.apply_damage(boss, player)
            self.is_warning = False

    def get_target_tiles(self):
        return [
            (self.target_x, self.target_y),
            (self.target_x + 1, self.target_y),
            (self.target_x - 1, self.target_y),
            (self.target_x, self.target_y + 1),
            (self.target_x, self.target_y - 1),
        ]

    def apply_damage(self, boss, player):
        for tile_x, tile_y in self.get_target_tiles():
            if player.x == tile_x and player.y == tile_y:
                boss.damage_player(
                    player,
                    boss.attack + self.damage_bonus,
                )
                return

    def draw(self, screen, boss, camera_x=0, camera_y=0):
        if not self.is_warning:
            return

        for tile_x, tile_y in self.get_target_tiles():
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
                (200, 245, 255),
                inner_rect,
            )