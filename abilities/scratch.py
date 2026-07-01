from settings import TILE_SIZE
from abilities.base_ability import BaseAbility


class ScratchAbility(BaseAbility):
    ability_id = "scratch"

    def use(
        self,
        player,
        projectile_manager,
        enemies,
        level,
        on_enemy_defeated=None,
    ):
        if not enemies:
            return False

        player_center_x = player.x * TILE_SIZE + TILE_SIZE // 2
        player_center_y = player.y * TILE_SIZE + TILE_SIZE // 2

        range_pixels = 55 + level * 8
        damage = 2 + level
        target_count = 1

        if level >= 4:
            target_count = 2

        if level >= 7:
            target_count = 3

        targets = []

        for enemy in enemies:
            if enemy.hp <= 0:
                continue

            enemy_center_x = enemy.x * TILE_SIZE + TILE_SIZE // 2
            enemy_center_y = enemy.y * TILE_SIZE + TILE_SIZE // 2

            dx = enemy_center_x - player_center_x
            dy = enemy_center_y - player_center_y

            distance_squared = dx * dx + dy * dy

            if distance_squared <= range_pixels * range_pixels:
                targets.append((distance_squared, enemy))

        if not targets:
            return False

        targets.sort(key=lambda item: item[0])

        for _, enemy in targets[:target_count]:
            result = enemy.take_damage(damage)

            if result == "enemy_defeated" and on_enemy_defeated is not None:
                on_enemy_defeated(enemy)

        return True