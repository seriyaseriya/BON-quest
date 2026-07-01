from settings import TILE_SIZE
from abilities.base_ability import BaseAbility


class LullabyAbility(BaseAbility):
    ability_id = "lullaby"

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

        range_pixels = 90 + level * 18
        freeze_time = 60 + level * 15

        affected = 0

        for enemy in enemies:
            if enemy.hp <= 0:
                continue

            enemy_center_x = enemy.x * TILE_SIZE + TILE_SIZE // 2
            enemy_center_y = enemy.y * TILE_SIZE + TILE_SIZE // 2

            dx = enemy_center_x - player_center_x
            dy = enemy_center_y - player_center_y

            distance_squared = dx * dx + dy * dy

            if distance_squared <= range_pixels * range_pixels:
                enemy.freeze_timer = freeze_time
                affected += 1

        return affected > 0