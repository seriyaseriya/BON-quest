import pygame

from settings import *
from boss_skills.base_boss_skill import BaseBossSkill


class PoisonBreathSkill(BaseBossSkill):
    def __init__(
        self,
        cooldown=100,
        warning_time=25,
        length=5,
        damage_bonus=1,
        color=(160, 40, 200),
    ):
        super().__init__(cooldown)

        self.warning_time = warning_time
        self.length = length
        self.damage_bonus = damage_bonus
        self.color = color

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

        self.start_warning(boss, player)

    def start_warning(self, boss, player):
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

    def get_tiles(self, boss):
        tiles = []

        center_x, center_y = boss.get_center_position()

        dx = self.target_x - center_x
        dy = self.target_y - center_y

        if abs(dx) > abs(dy):
            step_x = 1 if dx > 0 else -1
            step_y = 0
        else:
            step_x = 0
            step_y = 1 if dy > 0 else -1

        x = center_x
        y = center_y

        attack_length = self.length

        if boss.phase >= 2:
            attack_length += 1

        if boss.phase >= 3:
            attack_length += 1

        for _ in range(attack_length):
            x += step_x
            y += step_y
            tiles.append((x, y))

        return tiles

    def apply_damage(self, boss, player):
        for tile_x, tile_y in self.get_tiles(boss):
            if player.x == tile_x and player.y == tile_y:
                boss.damage_player(
                    player,
                    boss.attack + self.damage_bonus,
                )
                return

    def draw(self, screen, boss, camera_x=0, camera_y=0):
        if not self.is_warning:
            return

        for tile_x, tile_y in self.get_tiles(boss):
            rect = pygame.Rect(
                tile_x * TILE_SIZE - camera_x,
                tile_y * TILE_SIZE - camera_y,
                TILE_SIZE,
                TILE_SIZE,
            )

            pygame.draw.rect(
                screen,
                self.color,
                rect,
                2,
            )

            inner_rect = pygame.Rect(
                rect.x + 6,
                rect.y + 6,
                rect.width - 12,
                rect.height - 12,
            )

            pygame.draw.rect(
                screen,
                (90, 20, 120),
                inner_rect,
            )