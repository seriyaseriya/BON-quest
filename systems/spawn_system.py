from entities.enemy import Enemy
from entities.item import Item
from entities.king_rat import KingRat

from dungeon.game_map import (
    get_random_floor_position,
    get_boss_position,
)


class SpawnSystem:
    def create_enemies(self, player, floor):
        enemies = []
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

    def create_items(self, player, is_boss_floor):
        items = []

        if is_boss_floor:
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

    def create_boss(self):
        boss_x, boss_y = get_boss_position()
        return KingRat(boss_x, boss_y)