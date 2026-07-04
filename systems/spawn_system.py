from entities.enemy import Enemy
from entities.item import Item
from entities.king_rat import KingRat
from entities.big_snake import BigSnake
from entities.ice_crab import IceCrab
from entities.ghost_chan import GhostChan
from entities.white_tanto import WhiteTanto
from entities.denishi import Denishi
from entities.takashi import Takashi

from dungeon.game_map import (
    get_random_floor_position,
    get_boss_position,
)


class SpawnSystem:
    def create_enemies(self, player, floor, is_bonus_floor=False):
        enemies = []

        if is_bonus_floor:
            return enemies

        enemy_count = 2 + floor

        while len(enemies) < enemy_count:
            x, y = get_random_floor_position(player, min_distance=5)

            overlap = False
            for enemy in enemies:
                if enemy.x == x and enemy.y == y:
                    overlap = True

            if overlap:
                continue

            enemies.append(Enemy(x, y))

        return enemies

    def create_items(self, player, is_boss_floor, is_bonus_floor=False):
        items = []

        if is_boss_floor:
            return items

        if is_bonus_floor:
            return items

        for _ in range(3):
            x, y = get_random_floor_position(player, min_distance=3)

            overlap = False
            for item in items:
                if item.x == x and item.y == y:
                    overlap = True

            if overlap:
                continue

            items.append(Item(x, y, "potion"))

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