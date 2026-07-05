import random

from entities.enemy import Enemy
from entities.item import Item
from entities.king_rat import KingRat
from entities.big_snake import BigSnake
from entities.ice_crab import IceCrab
from entities.ghost_chan import GhostChan
from entities.white_tanto import WhiteTanto
from entities.denishi import Denishi
from entities.takashi import Takashi

from entities.snake_enemy import SnakeEnemy
from entities.penguin_enemy import PenguinEnemy
from entities.polar_bear_enemy import PolarBearEnemy
from entities.magma_snail_enemy import MagmaSnailEnemy
from entities.student_male_enemy import StudentMaleEnemy
from entities.student_female_enemy import StudentFemaleEnemy
from entities.metal_glasses_enemy import MetalGlassesEnemy

from dungeon.game_map import (
    get_random_floor_position,
    get_boss_position,
    get_large_rooms,
)


class SpawnSystem:
    def create_enemies(self, player, floor, is_bonus_floor=False):
        enemies = []

        if is_bonus_floor:
            return enemies

        large_rooms = get_large_rooms()

        if len(large_rooms) > 0:
            target_room = random.choice(large_rooms)
            enemy_count = self.get_enemy_count_by_floor(
                floor,
                room_size="large",
            )

            self.spawn_enemies_in_room(
                enemies,
                target_room,
                enemy_count,
                player,
                floor,
            )

            return enemies

        enemy_count = self.get_enemy_count_by_floor(
            floor,
            room_size="normal",
        )

        max_attempts = enemy_count * 30
        attempts = 0

        while len(enemies) < enemy_count and attempts < max_attempts:
            attempts += 1

            x, y = get_random_floor_position(
                player,
                min_distance=5,
            )

            if self.is_position_occupied(x, y, enemies):
                continue

            enemies.append(
                self.create_enemy_by_floor(
                    x,
                    y,
                    floor,
                )
            )

        return enemies

    def spawn_enemies_in_room(
        self,
        enemies,
        room,
        enemy_count,
        player,
        floor,
    ):
        room_x, room_y, room_w, room_h = room

        max_attempts = enemy_count * 40
        attempts = 0

        while len(enemies) < enemy_count and attempts < max_attempts:
            attempts += 1

            x = random.randint(
                room_x + 1,
                room_x + room_w - 2,
            )

            y = random.randint(
                room_y + 1,
                room_y + room_h - 2,
            )

            distance = abs(x - player.x) + abs(y - player.y)

            if distance < 5:
                continue

            if self.is_position_occupied(x, y, enemies):
                continue

            enemies.append(
                self.create_enemy_by_floor(
                    x,
                    y,
                    floor,
                )
            )

    def get_enemy_count_by_floor(self, floor, room_size="normal"):
        if room_size == "large":
            return random.randint(4, 7)

        return random.randint(2, 5)

    def create_items(self, player, is_boss_floor, is_bonus_floor=False):
        items = []

        if is_boss_floor:
            return items

        if is_bonus_floor:
            return items

        max_attempts = 30
        attempts = 0

        while len(items) < 3 and attempts < max_attempts:
            attempts += 1

            x, y = get_random_floor_position(
                player,
                min_distance=3,
            )

            overlap = False

            for item in items:
                if item.x == x and item.y == y:
                    overlap = True
                    break

            if overlap:
                continue

            items.append(
                Item(
                    x,
                    y,
                    "potion",
                )
            )

        return items

    def create_boss(self, floor):
        boss_x, boss_y = get_boss_position()

        if floor == 10:
            return BigSnake(boss_x, boss_y)

        if floor == 15:
            return IceCrab(boss_x, boss_y)

        if floor == 20:
            return GhostChan(boss_x, boss_y)

        if floor == 25:
            return WhiteTanto(boss_x, boss_y)

        if floor == 29:
            return Denishi(boss_x, boss_y)

        if floor == 30:
            return Takashi(boss_x, boss_y)

        return KingRat(boss_x, boss_y)

    def create_enemy_by_floor(self, x, y, floor):
        # ------------------------------
        # 超低確率ボーナスエネミー
        # ------------------------------

        if 1 <= floor <= 28:
            if random.random() < 0.015:
                return MetalGlassesEnemy(x, y)

        # ------------------------------
        # はじまりのどうくつ
        # ------------------------------

        if 6 <= floor <= 9:
            if random.random() < 0.35:
                return SnakeEnemy(x, y)

            return Enemy(x, y)

        # ------------------------------
        # さむいだいち
        # ------------------------------

        if 11 <= floor <= 15:
            return PenguinEnemy(x, y)

        if 16 <= floor <= 19:
            if random.random() < 0.35:
                return PolarBearEnemy(x, y)

            return PenguinEnemy(x, y)

        # ------------------------------
        # あつあつのにわ
        # ------------------------------

        if 21 <= floor <= 24:
            if random.random() < 0.35:
                return StudentMaleEnemy(x, y)

            return MagmaSnailEnemy(x, y)

        # ------------------------------
        # あったかおうち
        # ------------------------------

        if 26 <= floor <= 28:
            if random.random() < 0.40:
                return StudentFemaleEnemy(x, y)

            return StudentMaleEnemy(x, y)

        # ------------------------------
        # デフォルト
        # ------------------------------

        return Enemy(x, y)

    def is_position_occupied(self, x, y, enemies):
        for enemy in enemies:
            if enemy.x == x and enemy.y == y:
                return True

        return False